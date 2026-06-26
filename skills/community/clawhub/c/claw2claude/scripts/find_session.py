#!/usr/bin/env python3
"""
find_session.py — Find the most recently active user-facing OpenClaw session.

Reads the sessions registry and returns the session key of the channel where
the user most recently sent a message. Used by launch.sh to tell notifier.py
where to deliver results.

Excludes system sessions: cron, subagent, heartbeat, and the bare "main" session.

Usage:
  python3 find_session.py [--agent main] [--config ~/.openclaw/openclaw.json]
  → prints a single session key, e.g. "agent:main:discord:channel:1481879861273428010"
  → exits 1 with no output if nothing found
"""

import argparse
import json
import sys
from pathlib import Path

EXCLUDE_SEGMENTS = (":cron:", ":subagent:", ":heartbeat:")
EXCLUDE_EXACT    = {"agent:main:main"}

parser = argparse.ArgumentParser()
parser.add_argument("--agent",  default="main")
parser.add_argument("--config",
    default=str(Path.home() / ".openclaw" / "openclaw.json"))
args = parser.parse_args()

# Locate sessions.json next to openclaw.json
openclaw_dir = Path(args.config).parent
sessions_file = openclaw_dir / "agents" / args.agent / "sessions" / "sessions.json"

if not sessions_file.exists():
    print(f"⚠️  Sessions file not found: {sessions_file}", file=sys.stderr)
    sys.exit(1)

try:
    data = json.loads(sessions_file.read_text(encoding="utf-8"))
except json.JSONDecodeError as e:
    print(f"⚠️  Corrupted sessions file: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"⚠️  Failed to read sessions file: {e}", file=sys.stderr)
    sys.exit(1)

candidates = []
for key, session in data.items():
    if key in EXCLUDE_EXACT:
        continue
    if any(seg in key for seg in EXCLUDE_SEGMENTS):
        continue
    updated_at = session.get("updatedAt", 0)
    candidates.append((updated_at, key))

if not candidates:
    sys.exit(1)

candidates.sort(reverse=True)
print(candidates[0][1])
