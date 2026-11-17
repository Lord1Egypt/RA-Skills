"""
BiliYouTik2Brain — 系统+网络状态监控器 (Phase 2.1)

职责：
  1. 开工前检测系统资源（CPU/内存/磁盘）
  2. 网络状态检测（墙/YouTube可达性/API通断）
  3. 结果供 2.4 模型选择策略 + 动态调度使用

设计原则：
  - 轻量级（所有检测 ≤ 5s）
  - 结果缓存（20s内不重复检测）
  - 零异常（任何检测失败返回保守默认值）
"""

import os
import time
import socket
import subprocess
import platform
from typing import Dict, Optional

# 检测结果缓存
_last_check: Dict = {}
_last_check_time: float = 0
_CACHE_TTL = 20.0  # 缓存有效期（秒）


# ═══════════════════════════════════════════════════════════════
# 系统资源检测
# ═══════════════════════════════════════════════════════════════

def _get_cpu_percent() -> float:
    """获取当前 CPU 使用率（0~100），失败返回 50"""
    try:
        if platform.system() == "Windows":
            # Windows: 用 wmic
            result = subprocess.run(
                ["wmic", "cpu", "get", "loadpercentage"],
                capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.strip().split("\n")
            for line in lines:
                line = line.strip()
                if line.isdigit():
                    return float(line)
            return 50.0
        else:
            # Linux/macOS: 用 Python 管道替代 shell pipe
            result = subprocess.run(
                ["top", "-bn1"], capture_output=True, text=True, timeout=5
            )
            # 从 top 输出中提取 CPU 行的 idle 百分比
            cpu_lines = [l for l in result.stdout.split("\n") if "%Cpu" in l or "CPU" in l]
            result.stdout = "\n".join(cpu_lines) if cpu_lines else result.stdout
            # fallback to ps
            result = subprocess.run(
                ["ps", "-A", "-o", "%cpu", "--sort=-%cpu"],
                capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.strip().split("\n")
            if len(lines) > 1:
                values = [float(l.strip()) for l in lines[1:] if l.strip().replace(".", "").isdigit()]
                if values:
                    return min(sum(values), 100.0)
            return 50.0
    except Exception:
        return 50.0


def _get_memory_percent() -> float:
    """获取内存使用率（0~100），失败返回 50"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["wmic", "OS", "get", "TotalVisibleMemorySize,FreePhysicalMemory",
                 "/format:csv"],
                capture_output=True, text=True, timeout=5
            )
            # 解析 CSV 输出
            lines = result.stdout.strip().split("\n")
            for line in lines:
                parts = line.split(",")
                if len(parts) >= 3:
                    try:
                        total = float(parts[-2])
                        free = float(parts[-1])
                        if total > 0:
                            return round((1 - free / total) * 100, 1)
                    except (ValueError, IndexError):
                        pass
            return 50.0
        else:
            result = subprocess.run(
                ["free", "-m"],
                capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 2:
                parts = lines[1].split()
                if len(parts) >= 3:
                    total = float(parts[1])
                    used = float(parts[2])
                    if total > 0:
                        return round(used / total * 100, 1)
            return 50.0
    except Exception:
        return 50.0


def _get_disk_percent(path: str = None) -> float:
    """获取磁盘使用率（0~100），失败返回 50"""
    try:
        if path is None:
            path = os.path.expanduser("~")
        if platform.system() == "Windows":
            drive = os.path.splitdrive(path)[0] or "C:"
            result = subprocess.run(
                ["wmic", "logicaldisk", "where", f"name='{drive}'",
                 "get", "size,freespace", "/format:csv"],
                capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.strip().split("\n")
            for line in lines:
                parts = line.split(",")
                if len(parts) >= 3:
                    try:
                        free = float(parts[-2])
                        total = float(parts[-1])
                        if total > 0:
                            return round((1 - free / total) * 100, 1)
                    except (ValueError, IndexError):
                        pass
            return 50.0
        else:
            stat = os.statvfs(path)
            total = stat.f_frsize * stat.f_blocks
            free = stat.f_frsize * stat.f_bfree
            if total > 0:
                return round((1 - free / total) * 100, 1)
            return 50.0
    except Exception:
        return 50.0


# ═══════════════════════════════════════════════════════════════
# 网络状态检测
# ═══════════════════════════════════════════════════════════════

def _check_host_reachable(host: str, port: int = 443, timeout: float = 3.0) -> bool:
    """检测主机是否可达（TCP 连接）"""
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        return True
    except Exception:
        return False


def _check_gfw() -> bool:
    """检测是否存在 GFW（墙）
    
    策略：尝试连接 google.com，失败则可能被墙
    注：不精确，但够用（由于用户有 Mihomo TUN，实际可能全通）
    """
    return not _check_host_reachable("google.com", 443, timeout=2.0)


def _check_api_availability() -> Dict[str, bool]:
    """检测各 API 是否可达
    
    Returns:
        dict {api_name: is_reachable}
    """
    results = {}
    
    # 百炼 ASR API
    results["bailian_asr"] = _check_host_reachable(
        "dashscope.aliyuncs.com", 443, timeout=3.0
    )
    
    # DeepSeek API
    from .secrets import get_llm_config
    try:
        key, base, model = get_llm_config()
        if base:
            host = base.replace("https://", "").split("/")[0].split(":")[0]
            results["deepseek"] = _check_host_reachable(host, 443, timeout=3.0)
        else:
            results["deepseek"] = _check_host_reachable("api.deepseek.com", 443, timeout=3.0)
    except Exception:
        results["deepseek"] = False
    
    return results


# ═══════════════════════════════════════════════════════════════
# 主检测函数
# ═══════════════════════════════════════════════════════════════

def check_system_status(force: bool = False) -> Dict:
    """系统+网络状态一站式检测
    
    缓存 20 秒，避免重复检测浪费资源。
    
    Returns:
        dict {
            "cpu_percent": float,
            "memory_percent": float,
            "disk_percent": float,
            "network_ok": bool,
            "gfw_detected": bool,
            "youtube_reachable": bool,
            "api_available": bool,
            "api_details": dict,
            "system_ok": bool,         # 整体是否健康
            "resource_ok": bool,       # 资源是否充足 (CPU<80, RAM<80, Disk<90)
            "cached": bool,            # 是否使用缓存
        }
    """
    global _last_check, _last_check_time
    
    now = time.time()
    if not force and _last_check and (now - _last_check_time) < _CACHE_TTL:
        _last_check["cached"] = True
        return _last_check
    
    print(f"  [系统监控] 🔍 检测中...", end="", flush=True)
    
    cpu = _get_cpu_percent()
    mem = _get_memory_percent()
    disk = _get_disk_percent()
    
    print(f" CPU={cpu:.0f}% 内存={mem:.0f}% 磁盘={disk:.0f}%", end="", flush=True)
    
    youtube = _check_host_reachable("youtube.com", 443, timeout=3.0)
    gfw = _check_gfw()
    api_info = _check_api_availability()
    api_ok = any(api_info.values())
    network_ok = (youtube or not gfw)  # 能连YouTube或没墙=网络通
    
    system_ok = cpu < 90 and mem < 90 and disk < 95 and network_ok
    resource_ok = cpu < 80 and mem < 80 and disk < 90
    
    result = {
        "cpu_percent": cpu,
        "memory_percent": mem,
        "disk_percent": disk,
        "network_ok": network_ok,
        "gfw_detected": gfw,
        "youtube_reachable": youtube,
        "api_available": api_ok,
        "api_details": api_info,
        "system_ok": system_ok,
        "resource_ok": resource_ok,
        "cached": False,
        "checked_at": time.time(),
    }
    
    _last_check = result
    _last_check_time = now
    
    print(f" 网络={'✅' if network_ok else '❌'} API={'✅' if api_ok else '❌'}")
    
    return result


# ═══════════════════════════════════════════════════════════════
# 2.4 模型选择策略
# ═══════════════════════════════════════════════════════════════

def decide_upgrade_model(
    current_model: str,
    system_status: Dict,
    p2_severity: float = 0.0,
    proper_count: int = 0,
) -> Dict:
    """升级模型选择策略
    
    根据 system_monitor 数据计算性价比，决定：
    - 升 whisper large（本地，免费但慢）
    - 换百炼 ASR（API，快但可能收费）
    - 双模型交叉验证（最准但最贵）
    - 不升级（P2误报，容忍）
    
    性价比公式：benefit / cost
    
    Args:
        current_model: 当前模型名 ("tiny"|"base"|"small"|"medium"|"large")
        system_status: check_system_status() 输出
        p2_severity: P2 严重度（effective / threshold）
        proper_count: 专有名词犹豫词数量
    
    Returns:
        dict with "choice", "reason", "estimated_cost", "estimated_benefit"
    """
    choices = ["keep", "whisper_large", "bailian_asr", "dual"]
    
    cpu = system_status.get("cpu_percent", 50)
    mem = system_status.get("memory_percent", 50)
    network_ok = system_status.get("network_ok", True)
    api_ok = system_status.get("api_available", True)
    
    # 严重度评估
    severity = min(p2_severity / 1.0, 10.0) / 10.0  # 0~1
    
    if severity < 0.2:
        return {"choice": "keep", "reason": f"严重度低({p2_severity:.2f})，不升级", "estimated_cost": 0, "estimated_benefit": severity}
    
    # ── 算性价比 ──
    cost_whisper = 3.0 if current_model in ("tiny", "base") else 1.0  # tiny/base升large成本高
    cost_bailian = 1.0  # API固定成本
    cost_dual = cost_whisper + cost_bailian
    
    benefit = severity * (0.5 + proper_count * 0.1)
    
    # ── 决策 ──
    if not network_ok:
        # 网络不通 → 无法API
        if cpu < 70 and mem < 70:
            return {"choice": "whisper_large", "reason": f"网络通但API不通，本地资源充足(CPU={cpu}%)，升large", "estimated_cost": cost_whisper, "estimated_benefit": benefit}
        else:
            return {"choice": "keep", "reason": f"网络不通+本地资源紧张({cpu}%)，容忍", "estimated_cost": 0, "estimated_benefit": 0}
    
    if not api_ok:
        # API不通但网络通
        if cpu < 70:
            return {"choice": "whisper_large", "reason": f"API不通但网络通，本地资源够，升large", "estimated_cost": cost_whisper, "estimated_benefit": benefit}
        return {"choice": "keep", "reason": f"API不通+CPU高({cpu}%)，不升级", "estimated_cost": 0, "estimated_benefit": 0}
    
    # 网络+API都通
    value_whisper = benefit / cost_whisper if cost_whisper > 0 else 0
    value_bailian = benefit / cost_bailian
    value_dual = benefit / cost_dual
    
    if value_bailian >= value_whisper and value_bailian >= value_dual:
        if proper_count >= 3 and p2_severity > 5:
            choice = "dual"
            reason = f"专有名词多({proper_count})且严重(severity={p2_severity:.1f})，双保险"
        else:
            choice = "bailian_asr"
            reason = f"百炼ASR性价比最高(value={value_bailian:.2f})"
    elif value_dual >= value_whisper and proper_count >= 2:
        choice = "dual"
        reason = f"专有名词多({proper_count})，双保险更稳妥"
    else:
        choice = "whisper_large"
        reason = f"本地升级最有价值(value={value_whisper:.2f})"
    
    cost_map = {"bailian_asr": cost_bailian, "whisper_large": cost_whisper, "dual": cost_dual, "keep": 0}
    return {"choice": choice, "reason": reason, "estimated_cost": cost_map.get(choice, 0), "estimated_benefit": benefit}
