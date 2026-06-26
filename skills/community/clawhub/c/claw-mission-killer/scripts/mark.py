#!/usr/bin/env python3
"""
mark.py - Agent exec process marker

Agent calls this before/after long exec tasks to register/clear its running PID.
This allows agent-interrupt to precisely kill the correct process.

Usage:
    # Register current process tree (call from within the exec environment)
    python -X utf8 mark.py --agent <agent_id> --pid <pid> --session <session_id>

    # Clear marker when task completes
    python -X utf8 mark.py --agent <agent_id> --clear

The marker is saved to: ~/.openclaw/agents/<agent_id>/running.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def find_openclaw_home():
    env = os.environ.get("OPENCLAW_HOME")
    if env:
        return Path(env)
    return Path.home() / ".openclaw"


def get_marker_path(openclaw_home, agent_id):
    return openclaw_home / "agents" / agent_id / "running.json"


def main():
    parser = argparse.ArgumentParser(description="Mark/clear agent running process")
    parser.add_argument("--agent", required=True, help="Agent ID")
    parser.add_argument("--pid", type=int, help="PID to register")
    parser.add_argument("--session", help="Exec session ID (e.g. dawn-seaslug)")
    parser.add_argument("--clear", action="store_true", help="Clear the marker")
    args = parser.parse_args()

    openclaw_home = find_openclaw_home()
    marker_path = get_marker_path(openclaw_home, args.agent)
    marker_path.parent.mkdir(parents=True, exist_ok=True)

    if args.clear:
        if marker_path.exists():
            marker_path.unlink()
            print(f"[mark] Cleared marker for {args.agent}")
        else:
            print(f"[mark] No marker to clear for {args.agent}")
        return

    if not args.pid:
        print("[mark] ERROR: --pid required when registering")
        sys.exit(1)

    marker = {
        "agent_id": args.agent,
        "pid": args.pid,
        "session_id": args.session or "",
        "registered_at": datetime.now().isoformat()
    }
    with open(marker_path, "w", encoding="utf-8") as f:
        json.dump(marker, f, ensure_ascii=False, indent=2)
    print(f"[mark] Registered PID {args.pid} for agent {args.agent}")


if __name__ == "__main__":
    main()
