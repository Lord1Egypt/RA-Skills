"""Task memory models."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from .base import MemoryBase, StepStatus, TaskStatus


class TaskStep(MemoryBase):
    step_index: int
    description: str
    status: StepStatus = StepStatus.PENDING
    result: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class TaskState(MemoryBase):
    task_id: str = Field(default_factory=lambda: str(__import__("uuid").uuid4()))
    goal: str
    steps: list[TaskStep] = Field(default_factory=list)
    current_step_index: int = 0
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    checkpoint_data: Optional[dict[str, Any]] = None
    archived: bool = False
    user_id: Optional[str] = None


class TaskSummary(BaseModel):
    task_id: str
    goal: str
    outcome: str
    step_count: int
    success: bool
    duration_seconds: float = 0.0
    completed_at: datetime = Field(default_factory=datetime.utcnow)
