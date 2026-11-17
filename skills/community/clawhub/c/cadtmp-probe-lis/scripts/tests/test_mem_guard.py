#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests for scripts/mem_guard.py（POSIX / Windows / 降级 三分支）。

说明
----
- 纯 stdlib + unittest，不实际杀进程：终止动作全程用 mock 替换；
- 通过 mock.platform.system 模拟 win/darwin/linux，验证 resource 优先、
  psutil 回退、Windows 只用 psutil 的路径选择；
- 验证 start 对外签名 start(cap_mb, name, interval) 不变。
"""

from __future__ import annotations

import inspect
import os
import sys
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import mem_guard  # noqa: E402


class CurrentMbBranchTest(unittest.TestCase):
    """current_mb() 的平台分支选择。"""

    def test_posix_prefers_resource(self):
        with mock.patch.object(mem_guard, "_resource_peak_mb", return_value=3.5), \
                mock.patch.object(mem_guard, "_psutil_rss_mb",
                                  side_effect=AssertionError("不应调用 psutil")), \
                mock.patch.object(mem_guard.platform, "system", return_value="Darwin"):
            self.assertEqual(mem_guard.current_mb(), 3.5)

    def test_posix_falls_back_to_psutil_when_resource_blocked(self):
        with mock.patch.object(mem_guard, "_resource_peak_mb", return_value=None), \
                mock.patch.object(mem_guard, "_psutil_rss_mb", return_value=4.0), \
                mock.patch.object(mem_guard.platform, "system", return_value="Darwin"):
            self.assertEqual(mem_guard.current_mb(), 4.0)

    def test_windows_uses_psutil_only(self):
        with mock.patch.object(mem_guard.platform, "system", return_value="Windows"), \
                mock.patch.object(mem_guard, "_resource_peak_mb",
                                  side_effect=AssertionError("Windows 不应调用 resource")), \
                mock.patch.object(mem_guard, "_psutil_rss_mb", return_value=5.0):
            self.assertEqual(mem_guard.current_mb(), 5.0)

    def test_no_measure_returns_zero(self):
        with mock.patch.object(mem_guard.platform, "system", return_value="Windows"), \
                mock.patch.object(mem_guard, "_psutil_rss_mb", return_value=None):
            self.assertEqual(mem_guard.current_mb(), 0.0)


class ResourcePeeksTest(unittest.TestCase):
    """_resource_peak_mb 平台/单位差异。"""

    def test_linux_uses_kb_divisor(self):
        with mock.patch.object(mem_guard.platform, "system", return_value="Linux"):
            with mock.patch.dict(sys.modules, {"resource": mock.Mock(
                getrusage=lambda _s: mock.Mock(ru_maxrss=1536))}):
                self.assertAlmostEqual(mem_guard._resource_peak_mb(), 1.5)

    def test_darwin_uses_bytes_divisor(self):
        with mock.patch.object(mem_guard.platform, "system", return_value="Darwin"):
            with mock.patch.dict(sys.modules, {"resource": mock.Mock(
                getrusage=lambda _s: mock.Mock(ru_maxrss=1572864))}):
                self.assertAlmostEqual(mem_guard._resource_peak_mb(), 1.5)

    def test_windows_returns_none(self):
        with mock.patch.object(mem_guard.platform, "system", return_value="Windows"):
            self.assertIsNone(mem_guard._resource_peak_mb())


class StartSignatureAndActTest(unittest.TestCase):
    """对外签名与超限处置行为。"""

    def test_start_signature_unchanged(self):
        sig = inspect.signature(mem_guard.start)
        self.assertEqual(list(sig.parameters), ["cap_mb", "name", "interval"])

    def test_start_rejects_nonpositive_cap(self):
        for cap in (None, 0, -1):
            self.assertIsNone(mem_guard.start(cap))

    def test_start_returns_daemon_thread(self):
        with mock.patch.object(mem_guard, "current_mb", return_value=8.0):
            t = mem_guard.start(100000, name="测试闸", interval=0.01)
            self.assertIsInstance(t, threading.Thread)
            self.assertTrue(t.daemon)
            time.sleep(0.03)
            self.assertTrue(t.is_alive())

    def test_start_degrades_to_cooperative_when_unmeasurable(self):
        with mock.patch.object(mem_guard, "current_mb", return_value=0.0), \
                mock.patch.object(mem_guard.sys.stderr, "write") as write_mock:
            got = mem_guard.start(100, name="降级闸")
            self.assertIsNone(got)
            self.assertTrue(any("协作式超时" in str(c) for c in
                                [a[0] for a in write_mock.call_args_list]))

    def test_check_and_act_under_limit_does_not_terminate(self):
        with mock.patch.object(mem_guard, "current_mb", return_value=50.0), \
                mock.patch.object(mem_guard, "_terminate_current",
                                  side_effect=AssertionError("不应终止")) as kill_mock:
            self.assertEqual(mem_guard._check_and_act(100, "闸"), 50.0)
            kill_mock.assert_not_called()

    def test_check_and_act_over_limit_terminates(self):
        with mock.patch.object(mem_guard, "current_mb", return_value=9000.0), \
                mock.patch.object(mem_guard, "_terminate_current") as kill_mock:
            self.assertEqual(mem_guard._check_and_act(100, "闸"), "killed")
            kill_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
