"""
BiliYouTik2Brain — 资源配置 + 自适应调度配置

v3: 平台注册→ registry.py, 并发控制→ slots.py, 机密→ secrets.py
此文件只保留: 蜂群调参 + 资源评估 + 任务统计 + workflow管理
"""

from typing import Tuple, Optional
from ..core.schemas import RouteDecision

# 保持向后兼容：从新模块导出
from .registry import PlatformRegistry, _init_registry
from .slots import (
    init_concurrency,
    acquire_light_slot, release_light_slot, queue_light, dequeue_light,
    acquire_heavy_slot, release_heavy_slot,
)
from .secrets import DASHSCOPE_BASE_URL, DASHSCOPE_MULTIMODAL_URL


# ============================================================
# 蜂群参数自动校准（v1.8.1）
# ============================================================

SWARM_BASE_THRESHOLD = 4000
SWARM_BASE_CHUNK_SIZE = 4000


def auto_tune_swarm_params(
    text_len: int,
    low_conf_count: int,
    llm_response_ms: int = 0,
) -> Tuple[int, int]:
    # 很短 → 不分块
    if text_len < 2000:
        return text_len + 100, text_len + 100
    
    threshold = SWARM_BASE_THRESHOLD
    chunk_size = SWARM_BASE_CHUNK_SIZE
    
    density = low_conf_count / max(text_len, 1)
    if density > 0.1:
        factor = 0.7
    elif density > 0.05:
        factor = 0.85
    elif density < 0.01:
        factor = 1.3
    else:
        factor = 1.0
    
    chunk_size = int(SWARM_BASE_CHUNK_SIZE * factor)
    
    if llm_response_ms > 0 and chunk_size > 2000:
        per_char_ms = llm_response_ms / text_len
        if per_char_ms > 0.02:
            chunk_size = min(chunk_size, 3000)
        elif per_char_ms < 0.005:
            chunk_size = min(int(chunk_size * 1.2), 6000)
    
    chunk_size = max(1500, min(chunk_size, 6000))
    threshold = max(chunk_size + 100, min(threshold, chunk_size + 500))
    
    return threshold, chunk_size


# ─── 资源感知调度 ────────────────────────────────────────

import json, os

_WORKFLOW_HISTORY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "workflow_history.json"
)


def _load_history() -> dict:
    try:
        if os.path.exists(_WORKFLOW_HISTORY_PATH):
            with open(_WORKFLOW_HISTORY_PATH) as f:
                return json.load(f)
    except Exception:
        pass
    return {"cloud_tasks": [], "estimated_capacity": None}


def _save_history(history: dict):
    try:
        with open(_WORKFLOW_HISTORY_PATH, "w") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def assess_and_route(
    duration_s: int,
    model_complexity: float = 1.0,
    safety_margin: float = 0.8,
    local_available: bool = False,
    local_capacity: float = 0.0,
    system_status: dict = None,
) -> RouteDecision:
    """统一资源评估+决策（含pending逻辑）
    
    升级版（Phase 2.1+2.4）：集成系统状态监控，根据实时资源状况做模型选择。
    
    Args:
        duration_s: 视频时长（秒）
        model_complexity: 模型复杂度系数
        safety_margin: 安全裕量
        local_available: 是否可用本地算力
        local_capacity: 本地容量估算
        system_status: check_system_status() 输出（可选，不传则自动检测）
    """
    from .system_monitor import check_system_status
    
    decision = RouteDecision()
    
    # ── 系统状态检测（Phase 2.1） ──
    if system_status is None:
        system_status = check_system_status()
    
    cpu_pct = system_status.get("cpu_percent", 50)
    mem_pct = system_status.get("memory_percent", 50)
    disk_pct = system_status.get("disk_percent", 50)
    network_ok = system_status.get("network_ok", True)
    api_ok = system_status.get("api_available", True)
    
    MIN_CLOUD_CAPACITY = 60.0
    history = _load_history()
    estimated_capacity = history.get("estimated_capacity")
    
    if estimated_capacity is None:
        estimated_capacity = MIN_CLOUD_CAPACITY
    if not local_capacity:
        local_capacity = estimated_capacity * 3
    
    workload = duration_s / 60 * model_complexity
    decision.estimated_workload = workload
    decision.cloud_capacity = estimated_capacity
    decision.local_capacity = local_capacity
    decision.cloud_available = network_ok
    decision.local_available = local_available
    
    # ── Phase 2.4: 模型选择策略 ──
    # 根据系统资源动态调整模型
    model_weights = {"tiny": 0.5, "base": 1.0, "small": 2.0, "medium": 4.0, "large": 8.0}
    
    # 资源紧张 → 降级模型
    if cpu_pct > 85 or mem_pct > 85:
        decision.model = "tiny"
        decision.reason = f"系统资源紧张(CPU={cpu_pct}%,MEM={mem_pct}%), 降级tiny"
    elif cpu_pct > 70 or mem_pct > 75:
        decision.model = "small"
        decision.reason = f"资源中等(CPU={cpu_pct}%,MEM={mem_pct}%), small模型平衡"
    else:
        decision.model = "base"
        decision.reason = f"资源充足(CPU={cpu_pct}%,MEM={mem_pct}%)"
    
    # 磁盘空间不足 → 缩减缓存
    if disk_pct > 90:
        decision.reason += f", 磁盘告警({disk_pct}%)"
    
    # ── P0: 判断是否pending ──
    PENDING_THRESHOLD = 0.5  # 50%容量以下才pending
    if workload > estimated_capacity * safety_margin:
        if local_available and workload <= local_capacity * safety_margin:
            decision.target = "local"
            decision.reason = f"本地可用 (workload={workload:.1f} < capacity={local_capacity:.1f})"
        elif workload > estimated_capacity * (1 + PENDING_THRESHOLD):
            decision.target = "pending"
            decision.reason = f"算力不足: workload={workload:.1f}, cloud={estimated_capacity:.1f}"
        else:
            decision.target = "cloud"
            decision.reason = f"超载但可处理: workload={workload:.1f} > capacity={estimated_capacity:.1f}"
    else:
        decision.target = "cloud"
        decision.reason = f"充足: workload={workload:.1f}, capacity={estimated_capacity:.1f}"
    
    # VAD触发条件
    decision.use_vad = workload > estimated_capacity * 0.8
    decision.use_chunked = duration_s > 1800
    
    return decision


