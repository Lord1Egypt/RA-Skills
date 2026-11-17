"""
BiliYouTik2Brain — 优先级队列 (v4.0)

支持用户设优先级/插队，pending 队列持久化重启不丢。
"""

import os
import json
import time
import uuid
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import IntEnum


class Priority(IntEnum):
    """任务优先级"""
    URGENT = 0     # 紧急（插队）
    HIGH = 1       # 高
    MEDIUM = 2     # 中（默认）
    LOW = 3        # 低


@dataclass
class QueuedTask:
    """队列中的任务"""
    task_id: str
    url: str
    priority: int = Priority.MEDIUM
    title: str = ""
    uploader: str = ""
    duration_s: int = 0
    created_at: str = ""
    scheduled_at: Optional[str] = None  # 定时执行时间
    status: str = "queued"  # queued / running / done / failed / cancelled
    error: str = ""
    metadata: Dict = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════
#  持久化队列
# ═══════════════════════════════════════════════════════════

_QUEUE_PATH = os.path.expanduser("~/.biliyoutik2brain/pending_queue.json")


def _load_queue() -> List[Dict]:
    """加载持久化队列"""
    if not os.path.exists(_QUEUE_PATH):
        return []
    try:
        with open(_QUEUE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_queue(tasks: List[Dict]):
    """保存队列"""
    os.makedirs(os.path.dirname(_QUEUE_PATH), exist_ok=True)
    with open(_QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════
#  队列操作
# ═══════════════════════════════════════════════════════════

def add_to_queue(
    url: str,
    priority: int = Priority.MEDIUM,
    title: str = "",
    uploader: str = "",
    duration_s: int = 0,
    scheduled_at: Optional[str] = None,
    metadata: Dict = None,
) -> str:
    """添加任务到队列

    Args:
        url: 视频链接
        priority: 优先级
        title: 标题
        uploader: UP主
        duration_s: 时长
        scheduled_at: 定时执行时间（ISO 格式）
        metadata: 额外元数据

    Returns:
        task_id
    """
    tasks = _load_queue()

    task_id = f"qt_{uuid.uuid4().hex[:8]}"
    task = {
        "task_id": task_id,
        "url": url,
        "priority": priority,
        "title": title,
        "uploader": uploader,
        "duration_s": duration_s,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scheduled_at": scheduled_at,
        "status": "queued",
        "error": "",
        "metadata": metadata or {},
    }

    tasks.append(task)
    _save_queue(tasks)

    return task_id


def get_next_task() -> Optional[Dict]:
    """获取下一个任务（按优先级排序，返回最高优先级的 queued 任务）"""
    tasks = _load_queue()

    # 过滤 queued 且未到定时时间的任务
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    ready = [
        t for t in tasks
        if t.get("status") == "queued" and (
            not t.get("scheduled_at") or t["scheduled_at"] <= now
        )
    ]

    if not ready:
        return None

    # 按优先级排序（数字越小越优先）
    ready.sort(key=lambda t: (t.get("priority", Priority.MEDIUM), t.get("created_at", "")))

    return ready[0]


def mark_running(task_id: str):
    """标记任务为运行中"""
    tasks = _load_queue()
    for t in tasks:
        if t.get("task_id") == task_id:
            t["status"] = "running"
            break
    _save_queue(tasks)


def mark_done(task_id: str):
    """标记任务为完成"""
    tasks = _load_queue()
    for t in tasks:
        if t.get("task_id") == task_id:
            t["status"] = "done"
            t["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            break
    _save_queue(tasks)


def mark_failed(task_id: str, error: str = ""):
    """标记任务为失败"""
    tasks = _load_queue()
    for t in tasks:
        if t.get("task_id") == task_id:
            t["status"] = "failed"
            t["error"] = error[:500]
            t["failed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            break
    _save_queue(tasks)


def cancel_task(task_id: str) -> bool:
    """取消任务"""
    tasks = _load_queue()
    for t in tasks:
        if t.get("task_id") == task_id and t.get("status") == "queued":
            t["status"] = "cancelled"
            _save_queue(tasks)
            return True
    return False


def reprioritize(task_id: str, new_priority: int) -> bool:
    """调整任务优先级（插队）"""
    tasks = _load_queue()
    for t in tasks:
        if t.get("task_id") == task_id and t.get("status") == "queued":
            t["priority"] = new_priority
            _save_queue(tasks)
            return True
    return False


def list_queue(status: str = "all") -> List[Dict]:
    """列出队列中的任务"""
    tasks = _load_queue()
    if status != "all":
        tasks = [t for t in tasks if t.get("status") == status]
    return sorted(tasks, key=lambda t: (t.get("priority", 99), t.get("created_at", "")))


def clear_completed(max_age_days: int = 7):
    """清理完成的旧任务"""
    tasks = _load_queue()
    cutoff = time.time() - (max_age_days * 86400)

    filtered = []
    for t in tasks:
        if t.get("status") in ("done", "failed", "cancelled"):
            completed_at = t.get("completed_at") or t.get("failed_at", "")
            if completed_at:
                try:
                    ct = time.mktime(time.strptime(completed_at, "%Y-%m-%d %H:%M:%S"))
                    if ct > cutoff:
                        filtered.append(t)
                except Exception:
                    filtered.append(t)
            else:
                filtered.append(t)
        else:
            filtered.append(t)

    _save_queue(filtered)


# ═══════════════════════════════════════════════════════════
#  智能并发
# ═══════════════════════════════════════════════════════════

def compute_max_concurrency(
    cpu_cores: int = 4,
    ram_gb: float = 8.0,
    has_gpu: bool = False,
    network_mbps: float = 100,
    task_type: str = "transcribe",
) -> int:
    """基于环境计算最大并发数

    Args:
        cpu_cores: CPU 核心数
        ram_gb: 内存（GB）
        has_gpu: 是否有 GPU
        network_mbps: 网络带宽（Mbps）
        task_type: 任务类型（transcribe / download / ocr / enhance）

    Returns:
        推荐最大并发数
    """
    # 基础并发（按 CPU）
    base = max(1, cpu_cores // 2)

    # 内存限制
    ram_limit = int(ram_gb / 2)  # 每任务约 2GB

    # 网络限制（下载类任务）
    net_limit = max(1, int(network_mbps / 50))  # 每任务约 50Mbps

    # 任务类型权重
    weights = {
        "download": 1.0,
        "transcribe": 0.5,   # 转录 CPU 密集，减半
        "ocr": 0.3,          # OCR 更密集
        "enhance": 0.7,      # LLM 增强，主要等 API
    }
    weight = weights.get(task_type, 0.5)

    # 综合
    concurrency = min(base, ram_limit, net_limit)
    concurrency = int(concurrency * weight)

    # GPU 可以稍微提高转录并发
    if has_gpu and task_type == "transcribe":
        concurrency = int(concurrency * 1.5)

    return max(1, min(concurrency, 8))  # 最多 8
