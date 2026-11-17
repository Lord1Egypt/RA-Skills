"""DeepSeek model adapter for llm-core shared kernel."""
from __future__ import annotations

import json
import urllib.request
import urllib.error
from typing import Any, Dict, Generator, List, Optional

from .base import BaseAdapter
from ..types import (
    ChatMessage, ChatResponse, ContentChunk,
    EmbeddingResult, now_ms,
)


CHAT_URL = "https://api.deepseek.com/v1/chat/completions"
EMBED_URL = "https://api.deepseek.com/v1/embeddings"


class DeepSeekAdapter(BaseAdapter):
    provider_name = "deepseek"
    default_model = "deepseek-chat"

    def _build_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _build_payload(self, messages: List[ChatMessage], model: str,
                       stream: bool = False, **kwargs: Any) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": model,
            "messages": [m.to_dict() for m in messages],
            "stream": stream,
        }
        for key in ("temperature", "max_tokens", "top_p", "frequency_penalty"):
            if key in kwargs and kwargs[key] is not None:
                payload[key] = kwargs[key]
        if "tools" in kwargs and kwargs["tools"]:
            payload["tools"] = kwargs["tools"]
            if "tool_choice" in kwargs:
                payload["tool_choice"] = kwargs["tool_choice"]
        return payload

    def chat(self, messages: List[ChatMessage], *,
             model: Optional[str] = None, **kwargs: Any) -> ChatResponse:
        m = model or self.default_model
        start = self._now_ms()
        payload = self._build_payload(messages, m, stream=False, **kwargs)
        req = urllib.request.Request(
            CHAT_URL, data=json.dumps(payload).encode("utf-8"),
            headers=self._build_headers(), method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"[DeepSeek] HTTP {e.code}: {body[:200]}。请检查 api_key 是否正确。"
            ) from e
        except Exception as e:
            raise RuntimeError(f"[DeepSeek] 网络错误: {e}") from e

        usage = raw.get("usage", {})
        try:
            message = raw["choices"][0]["message"]
            text = message.get("content", "") or ""
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"[DeepSeek] 解析响应失败: {raw}") from e

        tool_calls = self.parse_tool_calls(raw)
        self._is_available = True
        return ChatResponse(
            content=text, model=m, provider=self.provider_name,
            usage=usage, finish_reason=raw.get("choices", [{}])[0].get("finish_reason", "stop"),
            duration_ms=self._now_ms() - start,
            tool_calls=tool_calls,
        )

    def stream_chat(self, messages: List[ChatMessage], *,
                    model: Optional[str] = None, **kwargs: Any) -> Generator[ContentChunk, None, None]:
        m = model or self.default_model
        payload = self._build_payload(messages, m, stream=True, **kwargs)
        req = urllib.request.Request(
            CHAT_URL, data=json.dumps(payload).encode("utf-8"),
            headers=self._build_headers(), method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                for line in resp:
                    line = line.decode("utf-8", errors="replace").strip()
                    if not line or not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        return
                    try:
                        chunk = json.loads(data)
                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            yield ContentChunk(type="text", text=content,
                                               metadata={"provider": self.provider_name, "model": m})
                    except json.JSONDecodeError:
                        continue
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"[DeepSeek] 流式 HTTP {e.code}: {body[:200]}") from e

    def check_health(self) -> bool:
        try:
            msgs = [ChatMessage(role="user", content="hi")]
            self.chat(msgs, max_tokens=1)
            self._is_available = True
        except Exception:
            self._is_available = False
        self._last_health_check = self._now_ms()
        return self._is_available

    # --- v1.6.0: embed_text ---

    def embed_text(self, texts: List[str], *,
                   model: Optional[str] = None, **kwargs: Any) -> EmbeddingResult:
        """DeepSeek supports embeddings via deepseek-embedding model."""
        m = model or "deepseek-embedding"
        start = self._now_ms()
        payload = {
            "model": m,
            "input": texts,
        }
        req = urllib.request.Request(
            EMBED_URL, data=json.dumps(payload).encode("utf-8"),
            headers=self._build_headers(), method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"[DeepSeek] embed_text HTTP {e.code}: {body[:200]}"
            ) from e
        except Exception as e:
            raise RuntimeError(f"[DeepSeek] embed_text 网络错误: {e}") from e

        embeddings = []
        for item in raw.get("data", []):
            embeddings.append(item.get("embedding", []))

        return EmbeddingResult(
            provider=self.provider_name,
            model=m,
            embeddings=embeddings,
            usage=raw.get("usage", {}),
            duration_ms=self._now_ms() - start,
        )
