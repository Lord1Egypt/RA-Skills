"""Abstract base adapter for llm-core shared kernel.

All model adapters must inherit from this.
Extends the original BaseAdapter with multimodal, Function Calling,
and the 4 new MCP tools: embed_text, rerank, audio_transcribe, video_understand.
"""
from __future__ import annotations

import abc
import json
from typing import Any, Dict, Generator, List, Optional

from ..types import (
    ChatMessage, ChatResponse, ContentChunk,
    EmbeddingResult, RerankResult, TranscriptionResult,
    VideoUnderstandingResult, now_ms,
)


class BaseAdapter(abc.ABC):
    """All model adapters must inherit from this."""

    provider_name: str = ""
    default_model: str = ""

    def __init__(self, api_key: str, **kwargs: Any) -> None:
        if not api_key:
            raise ValueError(
                f"[{self.provider_name}] API key is empty. "
                f"请在 config.json 中填写 {self.provider_name} 的 api_key。"
            )
        self.api_key = api_key
        self.extra_config = kwargs
        self._last_health_check: Optional[float] = None
        self._is_available: bool = True

    @abc.abstractmethod
    def chat(self, messages: List[ChatMessage], *,
             model: Optional[str] = None, **kwargs: Any) -> ChatResponse:
        """Send a non-streaming chat request. Returns full response."""
        ...

    @abc.abstractmethod
    def stream_chat(self, messages: List[ChatMessage], *,
                    model: Optional[str] = None, **kwargs: Any) -> Generator[ContentChunk, None, None]:
        """Send a streaming chat request. Yields content chunks."""
        ...

    @abc.abstractmethod
    def check_health(self) -> bool:
        """Check if the API key is valid and service is reachable."""
        ...

    # --- Multimodal support ---

    def describe_image(self, image: str, prompt: str = "请描述这张图片",
                       *, model: Optional[str] = None, **kwargs: Any) -> ChatResponse:
        """Convenience method for image description."""
        msgs = [ChatMessage(role="user", content=prompt, image=image)]
        return self.chat(msgs, model=model, **kwargs)

    # --- Function Calling / Tool Use ---

    def format_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format tool definitions into provider-specific format."""
        formatted = []
        for tool in tools:
            formatted.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {"type": "object", "properties": {}}),
                },
            })
        return formatted

    def parse_tool_calls(self, raw: Dict[str, Any]) -> List[Any]:
        """Parse tool calls from provider response."""
        from ..types import ToolCall
        tool_calls = []
        message = raw.get("choices", [{}])[0].get("message", {})
        raw_calls = message.get("tool_calls", [])
        for tc in raw_calls:
            func = tc.get("function", {})
            args_str = func.get("arguments", "{}")
            try:
                args = json.loads(args_str) if isinstance(args_str, str) else args_str
            except Exception:
                args = {}
            tool_calls.append(ToolCall(
                id=tc.get("id", ""),
                name=func.get("name", ""),
                arguments=args,
            ))
        return tool_calls

    # --- v1.6.0: New MCP tool interfaces ---

    def embed_text(self, texts: List[str], *,
                   model: Optional[str] = None, **kwargs: Any) -> EmbeddingResult:
        """Generate embeddings for a list of text strings.

        Default implementation raises NotImplementedError.
        Subclasses that support embeddings should override this method.
        """
        raise NotImplementedError(
            f"[{self.provider_name}] 暂不支持向量嵌入（embed_text）。"
            f"请使用支持嵌入的提供商如 deepseek、zhipu、doubao 等。"
        )

    def rerank(self, query: str, documents: List[str], *,
               model: Optional[str] = None, **kwargs: Any) -> RerankResult:
        """Rerank documents by relevance to a query.

        Default implementation raises NotImplementedError.
        Subclasses that support reranking should override this method.
        """
        raise NotImplementedError(
            f"[{self.provider_name}] 暂不支持重排序（rerank）。"
            f"请使用支持重排序的提供商如 zhipu、doubao 等。"
        )

    def audio_transcribe(self, audio: str, *,
                         model: Optional[str] = None, **kwargs: Any) -> TranscriptionResult:
        """Transcribe audio to text.

        Default implementation raises NotImplementedError.
        Subclasses that support audio transcription should override this method.
        """
        raise NotImplementedError(
            f"[{self.provider_name}] 暂不支持语音转文字（audio_transcribe）。"
            f"请使用支持语音的提供商如 zhipu、doubao 等。"
        )

    def video_understand(self, video: str, prompt: str = "请描述这个视频的内容",
                         *, model: Optional[str] = None, **kwargs: Any) -> VideoUnderstandingResult:
        """Understand video content by extracting keyframes and describing them.

        Default implementation raises NotImplementedError.
        Subclasses that support video understanding should override this method.
        """
        raise NotImplementedError(
            f"[{self.provider_name}] 暂不支持视频理解（video_understand）。"
            f"请使用支持视频的提供商如 zhipu、doubao、tongyi 等。"
        )

    def is_available(self) -> bool:
        """Return cached availability (refreshed by health check)."""
        return self._is_available

    @staticmethod
    def _now_ms() -> int:
        return now_ms()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} available={self._is_available}>"
