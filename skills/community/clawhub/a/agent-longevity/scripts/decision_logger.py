#!/usr/bin/env python3
"""
Decision Logger — 通用版
记录Agent决策到JSONL文件，支持L1/L2/L3分级。

用法:
  python3 decision_logger.py log --action "感知环境" --reasoning "转换点: day→dusk" --level L2
  python3 decision_logger.py log --action "跳过感知" --reasoning "距上次仅15分钟" --level L1
  python3 decision_logger.py stats
  python3 decision_logger.py query --hours 24 --limit 10
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(os.environ.get("AGENT_DATA_DIR", str(Path.cwd() / "data")))
LOG_FILE = DATA_DIR / "decision_logs.jsonl"

LEVELS = {
    "L1": "routine",
    "L2": "contextual",
    "L3": "reflective",
}

def log_decision(action, reasoning, level="L1", priority="low", source="manual", extra=None):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now().isoformat(),
        "action": action,
        "reasoning": reasoning,
        "metadata": {
            "level": level,
            "level_name": LEVELS.get(level, "unknown"),
            "priority": priority,
            "source": source,
        }
    }
    if extra:
        entry["metadata"]["extra"] = extra
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

def query_logs(level=None, source=None, hours=24, limit=20):
    if not LOG_FILE.exists():
        print("No decision logs found.")
        return
    cutoff = datetime.now().timestamp() - hours * 3600
    entries = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                ts = datetime.fromisoformat(entry["ts"]).timestamp()
                if ts < cutoff:
                    continue
                if level and entry["metadata"].get("level") != level:
                    continue
                if source and entry["metadata"].get("source") != source:
                    continue
                entries.append(entry)
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
    entries.sort(key=lambda x: x["ts"], reverse=True)
    for entry in entries[:limit]:
        meta = entry["metadata"]
        print(f"[{entry['ts'][:19]}] {meta['level']} {meta['priority']:5s} | {entry['action']}")
        print(f"  Reason: {entry['reasoning'][:100]}")
    print(f"\nTotal: {len(entries)} entries (showing {min(limit, len(entries))})")

def stats():
    if not LOG_FILE.exists():
        print("No decision logs found.")
        return
    level_counts = {"L1": 0, "L2": 0, "L3": 0}
    source_counts = {}
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                level = entry["metadata"].get("level", "unknown")
                source = entry["metadata"].get("source", "unknown")
                level_counts[level] = level_counts.get(level, 0) + 1
                source_counts[source] = source_counts.get(source, 0) + 1
            except (json.JSONDecodeError, KeyError):
                continue
    total = sum(level_counts.values())
    print(f"Decision Log Statistics (total: {total})")
    print(f"  L1 (routine):    {level_counts.get('L1', 0):5d} ({level_counts.get('L1', 0)/max(total,1)*100:.1f}%)")
    print(f"  L2 (contextual): {level_counts.get('L2', 0):5d} ({level_counts.get('L2', 0)/max(total,1)*100:.1f}%)")
    print(f"  L3 (reflective): {level_counts.get('L3', 0):5d} ({level_counts.get('L3', 0)/max(total,1)*100:.1f}%)")
    print(f"\nTop sources:")
    for source, count in sorted(source_counts.items(), key=lambda x: -x[1])[:5]:
        print(f"  {source}: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent Decision Logger")
    sub = parser.add_subparsers(dest="command")
    log_p = sub.add_parser("log", help="Record a decision")
    log_p.add_argument("--action", required=True)
    log_p.add_argument("--reasoning", required=True)
    log_p.add_argument("--level", default="L1", choices=["L1", "L2", "L3"])
    log_p.add_argument("--priority", default="low", choices=["low", "medium", "high", "critical"])
    log_p.add_argument("--source", default="manual")
    log_p.add_argument("--extra", default=None)
    q_p = sub.add_parser("query", help="Query decision logs")
    q_p.add_argument("--level", choices=["L1", "L2", "L3"])
    q_p.add_argument("--source")
    q_p.add_argument("--hours", type=int, default=24)
    q_p.add_argument("--limit", type=int, default=20)
    sub.add_parser("stats", help="Show decision statistics")
    args = parser.parse_args()
    if args.command == "log":
        entry = log_decision(args.action, args.reasoning, args.level, args.priority, args.source, args.extra)
        print(f"Logged: {entry['metadata']['level']} {args.action}")
    elif args.command == "query":
        query_logs(args.level, args.source, args.hours, args.limit)
    elif args.command == "stats":
        stats()
    else:
        parser.print_help()
