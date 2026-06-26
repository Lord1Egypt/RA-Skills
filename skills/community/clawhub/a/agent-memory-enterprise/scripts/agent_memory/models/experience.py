"""Experience memory models."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .base import MemoryBase


class ExperienceOutcome(str, Field):
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"


from enum import Enum


class ExperienceOutcome(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"


class ExperienceRecord(MemoryBase):
    task_type: str
    goal_description: str
    approach: str
    outcome: ExperienceOutcome
    duration_seconds: float = 0.0
    domain: str = ""
    steps_taken: list[str] = Field(default_factory=list)
    error_info: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    access_count: int = 0
    user_id: Optional[str] = None


class ExperiencePattern(MemoryBase):
    pattern_type: str  # "success", "failure", "optimization"
    description: str
    task_types: list[str] = Field(default_factory=list)
    domains: list[str] = Field(default_factory=list)
    success_rate: float = 0.0
    sample_record_ids: list[str] = Field(default_factory=list)
    record_count: int = 0
    consolidated_at: datetime = Field(default_factory=datetime.utcnow)
