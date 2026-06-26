"""Task Memory - structured state management in PostgreSQL."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from agent_memory.config import TaskMemoryConfig
from agent_memory.core.base_memory import BaseMemory
from agent_memory.exceptions import MemoryNotFoundError, TaskStateError
from agent_memory.models.base import StepStatus, TaskStatus
from agent_memory.models.task import TaskState, TaskStep, TaskSummary
from agent_memory.storage.postgres_client import PostgresClient
from agent_memory.storage.postgres_models import TaskModel, TaskStepModel


# Valid state transitions
_VALID_TRANSITIONS = {
    TaskStatus.PENDING: {TaskStatus.IN_PROGRESS, TaskStatus.FAILED},
    TaskStatus.IN_PROGRESS: {TaskStatus.COMPLETED, TaskStatus.FAILED},
    TaskStatus.COMPLETED: {TaskStatus.ARCHIVED},
    TaskStatus.FAILED: {TaskStatus.ARCHIVED},
}


class TaskMemory(BaseMemory):
    """Structured task state in PostgreSQL with state machine."""

    def __init__(self, pg_client: PostgresClient, config: TaskMemoryConfig):
        self._pg = pg_client
        self._config = config

    async def initialize(self) -> None:
        pass  # Tables created by PostgresClient

    async def shutdown(self) -> None:
        pass

    async def store(self, data: TaskState, **kwargs) -> str:
        async with self._pg.session_factory() as session:
            model = TaskModel(
                task_id=data.task_id,
                goal=data.goal,
                current_step_index=data.current_step_index,
                status=data.status.value,
                result=data.result,
                checkpoint_data=data.checkpoint_data,
                archived=data.archived,
                user_id=data.user_id,
            )
            session.add(model)
            for step in data.steps:
                step_model = TaskStepModel(
                    task_id=data.task_id,
                    step_index=step.step_index,
                    description=step.description,
                    status=step.status.value,
                    result=step.result,
                    metadata_=step.metadata,
                )
                session.add(step_model)
            await session.commit()
            return data.task_id

    async def retrieve(self, memory_id: str, **kwargs) -> Optional[TaskState]:
        return await self._load_task(memory_id)

    async def search(self, query: Any, **kwargs) -> list[TaskState]:
        async with self._pg.session_factory() as session:
            stmt = select(TaskModel)
            if isinstance(query, dict):
                if status := query.get("status"):
                    stmt = stmt.where(TaskModel.status == status)
                if user_id := query.get("user_id"):
                    stmt = stmt.where(TaskModel.user_id == user_id)
                if archived := query.get("archived"):
                    stmt = stmt.where(TaskModel.archived == archived)
            stmt = stmt.order_by(TaskModel.created_at.desc())
            if limit := kwargs.get("limit"):
                stmt = stmt.limit(limit)
            result = await session.execute(stmt)
            models = result.scalars().all()
            return [self._model_to_state(m) for m in models]

    async def delete(self, memory_id: str) -> bool:
        async with self._pg.session_factory() as session:
            stmt = select(TaskModel).where(TaskModel.task_id == memory_id)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model:
                await session.delete(model)
                await session.commit()
                return True
            return False

    async def count(self, **kwargs) -> int:
        from sqlalchemy import func
        async with self._pg.session_factory() as session:
            stmt = select(func.count(TaskModel.id))
            if status := kwargs.get("status"):
                stmt = stmt.where(TaskModel.status == status)
            if user_id := kwargs.get("user_id"):
                stmt = stmt.where(TaskModel.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalar_one()

    # --- Extended interface ---

    async def create_task(
        self,
        goal: str,
        steps: list[str],
        user_id: Optional[str] = None,
    ) -> TaskState:
        """Create a new task with named steps."""
        task = TaskState(
            goal=goal,
            status=TaskStatus.PENDING,
            steps=[
                TaskStep(step_index=i, description=s)
                for i, s in enumerate(steps)
            ],
            current_step_index=0,
            user_id=user_id,
        )
        await self.store(task)
        return task

    async def start_task(self, task_id: str) -> TaskState:
        """Transition task from PENDING to IN_PROGRESS."""
        return await self._transition(task_id, TaskStatus.IN_PROGRESS)

    async def advance_step(
        self, task_id: str, result: Optional[str] = None
    ) -> TaskState:
        """Complete current step and advance to next."""
        task = await self._load_task(task_id)
        if task is None:
            raise MemoryNotFoundError(f"Task {task_id} not found")
        if task.status != TaskStatus.IN_PROGRESS:
            raise TaskStateError(f"Cannot advance step of task in state {task.status}")

        idx = task.current_step_index
        if idx < len(task.steps):
            await self._update_step_status(task_id, idx, StepStatus.DONE, result)
            next_idx = idx + 1

            async with self._pg.session_factory() as session:
                stmt = (
                    update(TaskModel)
                    .where(TaskModel.task_id == task_id)
                    .values(current_step_index=next_idx)
                )
                await session.execute(stmt)
                await session.commit()

        return await self._load_task(task_id)

    async def update_step_status(
        self,
        task_id: str,
        step_index: int,
        status: StepStatus,
        result: Optional[str] = None,
    ) -> TaskState:
        """Update the status of a specific step."""
        return await self._update_step_status(task_id, step_index, status, result)

    async def complete_task(self, task_id: str, result: str) -> TaskState:
        """Transition task to COMPLETED."""
        task = await self._transition(task_id, TaskStatus.COMPLETED)
        async with self._pg.session_factory() as session:
            stmt = (
                update(TaskModel)
                .where(TaskModel.task_id == task_id)
                .values(result=result)
            )
            await session.execute(stmt)
            await session.commit()
        return await self._load_task(task_id)

    async def fail_task(self, task_id: str, error: str) -> TaskState:
        """Transition task to FAILED."""
        task = await self._transition(task_id, TaskStatus.FAILED)
        async with self._pg.session_factory() as session:
            stmt = (
                update(TaskModel)
                .where(TaskModel.task_id == task_id)
                .values(result=error)
            )
            await session.execute(stmt)
            await session.commit()
        return await self._load_task(task_id)

    async def save_checkpoint(self, task_id: str, checkpoint_data: dict) -> TaskState:
        """Save a checkpoint for the task."""
        async with self._pg.session_factory() as session:
            stmt = (
                update(TaskModel)
                .where(TaskModel.task_id == task_id)
                .values(checkpoint_data=checkpoint_data)
            )
            await session.execute(stmt)
            await session.commit()
        return await self._load_task(task_id)

    async def load_checkpoint(self, task_id: str) -> Optional[dict]:
        """Load the last checkpoint for a task."""
        task = await self._load_task(task_id)
        return task.checkpoint_data if task else None

    async def archive_task(self, task_id: str) -> TaskSummary:
        """Archive a completed/failed task and return summary."""
        task = await self._transition(task_id, TaskStatus.ARCHIVED)
        task = await self._load_task(task_id)
        success = task.status == TaskStatus.ARCHIVED and task.result is not None

        duration = 0.0
        if task.created_at and task.updated_at:
            duration = (task.updated_at - task.created_at).total_seconds()

        summary = TaskSummary(
            task_id=task.task_id,
            goal=task.goal,
            outcome=task.result or "",
            step_count=len(task.steps),
            success=success,
            duration_seconds=duration,
        )
        return summary

    async def get_active_tasks(self, user_id: Optional[str] = None, limit: int = 20) -> list[TaskState]:
        """Get active (non-archived) tasks."""
        return await self.search(
            {"archived": False, "user_id": user_id} if user_id else {"archived": False},
            limit=limit,
        )

    # --- Private helpers ---

    async def _load_task(self, task_id: str) -> Optional[TaskState]:
        async with self._pg.session_factory() as session:
            stmt = select(TaskModel).where(TaskModel.task_id == task_id)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return None
            return self._model_to_state(model)

    def _model_to_state(self, model: TaskModel) -> TaskState:
        steps = []
        for s in sorted(model.steps, key=lambda x: x.step_index):
            steps.append(TaskStep(
                id=s.id,
                step_index=s.step_index,
                description=s.description,
                status=StepStatus(s.status),
                result=s.result,
                metadata=s.metadata_,
                created_at=s.created_at,
                updated_at=s.updated_at,
            ))
        return TaskState(
            id=model.id,
            task_id=model.task_id,
            goal=model.goal,
            steps=steps,
            current_step_index=model.current_step_index,
            status=TaskStatus(model.status),
            result=model.result,
            checkpoint_data=model.checkpoint_data,
            archived=model.archived,
            user_id=model.user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def _transition(self, task_id: str, new_status: TaskStatus) -> TaskState:
        """Validate and execute a state transition."""
        task = await self._load_task(task_id)
        if task is None:
            raise MemoryNotFoundError(f"Task {task_id} not found")

        current = TaskStatus(task.status.value) if isinstance(task.status, str) else task.status
        if new_status not in _VALID_TRANSITIONS.get(current, set()):
            raise TaskStateError(
                f"Invalid transition: {current.value} -> {new_status.value}"
            )

        async with self._pg.session_factory() as session:
            stmt = (
                update(TaskModel)
                .where(TaskModel.task_id == task_id)
                .values(status=new_status.value)
            )
            await session.execute(stmt)
            await session.commit()

        return task

    async def _update_step_status(
        self, task_id: str, step_index: int, status: StepStatus, result: Optional[str] = None
    ) -> TaskState:
        async with self._pg.session_factory() as session:
            stmt = (
                update(TaskStepModel)
                .where(
                    and_(
                        TaskStepModel.task_id == task_id,
                        TaskStepModel.step_index == step_index,
                    )
                )
                .values(status=status.value, result=result)
            )
            await session.execute(stmt)
            await session.commit()
        return await self._load_task(task_id)
