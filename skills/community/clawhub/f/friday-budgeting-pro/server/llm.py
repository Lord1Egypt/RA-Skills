"""
server/llm.py — Thin LLM wrapper for Friday Budgeting Pro.

Design
------
Calls are routed **primarily** through OpenClaw's local completions API
(an OpenAI-compatible HTTP endpoint running on localhost).  If that endpoint
is unreachable (connection refused, timeout, HTTP error), the wrapper falls
back to calling the Anthropic SDK directly — using an API key read
automatically from OpenClaw's own config files (no manual setup needed).

Primary path (OpenClaw local API)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
POST to OPENCLAW_API_URL (or auto-discovered from ~/.openclaw/openclaw.json)
with body::

    {
        "messages": [...],
        "temperature": 0.0,
        "model": "<OPENCLAW_LLM_MODEL or openclaw/default>"
    }

Gateway endpoint + Bearer token are auto-discovered from
``~/.openclaw/openclaw.json`` when env vars are not set.

Uses stdlib ``urllib.request`` only (no extra dependencies, 60-second timeout).

Response parsing (tried in order):
    1. OpenAI-style:  {"choices": [{"message": {"content": "..."}}]}
    2. OpenAI delta:  {"choices": [{"delta":   {"content": "..."}}]}
    3. Flat text:     {"text": "..."}
    4. Flat content:  {"content": "..."}

If none of those match, or the response body is not valid JSON, the wrapper
logs a warning and falls back to the SDK path.

Fallback path (Anthropic SDK)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When OpenClaw is unreachable *or* returns an unparseable response, the wrapper
uses the Anthropic SDK directly.  The API key is resolved in this order:
  1. ``ANTHROPIC_API_KEY`` environment variable (standard)
  2. ``~/.openclaw/agents/main/agent/auth-profiles.json``
     (OpenClaw's own credential store — no manual copy needed)

Patchability
~~~~~~~~~~~~
The public ``chat()`` function is fully mockable in tests::

    with unittest.mock.patch("server.llm.chat", return_value="..."):
        ...

Env vars
~~~~~~~~
``OPENCLAW_API_URL``      — full URL of the local completions endpoint.
                            Auto-discovered from openclaw.json when unset.
``OPENCLAW_GATEWAY_PORT`` — gateway port (used when OPENCLAW_API_URL unset).
                            Auto-discovered from openclaw.json when unset.
``OPENCLAW_GATEWAY_TOKEN``— Bearer token for the gateway.
                            Auto-discovered from openclaw.json when unset.
``OPENCLAW_LLM_MODEL``    — model name forwarded to OpenClaw
                            (default: "openclaw/default").
``OPENCLAW_LLM_PROVIDER`` — "anthropic" or "openai" (SDK fallback provider).
``ANTHROPIC_API_KEY``     — Anthropic API key for SDK fallback.
                            Auto-discovered from OpenClaw config when unset.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants / env helpers
# ---------------------------------------------------------------------------

_OPENCLAW_TIMEOUT = 60  # seconds — agent turns can take time

# Paths to OpenClaw config files (resolved lazily)
_OPENCLAW_CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
_OPENCLAW_AUTH_PROFILES_PATH = (
    Path.home() / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json"
)

# Module-level cache so we only parse the JSON files once per process lifetime.
_openclaw_config_cache: dict | None = None
_openclaw_auth_cache: dict | None = None


def _load_openclaw_config() -> dict:
    """Return the parsed ~/.openclaw/openclaw.json (cached)."""
    global _openclaw_config_cache
    if _openclaw_config_cache is None:
        try:
            _openclaw_config_cache = json.loads(_OPENCLAW_CONFIG_PATH.read_text())
        except Exception:
            _openclaw_config_cache = {}
    return _openclaw_config_cache


def _load_openclaw_auth() -> dict:
    """Return the parsed auth-profiles.json (cached)."""
    global _openclaw_auth_cache
    if _openclaw_auth_cache is None:
        try:
            _openclaw_auth_cache = json.loads(_OPENCLAW_AUTH_PROFILES_PATH.read_text())
        except Exception:
            _openclaw_auth_cache = {}
    return _openclaw_auth_cache


def _openclaw_gateway_port() -> str:
    """Return the OpenClaw gateway port, auto-discovered from openclaw.json."""
    port = os.environ.get("OPENCLAW_GATEWAY_PORT")
    if port:
        return port
    cfg = _load_openclaw_config()
    discovered = cfg.get("gateway", {}).get("port")
    if discovered:
        return str(discovered)
    return "7531"  # legacy default


def _openclaw_gateway_token() -> str:
    """Return the OpenClaw gateway Bearer token, auto-discovered from openclaw.json."""
    token = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")
    if token:
        return token
    cfg = _load_openclaw_config()
    return cfg.get("gateway", {}).get("auth", {}).get("token", "")


def _anthropic_api_key_from_openclaw() -> str:
    """Return the Anthropic API key stored in OpenClaw's own credential store.

    Looks up ``anthropic:default`` in
    ``~/.openclaw/agents/main/agent/auth-profiles.json``.  Returns an empty
    string when the file is absent or the profile is not found.
    """
    auth = _load_openclaw_auth()
    return auth.get("profiles", {}).get("anthropic:default", {}).get("key", "")


def _openclaw_url() -> str:
    explicit = os.environ.get("OPENCLAW_API_URL")
    if explicit:
        return explicit
    port = _openclaw_gateway_port()
    return f"http://127.0.0.1:{port}/v1/chat/completions"


def _openclaw_model() -> str:
    return os.environ.get("OPENCLAW_LLM_MODEL", "openclaw/default")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def chat(messages: list[dict], temperature: float = 0.0) -> str:
    """Send *messages* to the LLM and return the response text.

    Tries the OpenClaw local API first; falls back to the direct SDK path
    when OpenClaw is unreachable or returns an unparseable response.

    Args:
        messages: A list of ``{"role": ..., "content": ...}`` dicts.
        temperature: Sampling temperature (0.0 = deterministic).

    Returns:
        The assistant's reply as a plain string.

    Raises:
        RuntimeError: If OpenClaw is unreachable **and** no SDK provider is
            available.
        Exception: Any unhandled exception from the SDK is propagated.
    """
    # --- Primary path: OpenClaw local API ---
    try:
        return _chat_openclaw(messages, temperature)
    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        TimeoutError,
        ConnectionError,
        OSError,
    ) as exc:
        logger.warning("OpenClaw local API unreachable (%s); falling back to direct SDK.", exc)
    except _UnparseableResponseError as exc:
        logger.warning(
            "OpenClaw response could not be parsed (%s); falling back to direct SDK.",
            exc,
        )

    # --- Fallback path: Anthropic SDK ---
    return _chat_sdk_fallback(messages, temperature)


# ---------------------------------------------------------------------------
# OpenClaw primary path
# ---------------------------------------------------------------------------


class _UnparseableResponseError(Exception):
    """Raised when the OpenClaw response body cannot be parsed."""


def _chat_openclaw(messages: list[dict], temperature: float) -> str:
    """POST to OpenClaw local completions endpoint and parse the reply."""
    url = _openclaw_url()
    payload = json.dumps(
        {
            "messages": messages,
            "temperature": temperature,
            "model": _openclaw_model(),
        }
    ).encode()

    headers = {"Content-Type": "application/json"}
    _token = _openclaw_gateway_token()
    if _token:
        headers["Authorization"] = f"Bearer {_token}"

    req = urllib.request.Request(
        url,
        data=payload,
        headers=headers,
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=_OPENCLAW_TIMEOUT) as resp:
        raw = resp.read()

    # Parse JSON
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        raise _UnparseableResponseError(f"Non-JSON response: {exc}") from exc

    # Try known response shapes in order of likelihood
    text = _extract_content(data)
    if text is None:
        raise _UnparseableResponseError(f"Unrecognised response shape: {list(data.keys())!r}")
    return text


def _extract_content(data: dict) -> str | None:
    """Try multiple plausible response shapes and return the content string.

    Shapes tried (in order):
        1. OpenAI-style:  {"choices": [{"message": {"content": "..."}}]}
        2. OpenAI delta:  {"choices": [{"delta":   {"content": "..."}}]}
        3. Flat text:     {"text": "..."}
        4. Flat content:  {"content": "..."}

    Returns ``None`` if none of the shapes matched.
    """
    # Shape 1 & 2: choices list
    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            # message.content
            msg = first.get("message")
            if isinstance(msg, dict) and "content" in msg:
                return str(msg["content"])
            # delta.content (streaming residue)
            delta = first.get("delta")
            if isinstance(delta, dict) and "content" in delta:
                return str(delta["content"])
            # bare "text" inside choice
            if "text" in first:
                return str(first["text"])

    # Shape 3: flat {"text": "..."}
    if "text" in data:
        return str(data["text"])

    # Shape 4: flat {"content": "..."}
    if "content" in data:
        return str(data["content"])

    return None


# ---------------------------------------------------------------------------
# SDK fallback path (lazy imports — no top-level SDK dependency)
# ---------------------------------------------------------------------------


def _chat_sdk_fallback(messages: list[dict], temperature: float) -> str:
    """Call the Anthropic or OpenAI SDK directly.

    Resolution order for the provider:
      1. ``OPENCLAW_LLM_PROVIDER`` env var
      2. Try importing ``anthropic`` (preferred)
      3. Try importing ``openai``

    Anthropic key resolution order (inside ``_chat_anthropic``):
      1. ``ANTHROPIC_API_KEY`` env var
      2. OpenClaw auth-profiles.json (``anthropic:default``)
    """
    provider = os.environ.get("OPENCLAW_LLM_PROVIDER", "").lower()
    model = os.environ.get("OPENCLAW_LLM_MODEL", "")

    # Auto-detect provider if not set
    if not provider:
        try:
            import anthropic as _  # noqa: F401

            provider = "anthropic"
        except ImportError:
            pass

    if not provider:
        try:
            import openai as _  # noqa: F401

            provider = "openai"
        except ImportError:
            pass

    if not provider:
        raise RuntimeError(
            "OpenClaw is unreachable and no LLM SDK is available. "
            "Set OPENCLAW_LLM_PROVIDER (e.g. 'anthropic') and OPENCLAW_LLM_MODEL."
        )

    if provider == "anthropic":
        return _chat_anthropic(messages, temperature, model)
    elif provider == "openai":
        return _chat_openai(messages, temperature, model)
    else:
        raise RuntimeError(
            f"Unknown OPENCLAW_LLM_PROVIDER={provider!r}. Supported values: 'anthropic', 'openai'."
        )


def _chat_anthropic(messages: list[dict], temperature: float, model: str) -> str:
    import anthropic  # type: ignore[import]

    # Strip "openclaw/" prefix if the model name came from the OpenClaw path
    # and fell through to the SDK (e.g. "openclaw/default" is not a real
    # Anthropic model name).
    if not model or model.startswith("openclaw"):
        model = "claude-3-5-haiku-20241022"

    # Resolve API key: env var first, then OpenClaw's own credential store.
    api_key = os.environ.get("ANTHROPIC_API_KEY", "") or _anthropic_api_key_from_openclaw()
    if not api_key:
        raise RuntimeError(
            "No Anthropic API key found.  Set ANTHROPIC_API_KEY or ensure "
            "~/.openclaw/agents/main/agent/auth-profiles.json contains "
            "an 'anthropic:default' profile."
        )

    system_parts = [m["content"] for m in messages if m["role"] == "system"]
    human_messages = [m for m in messages if m["role"] != "system"]

    client = anthropic.Anthropic(api_key=api_key)
    kwargs: dict = dict(
        model=model,
        max_tokens=1024,
        messages=human_messages,
        temperature=temperature,
    )
    if system_parts:
        kwargs["system"] = "\n\n".join(system_parts)

    logger.info("LLM fallback: using Anthropic SDK directly (model=%s).", model)
    response = client.messages.create(**kwargs)
    return response.content[0].text


def _chat_openai(messages: list[dict], temperature: float, model: str) -> str:
    import openai  # type: ignore[import]

    if not model:
        model = "gpt-4o-mini"

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=messages,  # type: ignore[arg-type]
        temperature=temperature,
    )
    return response.choices[0].message.content or ""
