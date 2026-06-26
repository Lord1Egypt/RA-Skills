#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SESSION_KEY = "agent:main:main"


def main() -> int:
    parser = argparse.ArgumentParser(description="Manually trigger Codex profile failover for a session")
    parser.add_argument("--config", required=True, help="Watchdog config path")
    parser.add_argument("--session-key", default=DEFAULT_SESSION_KEY, help=f"Session key to evaluate (default: {DEFAULT_SESSION_KEY})")
    parser.add_argument("--state-dir", default="/home/node/.openclaw", help="OpenClaw state directory")
    parser.add_argument("--timeout", type=int, default=15, help="Per-profile usage timeout seconds")
    parser.add_argument("--dry-run", action="store_true", help="Only inspect, do not apply a switch")
    args = parser.parse_args()

    command = [
        sys.executable,
        str(SKILL_DIR / "scripts" / "codex_profile_watchdog.py"),
        "--once",
        "--json",
        "--config",
        args.config,
        "--state-dir",
        args.state_dir,
        "--timeout",
        str(args.timeout),
    ]
    if not args.dry_run:
        command.append("--apply")

    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        sys.stderr.write(completed.stderr)
        return completed.returncode

    payload = json.loads(completed.stdout)
    payload["sessions"] = [item for item in (payload.get("sessions") or []) if item.get("sessionKey") == args.session_key]
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
