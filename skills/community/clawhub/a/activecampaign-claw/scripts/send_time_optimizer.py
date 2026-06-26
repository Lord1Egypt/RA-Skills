#!/usr/bin/env python3
"""
send_time_optimizer.py — Best send window from open-event timestamps.

Aggregates messageActivity events by hour and day-of-week. Falls back to
state.json baseline windows when AC's per-event API returns no data.

Usage:
  python3 send_time_optimizer.py
  python3 send_time_optimizer.py --max-events 20000 --format json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from _ac_client import ACClient, load_state

DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _parse_iso(s):
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def fetch(client: ACClient, max_events: int) -> list:
    return client.fetch_engagement_events(max_items=max_events)


def analyze(activities: list) -> dict:
    by_hour = Counter()
    by_dow = Counter()
    eng_count = 0
    for a in activities:
        if a.get("event") not in ("open", "click"):
            continue
        ts = _parse_iso(a.get("tstamp"))
        if not ts:
            continue
        eng_count += 1
        by_hour[ts.hour] += 1
        by_dow[DOW[ts.weekday()]] += 1
    return {
        "events_analyzed": len(activities),
        "open_events": eng_count,
        "best_hours_utc": [h for h, _ in by_hour.most_common(3)],
        "best_dow": [d for d, _ in by_dow.most_common(3)],
        "by_hour": dict(by_hour),
        "by_dow": dict(by_dow),
    }


def render_markdown(r: dict, baseline: dict) -> str:
    lines = ["# Send Time Optimizer", ""]
    if r["open_events"] == 0:
        lines.append("_No open events available from AC for this account. Falling back to calibration baseline:_")
        lines.append(f"- Best send hours (UTC): {baseline.get('best_send_window_utc', [])}")
        lines.append(f"- Best send days: {baseline.get('best_send_dow', [])}")
        return "\n".join(lines)
    lines.append(f"Open events analyzed: {r['open_events']}")
    lines.append("")
    lines.append(f"**Best hours (UTC):** {', '.join(str(h) for h in r['best_hours_utc'])}")
    lines.append(f"**Best days:** {', '.join(r['best_dow'])}")
    lines.append("")
    lines.append("## Distribution by hour (UTC)")
    for h in sorted(r["by_hour"].keys()):
        lines.append(f"- {h:02d}:00 — {r['by_hour'][h]}")
    lines.append("")
    lines.append("## Distribution by day of week")
    for d in DOW:
        lines.append(f"- {d}: {r['by_dow'].get(d, 0)}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Best send time analysis")
    parser.add_argument("--max-events", type=int, default=20000)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    activities = fetch(client, args.max_events)
    r = analyze(activities)
    state = load_state() or {}
    baseline = state.get("baselines", {})
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r, baseline)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
