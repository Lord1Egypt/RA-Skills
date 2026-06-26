# FILE_META
# INPUT:  message nodes (OpenClaw DAG) + system prompt + model_config
# OUTPUT: OpenAI trajectory dict {model_config, tools, messages}
# POS:    skill lib — called by the openclaw adapter (through pipeline.process_session)
# MISSION: Transparent OpenClaw → OpenAI conversion; no semantic edits beyond format reshaping.

"""Convert OpenClaw .jsonl message nodes directly to OpenAI trajectory format.

v2 path B: emit the OpenAI shape in a single pass instead of going through
an Anthropic intermediate. OpenAI tool results live in their own
``role="tool"`` messages, so parallel tool calls never collapse into a
single content array — meaning the old ``_merge_consecutive_messages`` step
has no reason to exist.

v2 principle (collection layer is a transparent recorder) pinned by PR 3:
  * No per-message filtering — the pipeline rejects entire sessions upfront
    via ``dag.check_session_models``; the converter trusts its input.
  * No encoding patching (U+FFFD passes through).
  * No semantic edits — empty assistant slots, ``stopReason=error`` messages,
    tool-error-terminated sessions all survive because the training side
    may want to learn how the model recovers.
  * ``metadata_stripper`` is explicitly not imported here — see the red-line
    comment at the top of ``metadata_stripper.py``.

v2 §5.3 scheme A (image handling, landed in PR 4):
  * OpenClaw ``{type: "image", data, mimeType}`` blocks pass through user
    and toolResult content verbatim — no field renaming, no data URL
    repackaging. When an image is present, the OpenAI content is emitted
    as a list so text and image blocks coexist; pure-text messages still
    collapse to a plain string for compactness.
"""

from __future__ import annotations

import json

from .tool_registry import get_tool_schemas


# ── model_config helpers ──────────────────────────────────────

# Default max_tokens by model (maxTokens / 3, from the OpenClaw model catalog).
_MODEL_MAX_TOKENS: dict[str, int] = {
    "claude-opus-4-6": 42666,
    "claude-opus-4-5": 21333,
    "claude-opus-4-5-thinking": 21333,
    "claude-sonnet-4-6": 42666,
    "claude-sonnet-4-5": 21845,
    "claude-haiku-4-5": 21845,
    "gpt-5.4": 42666,
}


def _normalize_provider(model: str) -> str:
    m = (model or "").lower()
    if "claude" in m:
        return "anthropic"
    if "gpt" in m or "o1" in m or "o3" in m:
        return "openai"
    if "gemini" in m:
        return "google"
    if "qwen" in m:
        return "alibaba"
    if "deepseek" in m:
        return "deepseek"
    return "anthropic"


def _resolve_max_tokens(model: str) -> int | None:
    m = (model or "").lower()
    for key, val in _MODEL_MAX_TOKENS.items():
        if key in m:
            return val
    return None


def build_model_config(
    model: str,
    *,
    provider: str = "",
    thinking_level: str = "off",
    max_tokens: int | None = None,
) -> dict:
    """Build the ``model_config`` object embedded in the OpenAI trajectory.

    ``provider`` is inferred from the model name when blank or ``"unknown"``.
    ``max_tokens`` falls back to the ``_MODEL_MAX_TOKENS`` catalog when not
    supplied. A ``max_tokens`` of ``0`` is treated the same as unspecified.
    """
    effective_provider = (
        provider if provider and provider != "unknown"
        else _normalize_provider(model)
    )
    effective_max = (
        max_tokens if isinstance(max_tokens, int) and max_tokens > 0
        else _resolve_max_tokens(model)
    )
    config: dict = {
        "model": model,
        "provider": effective_provider,
        # OpenClaw omits temperature when thinking is on, and the underlying
        # APIs default to 1.0; we record the effective value explicitly.
        "temperature": 1.0,
        "thinking": thinking_level,
    }
    if effective_max:
        config["max_tokens"] = effective_max
    return config


# ── tool schema conversion (Anthropic schema → OpenAI function) ──

def _convert_tools_to_openai(anthropic_tools: list[dict]) -> list[dict]:
    """Rewrap the Anthropic-shaped schemas from ``get_tool_schemas`` as OpenAI functions."""
    result: list[dict] = []
    for tool in anthropic_tools:
        result.append({
            "type": "function",
            "function": {
                "name": tool.get("name", ""),
                "description": tool.get("description", ""),
                "parameters": tool.get("input_schema", {}),
            },
        })
    return result


# ── content-block extraction helpers ──────────────────────────

def _build_user_or_tool_content(content):
    """Build the OpenAI-shaped content for a user or toolResult message.

    v2 §5.3 (scheme A): image blocks pass through verbatim as
    ``{"type": "image", "data": ..., "mimeType": ...}`` (no field rename,
    no data-URL repackaging). When any image block is present, we emit a
    list preserving the original block order so text + image coexist.
    When only text blocks are present, we collapse to a plain string for
    compactness (matches the pre-PR-4 shape for text-only messages).
    """
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""

    has_image = any(
        isinstance(b, dict) and b.get("type") == "image" for b in content
    )

    if not has_image:
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)

    blocks: list[dict] = []
    for block in content:
        if isinstance(block, str):
            blocks.append({"type": "text", "text": block})
        elif isinstance(block, dict):
            btype = block.get("type")
            if btype == "text":
                blocks.append({"type": "text", "text": block.get("text", "")})
            elif btype == "image":
                # v2 §5.3 scheme A: verbatim passthrough, extra fields preserved.
                blocks.append(dict(block))
    return blocks


