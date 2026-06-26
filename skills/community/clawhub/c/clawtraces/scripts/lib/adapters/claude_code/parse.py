# FILE_META
# INPUT:  SessionHandle + PipelineOptions
# OUTPUT: ParseResult (OpenAI trajectory IR + prompt_hint + attachments + stats)
# POS:    skill lib adapters/claude_code — per-session translator
# MISSION: Translate one Claude Code session jsonl into the OpenAI IR + companion data.

"""Parse a single Claude Code session jsonl.

Event types observed across 200+ local sessions:
  user / assistant / system / file-history-snapshot / attachment /
  queue-operation / permission-mode / last-prompt / progress /
  custom-title / agent-name

Only user + assistant carry dialogue content. Everything else is either
bookkeeping (queue-operation / progress / last-prompt / custom-title /
agent-name) or runtime metadata (system is *not* the API system prompt;
see risk #3/#4 notes in docs/adapter-design.md §12).

Scope of this file:
  - Read the jsonl once, split into the main-trunk dialogue stream
    (used for messages[]) and a side channel for prompt_hint signals
    (permission-mode / custom-title / agent-name / version).
  - Translate Anthropic Messages-API content blocks into OpenAI IR
    shapes.
  - Emit prompt_hint and stats alongside the trajectory. messages[0]
    is left as a placeholder for the server-side prompt assembler.

workspace_snapshot extraction (CLAUDE.md / settings.json / .mcp.json)
lives in P2-5 and composes with this module's output.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable

from .. import Attachment, ParseResult, SessionHandle
from . import _workspace

_ADAPTER_NAME = "claude-code"

# Event types we consider for the main dialogue stream.
_DIALOGUE_TYPES = {"user", "assistant"}

# Placeholder filled by the server-side prompt assembler.
_SYSTEM_PROMPT_PLACEHOLDER = "__PENDING_SYSTEM_PROMPT__"

# Raw jsonl attachment cap. Stays well under the 50MB session_bundle
# hard limit (docs/adapter-design.md §5.4) so workspace_snapshot files
# always fit alongside.
_RAW_SESSION_MAX_BYTES = 40 * 1024 * 1024


def parse(handle: SessionHandle, opts: Any = None) -> ParseResult:
    if handle.path is None or not handle.path.is_file():
        return ParseResult(
            trajectory={},
            reject_reason="claude_code_session_file_missing",
        )

    raw_bytes = handle.path.read_bytes()
    all_events = list(_iter_all_events(raw_bytes))
    if not all_events:
        return ParseResult(
            trajectory={},
            reject_reason="claude_code_empty_session",
        )

    dialogue = [e for e in all_events if _is_dialogue(e)]
    if not dialogue:
        return ParseResult(
            trajectory={},
            reject_reason="claude_code_no_dialogue_events",
        )

    # ─── Translate dialogue → OpenAI messages ──────────────────────────

    messages: list[dict] = [
        {"role": "system", "content": _SYSTEM_PROMPT_PLACEHOLDER}
    ]
    tool_names: set[str] = set()
    tool_use_count = 0
    reasoning_count = 0
    version_bumps: list[str] = []  # populated via _collect_version_bumps below

    for event in dialogue:
        for translated in _translate_event(event):
            messages.append(translated)
            tc = translated.get("tool_calls")
            if isinstance(tc, list):
                tool_use_count += len(tc)
                for call in tc:
                    name = (call.get("function") or {}).get("name")
                    if name:
                        tool_names.add(name)
            if translated.get("reasoning_content"):
                reasoning_count += 1

    tools = _synthesize_tool_schemas(sorted(tool_names))
    trajectory = {"tools": tools, "messages": messages}

    # ─── prompt_hint / stats side channel ──────────────────────────────

    signals = _extract_hint_signals(all_events)
    version_bumps = signals["versions_seen"]
    primary_version = version_bumps[0] if version_bumps else "unknown"
    cwd_hash = _sha256_hex(handle.cwd) if handle.cwd else None

    workspace = _workspace.collect(handle.cwd, opts)

    prompt_hint: dict = {
        "adapter": _ADAPTER_NAME,
        "version": primary_version,
        "model": handle.model,
        "session_id": handle.session_id,
        "session_started_at": (
            handle.started_at.isoformat() if handle.started_at else None
        ),
        "cwd": handle.cwd,
        "cwd_hash": f"sha256:{cwd_hash}" if cwd_hash else None,
        "system_prompt_ready": False,
        "extras": {
            "slug": handle.extras.get("slug"),
            "git_branch": handle.extras.get("git_branch"),
            "permission_mode": signals["permission_mode"],
            "custom_title": signals["custom_title"],
            "agent_name": signals["agent_name"],
            "version_bumps": version_bumps if len(version_bumps) > 1 else [],
            "mcp_servers": workspace["mcp_servers"],
            "skills_enabled": workspace["skills_enabled"],
        },
    }

    # ─── Attachments ───────────────────────────────────────────────────

    attachments: list[Attachment] = list(workspace["attachments"])
    if len(raw_bytes) <= _RAW_SESSION_MAX_BYTES:
        attachments.insert(
            0,
            Attachment(
                zip_path="raw_session.jsonl",
                content=raw_bytes,
                is_core=True,
            ),
        )
    else:
        prompt_hint["extras"]["raw_log_omitted"] = "size_exceeded"

    stats = {
        "domain": "coding",
        "model": handle.model or "unknown",
        "turns": sum(1 for m in messages if m["role"] == "user"),
        "tool_use_count": tool_use_count,
        "tool_names": sorted(tool_names),
        "effective_asst": sum(1 for m in messages if m["role"] == "assistant"),
        "reasoning_asst": reasoning_count,
        "system_prompt_source": "server_pending",
        "cwd": handle.cwd,
        "started_at": handle.started_at.isoformat() if handle.started_at else None,
        "raw_log_bytes": len(raw_bytes),
    }

    return ParseResult(
        trajectory=trajectory,
        prompt_hint=prompt_hint,
        attachments=attachments,
        stats=stats,
    )


# ─── Event loader + classifiers ────────────────────────────────────────

def _iter_all_events(raw_bytes: bytes) -> Iterable[dict]:
    """Yield every parsed jsonl event (no filtering).

    Decode as UTF-8 with ``errors='replace'`` first: handing raw bytes
    directly to ``json.loads`` triggers its BOM auto-detection, which
    blows up on lines that happen to start with bytes that look like a
    UTF-32 prefix. The raw bytes still ship verbatim in
    raw_session.jsonl, so the upstream copy remains byte-identical for
    forensics.
    """
    text = raw_bytes.decode("utf-8", errors="replace")
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def _is_dialogue(event: dict) -> bool:
    if event.get("type") not in _DIALOGUE_TYPES:
        return False
    if event.get("isMeta"):
        return False
    if event.get("isSidechain"):
        return False
    return True


def _extract_hint_signals(events: list[dict]) -> dict:
    """Harvest prompt_hint extras from the full event stream.

    ``version_bumps``: ordered list of unique versions seen (first = the
    value used in prompt_hint.version; presence of >1 entry is the
    signal the server needs to flag risk #7 — mid-session upgrades).
    """
    versions_seen: list[str] = []
    permission_mode: str | None = None
    custom_title: str | None = None
    agent_name: str | None = None

    for e in events:
        v = e.get("version")
        if isinstance(v, str) and v and v not in versions_seen:
            versions_seen.append(v)

        t = e.get("type")
        if t == "permission-mode" and permission_mode is None:
            pm = e.get("permissionMode") or e.get("permission_mode")
            if isinstance(pm, str):
                permission_mode = pm
        elif t == "custom-title" and custom_title is None:
            # Observed shape in local samples: {"type":"custom-title",...}
            # — we store the whole non-type-payload for downstream use.
            custom_title = _first_nontrivial_string(e, skip={"type", "timestamp", "sessionId"})
        elif t == "agent-name" and agent_name is None:
            agent_name = _first_nontrivial_string(e, skip={"type", "timestamp", "sessionId"})

    return {
        "versions_seen": versions_seen,
        "permission_mode": permission_mode,
        "custom_title": custom_title,
        "agent_name": agent_name,
    }


def _first_nontrivial_string(d: dict, *, skip: set[str]) -> str | None:
    for k, v in d.items():
        if k in skip:
            continue
        if isinstance(v, str) and v:
            return v
    return None


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# ─── Translation (Anthropic → OpenAI) ──────────────────────────────────

def _translate_event(event: dict) -> list[dict]:
    """Turn one user/assistant event into zero-or-more OpenAI messages."""
    etype = event.get("type")
    msg = event.get("message") or {}
    if etype == "user":
        return _translate_user(msg)
    if etype == "assistant":
        out = _translate_assistant(msg)
        return [out] if out else []
    return []


def _translate_user(msg: dict) -> list[dict]:
    content = msg.get("content")
    if isinstance(content, str):
        return [{"role": "user", "content": content}]
    if not isinstance(content, list):
        return []

    tool_msgs: list[dict] = []
    text_parts: list[str] = []
    for block in content:
        if not isinstance(block, dict):
            continue
        btype = block.get("type")
        if btype == "tool_result":
            tool_msgs.append(_tool_result_to_openai(block))
        elif btype == "text":
            text = block.get("text")
            if isinstance(text, str) and text:
                text_parts.append(text)
        # image / other blocks: intentionally dropped for now.

    out: list[dict] = list(tool_msgs)
    if text_parts:
        out.append({"role": "user", "content": "\n".join(text_parts)})
    return out


def _tool_result_to_openai(block: dict) -> dict:
    tool_call_id = block.get("tool_use_id") or block.get("tool_call_id") or ""
    inner = block.get("content")
    if isinstance(inner, str):
        text = inner
    elif isinstance(inner, list):
        parts = []
        for item in inner:
            if isinstance(item, dict) and item.get("type") == "text":
                t = item.get("text")
                if isinstance(t, str):
                    parts.append(t)
        text = "\n".join(parts)
    else:
        text = ""
    return {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": text,
    }


def _translate_assistant(msg: dict) -> dict | None:
    content = msg.get("content")
    if not isinstance(content, list):
        return None

    text_parts: list[str] = []
    reasoning_parts: list[str] = []
    tool_calls: list[dict] = []

    for block in content:
        if not isinstance(block, dict):
            continue
        btype = block.get("type")
        if btype == "text":
            t = block.get("text")
            if isinstance(t, str) and t:
                text_parts.append(t)
        elif btype == "thinking":
            t = block.get("thinking")
            if isinstance(t, str) and t:
                reasoning_parts.append(t)
        elif btype == "tool_use":
            tool_calls.append(_tool_use_to_openai(block, index=len(tool_calls)))

    if not text_parts and not tool_calls and not reasoning_parts:
        return None

    out: dict = {"role": "assistant"}
    if text_parts:
        out["content"] = "\n".join(text_parts)
    elif tool_calls:
        out["content"] = None
    else:
        out["content"] = ""

    if tool_calls:
        out["tool_calls"] = tool_calls
    if reasoning_parts:
        out["reasoning_content"] = "\n".join(reasoning_parts)
    return out


def _tool_use_to_openai(block: dict, index: int) -> dict:
    name = block.get("name") or ""
    inputs = block.get("input")
    if inputs is None:
        args_str = "{}"
    elif isinstance(inputs, str):
        args_str = inputs
    else:
        args_str = json.dumps(inputs, ensure_ascii=False)
    return {
        "id": block.get("id") or f"call_{index}",
        "type": "function",
        "function": {
            "name": name,
            "arguments": args_str,
        },
    }


def _synthesize_tool_schemas(names: list[str]) -> list[dict]:
    """Minimal OpenAI tools[] from observed tool names.

    Claude Code does not ship per-session tool schemas in the jsonl;
    placeholder function schemas keep the trajectory shape valid. The
    server-side prompt assembler (which knows the template version) is
    responsible for the real parameter schemas.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": "",
                "parameters": {"type": "object", "properties": {}, "required": []},
            },
        }
        for name in names
    ]


__all__ = ["parse"]
