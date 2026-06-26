# FILE_META
# INPUT:  SessionHandle (extras.candidate, extras.sp_cached) + PipelineOptions
# OUTPUT: ParseResult (OpenAI trajectory IR + prompt_hint + raw_session.jsonl attachment + stats)
# POS:    skill lib adapters/openclaw — per-session translator
# MISSION: Turn one OpenClaw SessionCandidate into an OpenAI-format trajectory via the v2 pipeline.

"""Parse a single OpenClaw session into the OpenAI IR.

Delegates to ``lib.pipeline.process_session`` which owns:

  * multi-era DAG concatenation with ``COMPACTION_BOUNDARY``
  * OpenAI IR conversion (with metadata preserved verbatim — red line)
  * stats computation (including heuristic domain / title)

This adapter adds the adapter-shaped wrappers:

  * ``prompt_hint.json`` with adapter metadata (docs/adapter-design.md §5.2)
  * ``raw_session.jsonl`` attachment — the original session jsonl,
    capped at 40MB to leave headroom under the 50MB session_bundle limit
  * ineligible / parse-error handling expressed via ``reject_reason``

Red line reminder: ``strip_metadata_prefix`` must never be applied to
trajectory content. It only feeds stats/summary/review metadata. Phase 4
migration preserves that invariant by reusing ``lib.convert.converter``
verbatim.
"""

from __future__ import annotations

import json
import os
from typing import Any

from .. import Attachment, ParseResult, SessionHandle


# Matches docs/adapter-design.md §5.4: 50MB bundle cap minus headroom
# for workspace_snapshot + extras.
_RAW_SESSION_MAX_BYTES = 40 * 1024 * 1024


def parse(handle: SessionHandle, opts: Any = None) -> ParseResult:
    """Parse one OpenClaw session into the OpenAI IR.

    Expects ``handle.extras`` populated by ``discover()`` with:

      * ``candidate`` — the SessionCandidate produced by filter_sessions
      * ``sp_cached`` — cache-trace-sourced system prompt (or None)
    """
    if opts is None:
        return ParseResult(
            trajectory={},
            reject_reason="adapter_missing_options",
        )

    candidate = (handle.extras or {}).get("candidate")
    sp_cached = (handle.extras or {}).get("sp_cached")
    if candidate is None:
        return ParseResult(
            trajectory={},
            reject_reason="adapter_missing_candidate",
        )

    # Ineligible sessions never parse — surface the pipeline's reason
    # so scan_adapter reports a meaningful filter_report entry.
    if not candidate.eligible:
        return ParseResult(
            trajectory={},
            reject_reason=candidate.reject_reason or "ineligible",
        )

    # Local import to keep the adapter lazy.
    from ...convert.system_prompt_builder import (
        build_system_prompt,
        extract_session_metadata,
    )
    from ...parse.dag import parse_jsonl
    from ...pipeline import pipeline as _pipeline

    try:
        nodes = parse_jsonl(candidate.file_path)
    except Exception as exc:  # noqa: BLE001 — defensive, report as reject
        return ParseResult(
            trajectory={},
            reject_reason="parse_error",
            stats={"detail": str(exc)},
        )

    real_sp, sp_source, session_meta = _resolve_system_prompt(
        candidate,
        nodes=nodes,
        sp_cached=sp_cached,
        allow_reconstruct=opts.eligibility.allow_non_cache_trace,
        build_system_prompt=build_system_prompt,
        extract_session_metadata=extract_session_metadata,
    )
    if not real_sp:
        return ParseResult(
            trajectory={},
            reject_reason="no_cache_trace",
        )

    result = _pipeline.process_session(
        candidate, opts,
        real_system_prompt=real_sp,
        system_prompt_source=sp_source,
        session_meta=session_meta,
    )
    if not result.ok:
        return ParseResult(
            trajectory={},
            reject_reason=result.reject_reason or "process_error",
            stats=dict(result.reject_detail or {}),
        )

    # process_session already wrote trajectory/stats to disk (legacy
    # contract). We re-read them into memory so scan_adapter's emit path
    # can own file layout end-to-end. B5 cleanup will let process_session
    # skip the disk write when called from the adapter.
    trajectory = _read_json(result.trajectory_path)
    stats = _read_json(result.stats_path)

    prompt_hint = {
        "adapter": "openclaw",
        "version": session_meta.get("skill_version") or "unknown",
        "model": stats.get("model"),
        "session_id": candidate.session_id,
        "session_started_at": stats.get("started_at"),
        "cwd": stats.get("cwd"),
        "cwd_hash": None,
        "system_prompt_ready": True,
        "extras": {
            "system_prompt_source": sp_source,
            "agent_id": candidate.agent_id,
            "thinking_level": session_meta.get("thinking_level"),
        },
    }

    attachments = _build_attachments(candidate.file_path)

    return ParseResult(
        trajectory=trajectory,
        prompt_hint=prompt_hint,
        attachments=attachments,
        stats=stats,
    )


# ─── System prompt resolution ──────────────────────────────────────────

def _resolve_system_prompt(
    candidate: Any,
    *,
    nodes: list[dict],
    sp_cached: str | None,
    allow_reconstruct: bool,
    build_system_prompt,
    extract_session_metadata,
) -> tuple[str | None, str, dict]:
    """Return (prompt, source, session_meta) mirroring scan_and_convert's legacy path.

    ``source`` is one of ``"cache_trace"`` / ``"reconstructed"`` / ``""``.
    """
    session_meta = extract_session_metadata(nodes)
    if sp_cached:
        return sp_cached, "cache_trace", session_meta
    if allow_reconstruct:
        built = build_system_prompt(
            tool_names=session_meta.get("tool_names", []),
            cwd=session_meta.get("cwd", ""),
            model=session_meta.get("model", ""),
            thinking_level=session_meta.get("thinking_level", "off"),
            timestamp=session_meta.get("timestamp", ""),
        )
        return built, "reconstructed", session_meta
    return None, "", session_meta


# ─── Attachments ───────────────────────────────────────────────────────

def _build_attachments(session_file_path: str | None) -> list[Attachment]:
    """Pack the raw OpenClaw session jsonl into session_bundle attachments.

    Files exceeding 40MB are skipped to protect the 50MB bundle cap;
    prompt_hint can advertise the omission in a future iteration.
    """
    if not session_file_path or not os.path.isfile(session_file_path):
        return []
    try:
        size = os.path.getsize(session_file_path)
    except OSError:
        return []
    if size > _RAW_SESSION_MAX_BYTES:
        return []
    with open(session_file_path, "rb") as f:
        content = f.read()
    return [
        Attachment(
            zip_path="raw_session.jsonl",
            content=content,
            is_core=True,
        )
    ]


def _read_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
