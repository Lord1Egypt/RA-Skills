#!/usr/bin/env python3
"""Ghost Mode Verify - 7-layer verification that ghost data is fully removed.

Generic version: no environment-specific assumptions.
"""

import json
import os
import re
import sys
from pathlib import Path

from ghost_registry import WORKSPACE, OPENCLAW_HOME, load_registry, validate_path

AGENT_DIR = os.environ.get("OPENCLAW_AGENT", "main")
SESSIONS_DIR = OPENCLAW_HOME / "agents" / AGENT_DIR / "sessions"
ARCHIVE_BASE = OPENCLAW_HOME / "ghost-archive"
MEMORY_DIR = WORKSPACE / "memory"


def verify_session(session_id):
    """Run 7-layer verification for a ghost session.

    Returns True if all checks pass, False otherwise.
    """
    registry = load_registry()
    entry = registry["sessions"].get(session_id)
    if not entry:
        print(f"Session {session_id} not found in registry", file=sys.stderr)
        return False

    ghost_start = entry["activatedAt"]
    archive_mode = entry.get("archiveMode", "full")
    all_pass = True

    checks = {
        "flag_removed": False,
        "registry_status": False,
        "session_jsonl_not_at_original": False,
        "checkpoints_not_at_original": False,
        "daily_logs_clean": False,
        "semantic_files_clean": False,
        "index_clean": False,
    }

    # Layer 1: Flag file removed
    flag_path = MEMORY_DIR / ".ghost-mode"
    checks["flag_removed"] = not flag_path.exists()
    if not checks["flag_removed"]:
        print(f"FAIL: Flag file still exists: {flag_path}", file=sys.stderr)

    # Layer 2: Registry shows correct status
    checks["registry_status"] = entry["status"] in ("verified", "scrubbed")
    if not checks["registry_status"]:
        print(f"FAIL: Registry status is {entry['status']}, expected scrubbed or verified", file=sys.stderr)

    # Layer 3: Session JSONL not at original path
    original_jsonl = SESSIONS_DIR / f"{session_id}.jsonl"
    if archive_mode == "full":
        checks["session_jsonl_not_at_original"] = not original_jsonl.exists()
    else:
        # Split mode: primary JSONL stays at original path
        checks["session_jsonl_not_at_original"] = True

    if not checks["session_jsonl_not_at_original"]:
        print(f"FAIL: Session JSONL still at original path: {original_jsonl}", file=sys.stderr)

    # Layer 4: Checkpoints not at original path
    checkpoints = list(SESSIONS_DIR.glob(f"{session_id}.checkpoint.*.jsonl"))
    checks["checkpoints_not_at_original"] = len(checkpoints) == 0
    if not checks["checkpoints_not_at_original"]:
        print(f"FAIL: {len(checkpoints)} checkpoint files still at original path", file=sys.stderr)

    # Layer 5: Daily logs contain no ghost-window entries
    daily_log_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}")
    ghost_refs_in_logs = 0
    for log_file in MEMORY_DIR.glob("*.md"):
        if not daily_log_pattern.match(log_file.name):
            continue
        try:
            content = log_file.read_text()
            if session_id in content:
                ghost_refs_in_logs += 1
        except Exception:
            pass
    checks["daily_logs_clean"] = ghost_refs_in_logs == 0
    if not checks["daily_logs_clean"]:
        print(f"FAIL: {ghost_refs_in_logs} daily log files still contain references to session {session_id}", file=sys.stderr)
    else:
        print(f"OK: No session references found in daily logs", file=sys.stderr)

    # Layer 6: Semantic files contain no ghost-window entries
    semantic_dir = MEMORY_DIR / "semantic"
    ghost_refs_in_semantic = 0
    if semantic_dir.exists():
        for sem_file in semantic_dir.glob("*.md"):
            try:
                content = sem_file.read_text()
                if session_id in content:
                    ghost_refs_in_semantic += 1
            except Exception:
                pass
    checks["semantic_files_clean"] = ghost_refs_in_semantic == 0
    if not checks["semantic_files_clean"]:
        print(f"FAIL: {ghost_refs_in_semantic} semantic files still contain references to session {session_id}", file=sys.stderr)
    else:
        print(f"OK: No session references found in semantic files", file=sys.stderr)

    # Layer 7: Memory index contains no ghost paths
    db_path = OPENCLAW_HOME / "data" / "memory.db"
    if db_path.exists():
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            # Check for any chunks referencing the ghost session
            cursor.execute(
                "SELECT COUNT(*) FROM chunks WHERE file_path LIKE ? OR file_path LIKE ?",
                (f"%/{session_id}.%", f"%/{session_id}/%"),
            )
            count = cursor.fetchone()[0]
            conn.close()
            checks["index_clean"] = count == 0
            if not checks["index_clean"]:
                print(f"FAIL: {count} index entries still reference session {session_id}", file=sys.stderr)
        except Exception as e:
            print(f"FAIL: Could not verify memory index (DB error): {e}", file=sys.stderr)
            checks["index_clean"] = False  # DB errors must not silently pass verification
    else:
        checks["index_clean"] = True  # No index to check
        print("INFO: No memory index found, skipping index check", file=sys.stderr)

    # Summary
    all_pass = all(checks.values())
    if all_pass:
        print(f"VERIFIED: All 7 checks passed for session {session_id}", file=sys.stderr)
    else:
        failed = [k for k, v in checks.items() if not v]
        print(f"FAILED: {', '.join(failed)}", file=sys.stderr)

    return all_pass


def verify_all_scrubbed():
    """Verify all sessions with status 'scrubbed'."""
    from ghost_registry import list_sessions, update_status

    sessions = list_sessions(status="scrubbed")
    verified = 0
    for session in sessions:
        session_id = session["sessionId"]
        if verify_session(session_id):
            update_status(session_id, "verified")
            verified += 1

    print(f"Verified {verified}/{len(sessions)} sessions", file=sys.stderr)
    return verified


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ghost Mode Verify")
    sub = parser.add_subparsers(dest="command")

    session_p = sub.add_parser("session", help="Verify a specific session")
    session_p.add_argument("session_id")

    all_p = sub.add_parser("scrubbed", help="Verify all scrubbed sessions")

    args = parser.parse_args()

    # Add scripts dir to path for imports
    sys.path.insert(0, str(Path(__file__).parent))

    if args.command == "session":
        success = verify_session(args.session_id)
        sys.exit(0 if success else 1)
    elif args.command == "scrubbed":
        count = verify_all_scrubbed()
        sys.exit(0 if count > 0 else 1)
    else:
        parser.print_help()