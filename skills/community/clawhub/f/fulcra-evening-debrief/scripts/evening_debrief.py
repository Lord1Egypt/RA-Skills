#!/usr/bin/env python3
"""Evening Debrief: end-of-day reflection stored in Fulcra.

  context
      Gather what the agent needs to lead the debrief:
        - today's calendar events (count + titles)
        - tomorrow's calendar events (count + first start)
        - this morning's subjective check-in (energy/mood) if one exists
      All best-effort; any missing piece comes back as available:false.

  save --payload <file.json> [--dry-run]
      Write one "Evening Debrief" moment annotation with the reflection + extracted
      action items + tomorrow preview, and verify it.

Payload schema (save):
{
  "date": "2026-05-29",
  "day_rating": 7,
  "meeting_count": 6,
  "meeting_cadence_feedback": "too many|about right|too few",
  "preferred_meeting_cap": 4,
  "energy_trajectory": "started at 7, dipped to 4 by 3pm",
  "improvement_note": "fewer back-to-back calls in the afternoon",
  "action_items": [{"action": "Send Alex the deck", "deadline": "tomorrow", "context": "..."}],
  "tomorrow_meeting_count": 4,
  "open_loops": ["Alex birthday planning"],
  "wins": ["shipped the proposal"]
}

Auth: Fulcra via fulcra-api CLI / FULCRA_ACCESS_TOKEN. No tokens printed.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import concierge_bootstrap  # noqa: F401

import concierge_fulcra as cf  # noqa: E402
import fulcra_read  # noqa: E402

ANNOTATION_NAME = "Evening Debrief"
ANNOTATION_DESC = "End-of-day debrief captured by the concierge evening-debrief skill."
ANNOTATION_TAGS = ["evening-debrief", "concierge"]
SOURCE = "com.fulcra.evening-debrief"

KEEP = ("date", "day_rating", "meeting_count", "meeting_cadence_feedback",
        "preferred_meeting_cap", "energy_trajectory", "improvement_note",
        "action_items", "tomorrow_meeting_count", "open_loops", "wins")


def fulcra_cli(args: list[str]) -> tuple[int, str]:
    base = os.environ.get("FULCRA_CLI_COMMAND", "uv tool run fulcra-api")
    try:
        proc = subprocess.run([*shlex.split(base), *args], capture_output=True, text=True, timeout=90)
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        return 1, f"{type(exc).__name__}: {exc}"
    return proc.returncode, proc.stdout if proc.returncode == 0 else proc.stdout + proc.stderr


def parse_records(raw: str) -> list:
    raw = raw.strip()
    if not raw:
        return []
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("data") or data.get("events") or [data]
    except json.JSONDecodeError:
        rows = []
        for line in raw.splitlines():
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return rows
    return []


def _events_in(day_start: datetime, day_end: datetime) -> dict:
    rc, body = fulcra_cli(["calendar-events", day_start.isoformat(), day_end.isoformat()])
    if rc != 0:
        return {"available": False, "reason": body[:200]}
    events = parse_records(body)
    titles = [e.get("title") or e.get("summary") or "Untitled" for e in events]
    starts = [e.get("start_date") or e.get("start_time") or e.get("start") for e in events]
    return {"available": True, "count": len(events), "titles": titles[:25],
            "first_start": min([s for s in starts if s], default=None)}


def cmd_context(args: argparse.Namespace) -> dict:
    now = datetime.now(timezone.utc)
    today0 = now.replace(hour=0, minute=0, second=0, microsecond=0)
    out: dict = {"ok": True, "as_of": now.isoformat()}
    out["today"] = _events_in(today0, today0 + timedelta(days=1))
    out["tomorrow"] = _events_in(today0 + timedelta(days=1), today0 + timedelta(days=2))

    # This morning's subjective check-in, if present (read back the most recent within 1 day).
    try:
        checkins = fulcra_read.read_annotation_events("Morning Check-In", days=1)
        out["morning_checkin"] = ({"available": True, **(checkins[-1]["data"] or {})}
                                  if checkins and isinstance(checkins[-1].get("data"), dict)
                                  else {"available": bool(checkins)})
    except Exception as exc:  # never let a read failure block the debrief
        out["morning_checkin"] = {"available": False, "reason": str(exc)[:200]}
    return out


def cmd_save(args: argparse.Namespace) -> dict:
    payload = json.loads(Path(args.payload).read_text(encoding="utf-8-sig"))
    recorded_at = payload.get("timestamp") or datetime.now(timezone.utc).isoformat()
    record = {k: payload.get(k) for k in KEEP if payload.get(k) is not None}
    res = cf.record_moment(
        name=ANNOTATION_NAME, description=ANNOTATION_DESC, tags=ANNOTATION_TAGS,
        payload=record, source=SOURCE, recorded_at=recorded_at, dry_run=args.dry_run,
    )
    return {"ok": res.get("ok", False), "date": record.get("date"), "fulcra": res,
            "payload_preview": record if args.dry_run else None}


def main() -> int:
    p = argparse.ArgumentParser(description="Evening Debrief")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("context")
    sv = sub.add_parser("save")
    sv.add_argument("--payload", required=True)
    sv.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    if args.command == "context":
        result = cmd_context(args)
    elif args.command == "save":
        result = cmd_save(args)
    else:
        result = {"ok": False, "error": "unknown command"}
    print(json.dumps(result, indent=2, sort_keys=True, default=str))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
