"""Memory router - routes queries to appropriate memory layers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from agent_memory.memories.context_memory import ContextMemory
from agent_memory.memories.experience_memory import ExperienceMemory
from agent_memory.memories.knowledge_memory import KnowledgeMemory
from agent_memory.memories.task_memory import TaskMemory
from agent_memory.memories.user_memory import UserMemory
from agent_memory.models.scoring import ImportanceScore
from agent_memory.routing.feature_extractor import TaskFeatureExtractor, TaskFeatures
from agent_memory.scoring.importance_scorer import ImportanceScorer


@dataclass
class RouterResult:
    """Result from memory routing."""
    user_profile: Any = None
    context_window: Any = None
    task_progress: list = field(default_factory=list)
    knowledge_results: list = field(default_factory=list)
    experience_records: list = field(default_factory=list)
    features: Optional[TaskFeatures] = None
    scores: dict[str, ImportanceScore] = field(default_factory=dict)


class MemoryRouter:
    """Routes queries to appropriate memory layers."""

    def __init__(
        self,
        context_memory: ContextMemory,
        task_memory: TaskMemory,
        user_memory: UserMemory,
        knowledge_memory: KnowledgeMemory,
        experience_memory: ExperienceMemory,
        feature_extractor: TaskFeatureExtractor,
        scorer: ImportanceScorer,
    ):
        self._context = context_memory
        self._task = task_memory
        self._user = user_memory
        self._knowledge = knowledge_memory
        self._experience = experience_memory
        self._extractor = feature_extractor
        self._scorer = scorer

    async def route(
        self,
        query: str,
        user_id: str,
        session_id: str,
        context: Optional[dict] = None,
    ) -> RouterResult:
        """Route a query to the appropriate memory layers.

        1. Always load user profile
        2. Extract task features
        3. Selectively load relevant memories
        4. Score all loaded memories
        """
        result = RouterResult()

        # 1. Always load user profile
        result.user_profile = await self._user.get_profile(user_id)

        # 2. Extract task features
        result.features = self._extractor.extract(query, context)

        # 3. Always load context window
        result.context_window = await self._context.get_window(session_id)

        # 4. Knowledge-based query
        if result.features.requires_knowledge:
            result.knowledge_results = await self._knowledge.search_similar(
                query=query,
                domain=result.features.domain,
            )

        # 5. Complex tasks: load similar experiences
        if result.features.is_complex:
            result.experience_records = await self._experience.find_similar(
                goal_description=query,
                task_type=result.features.task_type,
                domain=result.features.domain,
            )

        # 6. History: load active tasks for this user
        if result.features.has_history or context and context.get("continuation"):
            result.task_progress = await self._task.get_active_tasks(
                user_id=user_id, limit=5
            )

        # 7. Score all loaded memories
        scores = {}
        from agent_memory.models.base import MemoryType

        if result.user_profile:
            scores["user_profile"] = self._scorer.score(
                memory_id=result.user_profile.user_id,
                memory_type=MemoryType.USER,
                relevance=0.8,  # User profile is always highly relevant
                access_count=1,
            )

        for i, kr in enumerate(result.knowledge_results):
            scores[f"knowledge_{i}"] = self._scorer.score(
                memory_id=kr.chunk_id,
                memory_type=MemoryType.KNOWLEDGE,
                relevance=kr.score,
                access_count=1,
            )

        for i, exp in enumerate(result.experience_records):
            scores[f"experience_{i}"] = self._scorer.score(
                memory_id=exp.id,
                memory_type=MemoryType.EXPERIENCE,
                relevance=0.7,
                access_count=exp.access_count,
            )

        result.scores = scores
        return result
