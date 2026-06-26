"""
In-memory state for Bridge tasks and escrow.
"""

import time
import uuid
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from typing import Any


FEE_RATE = Decimal("0.05")  # 5% matchmaking fee


@dataclass
class BridgeTask:
    id: str = field(default_factory=lambda: f"bridge-{uuid.uuid4().hex[:8]}")
    description: str = ""
    status: str = "posted"  # posted, accepted, proof_submitted, verified, disputed, completed, refunded, failed
    budget_usdc: Decimal = Decimal("0")
    fee_usdc: Decimal = Decimal("0")
    escrow_status: str = "locked"  # locked, released, refunded, frozen
    location: Any = None
    verification_criteria: list = field(default_factory=list)
    priority: str = "standard"
    deadline_hours: int = 24
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    worker_id: str | None = None
    dispute_reason: str = ""


_tasks: dict[str, BridgeTask] = {}


def create_task(
    description: str,
    budget_usdc: Decimal,
    location: Any = None,
    verification_criteria: list | None = None,
    priority: str = "standard",
    deadline_hours: int = 24,
) -> BridgeTask:
    fee = (budget_usdc * FEE_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    task = BridgeTask(
        description=description,
        budget_usdc=budget_usdc,
        fee_usdc=fee,
        location=location,
        verification_criteria=verification_criteria or [],
        priority=priority,
        deadline_hours=deadline_hours,
    )
    _tasks[task.id] = task
    return task


def get_task(task_id: str) -> BridgeTask | None:
    return _tasks.get(task_id)


def list_tasks(status: str | None = None) -> list[BridgeTask]:
    tasks = list(_tasks.values())
    if status:
        tasks = [t for t in tasks if t.status == status]
    return tasks


def update_task_status(task_id: str, status: str, escrow_status: str | None = None, worker_id: str | None = None) -> BridgeTask | None:
    task = _tasks.get(task_id)
    if task is None:
        return None
    task.status = status
    if escrow_status:
        task.escrow_status = escrow_status
    if worker_id:
        task.worker_id = worker_id
    return task


def dispute_task(task_id: str, reason: str) -> BridgeTask | None:
    task = _tasks.get(task_id)
    if task is None:
        return None
    task.status = "disputed"
    task.escrow_status = "frozen"
    task.dispute_reason = reason
    return task


def bridge_stats() -> dict:
    tasks = list(_tasks.values())
    return {
        "total_tasks": len(tasks),
        "posted": sum(1 for t in tasks if t.status == "posted"),
        "completed": sum(1 for t in tasks if t.status == "completed"),
        "disputed": sum(1 for t in tasks if t.status == "disputed"),
        "total_budget_usdc": sum((t.budget_usdc for t in tasks), Decimal("0")),
        "total_fees_usdc": sum((t.fee_usdc for t in tasks), Decimal("0")),
    }
