"""Data models for the Roundtable library.

Pure dataclasses with zero external dependencies — only stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Discussion:
    id: str
    topic: str
    context: str | None
    status: str  # "active" | "concluded" | "cancelled"
    max_rounds: int
    current_round: int
    speech_order: str  # "fixed" | "random" | "priority" | "free"
    created_by: str
    created_at: int
    concluded_at: int | None
    conclusion: str | None
    convergence_score: float | None
    output_path: str | None
    notifications: dict[str, Any] | None = None


@dataclass
class Participant:
    discussion_id: str
    participant: str
    role: str | None
    perspective: str | None
    display_name: str | None
    joined_at: int
    is_active: bool


@dataclass
class Speech:
    id: int
    discussion_id: str
    round: int
    participant: str
    content: str
    reply_to: int | None
    created_at: int


@dataclass
class Finding:
    id: int
    discussion_id: str
    type: str  # "consensus" | "disagreement" | "new_point"
    content: str
    round: int
    related_speeches: list[int] | None


@dataclass
class ConvergenceRecord:
    discussion_id: str
    round: int
    score: float
    consensus_count: int
    disagreement_count: int
    new_point_count: int
