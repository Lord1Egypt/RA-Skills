#!/usr/bin/env python3
"""Process ambient-awareness wake requests without invoking an LLM."""

from __future__ import annotations
import argparse, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def parse_ts(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)

def load_new(log: Path, marker_path: Path) -> tuple[list[dict[str, Any]], int]:
    marker = None
    if marker_path.exists() and marker_path.read_text(encoding="utf-8").strip():
        marker = parse_ts(marker_path.read_text(encoding="utf-8").strip())
    entries, malformed = [], 0
    if not log.exists():
        return entries, malformed
    for line in log.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
            timestamp = parse_ts(str(item["timestamp"]))
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            malformed += 1
            continue
        if marker is None or timestamp > marker:
            entries.append(item)
    return entries, malformed

def notify(item: dict[str, Any]) -> bool:
    event = item.get("event") or {}
    kind = str(event.get("event_type", ""))
    decision = str(item.get("decision", event.get("attention_decision", "")))
    if kind == "clock_tick":
        return False
    if kind == "sensor_error" or decision == "wake_now":
        return True
    return decision == "queue" and kind != "file_modified"

def describe(item: dict[str, Any]) -> str:
    event = item.get("event") or {}
    kind = str(event.get("event_type", "event")).replace("_", " ")
    summary = str(event.get("summary") or item.get("reason") or kind)
    return f"• {kind}: {summary}"

def checkpoint(path: Path, now: datetime) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(now.strftime("%Y-%m-%dT%H:%M:%SZ") + "\n", encoding="utf-8")
    tmp.replace(path)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--channel", default="telegram")
    parser.add_argument("--target", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    started = datetime.now(timezone.utc)
    marker = args.state_dir / "last_cron_check.txt"
    try:
        entries, malformed = load_new(args.state_dir / "wake_requests.jsonl", marker)
    except (OSError, ValueError) as exc:
        print(f"ambient-awareness check failed: {exc}", file=sys.stderr)
        return 1
    lines = [describe(item) for item in entries if notify(item)]
    if malformed:
        lines.append(f"• sensor error: skipped {malformed} malformed wake-log line(s)")
    if not lines:
        if not args.dry_run:
            checkpoint(marker, started)
        print("NO_REPLY")
        return 0
    message = "Ambient awareness detected:\n" + "\n".join(lines[:20])
    if len(lines) > 20:
        message += f"\n• …and {len(lines) - 20} more event(s)"
    if args.dry_run:
        print(message)
        return 0
    result = subprocess.run(
        ["openclaw", "message", "send", "--channel", args.channel,
         "--target", args.target, "--message", message],
        check=False,
    )
    if result.returncode == 0:
        checkpoint(marker, started)
    return result.returncode

if __name__ == "__main__":
    raise SystemExit(main())
