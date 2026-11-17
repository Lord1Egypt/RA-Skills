"""HunYuan (Tencent Cloud) model adapter for llm-core shared kernel."""
from __future__ import annotations

import json
import urllib.request
import urllib.error
import hmac
import hashlib
import time
from typing import Any, Dict, Generator, List, Optional

from .base import BaseAdapter
from ..types import ChatMessage, ChatResponse, ContentChunk, now_ms


API_URL = "https://hunyuan.tencentcloudapi.com"
REGION = "ap-guangzhou"
SERVICE = "hunyuan"
VERSION = "2023-09-01"
ACTION = "ChatCompletions"


class HunYuanAdapter(BaseAdapter):
    provider_name = "hunyuan"
    default_model = "hunyuan-standard"

    def _parse_credentials(self) -> tuple:
        """Parse api_key as secret_id:secret_key."""
        parts = self.api_key.split(":")
        if len(parts) != 2:
            raise ValueError(
                f"[hunyuan] api_key 格式错误，应为 secret_id:secret_key。当前: {self.api_key[:10]}..."
            )
        return parts[0], parts[1]

    def _sign(self, payload: str, secret_id: str, secret_key: str) -> Dict[str, str]:
        """Generate Tencent Cloud API signature."""
        timestamp = int(time.time())
        date = time.strftime("%Y-%m-%d", time.gmtime(timestamp))
        # Simplified signing for demo - in production use TC3-HMAC-SHA256
        return {
            "Content-Type": "application/json",
            "X-TC-Action": ACTION,
            "X-TC-Version": VERSION,
            "X-TC-Region": REGION,
            "X-TC-Timestamp": str(timestamp),
            "Authorization": f"TC3-HMAC-SHA256 Credential={secret_id}/{date}/{SERVICE}/tc3_request",
        }

    def _build_payload(self, messages: List[ChatMessage], model: str,
                       stream: bool = False, **kwargs: Any) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "Model": model,
            "Messages": [{"Role": m.role, "Content": m.content} for m in messages],
            "Stream": stream,
        }
        if "temperature" in kwargs and kwargs["temperature"] is not None:
            payload["Temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs and kwargs["max_tokens"] is not None:
            payload["MaxTokens"] = kwargs["max_tokens"]
        return payload

    def chat(self, messages: List[ChatMessage], *,
             model: Optional[str] = None, **kwargs: Any) -> ChatResponse:
        m = model or self.default_model
        start = self._now_ms()
        payload = self._build_payload(messages, m, stream=False, **kwargs)
        secret_id, secret_key = self._parse_credentials()
        headers = self._sign(json.dumps(payload), secret_id, secret_key)
        req = urllib.request.Request(
            API_URL, data=json.dumps(payload).encode("utf-8"),
            headers=headers, method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"[HunYuan] HTTP {e.code}: {body[:200]}。请检查 api_key 是否正确。"
            ) from e
        except Exception as e:
            raise RuntimeError(f"[HunYuan] 网络错误: {e}") from e

        # HunYuan response format
        response = raw.get("Response", {})
        usage = response.get("Usage", {})
        try:
            text = response.get("Choices", [{}])[0].get("Message", {}).get("Content", "")
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"[HunYuan] 解析响应失败: {raw}") from e

        self._is_available = True
        return ChatResponse(
            content=text, model=m, provider=self.provider_name,
            usage={"prompt_tokens": usage.get("PromptTokens", 0),
                   "completion_tokens": usage.get("CompletionTokens", 0)},
            finish_reason=response.get("Choices", [{}])[0].get("FinishReason", "stop"),
            duration_ms=self._now_ms() - start,
        )

    def stream_chat(self, messages: List[ChatMessage], *,
                    model: Optional[str] = None, **kwargs: Any) -> Generator[ContentChunk, None, None]:
        m = model or self.default_model
        payload = self._build_payload(messages, m, stream=True, **kwargs)
        secret_id, secret_key = self._parse_credentials()
        headers = self._sign(json.dumps(payload), secret_id, secret_key)
        req = urllib.request.Request(
            API_URL, data=json.dumps(payload).encode("utf-8"),
            headers=headers, method="POST",
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
                        delta = chunk.get("Response", {}).get("Choices", [{}])[0].get("Delta", {})
                        content = delta.get("Content", "")
                        if content:
                            yield ContentChunk(type="text", text=content,
                                               metadata={"provider": self.provider_name, "model": m})
                    except json.JSONDecodeError:
                        continue
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"[HunYuan] 流式 HTTP {e.code}: {body[:200]}") from e

    def check_health(self) -> bool:
        try:
            msgs = [ChatMessage(role="user", content="hi")]
            self.chat(msgs, max_tokens=1)
            self._is_available = True
        except Exception:
            self._is_available = False
        self._last_health_check = self._now_ms()
        return self._is_available