def record_task(duration_s: int, model: str, elapsed_s: float, cpu_usage: float):
    """记录任务指标，校准容量公式"""
    history = _load_history()
    if "cloud_tasks" not in history:
        history["cloud_tasks"] = []
    
    history["cloud_tasks"].append({
        "duration": duration_s,
        "model": model,
        "elapsed": elapsed_s,
        "cpu": cpu_usage,
        "time": os.path.join(os.path.dirname(__file__), "..", "..", "..")
    })
    
    model_weight = {"tiny": 0.5, "base": 1.0, "small": 2.0, "medium": 4.0, "large": 8.0}.get(model, 1.0)
    workload = duration_s / 60 * model_weight
    
    # 只用最近10个任务算平滑容量
    recent = history["cloud_tasks"][-10:]
    if recent:
        total_workload = sum(
            (t.get("duration") or t.get("duration_s", 0)) / 60 * model_weight
            for t in recent
        )
        total_time = sum(t.get("elapsed") or t.get("elapsed_s", 0) for t in recent)
        if total_time > 0:
            new_capacity = total_workload / (total_time / 60) * 60
            history["estimated_capacity"] = max(10, min(new_capacity, 480))
    
    _save_history(history)


def _task_timestamp() -> str:
    import time
    return time.strftime("%Y-%m-%d %H:%M:%S")


# ─── 待处理任务队列 ──────────────────────────────────────

_PENDING_FILE = os.path.join(os.path.expanduser("~/.biliyoutik2brain"), "pending.json")


def list_pending() -> list:
    if not os.path.exists(_PENDING_FILE):
        return []
    try:
        with open(_PENDING_FILE) as f:
            return json.load(f)
    except Exception:
        return []


def add_pending(url: str, duration_s: int, workload: float, notes: str = "") -> str:
    import uuid
    wf_id = f"wf_{uuid.uuid4().hex[:8]}"
    pending = list_pending()
    pending.append({
        "id": wf_id,
        "url": url,
        "duration_s": duration_s,
        "workload": workload,
        "notes": notes,
        "created_at": _task_timestamp(),
        "status": "pending",
    })
    os.makedirs(os.path.dirname(_PENDING_FILE), exist_ok=True)
    with open(_PENDING_FILE, "w") as f:
        json.dump(pending, f, ensure_ascii=False, indent=2)
    return wf_id


def remove_pending(wf_id: str) -> bool:
    pending = list_pending()
    filtered = [p for p in pending if p["id"] != wf_id]
    if len(filtered) == len(pending):
        return False
    with open(_PENDING_FILE, "w") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
    return True


def schedule_pending(wf_id: str, channel: str = None, to: str = None) -> bool:
    """安排待处理任务（延后执行）"""
    pending = list_pending()
    for p in pending:
        if p["id"] == wf_id:
            p["status"] = "scheduled"
            with open(_PENDING_FILE, "w") as f:
                json.dump(pending, f, ensure_ascii=False, indent=2)
            message = f"任务已安排：{p.get('url', '')[:60]}"
            return True
    return False


def record_completed(url: str):
    """记录已完成URL（冷却期防递归自旋）"""
    completed_file = os.path.join(os.path.expanduser("~/.biliyoutik2brain"), "completed.json")
    completed = []
    if os.path.exists(completed_file):
        try:
            with open(completed_file) as f:
                completed = json.load(f)
        except Exception:
            completed = []
    import time
    completed.append({"url": url, "time": time.time()})
    # 只保留最近100个
    completed = completed[-100:]
    os.makedirs(os.path.dirname(completed_file), exist_ok=True)
    with open(completed_file, "w") as f:
        json.dump(completed, f, ensure_ascii=False, indent=2)
