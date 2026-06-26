# FILE_META
# INPUT:  PipelineOptions (sessions_dirs, session_id filter, since timestamp, ...)
# OUTPUT: iterable of SessionHandle (one per OpenClaw session that survives pipeline.filter_sessions)
# POS:    skill lib adapters/openclaw — session enumeration
# MISSION: Run v2 pipeline's discover → filter stages and hand each SessionCandidate
#          to downstream as a SessionHandle. Permanent rejects land in manifest.

"""Enumerate OpenClaw sessions.

Strategy:
  1. ``pipeline.discover_sessions`` — walk agents' ``sessions.json`` indexes
  2. ``pipeline.find_latest_sids_by_agent`` — identify the still-active
     session per agent (excluded from processing to avoid shipping a
     half-complete conversation)
  3. ``build_session_system_prompt_index`` — preload authoritative system
     prompts from ``cache-trace.jsonl`` (batched, keyed by session_id)
  4. ``pipeline.filter_sessions`` — apply OpenClaw-specific eligibility
     rules (model whitelist, cron tasks, compaction handling, ...)
  5. For each resulting SessionCandidate: yield a SessionHandle with the
     candidate embedded in ``extras`` so parse() can consume it verbatim.

**Hard reject side-effect**: when the pipeline marks a session as
``non_allowed_model_in_session`` we immediately record it to
manifest.rejected — this is the historical "model mismatch never retried"
contract and must not be weakened by the adapter migration.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .. import SessionHandle
from ._manifest import load_manifest, record_rejection


def discover(opts: Any = None) -> Iterable[SessionHandle]:
    """Yield one SessionHandle per OpenClaw SessionCandidate.

    ``opts`` must be a ``PipelineOptions`` (or duck-typed equivalent) —
    OpenClaw's pipeline depends on it for sessions_dirs, output_dir,
    eligibility thresholds and explicit session_id filters.
    """
    # Local import to keep the adapter lazy — callers that never pick
    # openclaw avoid loading the full pipeline.
    from ...parse.cache_trace import (
        build_session_system_prompt_index,
        get_cache_trace_path,
    )
    from ...pipeline import pipeline as _pipeline

    if opts is None:
        raise ValueError(
            "adapters.openclaw.discover requires a PipelineOptions "
            "instance; received None"
        )

    raw = _pipeline.discover_sessions(opts)
    if not raw:
        return

    latest_sids = _pipeline.find_latest_sids_by_agent(raw)
    manifest = load_manifest(opts.output_dir)

    sp_index = build_session_system_prompt_index(
        get_cache_trace_path(),
        target_session_ids={r["session_id"] for r in raw},
    )

    candidates = _pipeline.filter_sessions(
        raw, opts,
        manifest=manifest, latest_sids=latest_sids,
        system_prompt_index=sp_index,
    )

    for candidate in candidates:
        # Honour the legacy hard-reject path: a session whose jsonl
        # contains a non-whitelisted model is banned forever.
        if (
            not candidate.eligible
            and candidate.reject_reason == "non_allowed_model_in_session"
        ):
            record_rejection(
                opts.output_dir, candidate.session_id,
                reason=candidate.reject_reason,
                detail=candidate.reject_detail,
            )

        yield SessionHandle(
            adapter="openclaw",
            session_id=candidate.session_id,
            path=Path(candidate.file_path) if candidate.file_path else None,
            cwd=getattr(candidate, "cwd", None),
            model=candidate.model,
            started_at=_parse_started_at(candidate),
            size_bytes=_safe_filesize(candidate.file_path),
            extras={
                "candidate": candidate,
                "sp_cached": sp_index.get(candidate.session_id),
            },
        )


def _parse_started_at(candidate: Any) -> datetime | None:
    started = getattr(candidate, "started_at", None)
    if started is None:
        return None
    if isinstance(started, datetime):
        return started
    if isinstance(started, (int, float)):
        ts = float(started)
        if ts > 1e12:
            ts /= 1000
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    if isinstance(started, str):
        try:
            return datetime.fromisoformat(started.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def _safe_filesize(path: str | None) -> int:
    if not path:
        return 0
    try:
        import os
        return os.path.getsize(path)
    except OSError:
        return 0
