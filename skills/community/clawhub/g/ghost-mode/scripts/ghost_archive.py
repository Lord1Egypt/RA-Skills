#!/usr/bin/env python3
"""Ghost Mode Archiver - Move session files to archive and update registry.

Generic version: no agent-specific assumptions.
"""

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from ghost_registry import (
    WORKSPACE,
    OPENCLAW_HOME,
    load_registry,
    save_registry,
    update_status,
    validate_path,
    validate_session_id,
)

OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", Path.home() / ".openclaw"))
AGENT_DIR = os.environ.get("OPENCLAW_AGENT", "main")
SESSIONS_DIR = OPENCLAW_HOME / "agents" / AGENT_DIR / "sessions"
ARCHIVE_BASE = OPENCLAW_HOME / "ghost-archive"


def find_session_files(session_id):
    """Find all JSONL and checkpoint files for a session."""
    validate_session_id(session_id)
    files = []

    # Primary JSONL
    primary = SESSIONS_DIR / f"{session_id}.jsonl"
    if primary.exists():
        files.append(("primary", primary))

    # Checkpoints
    for cp in SESSIONS_DIR.glob(f"{session_id}.checkpoint.*.jsonl"):
        files.append(("checkpoint", cp))

    # Reset/deleted variants
    for variant in SESSIONS_DIR.glob(f"{session_id}.jsonl.*"):
        if ".tmp" not in variant.name:
            files.append(("variant", variant))

    return files


def archive_session(session_id, archive_mode="full"):
    """Archive a session's files.

    Args:
        session_id: The session UUID
        archive_mode: 'full' (remove originals) or 'split' (keep primary JSONL)

    Returns:
        True if archival succeeded, False otherwise
    """
    files = find_session_files(session_id)
    if not files:
        print(f"No session files found for {session_id}", file=sys.stderr)
        # Mark as completed even if no files — idempotent
        update_status(session_id, "completed")
        update_status(session_id, "archived")
        return True

    # Create archive directory
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    archive_dir = ARCHIVE_BASE / date_str / session_id
    validate_path(archive_dir)
    archive_dir.mkdir(parents=True, exist_ok=True)

    for file_type, src_path in files:
        dest = archive_dir / src_path.name

        # Copy to archive
        shutil.copy2(src_path, dest)
        print(f"Archived: {src_path.name} -> {archive_dir.relative_to(OPENCLAW_HOME)}", file=sys.stderr)

        # Remove original if full mode, or if checkpoint/split in split mode
        if archive_mode == "full":
            src_path.unlink()
        elif archive_mode == "split" and file_type != "primary":
            src_path.unlink()
        elif archive_mode == "split" and file_type == "primary":
            # Keep primary at original path in split mode
            pass

    # Update registry
    update_status(session_id, "completed")
    update_status(session_id, "archived")

    # Record archive mode
    registry = load_registry()
    if session_id in registry["sessions"]:
        registry["sessions"][session_id]["archiveMode"] = archive_mode
        save_registry(registry)

    print(f"Session {session_id} archived ({archive_mode} mode)", file=sys.stderr)
    return True


def archive_completed_sessions():
    """Find all sessions with status 'active' and archive them."""
    from ghost_registry import list_sessions

    active = list_sessions(status="active")
    archived = 0
    for session in active:
        session_id = session["sessionId"]
        archive_mode = session.get("archiveMode", "full")
        if archive_session(session_id, archive_mode):
            archived += 1

    print(f"Archived {archived} sessions", file=sys.stderr)
    return archived


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ghost Mode Archiver")
    sub = parser.add_subparsers(dest="command")

    archive_p = sub.add_parser("session", help="Archive a specific session")
    archive_p.add_argument("session_id")
    archive_p.add_argument("--mode", choices=["full", "split"], default="full")

    all_p = sub.add_parser("completed", help="Archive all active sessions")

    args = parser.parse_args()

    if args.command == "session":
        archive_session(args.session_id, args.mode)
    elif args.command == "completed":
        archive_completed_sessions()
    else:
        parser.print_help()