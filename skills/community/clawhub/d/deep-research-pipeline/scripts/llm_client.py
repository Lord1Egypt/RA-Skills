"""Shared LLM client — provider-agnostic OpenAI-compatible API caller.

Supports any OpenAI-compatible endpoint (Z.AI GLM, OpenAI, Anthropic via proxy,
Ollama, LM Studio, vLLM, etc.) via environment variables.

Priority:
  1. OPENAI_API_KEY + OPENAI_API_BASE (or OPENAI_BASE_URL) — standard OpenAI-compat
  2. ZAI_API_KEY + ZAI_API_ENDPOINT — Z.AI GLM (legacy, still supported)
  3. ANTHROPIC_API_KEY — Anthropic (requires OpenAI-compat proxy)

Environment variables:
  LLM_MODEL          Model name (default: auto-detected from provider)
  LLM_API_KEY        Universal API key (highest priority)
  LLM_API_BASE       Universal base URL (highest priority)
  OPENAI_API_KEY     OpenAI / compatible key
  OPENAI_API_BASE    OpenAI / compatible endpoint
  OPENAI_BASE_URL    Alternative to OPENAI_API_BASE
  ZAI_API_KEY        Z.AI GLM key (legacy)
  ZAI_API_ENDPOINT   Z.AI endpoint (legacy)
  GLM_MODEL          Z.AI model override (legacy)
"""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Optional


def _resolve_config() -> tuple[str, str, str]:
    """Resolve API key, base URL, and model from environment.

    Returns:
        (api_key, base_url, model)

    Raises:
        RuntimeError: if no API key is configured.
    """
    # Universal overrides (highest priority)
    api_key = os.environ.get("LLM_API_KEY", "")
    base_url = os.environ.get("LLM_API_BASE", "")
    model = os.environ.get("LLM_MODEL", "")

    if api_key and base_url:
        return api_key, base_url.rstrip("/"), model or "gpt-4o-mini"

    # OpenAI-compatible (standard)
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    openai_base = os.environ.get("OPENAI_API_BASE", "") or os.environ.get("OPENAI_BASE_URL", "")
    if openai_key:
        base = openai_base.rstrip("/") if openai_base else "https://api.openai.com/v1"
        return openai_key, base, model or "gpt-4o-mini"

    # Z.AI GLM (legacy)
    zai_key = os.environ.get("ZAI_API_KEY", "")
    zai_endpoint = os.environ.get("ZAI_API_ENDPOINT", "https://api.z.ai/api/coding/paas/v4")
    glm_model = os.environ.get("GLM_MODEL", "glm-5-turbo")
    if zai_key:
        return zai_key, zai_endpoint.rstrip("/"), model or glm_model

    raise RuntimeError(
        "No LLM API key configured. Set one of: "
        "LLM_API_KEY, OPENAI_API_KEY, or ZAI_API_KEY"
    )


def call_llm(
    prompt: str,
    system: str = "",
    max_tokens: int = 4096,
    temperature: float = 0.3,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    """Call an OpenAI-compatible chat completions API.

    Args:
        prompt: User message.
        system: Optional system message.
        max_tokens: Max tokens in response.
        temperature: Sampling temperature.
        model: Model override (else auto-detected from env).
        api_key: API key override (else auto-detected from env).
        base_url: Base URL override (else auto-detected from env).

    Returns:
        Response text content.

    Raises:
        RuntimeError: on API errors or missing config.
    """
    resolved_key, resolved_base, resolved_model = _resolve_config()
    key = api_key or resolved_key
    base = (base_url or resolved_base).rstrip("/")
    mdl = model or resolved_model

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": mdl,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    data = json.dumps(payload).encode()
    endpoint = f"{base}/chat/completions"
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"LLM API {e.code} ({endpoint}): {body}")


# Backward compatibility alias
_call_glm = call_llm
