#!/usr/bin/env python3
"""Ghost Mode Index Cleanup - Remove ghost session entries from OpenClaw memory index.

Generic version: works with OpenClaw's standard SQLite memory index.
"""

import sqlite3
import sys
from pathlib import Path

from ghost_registry import OPENCLAW_HOME, load_registry, validate_path

DB_PATH = OPENCLAW_HOME / "data" / "memory.db"


def cleanup_index(session_ids=None):
    """Remove index entries referencing ghost sessions.

    Args:
        session_ids: List of session IDs to clean up. If None, cleans all verified sessions.
    """
    if not DB_PATH.exists():
        print("No memory index found, skipping index cleanup", file=sys.stderr)
        return 0

    if session_ids is None:
        registry = load_registry()
        session_ids = [
            s["sessionId"] for s in registry["sessions"].values()
            if s["status"] in ("scrubbed", "verified")
        ]

    if not session_ids:
        print("No sessions to clean from index", file=sys.stderr)
        return 0

    total_removed = 0
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        for session_id in session_ids:
            # Match only paths where session_id is a complete path component:
            # - %/<session_id>.% covers session JSONL files and variants
            # - %/<session_id>/% covers anything inside a session-named directory
            # This avoids false positives if the UUID appears as a substring
            # elsewhere in an unrelated file path.
            path_as_file = f"%/{session_id}.%"
            path_as_dir = f"%/{session_id}/%"
            cursor.execute(
                "SELECT COUNT(*) FROM chunks WHERE file_path LIKE ? OR file_path LIKE ?",
                (path_as_file, path_as_dir),
            )
            count = cursor.fetchone()[0]

            if count > 0:
                cursor.execute(
                    "DELETE FROM chunks WHERE file_path LIKE ? OR file_path LIKE ?",
                    (path_as_file, path_as_dir),
                )
                print(f"Removed {count} index entries for session {session_id}", file=sys.stderr)
                total_removed += count

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Database error: {e}", file=sys.stderr)
        return total_removed

    print(f"Total index entries removed: {total_removed}", file=sys.stderr)
    return total_removed


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ghost Mode Index Cleanup")
    parser.add_argument("--session-id", help="Specific session ID to clean up")
    parser.add_argument("--all", action="store_true", help="Clean up all verified sessions")

    args = parser.parse_args()

    if args.session_id:
        cleanup_index([args.session_id])
    elif args.all:
        cleanup_index()
    else:
        parser.print_help()