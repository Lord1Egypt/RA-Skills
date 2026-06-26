#!/usr/bin/env python3
"""Prune bridge JSONL files to last N days. Run weekly via cron.

Usage: python3 bridge_prune.py [--days 7] [--dir /tmp/acp_bridge]
"""
import argparse, json, os, time
from pathlib import Path


def prune(bridge_dir: str, days: int):
    cutoff = time.time() - days * 86400
    for fname in ["inbox.jsonl", "outbox.jsonl"]:
        fpath = Path(bridge_dir) / fname
        if not fpath.exists():
            continue
        with open(fpath) as f:
            lines = f.readlines()
        kept = [l for l in lines if _ts(l) > cutoff]
        with open(fpath, "w") as f:
            f.writelines(kept)
        print(f"Pruned {fname}: {len(lines)} → {len(kept)} messages (kept last {days}d)")


def _ts(line):
    try:
        return json.loads(line.strip()).get("ts", 0)
    except (json.JSONDecodeError, AttributeError):
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--dir", default=os.environ.get("ACP_BRIDGE_DIR", "/tmp/acp_bridge"))
    args = parser.parse_args()
    prune(args.dir, args.days)
