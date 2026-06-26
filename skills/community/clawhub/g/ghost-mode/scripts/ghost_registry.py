#!/usr/bin/env python3
"""Ghost Mode Registry - State machine and CRUD for ghost sessions.

Generic version: no agent-specific or environment-specific assumptions.
Works with any OpenClaw workspace.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace"))
REGISTRY_PATH = WORKSPACE / "memory" / ".ghost-sessions.json"
FLAG_PATH = WORKSPACE / "memory" / ".ghost-mode"
OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", Path.home() / ".openclaw"))

# Path validation: ensure critical directories exist within expected workspace structure
ALLOWED_PREFIXES = [str(WORKSPACE), str(OPENCLAW_HOME)]

_USER_HOME = str(Path.home())


def _check_prefix_safety():
    """Verify that configured workspace/home paths are safe subdirectories.

    Rules:
    - Must resolve within the user's home directory (prevents /tmp, /, etc.)
    - Must NOT be the home directory root itself (prevents OPENCLAW_HOME=$HOME,
      which would allow destructive ops anywhere under ~)
    - Must be at least one level below home (e.g. ~/.openclaw is fine, ~ is not)

    Raises RuntimeError at import time if misconfigured.
    """
    for prefix in ALLOWED_PREFIXES:
        resolved = str(Path(prefix).resolve())
        # Must be within home
        if not resolved.startswith(_USER_HOME + "/"):
            raise RuntimeError(
                f"Safety check failed: {prefix!r} resolves to {resolved!r}. "
                f"OPENCLAW_WORKSPACE and OPENCLAW_HOME must be subdirectories of "
                f"the user home directory ({_USER_HOME}), not the home root itself "
                f"or a system path. Example: {_USER_HOME}/.openclaw"
            )


_check_prefix_safety()


def validate_path(path):
    """Validate that a path is within allowed workspace directories."""
    resolved = str(Path(path).resolve())
    if not any(resolved == p or resolved.startswith(p + "/") for p in ALLOWED_PREFIXES):
        raise ValueError(f"Path {path} is outside allowed workspace directories")
    return Path(path)


def validate_session_id(session_id):
    """Validate session ID to prevent path traversal attacks."""
    if not session_id or "/" in session_id or "\\" in session_id or ".." in session_id:
        raise ValueError(f"Invalid session ID: {session_id}")
    return session_id

VALID_STATUSES = ["active", "completed", "archived", "scrubbed", "verified"]

TRANSITIONS = {
    "active": ["completed"],
    "completed": ["archived"],
    "archived": ["scrubbed"],
    "scrubbed": ["verified"],
    "verified": [],  # terminal
}


def load_registry():
    """Load the ghost sessions registry. Create if not exists."""
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH) as f:
            return json.load(f)
    return {"sessions": {}}


def save_registry(registry):
    """Atomic write: save to .tmp then rename."""
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = REGISTRY_PATH.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(registry, f, indent=2)
    tmp.rename(REGISTRY_PATH)


def add_session(session_key, session_id):
    """Register a new ghost session."""
    registry = load_registry()
    if session_id in registry["sessions"]:
        print(f"Session {session_id} already in registry with status: {registry['sessions'][session_id]['status']}", file=sys.stderr)
        return registry["sessions"][session_id]

    entry = {
        "sessionKey": session_key,
        "sessionId": session_id,
        "activatedAt": datetime.now(timezone.utc).isoformat(),
        "status": "active",
        "archiveMode": "full",
        "archivedAt": None,
        "scrubbedAt": None,
        "verifiedAt": None,
    }
    registry["sessions"][session_id] = entry
    save_registry(registry)
    print(f"Registered ghost session {session_id} -> active", file=sys.stderr)
    return entry


def update_status(session_id, new_status):
    """Transition a session to a new status. Validates transition order."""
    registry = load_registry()
    if session_id not in registry["sessions"]:
        print(f"Session {session_id} not found in registry", file=sys.stderr)
        sys.exit(1)

    entry = registry["sessions"][session_id]
    current = entry["status"]

    if current == new_status:
        # Idempotent: already at this status
        print(f"Session {session_id} already {new_status}", file=sys.stderr)
        return entry

    if new_status not in TRANSITIONS.get(current, []):
        # Allow skipping ahead for idempotent re-runs
        valid_order = VALID_STATUSES
        current_idx = valid_order.index(current)
        new_idx = valid_order.index(new_status)
        if new_idx <= current_idx:
            print(f"Invalid transition: {current} -> {new_status}", file=sys.stderr)
            sys.exit(1)

    entry["status"] = new_status
    timestamp_field = f"{new_status}At"
    if timestamp_field in entry:
        entry[timestamp_field] = datetime.now(timezone.utc).isoformat()

    save_registry(registry)
    print(f"Session {session_id}: {current} -> {new_status}", file=sys.stderr)
    return entry


def get_session(session_id):
    """Get a session entry by ID."""
    registry = load_registry()
    return registry["sessions"].get(session_id)


def list_sessions(status=None):
    """List all sessions, optionally filtered by status."""
    registry = load_registry()
    sessions = registry["sessions"].values()
    if status:
        sessions = [s for s in sessions if s["status"] == status]
    return list(sessions)


def remove_session(session_id):
    """Remove a session from the registry (after shred is complete)."""
    registry = load_registry()
    if session_id in registry["sessions"]:
        del registry["sessions"][session_id]
        save_registry(registry)
        print(f"Removed session {session_id} from registry", file=sys.stderr)


def write_flag(session_key, session_id):
    """Write the .ghost-mode flag file."""
    flag_data = {
        "sessionKey": session_key,
        "sessionId": session_id,
        "activatedAt": datetime.now(timezone.utc).isoformat(),
    }
    FLAG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(FLAG_PATH, "w") as f:
        json.dump(flag_data, f, indent=2)
    print(f"Ghost mode flag written: {FLAG_PATH}", file=sys.stderr)


def read_flag():
    """Read the .ghost-mode flag file. Returns None if not active."""
    if not FLAG_PATH.exists():
        return None
    with open(FLAG_PATH) as f:
        return json.load(f)


def remove_flag():
    """Remove the .ghost-mode flag file."""
    if FLAG_PATH.exists():
        FLAG_PATH.unlink()
        print("Ghost mode flag removed", file=sys.stderr)


def is_ghost_active():
    """Check if ghost mode is currently active."""
    flag = read_flag()
    if flag is None:
        return False

    # Check for stale flag (>24h)
    activated = datetime.fromisoformat(flag["activatedAt"])
    age = (datetime.now(timezone.utc) - activated).total_seconds()
    if age > 86400:  # 24 hours
        print(f"Stale ghost flag detected ({age:.0f}s old). Run force-cleanup-all.", file=sys.stderr)
        return False

    return True


def get_stale_sessions():
    """Find sessions with flags older than 24 hours."""
    registry = load_registry()
    now = datetime.now(timezone.utc)
    stale = []
    for session_id, entry in registry["sessions"].items():
        if entry["status"] == "active":
            activated = datetime.fromisoformat(entry["activatedAt"])
            age = (now - activated).total_seconds()
            if age > 86400:
                stale.append(entry)
    return stale


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ghost Mode Registry")
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add", help="Register a new ghost session")
    add_p.add_argument("session_key")
    add_p.add_argument("session_id")

    status_p = sub.add_parser("update", help="Update session status")
    status_p.add_argument("session_id")
    status_p.add_argument("new_status", choices=VALID_STATUSES)

    get_p = sub.add_parser("get", help="Get session info")
    get_p.add_argument("session_id")

    list_p = sub.add_parser("list", help="List sessions")
    list_p.add_argument("--status", choices=VALID_STATUSES)

    remove_p = sub.add_parser("remove", help="Remove session from registry")
    remove_p.add_argument("session_id")

    flag_p = sub.add_parser("flag-read", help="Read ghost mode flag")

    stale_p = sub.add_parser("stale", help="List stale sessions (>24h)")

    args = parser.parse_args()

    if args.command == "add":
        entry = add_session(args.session_key, args.session_id)
        print(json.dumps(entry, indent=2))
    elif args.command == "update":
        entry = update_status(args.session_id, args.new_status)
        print(json.dumps(entry, indent=2))
    elif args.command == "get":
        entry = get_session(args.session_id)
        if entry:
            print(json.dumps(entry, indent=2))
        else:
            print("Not found", file=sys.stderr)
            sys.exit(1)
    elif args.command == "list":
        sessions = list_sessions(args.status)
        print(json.dumps(sessions, indent=2))
    elif args.command == "remove":
        remove_session(args.session_id)
    elif args.command == "flag-read":
        flag = read_flag()
        if flag:
            print(json.dumps(flag, indent=2))
        else:
            print("INACTIVE")
    elif args.command == "stale":
        stale = get_stale_sessions()
        print(json.dumps(stale, indent=2))
    else:
        parser.print_help()