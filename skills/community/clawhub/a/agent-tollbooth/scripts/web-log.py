#!/usr/bin/env python3
"""Shared event logger for web access/fetch scripts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ALLOWED_EVENT_TYPES = {
    "429",
    "timeout",
    "auth_failure",
    "cache_hit",
    "success",
    "workaround",
}


SCRIPT_DIR = Path(__file__).resolve().parent
MODULE_DIR = SCRIPT_DIR.parent

# Write operational data outside the skill bundle.
# Resolves to $OPENCLAW_WORKSPACE/data/agent-tollbooth/ on any standard OpenClaw install.
# Falls back to a local data/ dir if the workspace is not found.
import os
_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace"))
DATA_DIR = _WORKSPACE / "data" / "agent-tollbooth"
LOG_PATH = DATA_DIR / "web-access-log.json"
PROFILES_PATH = DATA_DIR / "profiles-annotations.md"


def _ensure_log_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists():
        LOG_PATH.write_text("[]\n", encoding="utf-8")


def _format_timestamp_for_profile(timestamp: str) -> str:
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return timestamp
    return parsed.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def annotate_profile(service: str, event_type: str, detail: str, timestamp: str) -> None:
    if not PROFILES_PATH.exists():
        return

    lines = PROFILES_PATH.read_text(encoding="utf-8").splitlines()
    if not lines:
        return

    target_heading = f"## {service}".strip().lower()
    section_start = None
    for idx, line in enumerate(lines):
        if line.strip().lower() == target_heading:
            section_start = idx
            break
    if section_start is None:
        return

    section_end = len(lines)
    for idx in range(section_start + 1, len(lines)):
        if lines[idx].startswith("## "):
            section_end = idx
            break

    formatted_ts = _format_timestamp_for_profile(timestamp)
    line_prefix = f"- [{formatted_ts}] {event_type}:"
    for existing in lines[section_start:section_end]:
        if existing.startswith(line_prefix):
            return

    annotation = f"- [{formatted_ts}] {event_type}: {detail}"
    lines.insert(section_end, annotation)
    PROFILES_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def log_event(
    service: str,
    event_type: str,
    detail: str,
    worked: Optional[str] = None,
) -> None:
    """Append a web access event to data/web-access-log.json."""
    if event_type not in ALLOWED_EVENT_TYPES:
        raise ValueError(f"Unsupported event_type: {event_type}")

    _ensure_log_file()
    try:
        events = json.loads(LOG_PATH.read_text(encoding="utf-8") or "[]")
    except json.JSONDecodeError:
        events = []

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": str(service),
        "event_type": event_type,
        "detail": str(detail),
        "worked": None if worked is None else str(worked),
    }
    events.append(entry)
    LOG_PATH.write_text(json.dumps(events, indent=2) + "\n", encoding="utf-8")
    annotate_profile(
        service=entry["service"],
        event_type=entry["event_type"],
        detail=entry["detail"],
        timestamp=entry["timestamp"],
    )

def _cli() -> int:
    parser = argparse.ArgumentParser(description="Append an entry to web-access-log.json")
    parser.add_argument("service")
    parser.add_argument("event_type", choices=sorted(ALLOWED_EVENT_TYPES))
    parser.add_argument("detail")
    parser.add_argument("--worked", default=None)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    log_event(service=args.service, event_type=args.event_type, detail=args.detail, worked=args.worked)
    if args.verbose:
        _ensure_log_file()
        events = json.loads(LOG_PATH.read_text(encoding="utf-8") or "[]")
        if events:
            print(json.dumps(events[-1], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
