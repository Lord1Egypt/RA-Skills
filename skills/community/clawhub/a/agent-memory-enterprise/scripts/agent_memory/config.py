"""Configuration for the Agent Memory System."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv


@dataclass
class RedisConfig:
    url: str = "redis://localhost:6379/0"
    max_connections: int = 20
    decode_responses: bool = True


@dataclass
class PostgreSQLConfig:
    url: str = "postgresql+asyncpg://user:pass@localhost:5432/agent_memory"
    pool_size: int = 10
    max_overflow: int = 20
    echo: bool = False


@dataclass
class ChromaConfig:
    persist_directory: str = "./chroma_data"
    collection_name: str = "knowledge_base"
    embedding_model: str = "all-MiniLM-L6-v2"


@dataclass
class ContextMemoryConfig:
    max_messages: int = 50
    max_tokens: int = 4000
    ttl_seconds: int = 1800


@dataclass
class TaskMemoryConfig:
    max_steps: int = 100
    archive_after_hours: int = 24


@dataclass
class UserMemoryConfig:
    cache_ttl_seconds: int = 3600
    max_preferences: int = 200


@dataclass
class KnowledgeMemoryConfig:
    chunk_size: int = 512
    chunk_overlap: int = 64
    top_k: int = 5
    similarity_threshold: float = 0.7


@dataclass
class ExperienceMemoryConfig:
    similarity_top_k: int = 10
    min_success_rate: float = 0.5
    consolidation_threshold: int = 50


@dataclass
class ScoringConfig:
    relevance_weight: float = 0.30
    recency_weight: float = 0.25
    frequency_weight: float = 0.20
    explicit_weight: float = 0.25
    decay_half_life_hours: float = 24.0


@dataclass
class InjectorConfig:
    token_budget: int = 4000
    budget_threshold: float = 0.80
    tokenizer_model: str = "cl100k_base"


@dataclass
class MemorySystemConfig:
    redis: RedisConfig = field(default_factory=RedisConfig)
    postgresql: PostgreSQLConfig = field(default_factory=PostgreSQLConfig)
    chroma: ChromaConfig = field(default_factory=ChromaConfig)
    context: ContextMemoryConfig = field(default_factory=ContextMemoryConfig)
    task: TaskMemoryConfig = field(default_factory=TaskMemoryConfig)
    user: UserMemoryConfig = field(default_factory=UserMemoryConfig)
    knowledge: KnowledgeMemoryConfig = field(default_factory=KnowledgeMemoryConfig)
    experience: ExperienceMemoryConfig = field(default_factory=ExperienceMemoryConfig)
    scoring: ScoringConfig = field(default_factory=ScoringConfig)
    injector: InjectorConfig = field(default_factory=InjectorConfig)


def load_config(config: Optional[MemorySystemConfig] = None) -> MemorySystemConfig:
    """Load configuration with environment variable overrides."""
    load_dotenv()
    if config is None:
        config = MemorySystemConfig()

    if url := os.getenv("AGENT_MEM_REDIS_URL"):
        config.redis.url = url
    if url := os.getenv("AGENT_MEM_POSTGRESQL_URL"):
        config.postgresql.url = url
    if d := os.getenv("AGENT_MEM_CHROMA_PERSIST_DIRECTORY"):
        config.chroma.persist_directory = d
    if n := os.getenv("AGENT_MEM_CHROMA_COLLECTION_NAME"):
        config.chroma.collection_name = n

    return config
