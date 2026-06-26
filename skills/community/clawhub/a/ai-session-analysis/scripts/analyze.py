#!/usr/bin/env python3
"""AI Session Analysis — data extraction only. No interpretation."""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from shared import strip_home_prefix  # noqa: E402

HOME = Path.home()

def fmt_ts_ms(ms):
    try: return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
    except Exception: return "?"

def fmt_ts_iso(s):
    try: return s[:10]
    except Exception: return "?"

# ── Claude Code ──────────────────────────────────────────────

def analyze_claude():
    print("=" * 60)
    print("CLAUDE CODE")
    print("=" * 60)

    projects_dir = HOME / ".claude" / "projects"
    jsonl_files = list(projects_dir.rglob("*.jsonl")) if projects_dir.exists() else []
    total_size = sum(f.stat().st_size for f in jsonl_files)
    print(f"\nTranscript files: {len(jsonl_files)} ({total_size//1024//1024}MB)")

    message_types = Counter()
    tool_counts = Counter()
    sessions = set()
    daily = Counter()
    projects = Counter()
    session_first_seen = {}
    session_last_seen = {}
    parse_errors = 0

    for jf in jsonl_files:
        sid = jf.stem
        sessions.add(sid)
        proj_name = strip_home_prefix(str(jf.relative_to(projects_dir).parts[0]))
        try:
            for line in jf.read_text().strip().splitlines():
                if not line.strip(): continue
                d = json.loads(line)
                typ = d.get("type", "?")
                message_types[typ] += 1
                ts_raw = d.get("timestamp", "")
                if not ts_raw: continue
                try:
                    dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
                    ts = dt.astimezone().strftime("%Y-%m-%d")
                except Exception:
                    continue

                # Track session time range
                if sid not in session_first_seen:
                    session_first_seen[sid] = ts
                session_last_seen[sid] = ts

                if typ == "assistant":
                    content = d.get("message", {}).get("content", [])
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "tool_use":
                                tn = block.get("name", "?")
                                tool_counts[tn] += 1
                                projects[proj_name] += 1
                                daily[ts] += 1
        except Exception:
            parse_errors += 1

    print(f"Sessions: {len(sessions)}")
    print(f"Messages: {sum(message_types.values()):,}")
    print(f"Message types: {dict(message_types)}")

    total_tools = sum(tool_counts.values())
    print(f"\n── Tools ({total_tools:,} calls, {len(tool_counts)} types) ──")
    for tn, cnt in tool_counts.most_common(15):
        pct = cnt / total_tools * 100 if total_tools > 0 else 0
        bar = "█" * max(1, cnt // 80)
        print(f"  {tn:<25} {cnt:>6} ({pct:>4.1f}%) {bar}")

    print(f"\n── Projects ranked by tool calls ──")
    for proj, cnt in projects.most_common(12):
        print(f"  {proj:<55} {cnt:>6}")

    print(f"\n── Daily tool calls (all time) ──")
    for date in sorted(daily.keys()):
        print(f"  {date}: {daily[date]:>5} {'█' * max(1, daily[date] // 50)}")

    # Summarize date range
    if session_first_seen:
        all_dates = sorted(set(list(session_first_seen.values()) + list(session_last_seen.values())))
        print(f"\nDate range: {all_dates[0]} → {all_dates[-1]}")
    if parse_errors:
        print(f"\nParse errors: {parse_errors}")

    return {
        "sessions": len(sessions),
        "tools": total_tools,
        "tool_names": tool_counts,
        "messages": sum(message_types.values()),
        "daily": daily,
        "projects": projects,
    }

# ── Codex ────────────────────────────────────────────────────

def analyze_codex():
    print("\n" + "=" * 60)
    print("CODEX (OpenAI)")
    print("=" * 60)

    sessions_dir = HOME / ".codex" / "sessions"
    jsonl_files = list(sessions_dir.rglob("*.jsonl")) if sessions_dir.exists() else []
    print(f"\nSession files: {len(jsonl_files)}")

    event_counts = Counter()
    exit_codes = Counter()
    session_count = 0
    daily = Counter()
    date_range = []
    parse_errors = 0

    for sf in jsonl_files:
        try:
            for line in sf.read_text().strip().splitlines():
                if not line.strip(): continue
                d = json.loads(line)
                if d.get("type") == "session_meta":
                    session_count += 1
                    ts = d.get("payload", {}).get("timestamp", "")
                    date = fmt_ts_iso(ts)
                    if date: daily[date] += 1; date_range.append(date)
                elif d.get("type") == "event_msg":
                    et = d.get("payload", {}).get("type", "?")
                    event_counts[et] += 1
                    if et == "exec_command_end":
                        exit_codes[str(d["payload"].get("exit_code", "?"))] += 1
        except Exception:
            parse_errors += 1

    print(f"Sessions: {session_count}")
    print(f"\n── Events ({sum(event_counts.values()):,}) ──")
    for et, cnt in event_counts.most_common(12):
        bar = "█" * max(1, cnt // 30)
        print(f"  {et:<25} {cnt:>5} {bar}")

    print(f"\n── Shell exit codes ──")
    for ec, cnt in exit_codes.most_common():
        print(f"  exit {ec}: {cnt:>5}")

    if daily:
        print(f"\n── Sessions per day ──")
        for date in sorted(daily.keys()):
            print(f"  {date}: {daily[date]} session(s)")

    if date_range:
        date_range.sort()
        print(f"\nDate range: {date_range[0]} → {date_range[-1]}")
    if parse_errors:
        print(f"\nParse errors: {parse_errors}")

    return {"sessions": session_count, "events": sum(event_counts.values())}

# ── Kimi Code ────────────────────────────────────────────────

def analyze_kimi():
    print("\n" + "=" * 60)
    print("KIMI CODE")
    print("=" * 60)

    sessions_dir = HOME / ".kimi" / "sessions"
    wire_files = list(sessions_dir.rglob("wire.jsonl")) if sessions_dir.exists() else []
    print(f"\nWire protocol files: {len(wire_files)}")

    tool_counts = Counter()
    session_count = 0
    all_tool_names = set()
    parse_errors = 0

    for wf in wire_files:
        has_tools = False
        try:
            for line in wf.read_text().strip().splitlines():
                if not line.strip(): continue
                d = json.loads(line)
                msg = d.get("message", {})
                if isinstance(msg, dict) and msg.get("type") == "ToolCall":
                    func = msg.get("payload", {}).get("function", msg.get("function", {}))
                    tn = func.get("name", "?")
                    tool_counts[tn] += 1
                    all_tool_names.add(tn)
                    has_tools = True
        except Exception:
            parse_errors += 1
        if has_tools:
            session_count += 1

    print(f"Sessions with tool calls: {session_count}")
    total = sum(tool_counts.values())
    print(f"\n── Tools ({total:,} calls, {len(tool_counts)} types) ──")
    for tn, cnt in tool_counts.most_common(15):
        pct = cnt / total * 100 if total > 0 else 0
        bar = "█" * max(1, cnt // 30)
        print(f"  {tn:<35} {cnt:>6} ({pct:>4.1f}%) {bar}")

    # List all tool names (for domain-specific discovery)
    print(f"\n── All tool names ({len(all_tool_names)}) ──")
    for tn in sorted(all_tool_names):
        print(f"  {tn}")
    if parse_errors:
        print(f"\nParse errors: {parse_errors}")

    return {"sessions": session_count, "tools": total, "tool_names": tool_counts}

# ── Cross-tool ───────────────────────────────────────────────

def cross_analysis(cc, cx, kc):
    print("\n" + "=" * 60)
    print("CROSS-TOOL COMPARISON")
    print("=" * 60)
    print(f"""
  ┌──────────────────────────┬───────────┬───────────┬───────────┐
  │ Metric                   │ Claude    │ Codex     │ Kimi      │
  ├──────────────────────────┼───────────┼───────────┼───────────┤
  │ Sessions                 │ {cc.get('sessions',0):>9} │ {cx.get('sessions',0):>9} │ {kc.get('sessions',0):>9} │
  │ Messages / Events        │ {cc.get('messages',0):>9} │ {cx.get('events',0):>9} │     —     │
  │ Tool calls               │ {cc.get('tools',0):>9} │     —     │ {kc.get('tools',0):>9} │
  │ Unique tool types        │ {len(cc.get('tool_names',{})):>9} │     —     │ {len(kc.get('tool_names',{})):>9} │
  └──────────────────────────┴───────────┴───────────┴───────────┘
""")
    print("Claude Code top tools:")
    for tn, cnt in cc.get("tool_names", {}).most_common(8):
        print(f"  {tn:<25} {cnt:>6}")
    print("\nKimi Code top tools:")
    for tn, cnt in kc.get("tool_names", {}).most_common(8):
        print(f"  {tn:<25} {cnt:>6}")

# ── Recent Activity (data only) ──────────────────────────────

def recent_activity(days=7):
    print("\n" + "=" * 60)
    print(f"RECENT ACTIVITY — Last {days} Days (Claude Code)")
    print("=" * 60)

    projects_dir = HOME / ".claude" / "projects"
    jsonl_files = list(projects_dir.rglob("*.jsonl"))

    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=days)

    recent_tools = Counter()
    recent_projects = Counter()
    recent_daily = Counter()
    recent_sessions = set()
    recent_session_dates = defaultdict(list)  # session -> [dates]
    parse_errors = 0

    for jf in jsonl_files:
        proj = strip_home_prefix(str(jf.relative_to(projects_dir).parts[0]))
        session_recent = False
        try:
            for line in jf.read_text().strip().splitlines():
                if not line.strip(): continue
                d = json.loads(line)
                ts = d.get("timestamp", "")
                if not ts: continue
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except Exception:
                    continue
                if dt < week_ago: continue
                session_recent = True
                date_key = dt.astimezone().strftime("%Y-%m-%d")
                recent_session_dates[jf.stem].append(date_key)

                if d.get("type") == "assistant":
                    content = d.get("message", {}).get("content", [])
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "tool_use":
                                tn = block.get("name", "?")
                                recent_tools[tn] += 1
                                recent_projects[proj] += 1
                                recent_daily[date_key] += 1
        except Exception:
            parse_errors += 1
        if session_recent:
            recent_sessions.add(jf.stem)

    if not recent_tools:
        print("\n  No activity in the last 7 days.")
        return

    total = sum(recent_tools.values())

    print(f"\nSessions: {len(recent_sessions)}")
    print(f"Tool calls: {total:,}")
    print(f"Active projects: {len(recent_projects)}")
    active_days = len(recent_daily)
    print(f"Active days: {active_days}/{days}")

    print(f"\n── Daily tool calls ──")
    for date in sorted(recent_daily.keys()):
        cnt = recent_daily[date]
        print(f"  {date}: {cnt:>5} {'█' * max(1, cnt // 30)}")

    print(f"\n── Projects ──")
    for proj, cnt in recent_projects.most_common(10):
        pct = cnt / total * 100 if total > 0 else 0
        print(f"  {proj:<55} {cnt:>6} ({pct:>4.1f}%)")

    print(f"\n── Tool mix ──")
    for tn, cnt in recent_tools.most_common(12):
        pct = cnt / total * 100 if total > 0 else 0
        print(f"  {tn:<25} {cnt:>6} ({pct:>4.1f}%)")

    # Session-level detail: for each recent session, show project + date range + tool count
    print(f"\n── Recent sessions ──")
    for sid in sorted(recent_sessions):
        dates = recent_session_dates.get(sid, [])
        date_range = f"{min(dates)}" if len(set(dates)) == 1 else f"{min(dates)}→{max(dates)}" if dates else "?"
        # Find project for this session
        sid_files = [jf for jf in jsonl_files if jf.stem == sid]
        proj = "?"
        if sid_files:
            proj = strip_home_prefix(str(sid_files[0].relative_to(projects_dir).parts[0]))
        print(f"  {date_range}  {proj[:55]}")

    if parse_errors:
        print(f"\nParse errors: {parse_errors}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze AI coding session data")
    parser.add_argument("--days", type=int, default=7,
                        help="Recent activity window in days (default: 7)")
    args = parser.parse_args()

    cc = analyze_claude()
    cx = analyze_codex()
    kc = analyze_kimi()
    cross_analysis(cc, cx, kc)
    recent_activity(days=args.days)
    print("\nDone.")
