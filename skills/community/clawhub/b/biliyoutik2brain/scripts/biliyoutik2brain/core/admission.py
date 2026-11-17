"""
BiliYouTik2Brain — 任务准入控制

职责：
  1. 在任务启动前检查资源是否充足
  2. 资源不足 → 拒绝或加入 pending 队列
  3. 资源充足 → 绿灯放行 + 半秒准入决策
"""

import os
import json
import time
import subprocess
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List


# ═══════════════════════════════════════════════════════════════
# AdmissionDecision — 准入决策
# ═══════════════════════════════════════════════════════════════

@dataclass
class AdmissionDecision:
    """半秒资源准入决策"""
    admitted: bool = False                 # 是否放行
    reason: str = ""                       # 决策原因
    required_ram_gb: float = 0.5           # 最低内存需求
    required_disk_gb: float = 1.0          # 最低磁盘需求
    required_network_ms: float = 2000      # 最大允许延迟
    estimated_duration_s: int = 0          # 预估耗时
    pending_queue_length: int = 0          # 当前排队长度
    degraded: bool = False                 # 是否降级执行
    degraded_ops: List[str] = field(default_factory=list)  # 降级了哪些功能


def try_admit(
    env: Dict[str, Any],
    video_duration_s: int = 0,
    priority: int = 0,
    platform: str = "",
) -> AdmissionDecision:
    """尝试准入一个任务（半秒决策，不调LLM）
    
    Args:
        env: EnvironmentContext.to_dict() 或兼容字典
        video_duration_s: 视频时长（秒），用于预估资源
        priority: 优先级（0=普通，正数=更高，负数=更低）
    
    Returns:
        AdmissionDecision — admitted=True 表示放行
    """
    decision = AdmissionDecision()

    # ── 检查必需资源 ──
    ram_avail = env.get("ram_available_gb", 0)
    disk_avail = env.get("disk_free_gb", 0)
    lat_ms = env.get("network_latency_ms", 0)
    cpu_pct = env.get("cpu_usage_percent", 50)

    # 内存不足
    if ram_avail < decision.required_ram_gb:
        decision.reason = f"内存不足 ({ram_avail:.1f}GB < {decision.required_ram_gb}GB)"
        return decision

    # 磁盘不足
    if disk_avail < decision.required_disk_gb:
        decision.reason = f"磁盘不足 ({disk_avail:.1f}GB < {decision.required_disk_gb}GB)"
        return decision

    # 网络不通
    if lat_ms > decision.required_network_ms and lat_ms > 0:
        decision.reason = f"网络延迟过高 ({lat_ms:.0f}ms > {decision.required_network_ms:.0f}ms)"
        return decision

    # 代理检测：YouTube 必须走代理
    if platform.lower() == "youtube":
        if not env.get("proxy_available", False):
            decision.reason = "YouTube 需要代理但 mihomo 不可用，请先启动代理"
            return decision

    # ── 预估资源消耗 ──
    # 1分钟视频 ≈ 10MB 临时文件
    est_duration = max(video_duration_s, 60)
    est_disk_mb = (est_duration / 60) * 30  # 音频+临时文件
    est_duration_str = f"{est_duration // 60}分{est_duration % 60}秒" if est_duration >= 60 else f"{est_duration}秒"

    # ── 检查 pending 队列长度 ──
    pending_file = os.path.expanduser("~/.biliyoutik2brain_run/queue.json")
    queue_len = 0
    if os.path.exists(pending_file):
        try:
            with open(pending_file) as f:
                queue = json.load(f)
                queue_len = len(queue)
        except Exception:
            pass
    decision.pending_queue_length = queue_len

    # 队列过长 → 降级但放行（不阻塞）
    if queue_len > 5 and priority <= 0:
        decision.degraded = True
        decision.degraded_ops.append("低优先级，队列已满")

    # ── 降级检查（资源紧张但仍可运行） ──
    if ram_avail < 2.0:
        decision.degraded = True
        decision.degraded_ops.append("低内存降级 (whisper→tiny)")
    if cpu_pct > 80:
        decision.degraded = True
        decision.degraded_ops.append("CPU高负载降级 (减少并发)")
    if lat_ms > 500 and lat_ms > 0:
        decision.degraded = True
        decision.degraded_ops.append("高延迟降级 (延长超时)")

    # ── 通过 ──
    decision.admitted = True
    decision.estimated_duration_s = est_duration

    if decision.degraded:
        ops = ", ".join(decision.degraded_ops)
        decision.reason = f"降级放行 ({ops}) — 预估{est_disk_mb:.0f}MB磁盘"
    else:
        decision.reason = f"正常放行 — 预估{est_disk_mb:.0f}MB磁盘 {est_duration_str}"

    return decision


# ═══════════════════════════════════════════════════════════════
# FFmpeg 自愈
# ═══════════════════════════════════════════════════════════════

