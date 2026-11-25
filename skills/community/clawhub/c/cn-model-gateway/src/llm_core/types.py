"""Core data types for llm-core shared kernel.

These types are shared between MCP and CLI forms.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ChatMessage:
    """A single chat message.

    v2.1.0: added tool_call_id / name / tool_calls for multi-round
    Function Calling chains (OpenAI-style round-trip).
    """
    role: str          # "user" | "assistant" | "system" | "tool"
    content: str
    image: str = ""    # base64 / URL / file path (empty = text-only)
    tool_call_id: str = ""                    # v2.1.0: role=tool → which call this result belongs to
    name: str = ""                            # v2.1.0: role=tool → tool name
    tool_calls: Optional[List[Dict[str, Any]]] = None  # v2.1.0: role=assistant → emitted tool calls

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"role": self.role}
        if self.image:
            d["content"] = [
                {"type": "image_url", "image_url": {"url": self.image}},
                {"type": "text", "text": self.content},
            ]
        else:
            d["content"] = self.content
        # v2.1.0: multi-round Function Calling chain fields (only emitted when set,
        # so legacy `{"role","content"}` shape stays unchanged for plain messages).
        if self.tool_call_id:
            d["tool_call_id"] = self.tool_call_id
        if self.name:
            d["name"] = self.name
        if self.tool_calls is not None:
            d["tool_calls"] = self.tool_calls
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

    def to_openai(self) -> Dict[str, Any]:
        """v2.1.0: normalize to OpenAI-style tool_call for multi-round chains."""
        return {
            "id": self.id,
            "type": "function",
            "function": {
                "name": self.name,
                "arguments": json.dumps(self.arguments, ensure_ascii=False),
            },
        }


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
