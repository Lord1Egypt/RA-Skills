"""
In-memory state for Bridge tasks and escrow.
"""

import os
import time
import uuid
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from typing import Any


FEE_RATE = Decimal(os.getenv("BRIDGE_FEE_RATE", "0.05"))
SURGE_URGENT = Decimal(os.getenv("BRIDGE_SURGE_URGENT", "0.15"))   # +15%
SURGE_CRITICAL = Decimal(os.getenv("BRIDGE_SURGE_CRITICAL", "0.40"))  # +40%


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
    milestones: list | None = None
    milestones_completed: int = 0
    milestones_total: int = 0
    budget_released_usdc: Decimal = Decimal("0")


_tasks: dict[str, BridgeTask] = {}


@dataclass
class WorkerReputation:
    worker_id: str
    tasks_completed: int = 0
    tasks_failed: int = 0
    tasks_disputed: int = 0
    total_earned_usdc: Decimal = Decimal("0")

    @property
    def total_tasks(self) -> int:
        return self.tasks_completed + self.tasks_failed + self.tasks_disputed

    @property
    def score(self) -> Decimal:
        if self.total_tasks == 0:
            return Decimal("0.5")  # neutral for new workers
        return (Decimal(self.tasks_completed) / Decimal(self.total_tasks)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )


_workers: dict[str, WorkerReputation] = {}


def get_worker(worker_id: str) -> WorkerReputation | None:
    return _workers.get(worker_id)


def list_workers() -> list[WorkerReputation]:
    return sorted(_workers.values(), key=lambda w: w.score, reverse=True)


def record_worker_outcome(worker_id: str, outcome: str, earned: Decimal = Decimal("0")) -> WorkerReputation:
    if worker_id not in _workers:
        _workers[worker_id] = WorkerReputation(worker_id=worker_id)
    w = _workers[worker_id]
    if outcome == "completed":
        w.tasks_completed += 1
        w.total_earned_usdc += earned
    elif outcome == "failed":
        w.tasks_failed += 1
    elif outcome == "disputed":
        w.tasks_disputed += 1
    return w


def create_task(
    description: str,
    budget_usdc: Decimal,
    location: Any = None,
    verification_criteria: list | None = None,
    priority: str = "standard",
    deadline_hours: int = 24,
    milestones: list | None = None,
) -> BridgeTask:
    # Base fee + surge pricing
    surge = Decimal("0")
    if priority == "urgent":
        surge = SURGE_URGENT
    elif priority == "critical":
        surge = SURGE_CRITICAL
    total_rate = FEE_RATE + surge
    fee = (budget_usdc * total_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    task = BridgeTask(
        description=description,
        budget_usdc=budget_usdc,
        fee_usdc=fee,
        location=location,
        verification_criteria=verification_criteria or [],
        priority=priority,
        deadline_hours=deadline_hours,
        milestones=milestones,
        milestones_total=len(milestones) if milestones else 0,
    )
    _tasks[task.id] = task
    return task


def complete_milestone(task_id: str, milestone_index: int) -> tuple[BridgeTask | None, Decimal]:
    """Mark a milestone as verified. Returns (task, budget_released)."""
    task = _tasks.get(task_id)
    if task is None or not task.milestones:
        return None, Decimal("0")
    if milestone_index < 0 or milestone_index >= len(task.milestones):
        return None, Decimal("0")

    task.milestones_completed += 1
    ms = task.milestones[milestone_index]
    pct = Decimal(ms.budget_pct if hasattr(ms, 'budget_pct') else ms.get("budget_pct", 0))
    released = (task.budget_usdc * pct / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    task.budget_released_usdc += released

    if task.milestones_completed >= task.milestones_total:
        task.status = "completed"
        task.escrow_status = "released"

    return task, released


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
