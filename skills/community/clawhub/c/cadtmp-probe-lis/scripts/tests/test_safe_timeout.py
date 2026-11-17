#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests for scripts/safe_timeout.py（POSIX 与 Windows 两条分支）。

说明
----
- 纯 stdlib + unittest，不需要外部后端或联网；
- 通过 mock 把 ``_use_posix_sigalrm()`` 强制为 False，完整模拟
  Windows 无 SIGALRM 的协作式分支，并断言该分支绝不引用
  ``signal.SIGALRM`` / ``setitimer``；
- ``run_with_timeout`` 走 multiprocessing 子进程，测试函数都定义为
  模块级可 pickle 函数。
"""

from __future__ import annotations

import os
import sys
import time
import types
import unittest
from pathlib import Path
from unittest import mock

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import safe_timeout  # noqa: E402


def _sleep_return(seconds: float, value: str):
    """模块级 worker：可被 multiprocessing 按引用序列化。"""
    time.sleep(seconds)
    return value


def _raise_value_error(message: str):
    raise ValueError(message)


class PosixSignalDeadlineTest(unittest.TestCase):
    """走真实 POSIX SIGALRM 分支（本测试机若无 SIGALRM 则跳过）。"""

    def setUp(self):
        if not safe_timeout._use_posix_sigalrm():
            self.skipTest("当前环境无 SIGALRM，跳过 POSIX 真分支测试")

    def test_posix_raises_deadline_exceeded_after_sleep(self):
        with self.assertRaises(safe_timeout.DeadlineExceeded):
            with safe_timeout.deadline(0.05):
                time.sleep(1.0)

    def test_posix_restores_previous_handler(self):
        old = safe_timeout.signal.getsignal(safe_timeout.signal.SIGALRM)
        with safe_timeout.deadline(1.0):
            current = safe_timeout.signal.getsignal(safe_timeout.signal.SIGALRM)
            self.assertIsNot(current, old)
        restored = safe_timeout.signal.getsignal(safe_timeout.signal.SIGALRM)
        self.assertIs(restored, old)

    def test_posix_zero_timeout_rejected(self):
        with self.assertRaises(ValueError):
            with safe_timeout.deadline(0):
                pass


class WindowsSimulatedBranchTest(unittest.TestCase):
    """强制切到 Windows 分支：协作式 Timer + 主动 check()。"""

    def test_windows_branch_check_raises_after_timer_expiry(self):
        with mock.patch.object(safe_timeout, "_use_posix_sigalrm", return_value=False):
            with safe_timeout.deadline(0.05) as dl:
                time.sleep(0.2)
                self.assertTrue(dl.expired)
                self.assertLessEqual(dl.remaining(), 0.0)
                with self.assertRaises(safe_timeout.DeadlineExceeded):
                    dl.check()

    def test_windows_branch_no_sigalrm_reference(self):
        # 用 no-SIGALRM 的假 signal 模块证明 Windows 分支根本不会碰它。
        fake_signal = types.SimpleNamespace(
            setitimer=_unreachable("setitimer"),
            getsignal=_unreachable("getsignal"),
            signal=_unreachable("signal"),
        )
        with mock.patch.object(safe_timeout, "signal", fake_signal), \
                mock.patch.object(safe_timeout, "_use_posix_sigalrm", return_value=False), \
                mock.patch.object(safe_timeout.threading, "Timer",
                                  return_value=mock.Mock()) as fake_timer_cls:
            with safe_timeout.deadline(0.5):
                pass
            fake_timer_cls.assert_called_once()
            # Windows 分支绝不应调用 SIGALRM 相关 API（上面任意一次调用都会抛 AssertionError）

    def test_windows_positive_timeout_rejected(self):
        with mock.patch.object(safe_timeout, "_use_posix_sigalrm", return_value=False):
            with self.assertRaises(ValueError):
                with safe_timeout.deadline(-1):
                    pass


def _unreachable(name):
    def _boom(*_a, **_k):
        raise AssertionError(f"Windows 分支不得调用 POSIX signal API: {name}")
    return _boom


class ProcessLevelRunWithTimeoutTest(unittest.TestCase):
    """run_with_timeout 进程级兜底。"""

    def test_run_with_timeout_success(self):
        got = safe_timeout.run_with_timeout(_sleep_return, 3.0, 0.05, "ok")
        self.assertEqual(got, "ok")

    def test_run_with_timeout_raises_on_slow_call(self):
        with self.assertRaises(safe_timeout.DeadlineExceeded):
            safe_timeout.run_with_timeout(_sleep_return, 0.1, 1.0, "slow")

    def test_run_with_timeout_propagates_child_exception(self):
        with self.assertRaisesRegex(ValueError, "boom"):
            safe_timeout.run_with_timeout(_raise_value_error, 3.0, "boom")

    def test_run_with_timeout_bad_timeout(self):
        with self.assertRaises(ValueError):
            safe_timeout.run_with_timeout(_sleep_return, 0, 0.1, "x")


if __name__ == "__main__":
    unittest.main()
