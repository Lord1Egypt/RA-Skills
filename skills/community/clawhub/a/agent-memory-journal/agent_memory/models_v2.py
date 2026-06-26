from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MemoryItem:
    id: str
    text: str
    category: str
    tier: str
    state: str
    source: str
    created_at: str = ''
    last_seen: str = ''
    pinned: bool = False
    supersedes: str | None = None


@dataclass
class CandidateItem:
    id: str
    text: str
    normalized_claim: str
    category: str | None
    source: str
    occurrences: int
    distinct_days: int
    score: float
