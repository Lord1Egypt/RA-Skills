#!/usr/bin/env python3
"""Purge expired masked case reports from the private runtime directory."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path


def runtime_dir() -> Path:
    state_override = os.environ.get("OPENCLAW_STATE_DIR")
    root = Path(state_override).expanduser() if state_override else Path.home() / ".openclaw"
    return root / "ecommerce-gmail-customer-service"


def read_retention_days() -> int:
    try:
        config = json.loads((runtime_dir() / "config.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to read runtime configuration: {exc}") from exc
    days = config.get("retention", {}).get("case_report_days")
    if not isinstance(days, int) or days < 0:
        raise SystemExit("retention.case_report_days must be a non-negative integer")
    return days


def purge_case_reports(_: argparse.Namespace) -> None:
    retention_days = read_retention_days()
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    directory = runtime_dir() / "case-reports"
    deleted = 0
    if directory.is_dir():
        for candidate in directory.iterdir():
            if not candidate.is_file() or candidate.suffix not in {".json", ".jsonl"}:
                continue
            try:
                modified_at = datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc)
                if modified_at < cutoff:
                    candidate.unlink()
                    deleted += 1
            except OSError:
                continue
    print(json.dumps({"deleted": deleted, "retention_days": retention_days}))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Purge expired masked case reports from the private runtime directory"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    purge_parser = subparsers.add_parser("purge")
    purge_parser.set_defaults(func=purge_case_reports)
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
