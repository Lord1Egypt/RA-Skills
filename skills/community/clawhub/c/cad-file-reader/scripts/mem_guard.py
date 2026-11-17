"""进程内内存看门狗（跨平台版，2026-10-21 重写）。

为什么不用 RLIMIT：macOS 13 上实测 setrlimit(RLIMIT_AS/RLIMIT_DATA) 直接报
`ValueError: current limit exceeds maximum limit`，`ulimit -v/-d` 也报
`cannot modify limit: Invalid argument` —— 内核不提供按进程虚拟内存硬上限。
所以只能采样峰值 RSS，越线立刻平台适配地终止当前进程，让整机不被拖死
（不触发长按电源键）比让这次解析跑完更重要。

三平台设计
----------
- POSIX（macOS/Linux）：优先 ``resource.getrusage(RUSAGE_SELF)``；
  该调用被阻断/异常时退到 ``psutil.Process().memory_info().rss``。
- Windows：没有 ``resource`` / ``SIGKILL``，用 ``psutil`` 读 RSS，
  终止改用平台适配路径（SIGTERM→TerminateProcess，最坏兜底 ``os._exit``）。
- 全部用标准库，psutil 为可选依赖：导入失败时本闸无法测量内存，
  降级为协作式超时模式（交由 safe_timeout.deadline()/run_with_timeout()
  兜底），不硬终止、不误杀。
"""
from __future__ import annotations

import os
import platform
import signal
import sys
import threading
import time
from typing import Optional

GB_SAFE_NOTE = "改走 cad_scan.sh 低内存路径（只解文字/图层/块名）"
DEGRADE_NOTE = ("无法测量当前进程内存（resource 与 psutil 均不可用）"
                "→ 本闸降级为协作式超时，交由 safe_timeout 兜底")


def _resource_peak_mb() -> Optional[float]:
    """POSIX：resource.getrusage 峰值 RSS → MB。失败返回 None。"""
    if platform.system() == "Windows":
        return None
    try:
        import resource
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # Linux 返回 KB；macOS/BSD 返回 bytes。
        divisor = 1024.0 if platform.system() == "Linux" else 1048576.0
        return rss / divisor
    except Exception:
        return None


def _psutil_rss_mb() -> Optional[float]:
    """psutil：Windows 主路径 / POSIX 阻断时的回退路径。失败返回 None。"""
    try:
        import psutil
        return psutil.Process(os.getpid()).memory_info().rss / 1048576.0
    except Exception:
        return None


def current_mb() -> float:
    """当前进程内存用量（MB）。无可用测量手段时返回 0.0。

    POSIX 优先 resource.getrusage；阻断/不适用时退到 psutil。
    """
    if platform.system() != "Windows":
        mb = _resource_peak_mb()
        if mb is not None and mb > 0:
            return mb
    mb = _psutil_rss_mb()
    if mb is not None and mb > 0:
        return mb
    return 0.0


def _terminate_current() -> None:
    """平台适配地终止当前进程（防整机卡死）。"""
    if os.name == "nt":
        # Windows：SIGTERM 也会走 TerminateProcess；万一失效，_exit 兜底。
        try:
            os.kill(os.getpid(), signal.SIGTERM)
        except Exception:
            pass
        os._exit(137)
    os.kill(os.getpid(), signal.SIGKILL)


def _check_and_act(cap_mb, name: str):
    """采样并判断：超限就终止并返回 "killed"，否则返回当前 MB。"""
    mb = current_mb()
    if mb > cap_mb:
        sys.stderr.write(
            "[%s] 峰值内存 %.0fMB 已超上限 %dMB → 主动终止，防整机卡死。%s\n"
            % (name, mb, cap_mb, GB_SAFE_NOTE))
        sys.stderr.flush()
        _terminate_current()
        return "killed"
    return mb


def start(cap_mb, name: str = "cad内存闸", interval: float = 0.08):
    if not cap_mb or cap_mb <= 0:
        return None
    if current_mb() <= 0:
        # 降级：resource 与 psutil 都不可用 —— 本闸无法测量内存，放弃硬终止，
        # 交由 safe_timeout.deadline()/run_with_timeout() 的协作式超时兜底。
        sys.stderr.write("[%s] %s\n" % (name, DEGRADE_NOTE))
        sys.stderr.flush()
        return None

    def loop():
        while True:
            time.sleep(interval)
            try:
                _check_and_act(cap_mb, name)
            except Exception:
                # 单次采样异常不退出看门狗，下一轮继续。
                continue

    t = threading.Thread(target=loop, daemon=True, name=name)
    t.start()
    return t
