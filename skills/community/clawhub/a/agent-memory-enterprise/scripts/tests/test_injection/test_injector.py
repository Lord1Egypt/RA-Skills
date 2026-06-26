"""Tests for the memory injector."""

import pytest
from agent_memory.config import InjectorConfig, ScoringConfig
from agent_memory.injection.injector import MemoryInjector
from agent_memory.models.base import MemoryType
from agent_memory.models.scoring import ImportanceScore, ScoreComponents
from agent_memory.models.user import UserProfile
from agent_memory.scoring.importance_scorer import ImportanceScorer


def make_score(memory_id: str, total: float) -> ImportanceScore:
    return ImportanceScore(
        memory_id=memory_id,
        memory_type=MemoryType.USER,
        total=total,
        components=ScoreComponents(),
    )


class TestMemoryInjector:
    def setup_method(self):
        config = InjectorConfig(token_budget=500, budget_threshold=0.8)
        self.scorer = ImportanceScorer(ScoringConfig())
        self.injector = MemoryInjector(config, self.scorer)

    def test_estimate_tokens(self):
        tokens = self.injector.estimate_tokens("Hello world")
        assert tokens > 0

    def test_estimate_tokens_empty(self):
        assert self.injector.estimate_tokens("") == 0

    @pytest.mark.asyncio
    async def test_inject_empty_memories(self):
        result = await self.injector.inject([], base_prompt="Hello")
        assert "Hello" in result

    @pytest.mark.asyncio
    async def test_inject_with_system_prompt(self):
        result = await self.injector.inject(
            [],
            base_prompt="Hello",
            system_prompt="You are a helpful assistant.",
        )
        assert "You are a helpful assistant." in result
        assert "Hello" in result

    @pytest.mark.asyncio
    async def test_inject_respects_budget(self):
        profile = UserProfile(user_id="user_1")
        # Create many items with high scores
        items = [(profile, make_score(f"mem_{i}", 0.9 - i * 0.05)) for i in range(20)]

        result = await self.injector.inject(items, base_prompt="Test")
        # Result should be within budget (not exact due to formatting overhead)
        assert len(result) < 5000  # rough sanity check
