"""兼容别名 — 调度决策已迁入 scheduler.py（v3.0 统一入口）

ZIP 版 orchestrator.py 的轻量级 helper 函数（get_model_for / 
get_concurrency_for / get_timeout_for）保留在此，高层调度
逻辑委托到 scheduler.py。

此文件保留向后兼容，原有 ZIP API 不变。
"""

from typing import Tuple, List, Dict

# ── 兼容：重导出 scheduler 的核心接口 ──
from .scheduler import (
    Task,
    TaskPriority,
    SchedulerDecision,
    decide,
    prioritize,
    diagnose,
    run_parallel,
    _estimate_cost,
)


# ── 轻量级 Helper（来自 ZIP orchestrator，scheduler 中无对应快速查询） ──

def get_model_for(duration_s: int, ram_avail_gb: float) -> str:
    """根据视频时长和可用内存，快速推荐 whisper 模型大小"""
    if ram_avail_gb < 2:
        return "tiny"
    if ram_avail_gb < 4 or duration_s > 3600:
        return "base"
    if duration_s > 1800:
        return "small"
    if duration_s < 300 and ram_avail_gb > 8:
        return "medium"
    return "base"


def get_concurrency_for(ram_avail_gb: float, cpu_pct: float, duration_s: int) -> int:
    """快速推荐下载/转录并发数"""
    if ram_avail_gb < 2 or cpu_pct > 80:
        return 1
    if ram_avail_gb < 4 or duration_s > 3600:
        return 2
    if duration_s < 600 and ram_avail_gb > 8:
        return 4
    return 3


def get_timeout_for(duration_s: int, model: str = "base", vad: bool = False) -> int:
    """快速估算下载/转录超时（秒）"""
    base = 120
    per_minute = {"tiny": 2, "base": 4, "small": 8, "medium": 16}.get(model, 4)
    estimated = base + (duration_s / 60) * per_minute
    if vad:
        estimated *= 1.2
    return max(60, int(estimated))
