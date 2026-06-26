"""Experience Memory - execution history with similarity search in PostgreSQL."""

from __future__ import annotations

import math
from typing import Any, Optional

from sqlalchemy import select, update, func, and_, or_, text

from agent_memory.config import ExperienceMemoryConfig
from agent_memory.core.base_memory import BaseMemory
from agent_memory.models.experience import ExperienceOutcome, ExperiencePattern, ExperienceRecord
from agent_memory.storage.postgres_client import PostgresClient
from agent_memory.storage.postgres_models import ExperiencePatternModel, ExperienceRecordModel


class ExperienceMemory(BaseMemory):
    """Execution history with PostgreSQL-based similarity search."""

    def __init__(self, pg_client: PostgresClient, config: ExperienceMemoryConfig):
        self._pg = pg_client
        self._config = config

    async def initialize(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    async def store(self, data: ExperienceRecord, **kwargs) -> str:
        async with self._pg.session_factory() as session:
            model = ExperienceRecordModel(
                task_type=data.task_type,
                goal_description=data.goal_description,
                approach=data.approach,
                outcome=data.outcome.value,
                duration_seconds=data.duration_seconds,
                domain=data.domain,
                steps_taken=data.steps_taken,
                error_info=data.error_info,
                tags=data.tags,
                access_count=data.access_count,
                user_id=data.user_id,
            )
            session.add(model)
            await session.commit()
            return model.id

    async def retrieve(self, memory_id: str, **kwargs) -> Optional[ExperienceRecord]:
        async with self._pg.session_factory() as session:
            stmt = select(ExperienceRecordModel).where(
                ExperienceRecordModel.id == memory_id
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model:
                return self._model_to_record(model)
            return None

    async def search(self, query: Any, **kwargs) -> list[ExperienceRecord]:
        if isinstance(query, dict):
            goal = query.get("goal_description", "")
            task_type = query.get("task_type")
            domain = query.get("domain")
            min_success_rate = query.get("min_success_rate", self._config.min_success_rate)
            return await self.find_similar(goal, task_type, domain, min_success_rate)
        return []

    async def delete(self, memory_id: str) -> bool:
        async with self._pg.session_factory() as session:
            stmt = select(ExperienceRecordModel).where(
                ExperienceRecordModel.id == memory_id
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model:
                await session.delete(model)
                await session.commit()
                return True
            return False

    async def count(self, **kwargs) -> int:
        async with self._pg.session_factory() as session:
            result = await session.execute(
                select(func.count(ExperienceRecordModel.id))
            )
            return result.scalar_one()

    # --- Extended interface ---

    async def record_experience(self, record: ExperienceRecord) -> str:
        """Record a new experience."""
        return await self.store(record)

    async def find_similar(
        self,
        goal_description: str,
        task_type: Optional[str] = None,
        domain: Optional[str] = None,
        min_success_rate: Optional[float] = None,
    ) -> list[ExperienceRecord]:
        """Find similar experiences using keyword matching and filters."""
        rate = min_success_rate or self._config.min_success_rate
        async with self._pg.session_factory() as session:
            stmt = select(ExperienceRecordModel)

            if task_type:
                stmt = stmt.where(ExperienceRecordModel.task_type == task_type)
            if domain:
                stmt = stmt.where(ExperienceRecordModel.domain == domain)

            # Filter by outcome success for success-rate calculation
            stmt = stmt.order_by(ExperienceRecordModel.created_at.desc())
            stmt = stmt.limit(self._config.similarity_top_k * 3)

            result = await session.execute(stmt)
            models = result.scalars().all()

            # Filter by keywords from goal description
            keywords = set(goal_description.lower().split())
            scored = []
            for m in models:
                desc_words = set(m.goal_description.lower().split())
                overlap = len(keywords & desc_words)
                if overlap > 0:
                    scored.append((overlap, m))

            scored.sort(key=lambda x: x[0], reverse=True)
            top = [m for _, m in scored[: self._config.similarity_top_k]]

            # Calculate success rate per task_type and filter
            result_records = []
            for m in top:
                # Check success rate for this task_type
                sr = await self.get_success_rate(m.task_type, m.domain)
                if sr >= rate:
                    result_records.append(self._model_to_record(m))

            return result_records

    async def get_success_rate(
        self, task_type: str, domain: Optional[str] = None
    ) -> float:
        """Calculate success rate for a task type."""
        async with self._pg.session_factory() as session:
            stmt = select(ExperienceRecordModel).where(
                ExperienceRecordModel.task_type == task_type
            )
            if domain:
                stmt = stmt.where(ExperienceRecordModel.domain == domain)

            result = await session.execute(stmt)
            records = result.scalars().all()

            if not records:
                return 0.0

            successes = sum(1 for r in records if r.outcome == "success")
            return successes / len(records)

    async def consolidate_experiences(
        self, task_type: Optional[str] = None
    ) -> list[ExperiencePattern]:
        """Consolidate experiences into patterns."""
        async with self._pg.session_factory() as session:
            stmt = select(ExperienceRecordModel)
            if task_type:
                stmt = stmt.where(ExperienceRecordModel.task_type == task_type)
            stmt = stmt.limit(500)
            result = await session.execute(stmt)
            records = result.scalars().all()

            # Group by (task_type, domain, outcome)
            groups: dict[tuple, list] = {}
            for r in records:
                key = (r.task_type, r.domain, r.outcome)
                groups.setdefault(key, []).append(r)

            patterns = []
            for (tt, dom, outcome), group in groups.items():
                if len(group) < 3:
                    continue

                success_count = sum(1 for r in group if r.outcome == "success")
                success_rate = success_count / len(group)

                pattern_model = ExperiencePatternModel(
                    pattern_type=outcome,
                    description=f"Pattern for {tt} in {dom}: {outcome} ({len(group)} records, {success_rate:.0%} success)",
                    task_types=[tt],
                    domains=[dom] if dom else [],
                    success_rate=success_rate,
                    sample_record_ids=[r.id for r in group[:5]],
                    record_count=len(group),
                )
                session.add(pattern_model)
                patterns.append(
                    ExperiencePattern(
                        id=pattern_model.id,
                        pattern_type=pattern_model.pattern_type,
                        description=pattern_model.description,
                        task_types=pattern_model.task_types,
                        domains=pattern_model.domains,
                        success_rate=pattern_model.success_rate,
                        sample_record_ids=pattern_model.sample_record_ids,
                        record_count=pattern_model.record_count,
                    )
                )

            await session.commit()
            return patterns

    async def get_patterns(
        self, pattern_type: Optional[str] = None
    ) -> list[ExperiencePattern]:
        """Get consolidated experience patterns."""
        async with self._pg.session_factory() as session:
            stmt = select(ExperiencePatternModel)
            if pattern_type:
                stmt = stmt.where(ExperiencePatternModel.pattern_type == pattern_type)
            result = await session.execute(stmt)
            models = result.scalars().all()
            return [
                ExperiencePattern(
                    id=m.id,
                    pattern_type=m.pattern_type,
                    description=m.description,
                    task_types=m.task_types,
                    domains=m.domains,
                    success_rate=m.success_rate,
                    sample_record_ids=m.sample_record_ids,
                    record_count=m.record_count,
                    consolidated_at=m.consolidated_at,
                )
                for m in models
            ]

    # --- Private helpers ---

    def _model_to_record(self, model: ExperienceRecordModel) -> ExperienceRecord:
        return ExperienceRecord(
            id=model.id,
            task_type=model.task_type,
            goal_description=model.goal_description,
            approach=model.approach,
            outcome=ExperienceOutcome(model.outcome),
            duration_seconds=model.duration_seconds,
            domain=model.domain,
            steps_taken=model.steps_taken or [],
            error_info=model.error_info,
            tags=model.tags or [],
            access_count=model.access_count,
            user_id=model.user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
