#!/usr/bin/env python3
"""
log_entry.py — Append a JSON log line to the claw2claude monthly log file.

Each line is a self-contained JSON object (newline-delimited JSON / NDJSON).
Fields:
  ts              ISO-8601 UTC timestamp
  status          "started" | "done" | "error" | "timeout"
  project         absolute project path
  mode            discuss | execute | continue | background
  session_key     OpenClaw session key (channel the result is sent to)
  claude_session  Claude Code session ID (first 8 chars for readability)
  prompt          first 200 chars of the user prompt

Usage:
  log_entry.py --log-file <path> --status <status> --project <path>
               --mode <mode> --session-key <key>
               --claude-session <id> --prompt <text>
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--log-file",       required=True)
parser.add_argument("--status",         required=True)
parser.add_argument("--project",        default="")
parser.add_argument("--mode",           default="")
parser.add_argument("--session-key",    default="")
parser.add_argument("--claude-session", default="")
parser.add_argument("--prompt",         default="")
args = parser.parse_args()

entry = {
    "ts":             datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "status":         args.status,
    "project":        args.project,
    "mode":           args.mode,
    "session_key":    args.session_key,
    "claude_session": args.claude_session[:8] if args.claude_session else "",
    "prompt":         args.prompt,
}

log_path = Path(args.log_file)
log_path.parent.mkdir(parents=True, exist_ok=True)

with open(log_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
