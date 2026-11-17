"""Core data types for llm-core shared kernel.

These types are shared between MCP and CLI forms.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ChatMessage:
    """A single chat message."""
    role: str          # "user" | "assistant" | "system"
    content: str
    image: str = ""    # base64 / URL / file path (empty = text-only)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"role": self.role}
        if self.image:
            d["content"] = [
                {"type": "image_url", "image_url": {"url": self.image}},
                {"type": "text", "text": self.content},
            ]
        else:
            d["content"] = self.content
        return d


@dataclass
class ContentChunk:
    """A single content chunk in a streaming response (MCP standard)."""
    type: str = "text"
    text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = {"type": self.type, "text": self.text}
        if self.metadata:
            d["metadata"] = self.metadata
        return d


@dataclass
class ToolCall:
    """A single tool call from model response."""
    id: str
    name: str
    arguments: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name, "arguments": self.arguments}


@dataclass
class ChatResponse:
    """A complete (non-streaming) chat response."""
    content: str
    model: str
    provider: str
    usage: Dict[str, int] = field(default_factory=dict)
    finish_reason: str = "stop"
    duration_ms: int = 0
    tool_calls: List[ToolCall] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "content": self.content,
            "model": self.model,
            "provider": self.provider,
            "usage": self.usage,
            "finish_reason": self.finish_reason,
            "duration_ms": self.duration_ms,
        }
        if self.tool_calls:
            d["tool_calls"] = [tc.to_dict() for tc in self.tool_calls]
        return d


@dataclass
class EmbeddingResult:
    """Result from embed_text operation."""
    provider: str
    model: str
    embeddings: List[List[float]]
    usage: Dict[str, int] = field(default_factory=dict)
    duration_ms: int = 0


@dataclass
class RerankResult:
    """Result from rerank operation."""
    provider: str
    model: str
    scores: List[float]  # relevance scores for each document
    usage: Dict[str, int] = field(default_factory=dict)
    duration_ms: int = 0


@dataclass
class TranscriptionResult:
    """Result from audio_transcribe operation."""
    provider: str
    model: str
    text: str
    language: str = "zh"
    duration_ms: int = 0


@dataclass
class VideoUnderstandingResult:
    """Result from video_understand operation."""
    provider: str
    model: str
    description: str
    keyframe_count: int = 0
    duration_ms: int = 0


def now_ms() -> int:
    return int(time.time() * 1000)
