#!/usr/bin/env python3
"""
Decide whether a timed status update is due for a task.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
CONFIG_PATH = ROOT / "config" / "defaults.json"


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def parse_ts(raw: str | None):
    if not raw:
        return None
    return datetime.fromisoformat(raw.replace('Z', '+00:00'))


def load_events(task_id: str) -> list[dict]:
    path = STATE_DIR / f"{task_id}.events.jsonl"
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    return rows


def latest_immediate_report_ts(task_id: str):
    latest = None
    for event in load_events(task_id):
        if event.get("type") != "status_reported":
            continue
        details = event.get("details", {}) or {}
        msg = details.get("message", "")
        if not isinstance(msg, str) or not msg.startswith("status sent (immediate"):
            continue
        ts = parse_ts(event.get("ts"))
        if ts is not None and (latest is None or ts > latest):
            latest = ts
    return latest


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('task_id')
    args = p.parse_args()

    defaults = load_json(CONFIG_PATH, {})
    task = load_json(STATE_DIR / f"{args.task_id}.json", None)
    if not task:
        raise SystemExit(f"task not found: {args.task_id}")

    reporting = defaults.get('reporting', {})
    interval = int(task.get('status_update_interval_seconds') or reporting.get('status_update_interval_seconds', 300))
    cooldown = int(reporting.get('timed_status_cooldown_after_immediate_seconds', 15) or 0)
    last = parse_ts(task.get('last_status_update_at'))
    now = datetime.now(timezone.utc)
    latest_immediate = latest_immediate_report_ts(args.task_id)
    if latest_immediate is not None and cooldown > 0:
        since_immediate = (now - latest_immediate).total_seconds()
        if since_immediate < cooldown:
            print(json.dumps({
                "due": False,
                "reason": "cooldown_after_immediate",
                "elapsed_seconds": round(since_immediate),
                "interval_seconds": interval,
                "cooldown_seconds": cooldown
            }))
            return 0
    if last is None:
        print(json.dumps({"due": True, "reason": "never_reported", "interval_seconds": interval, "cooldown_seconds": cooldown}))
        return 0
    elapsed = (now - last).total_seconds()
    print(json.dumps({
        "due": elapsed >= interval,
        "reason": "interval_elapsed" if elapsed >= interval else "not_due",
        "elapsed_seconds": round(elapsed),
        "interval_seconds": interval,
        "cooldown_seconds": cooldown
    }))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
