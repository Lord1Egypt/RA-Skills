"""Tests for the scoring module."""

import pytest
from datetime import datetime, timedelta, timezone

from agent_memory.models.base import MemoryType
from agent_memory.scoring.decay import exponential_decay, time_decay_score
from agent_memory.scoring.importance_scorer import ImportanceScorer
from agent_memory.config import ScoringConfig


class TestExponentialDecay:
    def test_zero_hours(self):
        assert exponential_decay(0.0, 24.0) == pytest.approx(1.0)

    def test_half_life(self):
        result = exponential_decay(24.0, 24.0)
        assert result == pytest.approx(0.5, abs=0.01)

    def test_double_half_life(self):
        result = exponential_decay(48.0, 24.0)
        assert result == pytest.approx(0.25, abs=0.01)

    def test_negative_hours(self):
        assert exponential_decay(-1.0, 24.0) == 1.0


class TestTimeDecayScore:
    def test_recent_item(self):
        now = datetime.now(timezone.utc)
        score = time_decay_score(now, now, half_life_hours=24.0)
        assert score == pytest.approx(1.0, abs=0.01)

    def test_old_item(self):
        now = datetime.now(timezone.utc)
        old = now - timedelta(hours=24)
        score = time_decay_score(old, now, half_life_hours=24.0)
        assert score == pytest.approx(0.5, abs=0.01)

    def test_very_old_item(self):
        now = datetime.now(timezone.utc)
        very_old = now - timedelta(hours=168)  # 1 week
        score = time_decay_score(very_old, now, half_life_hours=24.0)
        assert score < 0.01


class TestImportanceScorer:
    def test_high_relevance_high_score(self):
        scorer = ImportanceScorer(ScoringConfig())
        score = scorer.score(
            memory_id="test1",
            memory_type=MemoryType.KNOWLEDGE,
            relevance=1.0,
            access_count=5,
            reference_max_access=10,
        )
        assert score.total > 0.5

    def test_low_relevance_low_score(self):
        scorer = ImportanceScorer(ScoringConfig())
        score = scorer.score(
            memory_id="test2",
            memory_type=MemoryType.KNOWLEDGE,
            relevance=0.1,
            access_count=0,
        )
        assert score.total < 0.5

    def test_rank_ordering(self):
        scorer = ImportanceScorer(ScoringConfig())
        high = scorer.score("h", MemoryType.KNOWLEDGE, relevance=1.0, access_count=10, reference_max_access=10)
        low = scorer.score("l", MemoryType.KNOWLEDGE, relevance=0.1, access_count=0)
        ranked = scorer.rank([("item_low", low), ("item_high", high)])
        assert ranked[0][0] == "item_high"
        assert ranked[1][0] == "item_low"

    def test_score_components_bounds(self):
        scorer = ImportanceScorer(ScoringConfig())
        score = scorer.score(
            "test", MemoryType.CONTEXT,
            relevance=2.0,  # exceeds 1.0, should be clamped
        )
        assert score.components.relevance <= 1.0
