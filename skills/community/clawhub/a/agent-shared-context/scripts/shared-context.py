#!/usr/bin/env python3
"""
Shared Context Manager — Cross-agent communication via shared files.

Usage:
  python3 scripts/shared-context.py add-trend --source reddit --topic "self-hosting" --score 1500
  python3 scripts/shared-context.py add-highlight --source moltbook --title "Fame vs Reliability" --url "..."
  python3 scripts/shared-context.py get-trends [--limit 5]
  python3 scripts/shared-context.py get-highlights [--limit 5]
  python3 scripts/shared-context.py cleanup [--hours 48]
"""
import argparse
import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

SHARED_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "shared"
TRENDS_FILE = SHARED_DIR / "trends.json"
HIGHLIGHTS_FILE = SHARED_DIR / "highlights.json"


def load_json(path):
    if not path.exists():
        return {"updated_at": None, "items": []}
    return json.loads(path.read_text())


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_add_trend(args):
    data = load_json(TRENDS_FILE)
    data["items"].append({
        "source": args.source,
        "topic": args.topic,
        "score": args.score,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    save_json(TRENDS_FILE, data)
    print(f"Added trend: [{args.source}] {args.topic} (score: {args.score})")


def cmd_add_highlight(args):
    data = load_json(HIGHLIGHTS_FILE)
    data["items"].append({
        "source": args.source,
        "title": args.title,
        "url": args.url or "",
        "summary": args.summary or "",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    save_json(HIGHLIGHTS_FILE, data)
    print(f"Added highlight: [{args.source}] {args.title}")


def cmd_get_trends(args):
    data = load_json(TRENDS_FILE)
    items = sorted(data["items"], key=lambda x: x.get("score", 0), reverse=True)
    items = items[:args.limit]
    if not items:
        print("No trends yet.")
        return
    print(f"Top {len(items)} trends (updated: {data.get('updated_at', 'never')}):")
    for i, item in enumerate(items, 1):
        age = ""
        try:
            ts = datetime.fromisoformat(item["timestamp"])
            hours = (datetime.now(timezone.utc) - ts).total_seconds() / 3600
            age = f" ({hours:.0f}h ago)"
        except Exception:
            pass
        print(f"  {i}. [{item['source']}] {item['topic']} — score {item.get('score', '?')}{age}")


def cmd_get_highlights(args):
    data = load_json(HIGHLIGHTS_FILE)
    items = data["items"][-args.limit:]
    if not items:
        print("No highlights yet.")
        return
    print(f"Latest {len(items)} highlights:")
    for i, item in enumerate(items, 1):
        print(f"  {i}. [{item['source']}] {item['title']}")
        if item.get("summary"):
            print(f"     {item['summary']}")


def cmd_cleanup(args):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=args.hours)
    for fpath in [TRENDS_FILE, HIGHLIGHTS_FILE]:
        data = load_json(fpath)
        before = len(data["items"])
        data["items"] = [
            item for item in data["items"]
            if datetime.fromisoformat(item["timestamp"]) > cutoff
        ]
        after = len(data["items"])
        save_json(fpath, data)
        print(f"{fpath.name}: {before} → {after} items (removed {before - after})")


def main():
    parser = argparse.ArgumentParser(description="Shared context for cross-agent communication")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("add-trend")
    p.add_argument("--source", required=True)
    p.add_argument("--topic", required=True)
    p.add_argument("--score", type=int, default=0)

    p = sub.add_parser("add-highlight")
    p.add_argument("--source", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--url", default="")
    p.add_argument("--summary", default="")

    p = sub.add_parser("get-trends")
    p.add_argument("--limit", type=int, default=5)

    p = sub.add_parser("get-highlights")
    p.add_argument("--limit", type=int, default=5)

    p = sub.add_parser("cleanup")
    p.add_argument("--hours", type=int, default=48)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    {"add-trend": cmd_add_trend, "add-highlight": cmd_add_highlight,
     "get-trends": cmd_get_trends, "get-highlights": cmd_get_highlights,
     "cleanup": cmd_cleanup}[args.command](args)


if __name__ == "__main__":
    main()
