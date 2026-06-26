"""Shared test fixtures."""

import asyncio
import pytest
import pytest_asyncio

from agent_memory.config import (
    ChromaConfig,
    ContextMemoryConfig,
    ExperienceMemoryConfig,
    KnowledgeMemoryConfig,
    MemorySystemConfig,
    PostgreSQLConfig,
    RedisConfig,
    ScoringConfig,
    TaskMemoryConfig,
    UserMemoryConfig,
    InjectorConfig,
)


# --- Config fixtures ---

@pytest.fixture
def redis_config():
    return RedisConfig(url="redis://localhost:6379/15")


@pytest.fixture
def pg_config():
    return PostgreSQLConfig(url="sqlite+aiosqlite:///:memory:", echo=False)


@pytest.fixture
def chroma_config(tmp_path):
    return ChromaConfig(
        persist_directory=str(tmp_path / "chroma_test"),
        collection_name="test_collection",
    )


@pytest.fixture
def context_config():
    return ContextMemoryConfig(max_messages=10, max_tokens=1000, ttl_seconds=300)


@pytest.fixture
def task_config():
    return TaskMemoryConfig(max_steps=20, archive_after_hours=1)


@pytest.fixture
def user_config():
    return UserMemoryConfig(cache_ttl_seconds=60)


@pytest.fixture
def knowledge_config():
    return KnowledgeMemoryConfig(chunk_size=100, chunk_overlap=20, top_k=3)


@pytest.fixture
def experience_config():
    return ExperienceMemoryConfig(similarity_top_k=5, min_success_rate=0.3)


@pytest.fixture
def scoring_config():
    return ScoringConfig()


@pytest.fixture
def injector_config():
    return InjectorConfig(token_budget=2000, budget_threshold=0.8)


# --- Fake Redis ---

@pytest_asyncio.fixture
async def fake_redis():
    """Create a fake Redis client using fakeredis."""
    import fakeredis.aioredis
    client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    yield client
    await client.aclose()


# --- Fake PostgreSQL (SQLite in-memory) ---

@pytest_asyncio.fixture
async def fake_pg(pg_config):
    """Create an async SQLite-backed PostgreSQL client."""
    from agent_memory.storage.postgres_client import PostgresClient
    from agent_memory.storage.postgres_models import Base

    client = PostgresClient(pg_config, base=Base)
    await client.initialize()
    yield client
    await client.shutdown()


# --- Fake ChromaDB ---

@pytest_asyncio.fixture
async def fake_chroma(tmp_path):
    """Create an in-memory ChromaDB client."""
    import chromadb
    from agent_memory.storage.chroma_client import ChromaClient

    config = ChromaConfig(
        persist_directory=str(tmp_path / "chroma_test"),
        collection_name="test_collection",
    )
    client = ChromaClient(config)
    # Use ephemeral client instead for tests
    import asyncio
    client._client = chromadb.Client()
    client._collection = client._client.get_or_create_collection(
        name="test_collection",
        metadata={"hnsw:space": "cosine"},
    )
    yield client
    client._client = None
    client._collection = None
