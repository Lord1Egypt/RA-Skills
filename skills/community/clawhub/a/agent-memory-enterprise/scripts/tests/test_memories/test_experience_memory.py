"""Tests for Experience Memory."""

import pytest
import pytest_asyncio

from agent_memory.config import ExperienceMemoryConfig
from agent_memory.memories.experience_memory import ExperienceMemory
from agent_memory.models.experience import ExperienceOutcome, ExperienceRecord
from agent_memory.storage.postgres_client import PostgresClient
from agent_memory.storage.postgres_models import Base


@pytest_asyncio.fixture
async def experience_memory():
    from agent_memory.config import PostgreSQLConfig

    config = PostgreSQLConfig(url="sqlite+aiosqlite:///:memory:", echo=False)
    pg = PostgresClient(config, base=Base)
    await pg.initialize()

    memory = ExperienceMemory(pg, ExperienceMemoryConfig())
    await memory.initialize()
    yield memory
    await pg.shutdown()


class TestExperienceMemory:
    @pytest.mark.asyncio
    async def test_record_experience(self, experience_memory):
        record = ExperienceRecord(
            task_type="analysis",
            goal_description="Analyze Q4 financial report",
            approach="Collect data then build charts",
            outcome=ExperienceOutcome.SUCCESS,
            duration_seconds=300.0,
            domain="finance",
        )
        exp_id = await experience_memory.record_experience(record)
        assert exp_id is not None

    @pytest.mark.asyncio
    async def test_find_similar(self, experience_memory):
        # Record some experiences
        for i in range(5):
            record = ExperienceRecord(
                task_type="analysis",
                goal_description=f"Analyze financial data and create report number {i}",
                approach="Collect and analyze",
                outcome=ExperienceOutcome.SUCCESS if i < 4 else ExperienceOutcome.FAILURE,
                duration_seconds=100.0 + i * 10,
                domain="finance",
            )
            await experience_memory.record_experience(record)

        similar = await experience_memory.find_similar(
            goal_description="Analyze financial report",
            task_type="analysis",
            domain="finance",
        )
        assert len(similar) > 0

    @pytest.mark.asyncio
    async def test_get_success_rate(self, experience_memory):
        for i in range(4):
            await experience_memory.record_experience(ExperienceRecord(
                task_type="testing",
                goal_description=f"Test {i}",
                approach="Manual test",
                outcome=ExperienceOutcome.SUCCESS,
                duration_seconds=10.0,
            ))
        await experience_memory.record_experience(ExperienceRecord(
            task_type="testing",
            goal_description="Test failed",
            approach="Manual test",
            outcome=ExperienceOutcome.FAILURE,
            duration_seconds=10.0,
        ))

        rate = await experience_memory.get_success_rate("testing")
        assert rate == pytest.approx(0.8, abs=0.01)

    @pytest.mark.asyncio
    async def test_consolidate_experiences(self, experience_memory):
        for i in range(5):
            await experience_memory.record_experience(ExperienceRecord(
                task_type="consolidation_test",
                goal_description=f"Task {i}",
                approach="Standard approach",
                outcome=ExperienceOutcome.SUCCESS if i < 3 else ExperienceOutcome.FAILURE,
                duration_seconds=10.0,
                domain="test",
            ))

        patterns = await experience_memory.consolidate_experiences("consolidation_test")
        assert len(patterns) > 0
        assert any(p.task_types == ["consolidation_test"] for p in patterns)

    @pytest.mark.asyncio
    async def test_count(self, experience_memory):
        await experience_memory.record_experience(ExperienceRecord(
            task_type="count_test",
            goal_description="Count test",
            approach="Test",
            outcome=ExperienceOutcome.SUCCESS,
            duration_seconds=1.0,
        ))
        count = await experience_memory.count()
        assert count >= 1

    @pytest.mark.asyncio
    async def test_retrieve(self, experience_memory):
        record = ExperienceRecord(
            task_type="retrieve_test",
            goal_description="Retrieve test",
            approach="Test approach",
            outcome=ExperienceOutcome.SUCCESS,
            duration_seconds=1.0,
        )
        exp_id = await experience_memory.record_experience(record)
        retrieved = await experience_memory.retrieve(exp_id)
        assert retrieved is not None
        assert retrieved.task_type == "retrieve_test"
