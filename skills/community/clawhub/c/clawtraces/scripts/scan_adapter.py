#!/usr/bin/env python3
# FILE_META
# INPUT:  --adapter <name> + PipelineOptions-style flags
# OUTPUT: per-session <sid>.trajectory.json / .stats.json / .prompt_hint.json / .session_bundle.zip
# POS:    skill scripts — multi-adapter scan entry (openclaw + hermes + claude-code)
# MISSION: Drive any registered adapter through discover → filter → parse → emit.

"""Scan + convert entry for every registered adapter.

Historical note: during Phase 4 of the adapter migration this file
coexisted with ``scan_and_convert.py`` (OpenClaw-only). Starting with
B2/B3 the OpenClaw path is wired in here too — the legacy script stays
temporarily until B4 switches cli.py over.

Outputs follow the layout the upload pipeline expects:

    <output_dir>/<session_id>.trajectory.json       (OpenAI IR)
    <output_dir>/<session_id>.stats.json            (per-session stats)
    <output_dir>/<session_id>.prompt_hint.json      (system prompt metadata)
    <output_dir>/<session_id>.session_bundle.zip    (raw_session.jsonl + extras)

Submit side (P1-7) discovers these quads and ships them to /upload.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import zipfile
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.adapters import AdapterSpec, ParseResult, SessionHandle, get as get_adapter, names as adapter_names
from lib.core.config_loader import get_adapter_filters, load_config, is_allowed_model
from lib.paths import get_default_output_dir
from lib.pipeline_options import PipelineOptions
from lib.session_index import find_openclaw_sessions_dirs

# Trigger adapter registration side effects. Each ``import`` populates the
# global registry. Keep the list explicit so unused adapters don't pay the
# import cost and don't appear in ``--adapter`` help text unnecessarily.
import lib.adapters.openclaw  # noqa: F401  (registers "openclaw")
import lib.adapters.hermes  # noqa: F401  (registers "hermes")
import lib.adapters.claude_code  # noqa: F401  (registers "claude-code")


DEFAULT_OUTPUT_DIR = get_default_output_dir()


# ─── Filter application (minimal, adapter-agnostic) ────────────────────

def _filter_handle_by_model(handle: SessionHandle, filters: dict) -> str | None:
    whitelist = filters.get("model_whitelist") or []
    if not whitelist:
        return None  # empty = accept any
    if not handle.model:
        return None  # cannot judge without a model; defer to parse-time
    if not is_allowed_model(handle.model, whitelist):
        return f"model {handle.model!r} not in whitelist"
    return None


def _filter_result(result: ParseResult, filters: dict) -> str | None:
    if result.reject_reason:
        return result.reject_reason

    stats = result.stats or {}

    min_turns = filters.get("min_turns", 0) or 0
    if stats.get("turns", 0) < min_turns:
        return f"turns {stats.get('turns', 0)} < min {min_turns}"

    if filters.get("require_tool_use") and not stats.get("tool_use_count"):
        return "no tool_use (require_tool_use=True)"

    if filters.get("require_thinking") and not stats.get("reasoning_asst"):
        return "no reasoning (require_thinking=True)"

    return None


# ─── Emit helpers ──────────────────────────────────────────────────────

def _write_json(path: Path, obj: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def _zip_attachments(attachments: list) -> bytes:
    """Pack Attachment list into a session_bundle.zip byte string.

    Core attachments land at their zip_path; extras attachments land under
    ``extras/<zip_path>`` per docs/adapter-design.md §5.3.
    """
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for a in attachments:
            path = a.zip_path if a.is_core else f"extras/{a.zip_path.lstrip('/')}"
            zf.writestr(path, a.content)
    return buf.getvalue()


def _emit(output_dir: Path, session_id: str, result: ParseResult) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    trajectory_path = output_dir / f"{session_id}.trajectory.json"
    stats_path = output_dir / f"{session_id}.stats.json"
    hint_path = output_dir / f"{session_id}.prompt_hint.json"
    bundle_path = output_dir / f"{session_id}.session_bundle.zip"

    _write_json(trajectory_path, result.trajectory)
    _write_json(stats_path, result.stats)
    _write_json(hint_path, result.prompt_hint)

    bundle_bytes = _zip_attachments(result.attachments)
    bundle_path.write_bytes(bundle_bytes)

    return {
        "session_id": session_id,
        "trajectory_path": str(trajectory_path),
        "stats_path": str(stats_path),
        "prompt_hint_path": str(hint_path),
        "session_bundle_path": str(bundle_path),
        "session_bundle_bytes": len(bundle_bytes),
    }


# ─── Main flow ─────────────────────────────────────────────────────────

def _resolve_adapter(name: str) -> AdapterSpec:
    try:
        return get_adapter(name)
    except KeyError:
        raise SystemExit(
            f"unknown --adapter {name!r}; registered: {adapter_names()}"
        )


def _build_adapter_opts(
    adapter_name: str,
    output_dir: Path,
    *,
    explicit_session_ids: set[str] | None,
    since_ts: float | None,
    cfg: dict,
) -> Any:
    """Build adapter-specific opts object.

    OpenClaw needs a full ``PipelineOptions`` (its pipeline reads
    sessions_dirs / eligibility / explicit_session_ids). Other adapters
    currently self-bootstrap from env / defaults and receive ``None``.
    """
    if adapter_name == "openclaw":
        sessions_dirs = find_openclaw_sessions_dirs()
        if not sessions_dirs:
            raise SystemExit(
                "No OpenClaw sessions directories found. "
                "Install / use OpenClaw first, or point --sessions-dir manually."
            )
        return PipelineOptions.from_config(
            cfg,
            sessions_dirs=sessions_dirs,
            output_dir=str(output_dir),
            explicit_session_ids=list(explicit_session_ids)
                if explicit_session_ids else None,
            since_ts=since_ts,
            include_ineligible=True,  # adapter.parse surfaces ineligible as reject
        )
    return None


def run(
    adapter_name: str,
    output_dir: Path,
    *,
    explicit_session_ids: set[str] | None = None,
    limit: int | None = None,
    since_ts: float | None = None,
) -> dict:
    spec = _resolve_adapter(adapter_name)
    cfg = load_config()
    filters = get_adapter_filters(cfg, adapter_name, spec.default_filters)

    opts = _build_adapter_opts(
        adapter_name, output_dir,
        explicit_session_ids=explicit_session_ids,
        since_ts=since_ts,
        cfg=cfg,
    )

    emitted: list[dict] = []
    filtered: list[dict] = []

    count = 0
    for handle in spec.discover(opts):
        # For adapters that don't consume opts themselves (hermes / claude_code)
        # the caller still narrows by session_id here.
        if (
            opts is None
            and explicit_session_ids
            and handle.session_id not in explicit_session_ids
        ):
            continue

        reason = _filter_handle_by_model(handle, filters)
        if reason is not None:
            filtered.append({"session_id": handle.session_id, "reason": reason})
            continue

        result = spec.parse(handle, opts)
        reason = _filter_result(result, filters)
        if reason is not None:
            filtered.append({"session_id": handle.session_id, "reason": reason})
            continue

        emitted.append(_emit(output_dir, handle.session_id, result))

        count += 1
        if limit is not None and count >= limit:
            break

    return {"adapter": adapter_name, "emitted": emitted, "filtered": filtered}


def _run_list_only(adapter_name: str, output_dir: Path, *,
                   page: int, page_size: int,
                   since_ts: float | None) -> dict:
    """List-only view (no processing). Currently only openclaw is supported.

    Returns the paginated JSON shape SKILL.md step 2.1 expects:
        {items, total, page, page_size, has_more}
    """
    if adapter_name != "openclaw":
        raise SystemExit(
            f"--list-only is only supported for --adapter openclaw "
            f"(got {adapter_name!r})"
        )
    from lib.adapters.openclaw._list_ui import list_qualifying_sessions
    rows = list_qualifying_sessions(
        find_openclaw_sessions_dirs(), str(output_dir), since=since_ts,
    )
    total = len(rows)
    start = (page - 1) * page_size
    return {
        "items": rows[start:start + page_size],
        "total": total,
        "page": page,
        "page_size": page_size,
        "has_more": start + page_size < total,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan + convert sessions for any registered adapter",
    )
    parser.add_argument("--adapter", required=True,
                        help=f"adapter name (registered: {adapter_names() or 'none yet'})")
    parser.add_argument("--output-dir", "-o", default=DEFAULT_OUTPUT_DIR,
                        help="Output directory (default: skill output)")
    parser.add_argument("--sessions", nargs="+", metavar="ID",
                        help="Only process these specific session IDs")
    parser.add_argument("--limit", type=int, metavar="N",
                        help="Only process the first N sessions")
    parser.add_argument("--since", metavar="DATE",
                        help="Only process sessions after DATE (YYYY-MM-DD); "
                             "currently applied by the openclaw adapter only")
    parser.add_argument("--list-only", action="store_true",
                        help="List qualifying sessions without processing "
                             "(openclaw adapter only)")
    parser.add_argument("--page", type=int, default=1,
                        help="Page number for --list-only (default: 1)")
    parser.add_argument("--page-size", type=int, default=10,
                        help="Items per page for --list-only (default: 10)")
    args = parser.parse_args()

    since_ts: float | None = None
    if args.since:
        from datetime import datetime, timezone
        try:
            since_ts = datetime.strptime(args.since, "%Y-%m-%d").replace(
                tzinfo=timezone.utc).timestamp()
        except ValueError:
            raise SystemExit(f"--since must be YYYY-MM-DD, got {args.since!r}")

    if args.list_only:
        result = _run_list_only(
            args.adapter, Path(args.output_dir),
            page=args.page, page_size=args.page_size, since_ts=since_ts,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    explicit_ids = set(args.sessions) if args.sessions else None
    result = run(
        args.adapter,
        Path(args.output_dir),
        explicit_session_ids=explicit_ids,
        limit=args.limit,
        since_ts=since_ts,
    )

    summary = {
        "adapter": result["adapter"],
        "emitted": len(result["emitted"]),
        "filtered": len(result["filtered"]),
        "files": [r["session_id"] for r in result["emitted"]],
        "reject_reasons": result["filtered"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