def _assistant_blocks_to_openai(content) -> tuple[list[str], list[str], list[dict]]:
    """Split an assistant content list into (reasoning, text, tool_calls) parts."""
    reasoning_parts: list[str] = []
    text_parts: list[str] = []
    tool_calls: list[dict] = []

    if not isinstance(content, list):
        return reasoning_parts, text_parts, tool_calls

    for block in content:
        if not isinstance(block, dict):
            continue
        block_type = block.get("type")

        if block_type == "thinking":
            thinking_text = block.get("thinking", "")
            if thinking_text:
                reasoning_parts.append(thinking_text)

        elif block_type == "text":
            text = block.get("text", "")
            # Preserve the text as-is — v2 forbids stripping "empty" or
            # "whitespace" assistant text, the training side may care.
            text_parts.append(text)

        elif block_type == "toolCall":
            arguments = block.get("arguments", {})
            # Some OpenClaw builds serialize arguments as a JSON string.
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except (json.JSONDecodeError, ValueError):
                    arguments = {}
            if not isinstance(arguments, dict):
                arguments = {}
            tool_calls.append({
                "id": block.get("id", ""),
                "type": "function",
                "function": {
                    "name": block.get("name", ""),
                    "arguments": json.dumps(arguments, ensure_ascii=False),
                },
            })

    return reasoning_parts, text_parts, tool_calls


# ── collection helpers ────────────────────────────────────────

def _collect_tool_calls(messages: list[dict]) -> list[dict]:
    """Collect every OpenClaw toolCall block so ``get_tool_schemas`` can emit their signatures.

    v2: no per-message filtering. If the pipeline's session-level check let
    the session through, every assistant message inside it is in-bound and
    its tool calls count toward the schema set.
    """
    tool_calls = []
    for node in messages:
        if node.get("type") == "compaction":
            continue
        msg = node.get("message", {})
        if msg.get("role") != "assistant":
            continue
        for block in msg.get("content", []):
            if isinstance(block, dict) and block.get("type") == "toolCall":
                tool_calls.append(block)
    return tool_calls


# ── public entry ──────────────────────────────────────────────

def convert_to_trajectory(
    message_nodes: list[dict],
    *,
    real_system_prompt: str,
    model_config: dict,
) -> dict:
    """Convert OpenClaw message nodes to an OpenAI trajectory.

    Returns ``{model_config, tools, messages}``. ``messages[0]`` is the
    ``{"role": "system", ...}`` entry (always present when a system prompt
    is supplied); conversation turns follow.

    A ``_discarded`` sentinel is attached only when there is no usable
    system prompt — other v2 rejection reasons (model whitelist, turn count,
    cron, cache-trace) are enforced by the pipeline before this function
    is called, so it trusts every node it receives.
    """
    if not real_system_prompt:
        return {
            "model_config": model_config,
            "tools": [],
            "messages": [],
            "_discarded": "no_system_prompt",
        }

    tool_call_blocks = _collect_tool_calls(message_nodes)
    tool_schemas = get_tool_schemas(tool_call_blocks)
    openai_tools = _convert_tools_to_openai(tool_schemas)

    openai_messages: list[dict] = [{
        "role": "system",
        "content": real_system_prompt,
    }]

    for node in message_nodes:

        if node.get("type") == "compaction":
            summary = node.get("summary", "")
            if summary:
                openai_messages.append({
                    "role": "user",
                    "content": f"[COMPACTION_BOUNDARY] {summary}",
                })
            continue

        msg = node.get("message", {})
        role = msg.get("role")
        content = msg.get("content", [])

        if role == "user":
            openai_messages.append({
                "role": "user",
                "content": _build_user_or_tool_content(content),
            })

        elif role == "assistant":
            reasoning_parts, text_parts, tool_calls = _assistant_blocks_to_openai(content)

            out: dict = {"role": "assistant"}
            if reasoning_parts:
                out["reasoning_content"] = "\n".join(reasoning_parts)
            if tool_calls:
                out["content"] = "\n".join(text_parts) if text_parts else None
                out["tool_calls"] = tool_calls
            else:
                out["content"] = "\n".join(text_parts) if text_parts else ""
            openai_messages.append(out)

        elif role == "toolResult":
            openai_messages.append({
                "role": "tool",
                "tool_call_id": msg.get("toolCallId", ""),
                "content": _build_user_or_tool_content(content),
            })

    # Strip any leading non-user entries after the system message — OpenAI
    # training convention opens with the first user turn.
    if len(openai_messages) > 1:
        drop_until = 1
        while (
            drop_until < len(openai_messages)
            and openai_messages[drop_until]["role"] != "user"
        ):
            drop_until += 1
        if drop_until > 1:
            del openai_messages[1:drop_until]

    # Strip trailing non-assistant entries so the trajectory ends on a model turn.
    while len(openai_messages) > 1 and openai_messages[-1]["role"] != "assistant":
        openai_messages.pop()

    # Minimum viable trajectory: system + user + assistant.
    if len(openai_messages) < 3:
        return {
            "model_config": model_config,
            "tools": openai_tools,
            "messages": [],
        }

    return {
        "model_config": model_config,
        "tools": openai_tools,
        "messages": openai_messages,
    }
