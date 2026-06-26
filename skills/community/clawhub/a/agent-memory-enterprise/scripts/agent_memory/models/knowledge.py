"""Knowledge memory models."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field

from .base import MemoryBase


class DocumentChunk(MemoryBase):
    document_id: str
    chunk_index: int
    content: str
    embedding: Optional[list[float]] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Document(MemoryBase):
    title: str
    source: str = ""
    domain: str = ""
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchResult(BaseModel):
    chunk_id: str
    content: str
    score: float
    document_id: str
    chunk_index: int
    metadata: dict[str, Any] = Field(default_factory=dict)
    document_title: Optional[str] = None
