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

    # --- Function Calling / Tool Use (v2.1.0: normalized to OpenAI style) ---

    # Subclasses may override these to declare their wire-format dialect.
    # Dialects: "openai" (default) | "function_call" (legacy single-call field)
    tool_format: str = "openai"

    def format_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """v2.1.0: normalize tool definitions to OpenAI style.

        Accepts either already-normalized OpenAI tool dicts
        (``{"type":"function","function":{...}}``) or the compact form
        (``{"name":...,"description":...,"parameters":...}``). Output is always
        the OpenAI style so every adapter shares ONE wire-format contract.
        """
        formatted: List[Dict[str, Any]] = []
        for tool in tools or []:
            # Already OpenAI-style → pass through (idempotent).
            if tool.get("type") == "function" and isinstance(tool.get("function"), dict):
                formatted.append(tool)
                continue
            formatted.append({
                "type": "function",
                "function": {
                    "name": tool.get("name", ""),
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {"type": "object", "properties": {}}),
                },
            })
        return formatted

    def parse_tool_calls(self, raw: Dict[str, Any]) -> List[Any]:
        """v2.1.0: parse tool calls from any vendor response into unified ToolCall list.

        Handles three wire dialects:
          1. OpenAI ``message.tool_calls[]`` (multi-call, default)
          2. Legacy ``message.function_call`` (single call, some vendors)
          3. Top-level ``tool_calls`` (a few OpenAI-compatible vendors)
        Arguments may be a JSON string or already a dict.
        """
        from ..types import ToolCall
        choices = raw.get("choices") or [{}]
        message = (choices[0].get("message") if choices else {}) or {}

        raw_calls = message.get("tool_calls") or []
        if not raw_calls:
            raw_calls = raw.get("tool_calls") or []
        if not raw_calls:
            # Legacy single function_call field
            legacy = message.get("function_call") or raw.get("function_call")
            if legacy:
                raw_calls = [legacy]

        tool_calls: List[Any] = []
        for tc in raw_calls:
            # Legacy shape: {"name":..., "arguments":"..."} (no function wrapper)
            if "function" in tc:
                func = tc.get("function") or {}
                name = func.get("name", "")
                args_str = func.get("arguments", "{}")
                call_id = tc.get("id", "")
            else:
                name = tc.get("name", "")
                args_str = tc.get("arguments", "{}")
                call_id = tc.get("id", tc.get("call_id", ""))
            if isinstance(args_str, str):
                try:
                    args = json.loads(args_str) if args_str.strip() else {}
                except Exception:
                    args = {}
            elif isinstance(args_str, dict):
                args = args_str
            else:
                args = {}
            tool_calls.append(ToolCall(id=call_id, name=name, arguments=args))
        return tool_calls

    def apply_function_calling(self, payload: Dict[str, Any], kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """v2.1.0: apply normalized Function Calling fields to an OpenAI-style payload.

        Every OpenAI-compatible adapter calls this in ``_build_payload`` so that
        tool definitions share ONE normalized wire-format regardless of vendor.
        """
        tools = kwargs.get("tools")
        if tools:
            payload["tools"] = self.format_tools(tools)
            if "tool_choice" in kwargs:
                payload["tool_choice"] = kwargs["tool_choice"]
        return payload

    def normalize_tool_messages(self, messages: List[Any]) -> List[Dict[str, Any]]:
        """v2.1.0: serialize a multi-round chat (incl. tool results) to OpenAI wire format.

        A multi-round Function Calling chain looks like:
            user → assistant(tool_calls) → tool(result) → assistant(final)
        This method preserves ``tool_call_id`` / ``name`` / ``tool_calls`` fields
        so the model can correlate results back to their originating calls.
        """
        out: List[Dict[str, Any]] = []
        for m in messages:
            d = m.to_dict() if hasattr(m, "to_dict") else dict(m)
            # assistant turn that emitted tool calls: attach normalized tool_calls
            if isinstance(m, dict) and m.get("tool_calls"):
                from ..types import ToolCall
                d["tool_calls"] = [
                    tc.to_openai() if isinstance(tc, ToolCall) else tc
                    for tc in m["tool_calls"]
                ]
            out.append(d)
        return out

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
