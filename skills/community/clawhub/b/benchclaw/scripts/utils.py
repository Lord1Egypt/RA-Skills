"""
BenchClaw 通用工具函数。
"""
from __future__ import annotations

import json
import logging
import os
import shutil
import uuid

logger = logging.getLogger("benchclaw")


def get_bench_session_id() -> str:
    """
    从本地 cache.json 读取 Bench 会话标识；若不存在则生成随机 UUID 并写回文件后返回。
    """
    cache_path = os.path.join(os.path.dirname(__file__), "../data/cache.json")
    bench_session_id: str | None = None

    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            value = data.get("bench_session_id")
            if isinstance(value, str) and value.strip():
                bench_session_id = value.strip()
    except FileNotFoundError:
        pass
    except (OSError, json.JSONDecodeError):
        pass

    if not bench_session_id:
        bench_session_id = str(uuid.uuid4())
        try:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump({"bench_session_id": bench_session_id}, f, ensure_ascii=False, indent=2)
        except OSError:
            # 即使写入失败，也仍然返回本次生成的 id
            pass

    return bench_session_id

def get_temp_file(filename: str) -> str:
    """返回 temp 目录下指定文件的绝对路径，目录不存在时自动创建。"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(script_dir, "..", "temp")
    os.makedirs(temp_dir, exist_ok=True)
    return os.path.join(temp_dir, filename)

def clean_temp_files() -> None:
    """删除 temp 目录下的 messages.json 和 results.json（忽略不存在的文件）。"""
    for name in ("results.json", "prompt.md"):
        try:
            os.remove(get_temp_file(name))
        except FileNotFoundError:
            pass
        except Exception as e:
            logger.warning(f"删除临时文件失败 {name}: {e}")

def clean_benchclaw_workspace() -> None:
    """删除 ~/.openclaw/workspace/bench_claw 文件夹（如果存在）。"""
    home_dir = os.path.expanduser("~")
    bench_claw_path = os.path.join(home_dir, ".openclaw", "workspace", "bench_claw")

    if os.path.exists(bench_claw_path):
        try:
            shutil.rmtree(bench_claw_path)
            logger.info(f"已删除工作区文件夹: {bench_claw_path}")
        except Exception as e:
            logger.warning(f"删除工作区文件夹失败: {e}")
    else:
        logger.debug(f"bench_claw工作区文件夹不存在，跳过删除: {bench_claw_path}")


# C3: 硬件运行时动态监控
try:
    import psutil as _psutil
    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False

import threading as _threading

class HardwareMonitor:
    """评测期间后台监控 CPU 和内存使用率（每秒采样一次）。"""

    def __init__(self):
        self.cpu_samples: list[float] = []
        self.mem_min_available_gb: float = float('inf')
        self._running = False
        self._thread = None

    def start(self) -> None:
        if not _HAS_PSUTIL:
            return
        self._running = True
        def _run():
            while self._running:
                try:
                    self.cpu_samples.append(_psutil.cpu_percent(interval=1))
                    avail = _psutil.virtual_memory().available / (1024 ** 3)
                    self.mem_min_available_gb = min(self.mem_min_available_gb, avail)
                except Exception:
                    pass
        self._thread = _threading.Thread(target=_run, daemon=True)
        self._thread.start()

    def stop(self) -> dict:
        self._running = False
        if not _HAS_PSUTIL or not self.cpu_samples:
            return {}
        try:
            mem = _psutil.virtual_memory()
            return {
                "cpu_peak_percent": max(self.cpu_samples),
                "cpu_avg_percent": round(sum(self.cpu_samples) / len(self.cpu_samples), 1),
                "mem_min_available_gb": round(self.mem_min_available_gb, 1),
                "mem_total_gb": round(mem.total / (1024 ** 3), 1),
            }
        except Exception:
            return {}


def get_system_info() -> dict:
    """
    采集系统硬件和主机类型信息，用于上报到榜单。
    返回 dict，采集失败时对应字段为 None。
    """
    import subprocess as _subprocess

    info = {
        "cpu_cores": None,
        "ram_total_gb": None,
        "host_type": None,      # 例："云主机，阿里云 ECS" 或 "虚拟机（KVM）" 或 "物理机"
        "virt_type": None,      # systemd-detect-virt 原始值
    }

    # CPU 核数（物理核）
    try:
        info["cpu_cores"] = _psutil.cpu_count(logical=True) if _HAS_PSUTIL else None
    except Exception:
        pass

    # 内存总量
    try:
        if _HAS_PSUTIL:
            info["ram_total_gb"] = round(_psutil.virtual_memory().total / (1024**3), 1)
    except Exception:
        pass

    # 虚拟化类型
    try:
        result = _subprocess.run(
            ["systemd-detect-virt"], capture_output=True, text=True, timeout=5
        )
        virt = result.stdout.strip()
        info["virt_type"] = virt
    except Exception:
        virt = "unknown"

    # 主机类型（友好描述）
    try:
        vendor = open("/sys/class/dmi/id/sys_vendor").read().strip() if __import__("os").path.exists("/sys/class/dmi/id/sys_vendor") else ""
        product = open("/sys/class/dmi/id/product_name").read().strip() if __import__("os").path.exists("/sys/class/dmi/id/product_name") else ""

        if "Alibaba" in vendor or "Alibaba" in product:
            info["host_type"] = "云主机，阿里云 ECS"
        elif "Tencent" in vendor or "Tencent" in product:
            info["host_type"] = "云主机，腾讯云 CVM"
        elif "Amazon" in vendor or "EC2" in product:
            info["host_type"] = "云主机，AWS EC2"
        elif "Microsoft" in vendor and virt in ("hyperv", "microsoft"):
            info["host_type"] = "云主机，Azure"
        elif "Google" in vendor:
            info["host_type"] = "云主机，Google Cloud"
        elif virt == "none":
            info["host_type"] = "物理机"
        elif virt in ("kvm", "qemu", "vmware", "xen", "hyperv"):
            info["host_type"] = f"虚拟机（{virt.upper()}）"
        elif virt == "docker":
            info["host_type"] = "容器（Docker）"
        else:
            info["host_type"] = "虚拟机"
    except Exception:
        pass

    return info
