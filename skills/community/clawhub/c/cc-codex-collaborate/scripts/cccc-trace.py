#!/usr/bin/env python3
"""CCCC Trace — show recent state machine events from logs, reviews, and docs."""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", subprocess.getoutput("git rev-parse --show-toplevel 2>/dev/null || pwd")).strip())
WORKSPACE = ROOT / "docs/cccc"


def read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def lang() -> str:
    cfg = read_json(WORKSPACE / "config.json")
    if cfg:
        return cfg.get("language", {}).get("user_language", "zh")
    return "zh"


Event = tuple[str, str, str]  # (timestamp, event_type, detail)


def parse_stop_logs() -> list[Event]:
    events = []
    log_dir = WORKSPACE / "logs"
    if not log_dir.exists():
        return events

    for f in sorted(log_dir.glob("stop-*.json")):
        data = read_json(f)
        if not data:
            continue
        # Extract timestamp from filename
        ts_match = f.name.split("-")[1]  # stop-20260515T015640Z.json -> 20260515T015640Z
        try:
            ts = datetime.strptime(ts_match, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d %H:%M UTC")
        except Exception:
            ts = ts_match

        hook_active = data.get("stop_hook_active", "unknown")
        status = data.get("status", "")
        milestone = data.get("current_milestone_id", "")
        last_msg = data.get("last_assistant_message", "")
        event_name = data.get("hook_event_name", "Stop")

        # Determine what happened
        if isinstance(hook_active, bool) and not hook_active and len(data) <= 2:
            detail = "stop_hook_active=false (minimal payload)"
        elif last_msg:
            msg_preview = last_msg[:80].replace("\n", " ")
            detail = f"last_msg: {msg_preview}..."
        else:
            detail = f"hook_active={hook_active}"

        if milestone:
            detail = f"milestone={milestone} | {detail}"

        events.append((ts, f"stop-hook ({event_name})", detail))

    # Stop-failure logs
    for f in sorted(log_dir.glob("stop-failure-*.json")):
        data = read_json(f)
        if not data:
            continue
        ts_match = f.name.split("failure-")[1] if "failure-" in f.name else ""
        try:
            ts = datetime.strptime(ts_match.replace(".json", ""), "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%d %H:%M UTC")
        except Exception:
            ts = ts_match.replace(".json", "")
        detail = json.dumps(data, ensure_ascii=False)[:120]
        events.append((ts, "stop-failure", detail))

    return events


def parse_reviews() -> list[Event]:
    events = []
    for subdir in ("plan", "milestones", "final"):
        review_dir = WORKSPACE / "reviews" / subdir
        if not review_dir.exists():
            continue
        for f in sorted(review_dir.glob("*.json")):
            data = read_json(f)
            if not data:
                continue
            ts = data.get("timestamp", data.get("review_time", ""))
            if ts:
                try:
                    ts = datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M UTC")
                except Exception:
                    pass
            status = data.get("status", data.get("verdict", "unknown"))
            mid = data.get("milestone_id", "")
            detail = f"status={status}"
            if mid:
                detail = f"milestone={mid} | {detail}"
            events.append((ts, f"review ({subdir})", detail))
    return events


def parse_decision_log() -> list[Event]:
    events = []
    path = WORKSPACE / "decision-log.md"
    if not path.exists():
        return events
    text = path.read_text(encoding="utf-8")
    import re
    for m in re.finditer(r'(?:^|\n)##\s*(.*?)(?:\n|$)(.*?)(?=\n##|\Z)', text, re.DOTALL):
        title = m.group(1).strip()
        content = m.group(2).strip()[:100].replace("\n", " ")
        events.append(("", f"decision: {title}", content))
    return events


def parse_state_history() -> list[Event]:
    events = []
    st = read_json(WORKSPACE / "state.json")
    if not st:
        return events

    if st.get("created_at"):
        events.append((st["created_at"], "state created", ""))
    if st.get("last_state_rehydrated_at"):
        sources = st.get("last_state_rehydrate_sources", [])
        events.append((st["last_state_rehydrated_at"], "state rehydrated", f"sources: {sources}"))
    if st.get("last_resumed_at"):
        strategy = st.get("resume_strategy", "")
        events.append((st["last_resumed_at"], "resumed", f"strategy={strategy}"))
    if st.get("last_human_decision"):
        events.append(("", "human decision", st["last_human_decision"]))
    if st.get("last_context_update"):
        events.append((st["last_context_update"], "context updated", ""))
    if st.get("last_migration_at"):
        fr = st.get("last_migration_from_version", "?")
        to = st.get("last_migration_to_version", "?")
        events.append((st["last_migration_at"], "migration", f"{fr} → {to}"))

    return events


def main():
    print("CCCC Trace — 最近状态机事件")
    print()

    all_events: list[Event] = []
    all_events.extend(parse_state_history())
    all_events.extend(parse_stop_logs())
    all_events.extend(parse_reviews())
    all_events.extend(parse_decision_log())

    # Sort by timestamp (empty timestamps go first)
    all_events.sort(key=lambda e: (e[0] == "", e[0]))

    # Show last 20
    shown = all_events[-20:] if len(all_events) > 20 else all_events
    if len(all_events) > 20:
        print(f"(共 {len(all_events)} 个事件，显示最近 20 个)")
        print()

    for ts, event_type, detail in shown:
        ts_display = f"[{ts}]" if ts else "[unknown time]"
        print(f"  {ts_display} {event_type}")
        if detail:
            print(f"    {detail[:200]}")
        print()

    if not all_events:
        print("  没有找到事件记录。")

    return 0


if __name__ == "__main__":
    sys.exit(main())
