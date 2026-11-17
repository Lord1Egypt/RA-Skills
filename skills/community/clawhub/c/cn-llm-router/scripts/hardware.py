"""硬件自适应（自动采集用户电脑硬件，自动做任务 / 并发分配，不拖累电脑）。

纯标准库实现：
- CPU 核心数：os.cpu_count()
- 物理内存：跨平台最佳努力（Windows 用 ctypes 调 GlobalMemoryStatusEx；
  Linux 读 /proc/meminfo；macOS 用 sysctl；均失败则回退保守值）
- 档位：low / mid / high，据此给出最大并发与单批大小

探测失败一律回退保守 low 档，绝不把电脑跑满。
"""

import os
import sys


def detect_memory_bytes():
    """返回物理内存字节数；探测失败返回 0。"""
    try:
        if sys.platform.startswith("win"):
            import ctypes
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            st = MEMORYSTATUSEX()
            st.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(st))
            return int(st.ullTotalPhys)
        elif sys.platform.startswith("linux"):
            with open("/proc/meminfo", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        kb = int(line.split()[1])
                        return kb * 1024
        elif sys.platform == "darwin":
            import ctypes
            libc = ctypes.CDLL("libc.dylib", use_errno=True)
            size = ctypes.c_uint64(0)
            ctypes.c_uint64_p = ctypes.POINTER(ctypes.c_uint64)
            res = libc.sysctlbyname(b"hw.memsize", ctypes.byref(size),
                                    ctypes.byref(ctypes.c_uint64(8)), None, 0)
            if res == 0:
                return int(size.value)
    except Exception:
        pass
    return 0


def profile():
    """返回硬件画像 dict：tier / cpu_cores / mem_gb / max_concurrency / batch_size。"""
    cpu_cores = os.cpu_count() or 1
    mem_bytes = detect_memory_bytes()
    mem_gb = mem_bytes / (1024 ** 3) if mem_bytes else 0.0

    # 档位判定：探测失败一律回退保守 low；否则综合内存与核心
    if mem_gb == 0:
        tier = "low"          # 内存探测失败，保守回退，绝不把电脑跑满
    elif mem_gb < 4 or cpu_cores <= 2:
        tier = "low"
    elif mem_gb < 8 or cpu_cores <= 4:
        tier = "mid"
    else:
        tier = "high"

    # 并发 / 批大小（保守，避免占满资源）
    if tier == "low":
        max_concurrency = 1
        batch_size = 20
    elif tier == "mid":
        max_concurrency = 2
        batch_size = 60
    else:
        max_concurrency = min(8, max(4, cpu_cores // 2))
        batch_size = 200

    return {
        "tier": tier,
        "cpu_cores": cpu_cores,
        "mem_gb": round(mem_gb, 1),
        "max_concurrency": max_concurrency,
        "batch_size": batch_size,
    }


def recommend_subtasks(n_tasks, max_concurrency=None):
    """按任务量与硬件档位，建议拆成几个子任务（给上层调度用）。

    n_tasks: 待处理的任务总数
    返回建议的子任务数量（<= max_concurrency，且尽量均分）。
    """
    p = profile()
    cap = max_concurrency or p["max_concurrency"]
    if n_tasks <= cap:
        return max(1, n_tasks)
    return cap


def enforce_limit(concurrency):
    """把用户/上游请求的并发数限制到硬件允许上限内。"""
    p = profile()
    return max(1, min(int(concurrency or 1), p["max_concurrency"]))
