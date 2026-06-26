"""MemorySystem - top-level orchestrator composing all memory components."""

from __future__ import annotations

from typing import Any, Optional

from agent_memory.config import MemorySystemConfig, load_config
from agent_memory.injection.injector import MemoryInjector
from agent_memory.memories.context_memory import ContextMemory
from agent_memory.memories.experience_memory import ExperienceMemory
from agent_memory.memories.knowledge_memory import KnowledgeMemory
from agent_memory.memories.task_memory import TaskMemory
from agent_memory.memories.user_memory import UserMemory
from agent_memory.models.context import ContextMessage, ConversationWindow, MessageRole
from agent_memory.models.experience import ExperienceOutcome, ExperienceRecord
from agent_memory.models.task import TaskState, TaskSummary
from agent_memory.models.user import UserPreference, UserProfile
from agent_memory.routing.feature_extractor import TaskFeatureExtractor
from agent_memory.routing.router import MemoryRouter
from agent_memory.scoring.importance_scorer import ImportanceScorer
from agent_memory.storage.chroma_client import ChromaClient
from agent_memory.storage.postgres_client import PostgresClient
from agent_memory.storage.postgres_models import Base
from agent_memory.storage.redis_client import RedisClient


class MemorySystem:
    """Top-level orchestrator composing all memory components.

    Usage:
        mem = MemorySystem()
        await mem.initialize()

        # High-level operations
        await mem.add_context_message("sess1", "user", "Hello")
        prompt = await mem.build_prompt("How do I...", "user1", "sess1")

        await mem.shutdown()
    """

    def __init__(self, config: Optional[MemorySystemConfig] = None):
        self._config = load_config(config)

        # Storage backends
        self._redis = RedisClient(self._config.redis)
        self._pg = PostgresClient(self._config.postgresql, base=Base)
        self._chroma = ChromaClient(self._config.chroma)

        # Memory layers
        self._context_memory = ContextMemory(self._redis, self._config.context)
        self._task_memory = TaskMemory(self._pg, self._config.task)
        self._user_memory = UserMemory(self._pg, self._redis, self._config.user)
        self._knowledge_memory = KnowledgeMemory(self._chroma, self._config.knowledge)
        self._experience_memory = ExperienceMemory(self._pg, self._config.experience)

        # Cross-cutting components
        self._scorer = ImportanceScorer(self._config.scoring)
        self._extractor = TaskFeatureExtractor()
        self._router = MemoryRouter(
            self._context_memory,
            self._task_memory,
            self._user_memory,
            self._knowledge_memory,
            self._experience_memory,
            self._extractor,
            self._scorer,
        )
        self._injector = MemoryInjector(self._config.injector, self._scorer)

    async def initialize(self) -> None:
        """Initialize all storage backends and memory layers."""
        await self._redis.initialize()
        await self._pg.initialize()
        await self._chroma.initialize()

        await self._context_memory.initialize()
        await self._task_memory.initialize()
        await self._user_memory.initialize()
        await self._knowledge_memory.initialize()
        await self._experience_memory.initialize()

    async def shutdown(self) -> None:
        """Gracefully shut down all components."""
        await self._context_memory.shutdown()
        await self._task_memory.shutdown()
        await self._user_memory.shutdown()
        await self._knowledge_memory.shutdown()
        await self._experience_memory.shutdown()

        await self._redis.shutdown()
        await self._pg.shutdown()
        await self._chroma.shutdown()

    # --- Context Memory API ---

    async def add_context_message(
        self, session_id: str, role: str, content: str, token_count: int = 0
    ) -> ConversationWindow:
        """Add a message to the conversation context."""
        if token_count == 0:
            token_count = self._injector.estimate_tokens(content)
        msg = ContextMessage(
            role=MessageRole(role),
            content=content,
            token_count=token_count,
        )
        return await self._context_memory.add_message(session_id, msg)

    async def get_context(self, session_id: str) -> ConversationWindow:
        """Get the current conversation window."""
        return await self._context_memory.get_window(session_id)

    async def clear_context(self, session_id: str) -> None:
        """Clear all messages for a session."""
        await self._context_memory.clear_session(session_id)

    # --- Task Memory API ---

    async def create_task(
        self, goal: str, steps: list[str], user_id: Optional[str] = None
    ) -> TaskState:
        """Create a new task."""
        return await self._task_memory.create_task(goal, steps, user_id)

    async def start_task(self, task_id: str) -> TaskState:
        """Start a pending task."""
        return await self._task_memory.start_task(task_id)

    async def advance_task(
        self, task_id: str, step_result: Optional[str] = None
    ) -> TaskState:
        """Complete current step and advance."""
        return await self._task_memory.advance_step(task_id, step_result)

    async def complete_task(self, task_id: str, result: str) -> TaskState:
        """Mark a task as completed."""
        return await self._task_memory.complete_task(task_id, result)

    async def fail_task(self, task_id: str, error: str) -> TaskState:
        """Mark a task as failed."""
        return await self._task_memory.fail_task(task_id, error)

    async def get_task(self, task_id: str) -> Optional[TaskState]:
        """Get a task by ID."""
        return await self._task_memory.retrieve(task_id)

    async def archive_task(self, task_id: str) -> TaskSummary:
        """Archive a completed task."""
        return await self._task_memory.archive_task(task_id)

    # --- User Memory API ---

    async def update_user_preference(
        self, user_id: str, key: str, value: Any, source: str = "explicit"
    ) -> UserPreference:
        """Update a user preference."""
        return await self._user_memory.update_preference(user_id, key, value, source)

    async def get_user_profile(self, user_id: str) -> UserProfile:
        """Get user profile."""
        return await self._user_memory.get_profile(user_id)

    # --- Knowledge Memory API ---

    async def index_document(
        self, title: str, content: str, domain: str, **kwargs
    ) -> str:
        """Index a document into knowledge memory."""
        return await self._knowledge_memory.index_text(
            title=title, content=content, domain=domain, **kwargs
        )

    async def search_knowledge(
        self, query: str, domain: Optional[str] = None, top_k: int = 5
    ) -> list:
        """Search knowledge memory."""
        return await self._knowledge_memory.search_similar(
            query=query, domain=domain, top_k=top_k
        )

    # --- Experience Memory API ---

    async def record_experience(self, record: ExperienceRecord) -> str:
        """Record an execution experience."""
        return await self._experience_memory.record_experience(record)

    async def find_similar_experiences(
        self,
        goal: str,
        task_type: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> list:
        """Find similar past experiences."""
        return await self._experience_memory.find_similar(goal, task_type, domain)

    # --- High-level API ---

    async def build_prompt(
        self,
        query: str,
        user_id: str,
        session_id: str,
        base_prompt: str = "",
        system_prompt: Optional[str] = None,
    ) -> str:
        """Build a fully contextualized prompt by routing and injecting memories."""
        # Route to load relevant memories
        result = await self._router.route(query, user_id, session_id)

        # Collect all memory items with scores
        memory_items: list[tuple[Any, Any]] = []

        if result.user_profile and "user_profile" in result.scores:
            memory_items.append((result.user_profile, result.scores["user_profile"]))

        for i, kr in enumerate(result.knowledge_results):
            key = f"knowledge_{i}"
            if key in result.scores:
                memory_items.append((kr, result.scores[key]))

        for i, exp in enumerate(result.experience_records):
            key = f"experience_{i}"
            if key in result.scores:
                memory_items.append((exp, result.scores[key]))

        # Inject into prompt
        return await self._injector.inject(
            memories=memory_items,
            base_prompt=base_prompt or query,
            system_prompt=system_prompt,
        )

    # --- Direct access to sub-systems ---

    @property
    def context(self) -> ContextMemory:
        return self._context_memory

    @property
    def task(self) -> TaskMemory:
        return self._task_memory

    @property
    def user(self) -> UserMemory:
        return self._user_memory

    @property
    def knowledge(self) -> KnowledgeMemory:
        return self._knowledge_memory

    @property
    def experience(self) -> ExperienceMemory:
        return self._experience_memory

    @property
    def router(self) -> MemoryRouter:
        return self._router

    @property
    def injector(self) -> MemoryInjector:
        return self._injector

    @property
    def scorer(self) -> ImportanceScorer:
        return self._scorer
