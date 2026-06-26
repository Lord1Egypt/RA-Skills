#!/usr/bin/env python3
"""
load_session.py - AI Rebirth: Load conversation history from a previous CodeBuddy session.

Usage:
  python3 load_session.py                          # List sessions for current project
  python3 load_session.py --id UUID                # Load specific session (summary)
  python3 load_session.py --project /path          # List sessions for a project
  python3 load_session.py --id UUID --mode full    # Full message chain
  python3 load_session.py --id UUID --mode tail 5  # Last 5 turns
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


CODEBUDDY_DIR = Path.home() / ".codebuddy"
PROJECTS_DIR = CODEBUDDY_DIR / "projects"


def path_to_project_dir(path):
    return str(path).strip("/").replace("/", "-")


def find_session_file(session_id):
    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        candidate = project_dir / (session_id + ".jsonl")
        if candidate.exists():
            return candidate
    return None


def list_sessions(project_path=None):
    results = []
    if project_path:
        project_name = path_to_project_dir(project_path)
        dirs = [PROJECTS_DIR / project_name]
    else:
        dirs = [d for d in PROJECTS_DIR.iterdir() if d.is_dir()]

    for project_dir in dirs:
        if not project_dir.exists():
            continue
        for f in project_dir.glob("*.jsonl"):
            if f.stem.count("-") == 4:
                stat = f.stat()
                results.append({
                    "id": f.stem,
                    "project": project_dir.name,
                    "size_mb": round(stat.st_size / 1024 / 1024, 2),
                    "modified": datetime.fromtimestamp(stat.st_mtime),
                    "path": str(f),
                })
    results.sort(key=lambda x: x["modified"], reverse=True)
    return results


def extract_text_from_content(content):
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                t = item.get("type", "")
                if t in ("input_text", "output_text", "text"):
                    text = item.get("text", "").strip()
                    if text:
                        parts.append(text)
        return "\n".join(parts)
    return ""


def parse_session(session_file):
    messages = []
    topics = []
    with open(session_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            rec_type = record.get("type", "")
            if rec_type == "message":
                role = record.get("role", "unknown")
                content = record.get("content", "")
                text = extract_text_from_content(content)
                timestamp = record.get("timestamp", 0)
                messages.append({
                    "role": role,
                    "text": text,
                    "timestamp": timestamp,
                    "id": record.get("id", ""),
                })
            elif rec_type == "topic":
                topics.append({
                    "topic": record.get("topic", ""),
                    "timestamp": record.get("timestamp", 0),
                })
    messages.sort(key=lambda x: x["timestamp"])
    return messages, topics


def format_timestamp(ts):
    if not ts:
        return "unknown"
    try:
        dt = datetime.fromtimestamp(ts / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, OSError):
        return "unknown"


def generate_summary(messages, topics, session_id):
    user_msgs = [m for m in messages if m["role"] == "user" and m["text"]]
    assistant_msgs = [m for m in messages if m["role"] == "assistant" and m["text"]]

    lines = []
    lines.append("# Session Summary: " + session_id)
    lines.append("")

    if messages:
        first_ts = format_timestamp(messages[0]["timestamp"])
        last_ts = format_timestamp(messages[-1]["timestamp"])
        lines.append("- **Time range**: " + first_ts + " ~ " + last_ts)

    msg_count = str(len(messages))
    user_count = str(len(user_msgs))
    asst_count = str(len(assistant_msgs))
    lines.append("- **Total messages**: " + msg_count + " (" + user_count + " user, " + asst_count + " assistant)")
    lines.append("")

    if topics:
        lines.append("## Topics")
        for t in topics:
            lines.append("- [" + format_timestamp(t["timestamp"]) + "] " + t["topic"])
        lines.append("")

    lines.append("## User Requests (chronological)")
    for i, m in enumerate(user_msgs, 1):
        preview = m["text"][:200].replace("\n", " ")
        if len(m["text"]) > 200:
            preview += "..."
        lines.append(str(i) + ". [" + format_timestamp(m["timestamp"]) + "] " + preview)
    lines.append("")

    lines.append("## Last Conversation State")
    tail_msgs = [m for m in messages if m["text"]][-6:]
    for m in tail_msgs:
        role_label = "USER" if m["role"] == "user" else "ASSISTANT"
        lines.append("### [" + role_label + "] " + format_timestamp(m["timestamp"]))
        lines.append("")
        text = m["text"]
        if len(text) > 2000:
            text = text[:2000] + "\n\n... (truncated)"
        lines.append(text)
        lines.append("")

    return "\n".join(lines)


def generate_full(messages):
    lines = []
    for m in messages:
        if not m["text"]:
            continue
        role_label = "USER" if m["role"] == "user" else "ASSISTANT"
        lines.append("### [" + role_label + "] " + format_timestamp(m["timestamp"]))
        lines.append("")
        lines.append(m["text"])
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def generate_tail(messages, n):
    text_msgs = [m for m in messages if m["text"]]
    tail = text_msgs[-(n * 2):]
    lines = []
    lines.append("# Last " + str(n) + " turns")
    lines.append("")
    for m in tail:
        role_label = "USER" if m["role"] == "user" else "ASSISTANT"
        lines.append("### [" + role_label + "] " + format_timestamp(m["timestamp"]))
        lines.append("")
        lines.append(m["text"])
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AI Rebirth - Load CodeBuddy session history")
    parser.add_argument("--id", help="Session UUID to load")
    parser.add_argument("--project", help="Project path to list sessions for")
    parser.add_argument("--mode", default="summary", help="Output mode: summary, full, or tail N")
    parser.add_argument("--cwd", help="Current working directory (for auto-detecting project)")
    args = parser.parse_args()

    if not args.id:
        project_path = args.project or args.cwd or os.getcwd()
        sessions = list_sessions(project_path)
        if not sessions:
            print("No sessions found for project: " + str(project_path))
            sys.exit(1)
        print("# Sessions for: " + str(project_path) + "\n")
        for s in sessions:
            print("- **" + s["id"] + "**")
            print("  Modified: " + s["modified"].strftime("%Y-%m-%d %H:%M:%S"))
            print("  Size: " + str(s["size_mb"]) + " MB")
            print()
        sys.exit(0)

    session_file = find_session_file(args.id)
    if not session_file:
        print("Error: Session not found: " + args.id, file=sys.stderr)
        sys.exit(1)

    messages, topics = parse_session(str(session_file))
    if not messages:
        print("No messages found in session: " + args.id, file=sys.stderr)
        sys.exit(1)

    mode = args.mode.strip()
    if mode == "summary":
        print(generate_summary(messages, topics, args.id))
    elif mode == "full":
        print(generate_full(messages))
    elif mode.startswith("tail"):
        parts = mode.split()
        n = int(parts[1]) if len(parts) > 1 else 5
        print(generate_tail(messages, n))
    else:
        print("Unknown mode: " + mode, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
