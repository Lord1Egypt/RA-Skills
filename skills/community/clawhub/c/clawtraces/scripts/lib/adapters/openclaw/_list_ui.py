# FILE_META
# INPUT:  sessions_dirs, output_dir (+ optional limit/since)
# OUTPUT: list[dict] — UI-facing rows (session_id, model, turns, status, topic, ...)
# POS:    skill lib adapters/openclaw — list view used by cli.py and `scan_adapter --list-only`
# MISSION: Enumerate all OpenClaw sessions (eligible + ineligible) as a display-ready table,
#          preserving the legacy shape consumed by cli.list_and_select().

"""Session list for interactive selection.

Produces the same dict shape the legacy ``scan_and_convert.list_qualifying_sessions``
returned so cli.py's table rendering works unchanged. Sessions are tagged
with a legacy-friendly ``status`` field that maps pipeline reject
reasons to the UI strings cli.py expects:

    "non_allowed_model_in_session" → "model_mismatch"
    "cron_task_excluded"           → "cron_task"
    "turns_too_low"                → "turns_too_low"
    "tool_use_too_low"             → "tool_use_too_low"
    "reasoning_too_low"            → "reasoning_too_low"
    "no_cache_trace"               → "no_cache_trace"
    (pipeline runtime_status)      → "active" / "rejected"
    everything else                → None (processable)
"""

from __future__ import annotations

import os
from datetime import datetime

from ...core.config_loader import load_config
from ...parse.cache_trace import (
    build_session_system_prompt_index,
    get_cache_trace_path,
)
from ...pipeline import pipeline as _pipeline
from ...pipeline_options import PipelineOptions, SessionCandidate
from ._manifest import load_manifest


_LEGACY_STATUS_BY_REASON = {
    "non_allowed_model_in_session": "model_mismatch",
    "cron_task_excluded": "cron_task",
    "turns_too_low": "turns_too_low",
    "tool_use_too_low": "tool_use_too_low",
    "reasoning_too_low": "reasoning_too_low",
    "no_cache_trace": "no_cache_trace",
}


def _build_options(
    sessions_dirs: list[str],
    output_dir: str,
    *,
    limit: int | None,
    since: float | None,
) -> PipelineOptions:
    """Construct options tuned for the list-only UI preview.

    ``include_ineligible=True`` lets rejected / active / model_mismatch
    sessions show up tagged; cli.py filters them based on user intent.
    """
    config = load_config()
    max_size = config["max_list_size"]
    return PipelineOptions.from_config(
        config,
        sessions_dirs=sessions_dirs,
        output_dir=output_dir,
        list_size=limit if limit else max_size,
        include_ineligible=True,
        explicit_session_ids=None,
        force_active=False,
        force_rejected=False,
        since_ts=since,
    )


def _format_timestamp(iso_ts: str) -> str:
    if not iso_ts:
        return ""
    try:
        dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
        return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, AttributeError):
        return iso_ts[:19] if len(iso_ts) >= 19 else iso_ts


def _candidate_to_list_row(c: SessionCandidate, index: int) -> dict:
    try:
        fsize = os.path.getsize(c.file_path) if c.file_path else 0
    except OSError:
        fsize = 0

    if not c.eligible and c.reject_reason in _LEGACY_STATUS_BY_REASON:
        status: str | None = _LEGACY_STATUS_BY_REASON[c.reject_reason]
    elif c.runtime_status == "rejected":
        status = "rejected"
    elif c.runtime_status == "active":
        status = "active"
    else:
        status = None

    # For "model_mismatch" rows, surface the offending non-whitelisted model
    # (e.g. gpt-5.4) instead of whatever warm-up frame got picked first
    # (e.g. claude-opus-4-6). The list user needs to see the cause of rejection.
    display_model = c.model or "unknown"
    if c.reject_reason == "non_allowed_model_in_session":
        bad = (c.reject_detail or {}).get("non_allowed_models") or []
        if bad:
            display_model = bad[0]

    return {
        "index": index,
        "session_id": c.session_id,
        "agent_id": c.agent_id,
        "model": display_model,
        "started_at": _format_timestamp(c.started_at),
        "ended_at": _format_timestamp(c.ended_at),
        "file_size_kb": round(fsize / 1024),
        "turns": c.turns,
        "has_compaction": c.has_compaction,
        "topic": c.summary,
        "status": status,
    }


def list_qualifying_sessions(
    sessions_dirs: list[str],
    output_dir: str,
    limit: int | None = None,
    since: float | None = None,
) -> list[dict]:
    """UI-facing session list, one row per candidate (ineligible included).

    Returns legacy-shaped dicts sorted by ``started_at`` descending.
    Already-submitted sessions are hidden (filter_sessions drops them).
    Everything else is tagged via ``status``.
    """
    options = _build_options(sessions_dirs, output_dir, limit=limit, since=since)
    raw = _pipeline.discover_sessions(options)
    if not raw:
        return []

    latest_sids = _pipeline.find_latest_sids_by_agent(raw)
    manifest = load_manifest(output_dir)

    sp_index = build_session_system_prompt_index(
        get_cache_trace_path(),
        target_session_ids={r["session_id"] for r in raw},
    )

    candidates = _pipeline.filter_sessions(
        raw, options,
        manifest=manifest, latest_sids=latest_sids,
        system_prompt_index=sp_index,
    )

    rows = [_candidate_to_list_row(c, 0) for c in candidates]
    rows.sort(key=lambda r: r.get("started_at") or "", reverse=True)
    for i, row in enumerate(rows, 1):
        row["index"] = i
    return rows
