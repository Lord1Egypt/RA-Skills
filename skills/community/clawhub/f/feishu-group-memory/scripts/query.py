#!/usr/bin/env python3
"""
query.py — 本地记录检索（纯数据查询，不调用 LLM）

命令：
  search       --query TEXT --workspace DIR          关键词搜索
  list_records --period today|week|all --workspace   按时间段列出记录
"""

import argparse, json, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

RECORDS_FILENAME = "feishu-memory-records.jsonl"


def out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def err(msg):
    out({"error": msg})
    sys.exit(1)

def records_path(workspace):
    return Path(workspace).expanduser() / RECORDS_FILENAME

def load_all(workspace):
    rp = records_path(workspace)
    if not rp.exists():
        return []
    records = []
    with open(rp, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except Exception:
                continue
    return records


def cmd_search(args):
    records = load_all(args.workspace)
    if not records:
        out({"results": [], "total": 0, "query": args.query,
             "message": "暂无记录"})
        return

    query = args.query.lower()
    results = []
    for r in records:
        searchable = " ".join([
            r.get("summary", ""),
            r.get("key_entity", ""),
            r.get("raw_text", ""),
            r.get("text", ""),
            r.get("category", ""),
            r.get("sender", ""),
            json.dumps(r.get("fields", {}), ensure_ascii=False)
        ]).lower()
        if any(word in searchable for word in query.split()):
            results.append(r)

    # 按时间倒序，最多返回 30 条
    results.sort(key=lambda x: x.get("time", x.get("saved_at", "")), reverse=True)
    out({"results": results[:30], "total": len(results), "query": args.query})


def cmd_list_records(args):
    records = load_all(args.workspace)
    if not records:
        out({"records": [], "total": 0, "period": args.period})
        return

    now = datetime.now(tz=timezone.utc)
    if args.period == "today":
        cutoff = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif args.period == "week":
        cutoff = now - timedelta(days=7)
    else:
        cutoff = None

    filtered = []
    for r in records:
        if cutoff:
            time_str = r.get("time", r.get("saved_at", ""))
            if not time_str:
                continue
            try:
                # 支持多种时间格式
                if "T" in time_str:
                    dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
                else:
                    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
                if dt < cutoff:
                    continue
            except Exception:
                pass
        filtered.append(r)

    filtered.sort(key=lambda x: x.get("time", x.get("saved_at", "")), reverse=True)
    out({"records": filtered, "total": len(filtered), "period": args.period})


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("search")
    s.add_argument("--query",     required=True)
    s.add_argument("--workspace", default="~/.openclaw/workspace")

    l = sub.add_parser("list_records")
    l.add_argument("--period",    default="week", choices=["today", "week", "all"])
    l.add_argument("--workspace", default="~/.openclaw/workspace")

    args = p.parse_args()
    if   args.cmd == "search":       cmd_search(args)
    elif args.cmd == "list_records": cmd_list_records(args)
    else: err("请指定命令: search | list_records")

if __name__ == "__main__":
    main()
