# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Conversation summary manager — manages cross-session dialogue history under ~/.mbti/conversations/."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Conversation volume thresholds
MIN_TOTAL_TURNS = 50
MIN_OPEN_TURNS = 10


def get_conversations_dir(mbti_dir: str | None = None) -> Path:
    """Return the conversation summary storage directory."""
    base = Path(mbti_dir).expanduser().resolve() if mbti_dir else Path.home() / ".mbti"
    return base / "conversations"


def ensure_dir(conversations_dir: Path) -> None:
    """Ensure the directory exists."""
    conversations_dir.mkdir(parents=True, exist_ok=True)


def load_all_sessions(conversations_dir: Path) -> list[dict[str, Any]]:
    """Load all session summary files, sorted by time."""
    sessions: list[dict[str, Any]] = []
    if not conversations_dir.exists():
        return sessions

    for f in sorted(conversations_dir.glob("session-*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            data["_file"] = f.name
            sessions.append(data)
        except (json.JSONDecodeError, OSError):
            continue

    return sessions


def cmd_save_session(args: argparse.Namespace) -> None:
    """Save a session summary."""
    conversations_dir = get_conversations_dir(args.mbti_dir)
    ensure_dir(conversations_dir)

    session_data: dict[str, Any] = json.loads(args.data)

    now = datetime.now(timezone.utc)
    if "session_id" not in session_data:
        session_data["session_id"] = now.strftime("%Y-%m-%dT%H-%M")
    if "saved_at" not in session_data:
        session_data["saved_at"] = now.isoformat()

    filename = f"session-{now.strftime('%Y%m%d-%H%M%S')}.json"
    filepath = conversations_dir / filename

    filepath.write_text(
        json.dumps(session_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps({"status": "ok", "path": str(filepath)}, indent=2))


def cmd_list_sessions(args: argparse.Namespace) -> None:
    """List all historical session summaries (brief info)."""
    conversations_dir = get_conversations_dir(args.mbti_dir)
    sessions = load_all_sessions(conversations_dir)

    summaries: list[dict[str, Any]] = []
    for s in sessions:
        turns = s.get("turns", {})
        dialogues = s.get("open_dialogues", [])
        topics = [d.get("topic", "") for d in dialogues if d.get("topic")]

        summaries.append({
            "session_id": s.get("session_id", ""),
            "saved_at": s.get("saved_at", ""),
            "total_turns": turns.get("total", 0),
            "open_turns": turns.get("open", 0),
            "topics": topics,
        })

    print(json.dumps(summaries, indent=2, ensure_ascii=False))


def cmd_read_history(args: argparse.Namespace) -> None:
    """Read all historical summaries (for MBTI analysis)."""
    conversations_dir = get_conversations_dir(args.mbti_dir)
    sessions = load_all_sessions(conversations_dir)

    # Remove internal fields
    for s in sessions:
        s.pop("_file", None)

    print(json.dumps(sessions, indent=2, ensure_ascii=False))


def cmd_stats(args: argparse.Namespace) -> None:
    """Aggregate cumulative conversation statistics."""
    conversations_dir = get_conversations_dir(args.mbti_dir)
    sessions = load_all_sessions(conversations_dir)

    total_turns = 0
    open_turns = 0

    for s in sessions:
        turns = s.get("turns", {})
        total_turns += turns.get("total", 0)
        open_turns += turns.get("open", 0)

    ready = total_turns >= MIN_TOTAL_TURNS and open_turns >= MIN_OPEN_TURNS

    result: dict[str, Any] = {
        "session_count": len(sessions),
        "total_turns": total_turns,
        "open_turns": open_turns,
        "ready_for_analysis": ready,
        "thresholds": {
            "min_total_turns": MIN_TOTAL_TURNS,
            "min_open_turns": MIN_OPEN_TURNS,
        },
    }
    print(json.dumps(result, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Conversation summary manager")
    parser.add_argument(
        "--mbti-dir", type=str, default=None,
        help="~/.mbti/ directory path, defaults to ~/.mbti",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    save_session = subparsers.add_parser("save-session", help="Save a session summary")
    save_session.add_argument("--data", required=True, help="Session summary JSON string")

    subparsers.add_parser("list-sessions", help="List all session summaries")
    subparsers.add_parser("read-history", help="Read all historical summaries")
    subparsers.add_parser("stats", help="Aggregate conversation statistics")

    args = parser.parse_args()

    commands: dict[str, Any] = {
        "save-session": cmd_save_session,
        "list-sessions": cmd_list_sessions,
        "read-history": cmd_read_history,
        "stats": cmd_stats,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