_FFMPEG_LAST_CRASH = 0.0
_FFMPEG_CRASH_COUNT = 0
_FFMPEG_MAX_CRASHES = 3
_FFMPEG_COOLDOWN = 300  # 5分钟内崩溃3次进入冷却


def ffmpeg_health_check() -> bool:
    """检查 FFmpeg 是否可用"""
    import shutil
    return shutil.which("ffmpeg") is not None


def ffmpeg_revive() -> bool:
    """尝试恢复 FFmpeg（重新安装/修复）"""
    import shutil
    
    # 检查 ffmpeg 是否真的不可用
    if shutil.which("ffmpeg"):
        return True  # 其实可用，标记为恢复
    
    # 尝试 apt install（有权限的话）
    try:
        result = subprocess.run(
            ["apt-get", "install", "-y", "--reinstall", "ffmpeg"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0 and shutil.which("ffmpeg"):
            print("  [自愈] FFmpeg 已重新安装")
            return True
    except Exception:
        pass
    
    # 尝试 pip install ffmpeg-python（Python 包装）
    try:
        result = subprocess.run(
            ["pip3", "install", "--quiet", "ffmpeg-python"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print("  [自愈] ffmpeg-python 已安装")
            return True
    except Exception:
        pass
    
    print("  [自愈] FFmpeg 恢复失败，需人工介入")
    return False


def handle_ffmpeg_crash() -> bool:
    """处理 FFmpeg 崩溃，自动重试+冷却"""
    global _FFMPEG_LAST_CRASH, _FFMPEG_CRASH_COUNT
    now = time.time()

    # 冷却期内
    if now - _FFMPEG_LAST_CRASH < _FFMPEG_COOLDOWN:
        _FFMPEG_CRASH_COUNT += 1
    else:
        _FFMPEG_CRASH_COUNT = 1

    _FFMPEG_LAST_CRASH = now

    if _FFMPEG_CRASH_COUNT > _FFMPEG_MAX_CRASHES:
        print(f"  ⚠️ FFmpeg 5分钟内崩溃{_FFMPEG_CRASH_COUNT}次，进入冷却")
        return False

    print(f"  🔧 FFmpeg 崩溃 ({_FFMPEG_CRASH_COUNT}/{_FFMPEG_MAX_CRASHES})，尝试自愈...")
    return ffmpeg_revive()


# ═══════════════════════════════════════════════════════════════
# 性能指标采集（轻量，不调外部监控系统）
# ═══════════════════════════════════════════════════════════════

_METRICS_FILE = os.path.expanduser("~/.biliyoutik2brain_run/metrics.jsonl")


@dataclass
class TaskMetrics:
    """单次任务性能指标"""
    url: str = ""
    video_duration_s: int = 0
    pipeline_duration_s: float = 0.0
    model_used: str = "base"
    node_timings: Dict[str, float] = field(default_factory=dict)  # node_id → 耗时
    errors: List[str] = field(default_factory=list)
    degraded: bool = False
    timestamp: str = ""

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["timestamp"] = self.timestamp or time.strftime("%Y-%m-%dT%H:%M:%S")
        return d


def record_metrics(m: TaskMetrics):
    """记录单次任务指标到 metrics.jsonl"""
    os.makedirs(os.path.dirname(_METRICS_FILE), exist_ok=True)
    try:
        with open(_METRICS_FILE, "a") as f:
            f.write(json.dumps(m.to_dict(), ensure_ascii=False) + "\n")
    except Exception:
        pass


def get_recent_metrics(n: int = 20) -> List[Dict]:
    """读取最近 N 条指标"""
    results = []
    try:
        if not os.path.exists(_METRICS_FILE):
            return results
        # tail 最后 N 行
        with open(_METRICS_FILE) as f:
            lines = f.readlines()
        for line in lines[-n:]:
            try:
                results.append(json.loads(line.strip()))
            except Exception:
                pass
    except Exception:
        pass
    return results


def estimate_throughput() -> float:
    """估算当前吞吐量（分钟/分钟），用于自适应调参"""
    recent = get_recent_metrics(20)
    if not recent:
        return 1.0
    # 处理时间 / 视频时长比
    ratios = []
    for m in recent:
        dur = m.get("video_duration_s", 0)
        pipe = m.get("pipeline_duration_s", 0)
        if dur > 0 and pipe > 0:
            ratios.append(dur / pipe)
    if not ratios:
        return 1.0
    # 取中位数
    ratios.sort()
    mid = ratios[len(ratios) // 2]
    return round(mid, 2)


def suggest_whisper_model(current: str = "base") -> str:
    """基于历史吞吐量建议 whisper 模型"""
    tp = estimate_throughput()
    if tp < 0.3:
        return "tiny"
    elif tp < 0.6:
        return "base"
    return "base"  # 暂不加 small/medium
