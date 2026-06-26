"""
In-memory priority task queue.
"""

import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    status: str = "pending"  # pending, running, completed, failed
    priority: int = 0
    tags: list[str] = field(default_factory=list)
    payload: Any = None
    result: Any = None
    error: str = ""
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))


_tasks: dict[str, Task] = {}


def create_task(title: str, payload: Any, priority: int = 0, tags: list[str] | None = None) -> Task:
    task = Task(title=title, payload=payload, priority=priority, tags=tags or [])
    _tasks[task.id] = task
    return task


def get_task(task_id: str) -> Task | None:
    return _tasks.get(task_id)


def list_tasks(status: str | None = None, tag: str | None = None) -> list[Task]:
    results = list(_tasks.values())
    if status:
        results = [t for t in results if t.status == status]
    if tag:
        results = [t for t in results if tag in t.tags]
    return sorted(results, key=lambda t: -t.priority)


def claim_next() -> Task | None:
    """Claim the highest-priority pending task."""
    pending = [t for t in _tasks.values() if t.status == "pending"]
    if not pending:
        return None
    pending.sort(key=lambda t: -t.priority)
    task = pending[0]
    task.status = "running"
    return task


def complete_task(task_id: str, result: Any) -> Task | None:
    task = _tasks.get(task_id)
    if task is None:
        return None
    task.status = "completed"
    task.result = result
    return task


def fail_task(task_id: str, error: str) -> Task | None:
    task = _tasks.get(task_id)
    if task is None:
        return None
    task.status = "failed"
    task.error = error
    return task


def queue_stats() -> dict[str, int]:
    tasks = list(_tasks.values())
    return {
        "total": len(tasks),
        "pending": sum(1 for t in tasks if t.status == "pending"),
        "running": sum(1 for t in tasks if t.status == "running"),
        "completed": sum(1 for t in tasks if t.status == "completed"),
        "failed": sum(1 for t in tasks if t.status == "failed"),
    }
