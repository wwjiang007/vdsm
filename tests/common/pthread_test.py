#
# Copyright 2015-2017 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#
from __future__ import absolute_import
from __future__ import division

import threading

from vdsm.common import pthread

from testlib import VdsmTestCase as TestCaseBase


class PthreadNameTests(TestCaseBase):

    def test_name_too_long(self):
        self.assertRaises(ValueError,
                          pthread.setname,
                          "any name longer than fifteen ASCII characters")

    def test_name_is_set(self):
        NAME = "test-name"
        names = [None]

        def run():
            pthread.setname(NAME)
            names[0] = pthread.getname()

        t = threading.Thread(target=run)
        t.daemon = True
        t.start()
        t.join()

        self.assertEqual(names[0], NAME)

    def test_name_set_doesnt_change_parent(self):
        HELPER_NAME = "helper-name"
        parent_name = pthread.getname()
        ready = threading.Event()
        done = threading.Event()

        def run():
            pthread.setname(HELPER_NAME)
            ready.set()
            done.wait()

        t = threading.Thread(target=run)
        t.daemon = True
        t.start()
        try:
            ready.wait()
            try:
                self.assertEqual(parent_name, pthread.getname())
            finally:
                done.set()
        finally:
            t.join()
