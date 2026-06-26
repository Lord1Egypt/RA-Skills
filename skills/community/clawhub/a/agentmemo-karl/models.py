"""Pydantic models for agentMemo v3.0.0 API."""
from __future__ import annotations
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


class MemoryCreate(BaseModel):
    text: str
    namespace: str = "default"
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    ttl_seconds: Optional[int] = Field(default=None, ge=1)
    metadata: dict[str, Any] = Field(default_factory=dict)
    half_life_hours: float = Field(default=168.0, gt=0)
    tags: list[str] = Field(default_factory=list)


class MemoryUpdate(BaseModel):
    text: Optional[str] = None
    importance: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    ttl_seconds: Optional[int] = Field(default=None, ge=1)
    metadata: Optional[dict[str, Any]] = None
    half_life_hours: Optional[float] = Field(default=None, gt=0)
    tags: Optional[list[str]] = None


class MemoryResponse(BaseModel):
    id: str
    text: str
    namespace: str
    importance: float
    effective_importance: float
    ttl_seconds: Optional[int]
    metadata: dict[str, Any]
    tags: list[str]
    embedding_dim: int
    created_at: str
    age_hours: float
    version: int


class MemorySearchResult(BaseModel):
    id: str
    text: str
    namespace: str
    score: float
    effective_importance: float
    metadata: dict[str, Any]
    tags: list[str]
    created_at: str


class MemorySearchResponse(BaseModel):
    results: list[MemorySearchResult]
    total_tokens: int
    budget_tokens: Optional[int]
    mode: str = "semantic"
    cursor: Optional[str] = None


class MemoryCreateResponse(BaseModel):
    id: str
    embedding_dim: int


class MemoryVersionResponse(BaseModel):
    id: str
    memory_id: str
    text: str
    namespace: str
    importance: float
    tags: list[str]
    metadata: dict[str, Any]
    version: int
    created_at: str


class BatchCreateItem(BaseModel):
    text: str
    namespace: str = "default"
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    ttl_seconds: Optional[int] = Field(default=None, ge=1)
    metadata: dict[str, Any] = Field(default_factory=dict)
    half_life_hours: float = Field(default=168.0, gt=0)
    tags: list[str] = Field(default_factory=list)


class BatchDeleteItem(BaseModel):
    id: str


class BatchSearchItem(BaseModel):
    q: str
    namespace: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=100)
    min_score: float = Field(default=0.3, ge=0.0, le=1.0)
    mode: str = Field(default="semantic")


class BatchRequest(BaseModel):
    create: list[BatchCreateItem] = Field(default_factory=list)
    delete: list[BatchDeleteItem] = Field(default_factory=list)
    search: list[BatchSearchItem] = Field(default_factory=list)


class BatchResponse(BaseModel):
    created: list[MemoryCreateResponse] = Field(default_factory=list)
    deleted: list[str] = Field(default_factory=list)
    searches: list[MemorySearchResponse] = Field(default_factory=list)


class EventCreate(BaseModel):
    type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    namespace: str = "default"


class EventResponse(BaseModel):
    id: str
    type: str
    payload: dict[str, Any]
    namespace: str
    created_at: str


class NamespaceInfo(BaseModel):
    namespace: str
    memory_count: int
    event_count: int


class StatsResponse(BaseModel):
    total_memories: int
    total_events: int
    total_namespaces: int
    storage_size_bytes: int
    storage_size_human: str


class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    db_ok: bool
    embedding_model_loaded: bool


class MetricsResponse(BaseModel):
    uptime_seconds: float
    total_requests: int
    requests_per_minute: float
    total_memories: int
    total_events: int
    total_namespaces: int
    storage_size_bytes: int
    embedding_cache_size: int
    embedding_cache_hits: int
    embedding_cache_misses: int
    hnsw_index_size: int
    active_websockets: int


class ImportMemory(BaseModel):
    text: str
    namespace: str = "default"
    importance: float = 0.5
    half_life_hours: float = 168.0
    ttl_seconds: Optional[int] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    created_at: Optional[str] = None


class ImportRequest(BaseModel):
    memories: list[ImportMemory]


class ImportResponse(BaseModel):
    imported: int
    ids: list[str]


class ExportResponse(BaseModel):
    memories: list[dict[str, Any]]
    exported: int
    namespace: Optional[str]


class ApiKeyCreate(BaseModel):
    name: str
    namespaces: list[str] = Field(default_factory=lambda: ["*"])


class ApiKeyResponse(BaseModel):
    key: str
    name: str
    namespaces: list[str]
    created_at: str
