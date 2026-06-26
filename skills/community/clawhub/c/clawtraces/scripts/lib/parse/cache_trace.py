# FILE_META
# INPUT:  cache-trace.jsonl log file
# OUTPUT: dict mapping session_id → system prompt
# POS:    skill lib — primary system prompt source, called by the openclaw adapter
# MISSION: Extract real system prompts from OpenClaw's cache-trace log.

"""Parse cache-trace.jsonl to extract real system prompts by session ID."""

from __future__ import annotations

import json
import os
from typing import Iterable, Optional


def _normalize_system_prompt(system) -> Optional[str]:
    """Normalize system prompt to a string.

    Handles both string format and Anthropic content-blocks format
    (list of dicts with type/text).
    """
    if isinstance(system, str):
        return system
    if isinstance(system, list):
        # Content blocks format: [{"type": "text", "text": "..."}]
        parts = []
        for block in system:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        if parts:
            return "\n".join(parts)
    return None


def get_cache_trace_path() -> str:
    """Get cache-trace.jsonl path from OpenClaw state directory."""
    state_dir = os.environ.get("OPENCLAW_STATE_DIR", os.path.expanduser("~/.openclaw"))

    # Check if openclaw.json specifies a custom path
    config_path = os.path.join(state_dir, "openclaw.json")
    if os.path.isfile(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            custom_path = (
                config.get("diagnostics", {})
                .get("cacheTrace", {})
                .get("filePath", "")
            )
            if custom_path:
                return os.path.expanduser(custom_path)
        except (json.JSONDecodeError, OSError):
            pass

    return os.path.join(state_dir, "logs", "cache-trace.jsonl")


def build_session_system_prompt_index(
    cache_trace_path: str,
    target_session_ids: Optional[Iterable[str]] = None,
) -> dict[str, str]:
    """Build a mapping of sessionId → system prompt from cache-trace.jsonl.

    For each session, takes the last occurrence of a system prompt
    (from stages that include the system field), which is the most complete.

    The file is streamed line by line and assumed to be UTF-8 (it is
    written by OpenClaw's own logger as JSON, always UTF-8). We do NOT
    run encoding detection here because that requires reading a sample
    of the file and, on long-running hosts, this file can grow to GB
    scale — cheap to stream, fatal to slurp.

    Args:
        cache_trace_path: Path to cache-trace.jsonl.
        target_session_ids: Optional iterable of session IDs to limit the
            index to. When provided, only entries for these sessions are
            kept, which drastically reduces peak memory when the caller
            already knows which sessions it needs (e.g. single-session
            explicit mode).

    Returns:
        Dict mapping sessionId to system prompt string.
    """
    index: dict[str, str] = {}

    if not os.path.isfile(cache_trace_path):
        return index

    target_set: Optional[set[str]] = (
        set(target_session_ids) if target_session_ids is not None else None
    )
    if target_set is not None and not target_set:
        return index

    try:
        with open(cache_trace_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue

                session_id = obj.get("sessionId")
                if not session_id:
                    continue
                if target_set is not None and session_id not in target_set:
                    continue

                system = obj.get("system")
                if not system:
                    continue

                normalized = _normalize_system_prompt(system)
                if normalized:
                    # Keep updating — last entry wins (most complete)
                    index[session_id] = normalized
    except OSError:
        pass

    return index


def get_system_prompt_for_session(
    cache_trace_path: str,
    session_id: str,
) -> Optional[str]:
    """Get the system prompt for a specific session from cache-trace.jsonl.

    Returns the last system prompt recorded for this session, or None.
    """
    result: Optional[str] = None

    if not os.path.isfile(cache_trace_path):
        return None

    try:
        with open(cache_trace_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue

                if obj.get("sessionId") == session_id:
                    system = obj.get("system")
                    if system:
                        normalized = _normalize_system_prompt(system)
                        if normalized:
                            result = normalized
    except OSError:
        pass

    return result
