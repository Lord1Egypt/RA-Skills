"""Scoring models."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from .base import MemoryType


class ScoreComponents(BaseModel):
    relevance: float = 0.0
    recency: float = 0.0
    frequency: float = 0.0
    explicit_rating: float = 0.5


class ImportanceScore(BaseModel):
    memory_id: str
    memory_type: MemoryType
    total: float = 0.0
    components: ScoreComponents = Field(default_factory=ScoreComponents)
    scored_at: datetime = Field(default_factory=datetime.utcnow)
