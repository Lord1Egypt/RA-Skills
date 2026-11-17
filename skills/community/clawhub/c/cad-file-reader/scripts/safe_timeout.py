#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨平台安全超时辅助（cad-file-reader 专用）。

用途
----
- ``deadline(seconds)`` 上下文管理器：给一段代码设置一个硬时间预算。
  * POSIX（macOS / Linux）：保留原有 SIGALRM + setitimer(ITIMER_REAL)
    语义，超时由内核信号打断当前代码并抛出 ``DeadlineExceeded``。
  * Windows（无 SIGALRM）：退化为 ``threading.Timer`` 协作式超时——
    定时器只标记过期，不会打断正在运行的字节码；代码块内可通过捕获的
    ``Deadline`` 对象主动调用 ``check()`` 在安全点检查并抛异常。
- ``run_with_timeout(func, timeout, *args, **kwargs)``：进程级兜底。
  不管有没有 SIGALRM，都把 ``func`` 放到独立子进程里执行并在墙上时间
  超时后强制终止，适合无法在代码内插检查点的阻塞调用（例如第三方
  原生库、拒绝协作的循环）。POSIX 和 Windows 均可用。
- ``cad_scan.py`` 继续沿用它自己的 SIGALRM 时间预算写法，本模块暂不
  改变任何既有脚本的调用方式；本模块只是把跨平台安全超时能力沉淀为
  可复用、可单测的工具。

三平台设计
----------
- macOS / Linux：signal 路径最快、语义与 cad_scan 现有逻辑一致。
- Windows：signal.SIGALRM 不存在，用 Timer 协作式超时 + 子进程兜底。
- 全部实现只用 Python 标准库，不依赖外部后端。
"""

from __future__ import annotations

import contextlib
import multiprocessing
import os
import platform
import queue
import signal
import threading
import time
from typing import Any, Callable


class DeadlineExceeded(TimeoutError):
    """执行超过 deadline() / run_with_timeout() 的时限。"""


def _use_posix_sigalrm() -> bool:
    """判断是否应走 POSIX SIGALRM 硬超时路径。

    返回 False 的两个典型场景：
    1. Windows：标准库没有 SIGALRM。
    2. 被测试注入模拟为 Windows 分支。
    """
    return platform.system() != "Windows" and hasattr(signal, "SIGALRM")


class Deadline:
    """协作式截止时间句柄。

    记录一个单调钟截止时间；Windows / 无 SIGALRM 路径由 ``threading.Timer``
    在后台把 ``expired`` 标记为 True。使用者在安全点调用 :meth:`check` 即可
    把超时转成 ``DeadlineExceeded``。
    """

    def __init__(self, seconds: float, cooperative: bool = False) -> None:
        seconds = float(seconds)
        if seconds <= 0:
            raise ValueError("deadline 秒数必须为正数")
        self.seconds = seconds
        self._deadline_at = time.monotonic() + seconds
        self._timer_fired = False
        self._timer: threading.Timer | None = None
        if cooperative:
            self._timer = threading.Timer(seconds, self._mark_timer)
            self._timer.daemon = True
            self._timer.start()

    def _mark_timer(self) -> None:
        self._timer_fired = True

    @property
    def expired(self) -> bool:
        if self._timer_fired:
            return True
        return time.monotonic() >= self._deadline_at

    def remaining(self) -> float:
        """返回剩余秒数（下界为 0.0），用于主动缩窄后续子步骤预算。"""
        return max(0.0, self._deadline_at - time.monotonic())

    def check(self) -> None:
        """安全点检查：协作式分支需要调用方在循环/阻塞间隙主动调用。"""
        if self.expired:
            raise DeadlineExceeded(
                f"任务超时（{self.seconds:g} 秒）"
            )

    def cancel(self) -> None:
        """停止后台 Timer；POSIX 无需调用（signal 由上下文管理器恢复）。"""
        if self._timer is not None and self._timer.is_alive():
            self._timer.cancel()


@contextlib.contextmanager
def deadline(seconds: float):
    """给 with 代码块设置时间预算（POSIX 硬超时，Windows 协作式超时）。

    用法::

        with safe_timeout.deadline(3.0) as dl:
            dl.check()   # Windows 协作式分支的安全检查点（可选）

    超时抛出的异常统一为 ``DeadlineExceeded``。
    """
    seconds = float(seconds)
    if seconds <= 0:
        raise ValueError("deadline 秒数必须为正数")

    if not _use_posix_sigalrm():
        dl = Deadline(seconds, cooperative=True)
        try:
            yield dl
        finally:
            dl.cancel()
        return

    # ---- POSIX：SIGALRM + ITIMER_REAL（保持 cad_scan.py 既有语义） ----
    prev_handler = signal.getsignal(signal.SIGALRM)

    def _boom(_signum: int, _frame: object) -> None:
        raise DeadlineExceeded(f"任务超时（{seconds:g} 秒）")

    signal.signal(signal.SIGALRM, _boom)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    dl = Deadline(seconds, cooperative=False)
    try:
        yield dl
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, prev_handler or signal.SIG_DFL)


def _run_child(q: "multiprocessing.Queue", func: Callable,
               args: tuple, kwargs: dict) -> None:
    """子进程执行体：结果或异常统一放回 :class:`multiprocessing.Queue`。"""
    try:
        result = func(*args, **kwargs)
        q.put(("ok", result))
    except BaseException as exc:  # noqa: B036 - 必须把子进程异常带回父进程
        q.put(("error", exc))


def run_with_timeout(func: Callable, timeout: float,
                     *args: Any, **kwargs: Any) -> Any:
    """在独立子进程里执行 ``func``，超过 ``timeout`` 秒强制终止。

    这是没有 SIGALRM（主要是 Windows）时的兜底方案，POSIX 也能用。
    注意：``func`` 必须能从模块顶层按引用序列化（Windows spawn 需要
    picklable）；本地闭包 / lambda 在 Windows 会失败，应改用模块级函数。
    返回值传给父进程；``func`` 自身抛出的异常原样传给父进程。
    """
    timeout = float(timeout)
    if timeout <= 0:
        raise ValueError("timeout 秒数必须为正数")

    result_q: multiprocessing.Queue = multiprocessing.Queue()
    proc = multiprocessing.Process(
        target=_run_child,
        args=(result_q, func, args, kwargs),
        daemon=True,
    )
    proc.start()
    proc.join(timeout)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        result_q.close()
        result_q.join_thread()
        raise DeadlineExceeded(f"子进程超时（{timeout:g} 秒）")

    try:
        kind, payload = result_q.get_nowait()
    except queue.Empty:
        result_q.close()
        result_q.join_thread()
        raise DeadlineExceeded(f"子进程超时（{timeout:g} 秒）")

    result_q.close()
    result_q.join_thread()
    if kind == "ok":
        return payload
    assert kind == "error"
    if isinstance(payload, BaseException):
        raise payload
    raise DeadlineExceeded(f"子进程异常：{payload!r}")


if __name__ == "__main__":
    print("safe_timeout 模块：",
          "POSIX 路径" if _use_posix_sigalrm() else "Windows 协作式路径")
