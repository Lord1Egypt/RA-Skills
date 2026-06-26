#!/usr/bin/env python3
"""Discover candidate sources for the mbti skill."""

from __future__ import annotations

import argparse
from pathlib import Path

from mbti_common import (
    DEFAULT_EXCLUDED_PATTERNS,
    SOURCE_DEFINITIONS,
    iso_now,
    load_sqlite_rows,
    resolve_path,
    write_json,
)


def session_files(openclaw_home: Path) -> list[Path]:
    if not openclaw_home.exists():
        return []
    results: list[Path] = []
    for path in openclaw_home.glob("agents/*/sessions/*.jsonl"):
        if any(suffix in path.name for suffix in (".bak", ".reset", ".deleted", ".lock")):
            continue
        results.append(path)
    return sorted(results)


def discover(workspace_root: Path, openclaw_home: Path) -> dict:
    candidates = []

    memory_md = workspace_root / "MEMORY.md"
    candidates.append(
        {
            "source_type": "workspace-long-memory",
            "label": SOURCE_DEFINITIONS["workspace-long-memory"]["label"],
            "note": SOURCE_DEFINITIONS["workspace-long-memory"]["note"],
            "path_pattern": str(memory_md),
            "available": memory_md.exists(),
            "item_count": 1 if memory_md.exists() else 0,
            "examples": [str(memory_md)] if memory_md.exists() else [],
        }
    )

    daily_files = sorted((workspace_root / "memory").glob("*.md")) if (workspace_root / "memory").exists() else []
    candidates.append(
        {
            "source_type": "workspace-daily-memory",
            "label": SOURCE_DEFINITIONS["workspace-daily-memory"]["label"],
            "note": SOURCE_DEFINITIONS["workspace-daily-memory"]["note"],
            "path_pattern": str(workspace_root / "memory" / "*.md"),
            "available": bool(daily_files),
            "item_count": len(daily_files),
            "examples": [str(path) for path in daily_files[:3]],
        }
    )

    sessions = session_files(openclaw_home)
    candidates.append(
        {
            "source_type": "openclaw-sessions",
            "label": SOURCE_DEFINITIONS["openclaw-sessions"]["label"],
            "note": SOURCE_DEFINITIONS["openclaw-sessions"]["note"],
            "path_pattern": str(openclaw_home / "agents" / "*" / "sessions" / "*.jsonl"),
            "available": bool(sessions),
            "item_count": len(sessions),
            "examples": [str(path) for path in sessions[:3]],
        }
    )

    main_sqlite = openclaw_home / "memory" / "main.sqlite"
    indexed_rows = load_sqlite_rows(main_sqlite, "select path from files order by path") if main_sqlite.exists() else []
    candidates.append(
        {
            "source_type": "openclaw-memory-index",
            "label": SOURCE_DEFINITIONS["openclaw-memory-index"]["label"],
            "note": SOURCE_DEFINITIONS["openclaw-memory-index"]["note"],
            "path_pattern": str(main_sqlite),
            "available": main_sqlite.exists(),
            "item_count": len(indexed_rows),
            "examples": [row["path"] for row in indexed_rows[:5]],
        }
    )

    task_sqlite = openclaw_home / "tasks" / "runs.sqlite"
    task_rows = load_sqlite_rows(task_sqlite, "select count(*) as count from task_runs") if task_sqlite.exists() else []
    candidates.append(
        {
            "source_type": "openclaw-task-runs",
            "label": SOURCE_DEFINITIONS["openclaw-task-runs"]["label"],
            "note": SOURCE_DEFINITIONS["openclaw-task-runs"]["note"],
            "path_pattern": str(task_sqlite),
            "available": task_sqlite.exists(),
            "item_count": task_rows[0]["count"] if task_rows else 0,
            "examples": [str(task_sqlite)] if task_sqlite.exists() else [],
        }
    )

    cron_files = sorted((openclaw_home / "cron" / "runs").glob("*.jsonl")) if (openclaw_home / "cron" / "runs").exists() else []
    candidates.append(
        {
            "source_type": "openclaw-cron-runs",
            "label": SOURCE_DEFINITIONS["openclaw-cron-runs"]["label"],
            "note": SOURCE_DEFINITIONS["openclaw-cron-runs"]["note"],
            "path_pattern": str(openclaw_home / "cron" / "runs" / "*.jsonl"),
            "available": bool(cron_files),
            "item_count": len(cron_files),
            "examples": [str(path) for path in cron_files[:3]],
        }
    )

    return {
        "generated_at": iso_now(),
        "workspace_root": str(workspace_root),
        "openclaw_home": str(openclaw_home),
        "default_excluded_patterns": DEFAULT_EXCLUDED_PATTERNS,
        "candidates": candidates,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover candidate MBTI data sources.")
    parser.add_argument("--workspace-root", default=".", help="Workspace root to inspect.")
    parser.add_argument("--openclaw-home", default="~/.openclaw", help="OpenClaw state directory.")
    parser.add_argument("--output", required=True, help="Where to write the manifest JSON.")
    args = parser.parse_args()

    manifest = discover(resolve_path(args.workspace_root), resolve_path(args.openclaw_home))
    write_json(resolve_path(args.output), manifest)


if __name__ == "__main__":
    main()
