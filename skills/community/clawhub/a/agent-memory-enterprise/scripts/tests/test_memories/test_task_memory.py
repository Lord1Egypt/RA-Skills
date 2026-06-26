"""Tests for Task Memory with SQLite backend."""

import pytest
import pytest_asyncio
from datetime import datetime

from agent_memory.config import TaskMemoryConfig
from agent_memory.exceptions import TaskStateError, MemoryNotFoundError
from agent_memory.memories.task_memory import TaskMemory
from agent_memory.models.base import StepStatus, TaskStatus
from agent_memory.models.task import TaskState, TaskStep
from agent_memory.storage.postgres_client import PostgresClient
from agent_memory.storage.postgres_models import Base


@pytest_asyncio.fixture
async def task_memory(pg_config):
    from tests.conftest import fake_pg
    from agent_memory.config import PostgreSQLConfig

    config = PostgreSQLConfig(url="sqlite+aiosqlite:///:memory:", echo=False)
    pg = PostgresClient(config, base=Base)
    await pg.initialize()

    memory = TaskMemory(pg, TaskMemoryConfig())
    await memory.initialize()
    yield memory
    await pg.shutdown()


class TestTaskMemory:
    @pytest.mark.asyncio
    async def test_create_task(self, task_memory):
        task = await task_memory.create_task(
            goal="Generate report",
            steps=["Collect data", "Analyze", "Generate"],
        )
        assert task.goal == "Generate report"
        assert task.status == TaskStatus.PENDING
        assert len(task.steps) == 3

    @pytest.mark.asyncio
    async def test_task_lifecycle(self, task_memory):
        # Create
        task = await task_memory.create_task(
            goal="Test lifecycle",
            steps=["Step 1", "Step 2"],
        )
        task_id = task.task_id

        # Start
        task = await task_memory.start_task(task_id)
        assert task.status == TaskStatus.IN_PROGRESS

        # Advance step
        task = await task_memory.advance_step(task_id, "Step 1 done")
        assert task.current_step_index == 1

        # Complete
        task = await task_memory.complete_task(task_id, "All done")
        assert task.status == TaskStatus.COMPLETED
        assert task.result == "All done"

    @pytest.mark.asyncio
    async def test_fail_task(self, task_memory):
        task = await task_memory.create_task(goal="Will fail", steps=["Step 1"])
        task = await task_memory.start_task(task.task_id)
        task = await task_memory.fail_task(task.task_id, "Something went wrong")
        assert task.status == TaskStatus.FAILED

    @pytest.mark.asyncio
    async def test_invalid_transition(self, task_memory):
        task = await task_memory.create_task(goal="Bad transition", steps=["Step 1"])
        with pytest.raises(TaskStateError):
            await task_memory.complete_task(task.task_id, "Can't complete pending")

    @pytest.mark.asyncio
    async def test_checkpoint(self, task_memory):
        task = await task_memory.create_task(goal="Checkpoint test", steps=["Step 1"])
        await task_memory.start_task(task.task_id)

        checkpoint = {"progress": 50, "data": [1, 2, 3]}
        await task_memory.save_checkpoint(task.task_id, checkpoint)

        loaded = await task_memory.load_checkpoint(task.task_id)
        assert loaded == checkpoint

    @pytest.mark.asyncio
    async def test_archive_task(self, task_memory):
        task = await task_memory.create_task(goal="Archive test", steps=["Step 1"])
        await task_memory.start_task(task.task_id)
        await task_memory.complete_task(task.task_id, "Done")

        summary = await task_memory.archive_task(task.task_id)
        assert summary.task_id == task.task_id
        assert summary.goal == "Archive test"
        assert summary.step_count == 1

    @pytest.mark.asyncio
    async def test_get_active_tasks(self, task_memory):
        await task_memory.create_task(goal="Task 1", steps=["S1"])
        await task_memory.create_task(goal="Task 2", steps=["S2"])

        active = await task_memory.get_active_tasks()
        assert len(active) == 2

    @pytest.mark.asyncio
    async def test_count(self, task_memory):
        await task_memory.create_task(goal="Task 1", steps=["S1"])
        await task_memory.create_task(goal="Task 2", steps=["S2"])
        count = await task_memory.count()
        assert count == 2

    @pytest.mark.asyncio
    async def test_delete(self, task_memory):
        task = await task_memory.create_task(goal="Delete me", steps=["S1"])
        assert await task_memory.delete(task.task_id) is True
        assert await task_memory.retrieve(task.task_id) is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, task_memory):
        assert await task_memory.delete("nonexistent") is False
