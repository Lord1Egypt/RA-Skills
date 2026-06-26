#!/usr/bin/env python3
"""Context Window Reporter for OpenClaw.

Lightweight context usage check. Shows tokens used, percentage remaining,
estimated turns left, and cache hit rate.

Usage:
    python3 context_report.py [--session <session_key>] [--agent <agent_name>]

If no session/agent specified, auto-detects the most recently updated session.
"""

import argparse
import json
import sys
from pathlib import Path

OPENCLAW_DIR = Path.home() / ".openclaw"
AGENTS_DIR = OPENCLAW_DIR / "agents"


def find_current_session(agent: str | None = None) -> tuple[str, dict, str]:
    """Find the most recently updated session.

    Returns (session_key, session_data, agent_name).
    """
    if agent is None:
        agent = "main"

    store_path = AGENTS_DIR / agent / "sessions" / "sessions.json"
    if not store_path.exists():
        for d in AGENTS_DIR.iterdir():
            if d.is_dir():
                p = d / "sessions" / "sessions.json"
                if p.exists():
                    agent = d.name
                    store_path = p
                    break

    if not store_path.exists():
        print("ERROR: No sessions.json found", file=sys.stderr)
        sys.exit(1)

    with open(store_path) as f:
        sessions = json.load(f)

    if not sessions:
        print("ERROR: No sessions found", file=sys.stderr)
        sys.exit(1)

    best_key = max(sessions, key=lambda k: sessions[k].get("updatedAt", ""))
    return best_key, sessions[best_key], agent


