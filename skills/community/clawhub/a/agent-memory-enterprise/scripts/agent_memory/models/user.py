"""User memory models."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from .base import MemoryBase


class UserPreference(MemoryBase):
    key: str
    value: Any
    source: str = "explicit"  # "explicit" or "implicit"
    confidence: float = 1.0
    version: int = 1


class PreferenceVersion(BaseModel):
    version: int
    previous_value: Any
    new_value: Any
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    change_reason: str = "update"


class UserProfile(MemoryBase):
    user_id: str
    preferences: dict[str, UserPreference] = Field(default_factory=dict)
    history_task_ids: list[str] = Field(default_factory=list)
    usage_patterns: dict[str, Any] = Field(default_factory=dict)
