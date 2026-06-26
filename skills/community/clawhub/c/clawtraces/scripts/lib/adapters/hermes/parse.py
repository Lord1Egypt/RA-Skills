# FILE_META
# INPUT:  SessionHandle + PipelineOptions
# OUTPUT: ParseResult (OpenAI trajectory IR + prompt_hint + attachments + stats)
# POS:    skill lib adapters/hermes — per-session translator
# MISSION: Turn one Hermes session into an OpenAI-format trajectory + companion metadata.

"""Parse a single Hermes session into the OpenAI IR.

The SQLite schema we target (as of the April 2026 docs):

    sessions(session_id, started_at, model, system_prompt, ...)
    messages(session_id, seq, role, content, tool_call_id, tool_calls,
             tool_name, reasoning, reasoning_details, finish_reason, ...)

We read defensively: every optional column is probed first and missing
ones degrade to NULL without crashing. The ``system_prompt`` snapshot on
the sessions row is used verbatim as ``messages[0]`` so the server can
record ``prompt_status='skipped'``.

NOTE: Not yet validated against a real Hermes DB (risk #2 in
docs/adapter-design.md §12). Field names here match what Nous' public
docs describe; real-data smoke test in P1-8 may require micro-adjustments.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any

from .. import Attachment, ParseResult, SessionHandle
from ._db import column_names, open_readonly, table_exists


# Message-row columns we try to read. Same resolution strategy as discover.
_MSG_COL_MAP: dict[str, tuple[str, ...]] = {
    "seq": ("seq", "idx", "id"),
    "role": ("role",),
    "content": ("content", "text"),
    "tool_call_id": ("tool_call_id",),
    "tool_calls": ("tool_calls",),
    "tool_name": ("tool_name",),
    "reasoning": ("reasoning", "reasoning_content"),
    "finish_reason": ("finish_reason", "stop_reason"),
}


def parse(handle: SessionHandle, opts: Any = None) -> ParseResult:
    conn = open_readonly(opts)
    try:
        if not table_exists(conn, "sessions") or not table_exists(conn, "messages"):
            return ParseResult(
                trajectory={},
                reject_reason="hermes_schema_missing_tables",
            )

        sess_row = _fetch_session_row(conn, handle.session_id)
        if sess_row is None:
            return ParseResult(
                trajectory={},
                reject_reason="session_not_found",
            )

        msg_rows = _fetch_message_rows(conn, handle.session_id)
    finally:
        conn.close()

    system_prompt = sess_row.get("system_prompt") or ""
    messages: list[dict] = [{"role": "system", "content": system_prompt}]
    tool_names: set[str] = set()
    tool_use_count = 0
    reasoning_count = 0

    for row in msg_rows:
        translated = _translate_message(row)
        if translated is None:
            continue
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

    prompt_hint = {
        "adapter": "hermes",
        "version": sess_row.get("hermes_version") or "unknown",
        "model": handle.model or sess_row.get("model"),
        "session_id": handle.session_id,
        "session_started_at": handle.started_at.isoformat() if handle.started_at else None,
        "cwd": handle.cwd,
        "cwd_hash": None,
        "system_prompt_ready": True,
        "extras": {
            "message_count": len(msg_rows),
            "tool_use_count": tool_use_count,
            "reasoning_asst": reasoning_count,
        },
    }

    raw_jsonl = _build_raw_jsonl(sess_row, msg_rows)
    attachments = [
        Attachment(
            zip_path="raw_session.jsonl",
            content=raw_jsonl.encode("utf-8"),
            is_core=True,
        )
    ]

    stats = {
        "domain": "coding",  # Hermes's domain is generic; refine later if needed
        "model": handle.model or sess_row.get("model") or "unknown",
        "turns": sum(1 for m in messages if m["role"] == "user"),
        "tool_use_count": tool_use_count,
        "tool_names": sorted(tool_names),
        "system_prompt_source": "hermes_snapshot",
        "effective_asst": sum(1 for m in messages if m["role"] == "assistant"),
        "reasoning_asst": reasoning_count,
        "cwd": handle.cwd,
        "started_at": handle.started_at.isoformat() if handle.started_at else None,
    }

    return ParseResult(
        trajectory=trajectory,
        prompt_hint=prompt_hint,
        attachments=attachments,
        stats=stats,
    )


# ─── SQL helpers ───────────────────────────────────────────────────────

def _fetch_session_row(conn: sqlite3.Connection, session_id: str) -> dict | None:
    cols = set(column_names(conn, "sessions"))
    want = [
        ("session_id", ("session_id", "id")),
        ("model", ("model",)),
        ("system_prompt", ("system_prompt",)),
        ("started_at", ("started_at", "created_at")),
        ("hermes_version", ("hermes_version", "version")),
    ]
    selects = []
    for logical, candidates in want:
        picked = next((c for c in candidates if c in cols), None)
        if picked:
            selects.append(f"{picked} AS {logical}")
        else:
            selects.append(f"NULL AS {logical}")
    # primary key column resolves the same way as discover
    pk = "session_id" if "session_id" in cols else "id"
    row = conn.execute(
        f"SELECT {', '.join(selects)} FROM sessions WHERE {pk} = ? LIMIT 1",
        (session_id,),
    ).fetchone()
    return dict(row) if row else None


def _fetch_message_rows(conn: sqlite3.Connection, session_id: str) -> list[dict]:
    cols = set(column_names(conn, "messages"))
    selects = []
    for logical, candidates in _MSG_COL_MAP.items():
        picked = next((c for c in candidates if c in cols), None)
        selects.append(f"{picked} AS {logical}" if picked else f"NULL AS {logical}")

    order_col = "seq" if "seq" in cols else ("idx" if "idx" in cols else "id")
    query = (
        f"SELECT {', '.join(selects)} FROM messages "
        f"WHERE session_id = ? ORDER BY {order_col}"
    )
    rows = conn.execute(query, (session_id,)).fetchall()
    return [dict(r) for r in rows]


# ─── Message translation (Hermes → OpenAI) ─────────────────────────────

def _translate_message(row: dict) -> dict | None:
    role = row.get("role")
    if role not in ("user", "assistant", "tool", "system"):
        return None  # unknown role — skip rather than corrupt trajectory
    if role == "system":
        return None  # system prompt comes from sessions.system_prompt snapshot

    out: dict = {"role": role}

    content = row.get("content")
    if content is not None:
        out["content"] = content

    if role == "tool":
        tid = row.get("tool_call_id")
        if tid:
            out["tool_call_id"] = tid

    if role == "assistant":
        tool_calls_raw = row.get("tool_calls")
        parsed_calls = _parse_tool_calls(tool_calls_raw)
        if parsed_calls:
            out["tool_calls"] = parsed_calls
            # OpenAI allows content=null when tool_calls present
            if content in (None, ""):
                out["content"] = None

        reasoning = row.get("reasoning")
        if reasoning:
            out["reasoning_content"] = reasoning

    return out


def _parse_tool_calls(raw: Any) -> list[dict] | None:
    """Hermes stores tool_calls as JSON. Normalize to OpenAI array shape."""
    if raw in (None, "", "[]"):
        return None
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8", errors="replace")
    if isinstance(raw, str):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return None
    else:
        data = raw

    if not isinstance(data, list):
        return None

    out: list[dict] = []
    for i, call in enumerate(data):
        if not isinstance(call, dict):
            continue
        fn = call.get("function") or {
            "name": call.get("name"),
            "arguments": call.get("arguments"),
        }
        name = fn.get("name") if isinstance(fn, dict) else None
        args = fn.get("arguments") if isinstance(fn, dict) else None
        if args is not None and not isinstance(args, str):
            args = json.dumps(args, ensure_ascii=False)

        out.append({
            "id": call.get("id") or f"call_{i}",
            "type": call.get("type") or "function",
            "function": {
                "name": name or "",
                "arguments": args if args is not None else "{}",
            },
        })
    return out or None


def _synthesize_tool_schemas(names: list[str]) -> list[dict]:
    """Build a minimal OpenAI tools[] from observed tool names.

    Hermes does not expose per-session tool schemas in the DB as of the
    documented layout; we ship placeholder schemas so the trajectory is
    syntactically valid. Real parameter schemas are a follow-up concern.
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


def _build_raw_jsonl(sess_row: dict, msg_rows: list[dict]) -> str:
    """Emit a reproducible raw_session.jsonl derived from the DB.

    Line 1 is a synthetic session record; subsequent lines are the raw
    message rows verbatim (dict form). This is the deterministic "raw"
    we ship inside session_bundle.zip when we cannot shell out to the
    Hermes CLI.
    """
    lines = [json.dumps({"type": "session", **sess_row}, ensure_ascii=False)]
    for row in msg_rows:
        lines.append(json.dumps({"type": "message", **row}, ensure_ascii=False))
    return "\n".join(lines) + "\n"


__all__ = ["parse"]
