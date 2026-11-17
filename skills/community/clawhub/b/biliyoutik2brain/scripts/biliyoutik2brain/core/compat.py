"""跨平台兼容工具层

提供 OS 检测常量、安全的子进程调用、路径处理等跨平台适配。
所有跨平台差异集中在此模块，其他模块避免直接使用 sys.platform。
"""

import sys
import os
import subprocess
from typing import List, Optional

# ── 平台检测 ──
IS_WINDOWS = sys.platform == "win32"
IS_MACOS = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")


# ── 子进程安全调用 ──

def safe_run(cmd: List[str], **kwargs) -> subprocess.CompletedProcess:
    """跨平台安全执行命令。

    Windows 自动处理路径分隔符差异、禁用 shell。
    macOS/Linux 保持原生行为。
    """
    if IS_WINDOWS:
        kwargs.setdefault("shell", False)
        cmd = [str(c).replace("/", "\\") for c in cmd]
    return subprocess.run(cmd, **kwargs)


# ── 路径展开 ──

def path_expand(path: str) -> str:
    """跨平台路径展开（处理 ~ 等）"""
    if path.startswith("~"):
        path = os.path.expanduser(path)
    return os.path.abspath(path)


# ── 文件锁 ──

def file_lock(fd) -> bool:
    """跨平台文件锁（仅 Unix 支持 fcntl，Windows 跳过）"""
    if IS_WINDOWS:
        return True  # Windows 不阻塞（调用者自行处理竞态）
    try:
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except (ImportError, OSError):
        return False


def file_unlock(fd):
    """跨平台文件解锁"""
    if IS_WINDOWS:
        return
    try:
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_UN)
    except ImportError:
        pass


# ── 内存信息 ──

def get_total_ram_gb() -> float:
    """获取系统总内存 (GB)，跨平台兜底 4GB"""
    try:
        if IS_WINDOWS:
            import subprocess
            r = subprocess.run(
                ["wmic", "ComputerSystem", "get", "TotalPhysicalMemory"],
                capture_output=True, text=True, timeout=10
            )
            for line in r.stdout.splitlines():
                val = line.strip()
                if val.isdigit():
                    return int(val) / (1024 ** 3)
        elif IS_LINUX:
            with open("/proc/meminfo") as f:
                for line in f:
                    if "MemTotal" in line:
                        return int(line.split()[1]) / (1024 ** 2)
        elif IS_MACOS:
            import subprocess
            r = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True, text=True, timeout=5
            )
            return int(r.stdout.strip()) / (1024 ** 3)
    except Exception:
        pass
    return 4.0  # 保守估算
