#!/usr/bin/env python3
"""
run.py - Auto-registering process wrapper for agent-interrupt

Wraps any command, automatically registers the PID before execution
and clears the marker when done. Agents use this instead of running
scripts directly to enable precise kill support.

Usage:
    python -X utf8 run.py --agent <agent_id> -- <command> [args...]

Examples:
    python -X utf8 run.py --agent my_agent -- python backtest.py
    python -X utf8 run.py --agent my_agent -- python -X utf8 main.py --mode A

Environment:
    OPENCLAW_HOME  Override default ~/.openclaw location
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def find_openclaw_home():
    env = os.environ.get("OPENCLAW_HOME")
    if env:
        return Path(env)
    return Path.home() / ".openclaw"


def get_marker_path(openclaw_home, agent_id):
    return openclaw_home / "agents" / agent_id / "running.json"


def register(openclaw_home, agent_id, pid, session_id=""):
    marker_path = get_marker_path(openclaw_home, agent_id)
    marker_path.parent.mkdir(parents=True, exist_ok=True)
    with open(marker_path, "w", encoding="utf-8") as f:
        json.dump({
            "agent_id": agent_id,
            "pid": pid,
            "session_id": session_id,
            "registered_at": time.strftime("%Y-%m-%dT%H:%M:%S")
        }, f, ensure_ascii=False)


def clear(openclaw_home, agent_id):
    marker_path = get_marker_path(openclaw_home, agent_id)
    marker_path.unlink(missing_ok=True)


def main():
    # Split args at '--'
    argv = sys.argv[1:]
    if "--" not in argv:
        print("[run] ERROR: Missing '--' separator. Usage: run.py --agent <id> -- <command>")
        sys.exit(1)

    sep = argv.index("--")
    our_args = argv[:sep]
    cmd_args = argv[sep + 1:]

    if not cmd_args:
        print("[run] ERROR: No command specified after '--'")
        sys.exit(1)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--agent", required=True)
    parser.add_argument("--session", default="")
    args = parser.parse_args(our_args)

    openclaw_home = find_openclaw_home()

    proc = subprocess.Popen(cmd_args)
    register(openclaw_home, args.agent, proc.pid, args.session)
    print(f"[run] Started PID {proc.pid} for agent {args.agent}: {' '.join(cmd_args)}")

    try:
        exit_code = proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        proc.wait()
        exit_code = 130
    finally:
        clear(openclaw_home, args.agent)
        print(f"[run] PID {proc.pid} finished (exit={exit_code}), marker cleared")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
