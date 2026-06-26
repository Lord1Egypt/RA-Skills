"""Importance scorer for memory items."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from agent_memory.config import ScoringConfig
from agent_memory.models.base import MemoryType
from agent_memory.models.scoring import ImportanceScore, ScoreComponents
from agent_memory.scoring.decay import time_decay_score


class ImportanceScorer:
    """Scores memory importance using weighted components."""

    def __init__(self, config: ScoringConfig):
        self._config = config

    def score(
        self,
        memory_id: str,
        memory_type: MemoryType,
        relevance: float = 0.0,
        last_accessed: Optional[datetime] = None,
        access_count: int = 0,
        explicit_rating: Optional[float] = None,
        reference_max_access: int = 10,
    ) -> ImportanceScore:
        """Calculate importance score for a memory item.

        Args:
            memory_id: Unique ID of the memory.
            memory_type: Type of the memory.
            relevance: Pre-computed relevance score [0, 1].
            last_accessed: When the memory was last accessed.
            access_count: Number of times this memory has been accessed.
            explicit_rating: User-provided rating [0, 1], None = neutral (0.5).
            reference_max_access: Highest access count in current batch for normalization.
        """
        # Recency: exponential decay from last access time
        recency = 0.5
        if last_accessed:
            recency = time_decay_score(
                last_accessed, half_life_hours=self._config.decay_half_life_hours
            )

        # Frequency: log-normalized access count
        import math
        frequency = 0.0
        if reference_max_access > 0 and access_count > 0:
            frequency = math.log(1 + access_count) / math.log(1 + reference_max_access)

        # Explicit rating: default neutral
        rating = explicit_rating if explicit_rating is not None else 0.5

        components = ScoreComponents(
            relevance=min(max(relevance, 0.0), 1.0),
            recency=min(max(recency, 0.0), 1.0),
            frequency=min(max(frequency, 0.0), 1.0),
            explicit_rating=min(max(rating, 0.0), 1.0),
        )

        total = (
            components.relevance * self._config.relevance_weight
            + components.recency * self._config.recency_weight
            + components.frequency * self._config.frequency_weight
            + components.explicit_rating * self._config.explicit_weight
        )

        return ImportanceScore(
            memory_id=memory_id,
            memory_type=memory_type,
            total=total,
            components=components,
        )

    def rank(
        self,
        items: list[tuple[any, ImportanceScore]],
    ) -> list[tuple[any, ImportanceScore]]:
        """Rank items by importance score, highest first."""
        return sorted(items, key=lambda x: x[1].total, reverse=True)