def read_usage_entries(transcript_path: str) -> list[dict]:
    """Read all assistant usage entries from the transcript."""
    entries = []
    if not Path(transcript_path).exists():
        return entries

    with open(transcript_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("type") != "message":
                continue
            msg = entry.get("message", {})
            if msg.get("role") != "assistant":
                continue
            usage = msg.get("usage", {})
            if usage and usage.get("totalTokens"):
                entries.append(usage)

    return entries


def fmt(n: int) -> str:
    """Format number with K suffix."""
    if n >= 1000:
        return f"{n / 1000:.1f}K"
    return str(n)


def health_indicator(pct_used: float) -> str:
    """Return a colour indicator based on context usage percentage."""
    if pct_used >= 80:
        return "🔴"
    if pct_used >= 60:
        return "🟡"
    return "🟢"


def make_bar(pct: float, width: int = 20) -> str:
    """Create a unicode progress bar. pct = 0..100 (percentage used)."""
    filled = round(width * pct / 100)
    empty = width - filled
    return f"[{'█' * filled}{'░' * empty}]"


def pct_str(n: int, total: int) -> str:
    """Format as percentage string."""
    return f"{n / total * 100:.0f}%" if total > 0 else "N/A"


def build_compact_report(session: dict) -> str:
    """Build the compact one-line report."""
    transcript_path = session.get("sessionFile", "")
    context_window = session.get("contextTokens") or 0
    usage_entries = read_usage_entries(transcript_path)

    if not usage_entries:
        return "No usage data found in transcript."

    latest = usage_entries[-1]
    current_total = latest.get("totalTokens", 0)

    if context_window <= 0:
        return f"{fmt(current_total)} tokens used (context limit unknown)"

    pct_used = current_total / context_window * 100
    bar = make_bar(pct_used)
    indicator = health_indicator(pct_used)

    parts = [f"{indicator} {bar} Context Usage: {fmt(current_total)} / {fmt(context_window)} ({pct_str(current_total, context_window)})"]

    # Turns estimate
    if len(usage_entries) >= 2:
        window = min(10, len(usage_entries))
        recent = usage_entries[-window:]
        growths = []
        for i in range(1, len(recent)):
            growth = recent[i]["totalTokens"] - recent[i - 1]["totalTokens"]
            if growth > 0:
                growths.append(growth)
        if growths:
            avg_g = sum(growths) / len(growths)
            remaining = context_window - current_total
            if remaining > 0:
                turns = int(remaining / avg_g)
                parts.append(f"~{turns} turns left")

    # Cache hit rate (from latest response — most accurate for real-time)
    cache_read = latest.get("cacheRead", 0)
    cache_total = latest.get("totalTokens", 0)
    if cache_total > 0 and cache_read > 0:
        hit_rate = cache_read / cache_total * 100
        parts.append(f"Cache: {hit_rate:.0f}%")

    return " | ".join(parts)


SPACER = "─" * 20  # visible divider for Slack compatibility


def build_detailed_report(session: dict) -> str:
    """Build the detailed multi-line report."""
    transcript_path = session.get("sessionFile", "")
    context_window = session.get("contextTokens") or 0
    usage_entries = read_usage_entries(transcript_path)

    if not usage_entries:
        return "No usage data found in transcript."

    latest = usage_entries[-1]
    current_total = latest.get("totalTokens", 0)
    input_tokens = session.get("inputTokens", 0)
    output_tokens = session.get("outputTokens", 0)

    lines = []

    if context_window > 0:
        pct_used = current_total / context_window * 100
        remaining = context_window - current_total
        indicator = health_indicator(pct_used)
        bar = make_bar(pct_used)

        lines.append(f"{indicator} {bar} Context Usage: {fmt(current_total)} / {fmt(context_window)} ({pct_str(current_total, context_window)})")
    else:
        lines.append(f"📊 Context Usage: {fmt(current_total)} (context limit unknown)")
        context_window = 0
        remaining = 0

    # System prompt breakdown
    spr = session.get("systemPromptReport", {})
    non_project_chars = spr.get("systemPrompt", {}).get("nonProjectContextChars", 0)
    injected_files = spr.get("injectedWorkspaceFiles", [])

    # Use first response input as system prompt token estimate
    sys_prompt_tokens = usage_entries[0].get("input", 0) if usage_entries else 0
    conversation_tokens = max(0, current_total - sys_prompt_tokens)
    framework_tokens = non_project_chars // 4

    if context_window > 0:
        lines.append("")
        lines.append(SPACER)
        lines.append("*Token Breakdown*")
        lines.append(f"System Prompt: ~{fmt(sys_prompt_tokens)} tokens ({pct_str(sys_prompt_tokens, context_window)})")
        for f in injected_files:
            f_tokens = f["injectedChars"] // 4
            trunc = " [TRUNCATED]" if f.get("truncated") else ""
            lines.append(f"{f['name']}: ~{fmt(f_tokens)} tokens{trunc}")
        lines.append(f"📦 Framework overhead: ~{fmt(framework_tokens)} (tool schemas, skill list, runtime)")
        lines.append(f"• Conversation: ~{fmt(conversation_tokens)} tokens ({pct_str(conversation_tokens, context_window)})")
        lines.append(f"• 📊 Total Used: {fmt(current_total)} ({pct_str(current_total, context_window)})")
        lines.append(f"• Remaining: {fmt(remaining)} ({pct_str(remaining, context_window)})")

    # Trends
    if len(usage_entries) >= 2 and context_window > 0:
        window = min(10, len(usage_entries))
        recent = usage_entries[-window:]
        growths = []
        for i in range(1, len(recent)):
            growth = recent[i]["totalTokens"] - recent[i - 1]["totalTokens"]
            if growth > 0:
                growths.append(growth)
        if growths and remaining > 0:
            avg_g = sum(growths) / len(growths)
            turns = int(remaining / avg_g)
            lines.append(SPACER)
            lines.append("*Trends*")
            lines.append(f"• Avg tokens per turn: ~{fmt(int(avg_g))} tokens")
            lines.append(f"• ⏳ Estimated turns remaining: ~{turns}")

    # Session stats
    cache_read = latest.get("cacheRead", 0)
    cache_hit_rate = (cache_read / current_total * 100) if current_total > 0 else 0
    thinking_count = _count_thinking(transcript_path)
    total_responses = len(usage_entries)

    lines.append(SPACER)
    lines.append("*Session Stats*")
    lines.append(f"• 📥 Total input: {fmt(input_tokens)} | 📤 Total output: {fmt(output_tokens)} | Cache hit rate: {cache_hit_rate:.0f}%")
    if thinking_count > 0:
        lines.append(f"• Thinking: active ({thinking_count}/{total_responses} responses)")
    else:
        lines.append(f"• Thinking: not active")
    lines.append(SPACER)

    return "\n".join(lines)


def _count_thinking(transcript_path: str) -> int:
    """Count assistant responses that contain thinking blocks."""
    if not Path(transcript_path).exists():
        return 0
    count = 0
    with open(transcript_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("type") != "message":
                continue
            msg = entry.get("message", {})
            if msg.get("role") != "assistant":
                continue
            content = msg.get("content", [])
            if any(isinstance(c, dict) and c.get("type") == "thinking" for c in content):
                count += 1
    return count


def build_report(session: dict, detailed: bool = False) -> str:
    """Build the context usage report."""
    if detailed:
        return build_detailed_report(session)
    return build_compact_report(session)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw Context Window Reporter")
    parser.add_argument("--session", "-s", help="Session key")
    parser.add_argument("--agent", "-a", help="Agent name (default: auto-detect)")
    parser.add_argument("--detailed", "-d", action="store_true", help="Full breakdown instead of compact")
    args = parser.parse_args()

    if args.session:
        agent = args.agent or "main"
        store_path = AGENTS_DIR / agent / "sessions" / "sessions.json"
        if not store_path.exists():
            print(f"ERROR: {store_path} not found", file=sys.stderr)
            sys.exit(1)
        with open(store_path) as f:
            sessions = json.load(f)
        if args.session not in sessions:
            print(f"ERROR: Session '{args.session}' not found", file=sys.stderr)
            sys.exit(1)
        session = sessions[args.session]
    else:
        _, session, _ = find_current_session(args.agent)

    print(build_report(session, detailed=args.detailed))


if __name__ == "__main__":
    main()
