#!/usr/bin/env python3
"""
记忆锚定 — 把insight写入记忆文件
支持查询、追加、列出今日洞见
"""

from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_SKILL_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = _SKILL_DIR / "memory"
INSIGHTS_FILE = MEMORY_DIR / "insights" / "insights.jsonl"


def anchor(text: str, insight_type: str = "general", domain: str = "") -> dict:
    """锚定一条insight到记忆"""
    INSIGHTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "op": "insight",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "type": insight_type,
        "domain": domain,
        "text": text,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    with open(INSIGHTS_FILE, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record


def query(keyword: str = "", limit: int = 10) -> list[dict]:
    """查询insights"""
    if not INSIGHTS_FILE.exists():
        return []

    results = []
    with open(INSIGHTS_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if keyword:
                if keyword in record.get("text", ""):
                    results.append(record)
            else:
                results.append(record)

    return results[-limit:]


def list_today() -> list[dict]:
    """列出今日所有洞见"""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return [r for r in query(limit=100) if r.get("date") == today]


def main():
    parser = argparse.ArgumentParser(description="记忆锚定工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # anchor
    ap = subparsers.add_parser("anchor", help="锚定一条insight")
    ap.add_argument("--text", "-t", required=True, help="insight内容")
    ap.add_argument("--type", "-y", default="general", help="类型: general/judgment/pattern")
    ap.add_argument("--domain", "-d", default="", help="领域标签")

    # query
    qp = subparsers.add_parser("query", help="查询insights")
    qp.add_argument("--keyword", "-k", default="", help="关键词")
    qp.add_argument("--limit", "-n", type=int, default=10, help="返回条数")

    # today
    subparsers.add_parser("today", help="列出今日洞见")

    args = parser.parse_args()

    if args.command == "anchor":
        record = anchor(args.text, args.type, args.domain)
        print(f"✓ 锚定成功 [{record['date']}] {record['type']}: {record['text'][:80]}")

    elif args.command == "query":
        results = query(args.keyword, args.limit)
        if not results:
            print("无结果")
        for r in results:
            print(f"[{r['date']}] {r['type']}: {r['text'][:100]}")

    elif args.command == "today":
        results = list_today()
        print(f"=== 今日洞见 ({len(results)}) ===")
        for r in results:
            print(f"  • {r['text'][:100]}")


if __name__ == "__main__":
    sys.exit(main())
