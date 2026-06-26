#!/usr/bin/env python3
"""
log_interaction.py — Append a Q&A interaction to the daily audit log.

Usage:
    python3 log_interaction.py \
        --log-dir <path>     \
        --user-id <id>       \
        --channel <id>       \
        --thread <id|"">     \
        --question <text>    \
        --answer <text>      \
        --status <ok|rate_limited|out_of_scope|no_material>

Output: JSON entry appended to <log-dir>/YYYY-MM-DD.jsonl
Prints the log entry to stdout on success.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-dir", type=Path, required=True)
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--channel", default="")
    parser.add_argument("--thread", default="")
    parser.add_argument("--question", required=True)
    parser.add_argument("--answer", required=True)
    parser.add_argument("--status", default="ok",
                        choices=["ok", "rate_limited", "out_of_scope",
                                 "no_material", "admin_edit", "canvas_write",
                                 "forward_failed"])
    args = parser.parse_args()

    args.log_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)
    log_file = args.log_dir / f"{now.strftime('%Y-%m-%d')}.jsonl"

    entry = {
        "timestamp": now.isoformat(),
        "userId": args.user_id,
        "channelId": args.channel,
        "threadId": args.thread,
        "status": args.status,
        "question": args.question[:300],
        "answer": args.answer[:500],
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(json.dumps({"logged": True, "file": str(log_file), "status": args.status}))


if __name__ == "__main__":
    main()
