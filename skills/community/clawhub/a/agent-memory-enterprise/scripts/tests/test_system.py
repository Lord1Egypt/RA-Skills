"""Integration test for MemorySystem."""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from agent_memory.config import (
    ChromaConfig,
    ContextMemoryConfig,
    InjectorConfig,
    KnowledgeMemoryConfig,
    MemorySystemConfig,
    PostgreSQLConfig,
    RedisConfig,
    ScoringConfig,
    TaskMemoryConfig,
    UserMemoryConfig,
    ExperienceMemoryConfig,
)
from agent_memory.memories.context_memory import ContextMemory
from agent_memory.memories.task_memory import TaskMemory
from agent_memory.memories.user_memory import UserMemory
from agent_memory.memories.knowledge_memory import KnowledgeMemory
from agent_memory.memories.experience_memory import ExperienceMemory
from agent_memory.storage.postgres_client import PostgresClient
from agent_memory.storage.postgres_models import Base
from agent_memory.storage.chroma_client import ChromaClient


@pytest_asyncio.fixture
async def memory_system():
    """Create a MemorySystem with test backends (no external services)."""
    import chromadb
    import fakeredis.aioredis
    from agent_memory.config import PostgreSQLConfig
    from agent_memory.routing.feature_extractor import TaskFeatureExtractor
    from agent_memory.routing.router import MemoryRouter
    from agent_memory.scoring.importance_scorer import ImportanceScorer
    from agent_memory.injection.injector import MemoryInjector

    # Config
    pg_config = PostgreSQLConfig(url="sqlite+aiosqlite:///:memory:", echo=False)
    chroma_config = ChromaConfig(
        persist_directory="/tmp/test_chroma",
        collection_name="test",
    )
    scoring_config = ScoringConfig()
    injector_config = InjectorConfig(token_budget=2000)

    # Storage backends
    redis_client = MagicMock()
    redis_client.client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    redis_client.initialize = AsyncMock()
    redis_client.shutdown = AsyncMock()

    pg_client = PostgresClient(pg_config, base=Base)
    await pg_client.initialize()

    chroma_client = ChromaClient(chroma_config)
    chroma_client._client = chromadb.Client()
    chroma_client._collection = chroma_client._client.get_or_create_collection(
        name="test", metadata={"hnsw:space": "cosine"}
    )

    # Memory layers
    ctx_memory = ContextMemory(redis_client, ContextMemoryConfig(max_tokens=500))
    task_memory = TaskMemory(pg_client, TaskMemoryConfig())
    user_memory = UserMemory(pg_client, redis_client, UserMemoryConfig())
    knowledge_memory = KnowledgeMemory(chroma_client, KnowledgeMemoryConfig(chunk_size=50, chunk_overlap=10))
    experience_memory = ExperienceMemory(pg_client, ExperienceMemoryConfig())

    # Cross-cutting
    scorer = ImportanceScorer(scoring_config)
    extractor = TaskFeatureExtractor()
    router = MemoryRouter(
        ctx_memory, task_memory, user_memory,
        knowledge_memory, experience_memory,
        extractor, scorer,
    )
    injector = MemoryInjector(injector_config, scorer)

    class TestSystem:
        pass

    sys = TestSystem()
    sys._redis = redis_client
    sys._pg = pg_client
    sys._chroma = chroma_client
    sys._context_memory = ctx_memory
    sys._task_memory = task_memory
    sys._user_memory = user_memory
    sys._knowledge_memory = knowledge_memory
    sys._experience_memory = experience_memory
    sys._scorer = scorer
    sys._extractor = extractor
    sys._router = router
    sys._injector = injector

    yield sys

    await pg_client.shutdown()


class TestIntegration:
    @pytest.mark.asyncio
    async def test_full_task_lifecycle(self, memory_system):
        """Test creating, executing, and archiving a task."""
        # Create task
        task = await memory_system._task_memory.create_task(
            goal="Generate Q4 report",
            steps=["Collect data", "Analyze trends", "Write report"],
            user_id="user_1",
        )
        assert task.goal == "Generate Q4 report"

        # Start
        task = await memory_system._task_memory.start_task(task.task_id)
        assert task.status.value == "in_progress"

        # Advance
        task = await memory_system._task_memory.advance_step(task.task_id, "Collected 100 records")
        assert task.current_step_index == 1

        # Complete
        task = await memory_system._task_memory.complete_task(task.task_id, "Report generated")
        assert task.status.value == "completed"

    @pytest.mark.asyncio
    async def test_user_preferences(self, memory_system):
        """Test user preference management."""
        pref = await memory_system._user_memory.update_preference(
            "user_1", "language", "zh-CN", "explicit"
        )
        assert pref.key == "language"
        assert pref.value == "zh-CN"
        assert pref.confidence == 1.0

        profile = await memory_system._user_memory.get_profile("user_1")
        assert "language" in profile.preferences
        assert profile.preferences["language"].value == "zh-CN"

    @pytest.mark.asyncio
    async def test_knowledge_indexing_and_search(self, memory_system):
        """Test knowledge document indexing and retrieval."""
        doc_id = await memory_system._knowledge_memory.index_text(
            title="Python Basics",
            content="Python is a versatile programming language used for web development, data science, and AI.",
            domain="programming",
        )
        assert doc_id is not None

        results = await memory_system._knowledge_memory.search_similar(
            "What programming language for AI?", domain="programming"
        )
        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_experience_recording(self, memory_system):
        """Test recording and finding experiences."""
        from agent_memory.models.experience import ExperienceOutcome, ExperienceRecord

        record = ExperienceRecord(
            task_type="analysis",
            goal_description="Analyze quarterly financial data",
            approach="Collect data from APIs then process with pandas",
            outcome=ExperienceOutcome.SUCCESS,
            duration_seconds=300.0,
            domain="finance",
        )
        exp_id = await memory_system._experience_memory.record_experience(record)
        assert exp_id is not None

    @pytest.mark.asyncio
    async def test_context_window(self, memory_system):
        """Test context window management."""
        from agent_memory.models.context import ContextMessage, MessageRole

        msg = ContextMessage(role=MessageRole.USER, content="Hello", token_count=5)
        window = await memory_system._context_memory.add_message("sess_1", msg)
        assert len(window.messages) == 1

        msg2 = ContextMessage(role=MessageRole.ASSISTANT, content="Hi there", token_count=5)
        window = await memory_system._context_memory.add_message("sess_1", msg2)
        assert len(window.messages) == 2
