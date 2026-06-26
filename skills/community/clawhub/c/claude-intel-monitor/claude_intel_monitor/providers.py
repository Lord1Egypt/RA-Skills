"""Provider abstraction for talking to different AI models.

Supports:
- OpenAI-compatible APIs (OpenAI, DeepSeek, any OpenAI-compatible endpoint)
- Anthropic native API
- Local/self-test mode (for testing the tool without API keys)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
import os
import json
import time

import httpx


@dataclass
class ModelResponse:
    """Standardized response from any provider."""
    text: str
    model: str
    latency_ms: float
    tokens_used: int = 0
    raw: dict = field(default_factory=dict)


class ProviderError(Exception):
    """Provider-level errors (auth, rate limit, network)."""
    pass


class BaseProvider(ABC):
    """Abstract provider with OpenAI-compatible assumption."""

    def __init__(self, model: str, api_key: Optional[str] = None,
                 base_url: Optional[str] = None, timeout: float = 60.0,
                 max_tokens: int = 2048):
        self.model = model
        self.api_key = api_key or os.environ.get(f"{self._env_prefix}_API_KEY", "")
        self.base_url = base_url or os.environ.get(f"{self._env_prefix}_BASE_URL", self._default_base_url)
        self.timeout = timeout
        self.max_tokens = max_tokens

    @property
    @abstractmethod
    def _env_prefix(self) -> str:
        """Environment variable prefix (e.g. 'OPENAI', 'ANTHROPIC')."""
        ...

    @property
    @abstractmethod
    def _default_base_url(self) -> str:
        ...

    @abstractmethod
    async def chat(self, prompt: str, system: str = "") -> ModelResponse:
        """Send a chat completion request."""
        ...

    async def _post_json(self, url: str, payload: dict, headers: dict) -> dict:
        """Send HTTP POST with error handling."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code == 401:
                raise ProviderError(f"API key invalid for {self.__class__.__name__}")
            if resp.status_code == 429:
                raise ProviderError(f"Rate limited by {self.__class__.__name__}")
            if resp.status_code >= 400:
                body = resp.text[:200]
                raise ProviderError(f"HTTP {resp.status_code}: {body}")
            return resp.json()


class OpenAIProvider(BaseProvider):
    """OpenAI Chat Completions API (also works for DeepSeek, local LLMs)."""

    @property
    def _env_prefix(self) -> str:
        return "OPENAI"

    @property
    def _default_base_url(self) -> str:
        return "https://api.openai.com/v1"

    async def chat(self, prompt: str, system: str = "") -> ModelResponse:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": 0.0,  # deterministic for benchmarking
        }

        t0 = time.monotonic()
        try:
            data = await self._post_json(url, payload, headers)
        except ProviderError:
            raise
        except Exception as e:
            raise ProviderError(f"OpenAI request failed: {e}")
        elapsed = (time.monotonic() - t0) * 1000

        choice = data.get("choices", [{}])[0]
        text = choice.get("message", {}).get("content", "") or ""
        usage = data.get("usage", {})
        tokens = usage.get("total_tokens", 0)

        return ModelResponse(
            text=text,
            model=data.get("model", self.model),
            latency_ms=elapsed,
            tokens_used=tokens,
            raw=data,
        )


class AnthropicProvider(BaseProvider):
    """Anthropic Messages API (native, not OpenAI-compatible)."""

    ANTHROPIC_VERSION = "2023-06-01"

    @property
    def _env_prefix(self) -> str:
        return "ANTHROPIC"

    @property
    def _default_base_url(self) -> str:
        return "https://api.anthropic.com/v1"

    async def chat(self, prompt: str, system: str = "") -> ModelResponse:
        url = f"{self.base_url.rstrip('/')}/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.ANTHROPIC_VERSION,
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": 0.0,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system

        t0 = time.monotonic()
        try:
            data = await self._post_json(url, payload, headers)
        except ProviderError:
            raise
        except Exception as e:
            raise ProviderError(f"Anthropic request failed: {e}")
        elapsed = (time.monotonic() - t0) * 1000

        content = data.get("content", [{}])
        text = ""
        for block in content:
            if block.get("type") == "text":
                text += block.get("text", "")

        usage = data.get("usage", {})
        tokens = usage.get("output_tokens", 0) + usage.get("input_tokens", 0)

        return ModelResponse(
            text=text,
            model=data.get("model", self.model),
            latency_ms=elapsed,
            tokens_used=tokens,
            raw=data,
        )


class DeepSeekProvider(OpenAIProvider):
    """DeepSeek API (OpenAI-compatible)."""

    @property
    def _env_prefix(self) -> str:
        return "DEEPSEEK"

    @property
    def _default_base_url(self) -> str:
        return "https://api.deepseek.com/v1"


# Provider registry
PROVIDER_MAP = {
    "openai": OpenAIProvider,
    "deepseek": DeepSeekProvider,
    "anthropic": AnthropicProvider,
}


def get_provider(provider_name: str, model: str, **kwargs) -> BaseProvider:
    """Factory: get a provider instance by name.

    provider_name: 'openai', 'deepseek', or 'anthropic'
    model: e.g. 'gpt-4o', 'deepseek-chat', 'claude-sonnet-4-20250514'

    Reads API key from environment: {PREFIX}_API_KEY
    """
    cls = PROVIDER_MAP.get(provider_name.lower())
    if cls is None:
        raise ValueError(f"Unknown provider: {provider_name}. Choose from: {list(PROVIDER_MAP)}")
    return cls(model=model, **kwargs)
