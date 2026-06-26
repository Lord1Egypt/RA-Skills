#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
expnote - Experiment Notes System for AI Agents

Track, search, and learn from your experiments.

Usage:
  python expnote.py log --task "..." --outcome success|failure|partial --tags tag1,tag2 [--cmd "..." --error "..." --fix "..." --lesson "..."]
  python expnote.py search <query> [--limit N]
  python expnote.py similar <task_description> [--limit N]
  python expnote.py lessons [--tag TAG] [--limit N]
  python expnote.py stats
  python expnote.py distill --tag TAG --lesson "..."
"""

import json, sys, time, argparse, os, hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Fix Windows console encoding for Unicode output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def get_data_dir():
    """Get experiment notes data directory."""
    d = Path.home() / ".openclaw" / "memory" / "experiments"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_experiments_file():
    return get_data_dir() / "experiments.jsonl"


def get_lessons_file():
    return get_data_dir() / "lessons.jsonl"


def gen_id():
    """Generate a short unique ID."""
    ts = str(time.time()).encode()
    return f"exp_{hashlib.sha256(ts).hexdigest()[:12]}"


def load_experiments():
    """Load all experiments from JSONL file."""
    f = get_experiments_file()
    if not f.exists():
        return []
    experiments = []
    for line in f.read_text(encoding="utf-8").strip().split("\n"):
        if line.strip():
            try:
                experiments.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return experiments


def save_experiment(exp):
    """Append an experiment to the JSONL file."""
    f = get_experiments_file()
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(exp, ensure_ascii=False) + "\n")


def load_lessons():
    """Load distilled lessons."""
    f = get_lessons_file()
    if not f.exists():
        return []
    lessons = []
    for line in f.read_text(encoding="utf-8").strip().split("\n"):
        if line.strip():
            try:
                lessons.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return lessons


def save_lesson(lesson):
    """Append a lesson to the JSONL file."""
    f = get_lessons_file()
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(lesson, ensure_ascii=False) + "\n")


# --- Commands ---

def cmd_log(args):
    """Log a new experiment."""
    now = datetime.now(timezone(timedelta(hours=8)))
    exp = {
        "id": gen_id(),
        "timestamp": now.isoformat(),
        "task": args.task,
        "outcome": args.outcome,
        "attempt": {
            "command": args.cmd or "",
            "description": args.description or args.task,
        },
        "result": {
            "error": args.error or "",
            "fix": args.fix or "",
        },
        "tags": [t.strip() for t in args.tags.split(",")] if args.tags else [],
        "lesson": args.lesson or "",
    }
    save_experiment(exp)
    print(f"✅ Logged: [{exp['id']}] {args.task} → {args.outcome}")
    if exp["lesson"]:
        print(f"   💡 Lesson: {exp['lesson']}")


def cmd_search(args):
    """Full-text search experiments."""
    experiments = load_experiments()
    query = args.query.lower()
    results = []
    for exp in experiments:
        searchable = " ".join([
            exp.get("task", ""),
            exp.get("attempt", {}).get("description", ""),
            exp.get("attempt", {}).get("command", ""),
            exp.get("result", {}).get("error", ""),
            exp.get("result", {}).get("fix", ""),
            exp.get("lesson", ""),
            " ".join(exp.get("tags", [])),
        ]).lower()
        if query in searchable:
            results.append(exp)
    
    results = results[-args.limit:]  # most recent first
    results.reverse()
    
    if not results:
        print(f"🔍 No results for: {args.query}")
        return
    
    print(f"🔍 Found {len(results)} experiment(s):\n")
    for exp in results:
        icon = {"success": "✅", "failure": "❌", "partial": "⚠️"}.get(exp["outcome"], "❓")
        print(f"{icon} [{exp['id']}] {exp['task']}")
        print(f"   Time: {exp['timestamp'][:16]}")
        if exp["result"].get("error"):
            print(f"   Error: {exp['result']['error'][:100]}")
        if exp["result"].get("fix"):
            print(f"   Fix: {exp['result']['fix'][:100]}")
        if exp.get("lesson"):
            print(f"   💡 {exp['lesson'][:100]}")
        print()


def cmd_similar(args):
    """Find experiments with similar tasks."""
    experiments = load_experiments()
    task_words = set(args.task.lower().split())
    
    scored = []
    for exp in experiments:
        exp_words = set(exp.get("task", "").lower().split())
        tag_words = set(" ".join(exp.get("tags", [])).lower().split())
        overlap = len(task_words & (exp_words | tag_words))
        if overlap > 0:
            scored.append((overlap, exp))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    results = [s[1] for s in scored[:args.limit]]
    
    if not results:
        print(f"🔍 No similar experiments for: {args.task}")
        return
    
    print(f"🔍 Found {len(results)} similar experiment(s):\n")
    for exp in results:
        icon = {"success": "✅", "failure": "❌", "partial": "⚠️"}.get(exp["outcome"], "❓")
        print(f"{icon} [{exp['id']}] {exp['task']}")
        if exp["result"].get("error"):
            print(f"   ⚠️ Error: {exp['result']['error'][:100]}")
        if exp["result"].get("fix"):
            print(f"   🔧 Fix: {exp['result']['fix'][:100]}")
        if exp.get("lesson"):
            print(f"   💡 {exp['lesson'][:100]}")
        print()


def cmd_lessons(args):
    """Show distilled lessons, optionally filtered by tag."""
    experiments = load_experiments()
    tag_filter = args.tag.lower() if args.tag else None
    
    # Collect experiments with lessons
    learned = []
    for exp in experiments:
        if not exp.get("lesson"):
            continue
        if tag_filter and tag_filter not in [t.lower() for t in exp.get("tags", [])]:
            continue
        learned.append(exp)
    
    # Also load distilled lessons
    distilled = load_lessons()
    if tag_filter:
        distilled = [l for l in distilled if tag_filter in [t.lower() for t in l.get("tags", [])]]
    
    all_lessons = learned[-args.limit:] + distilled[-args.limit:]
    
    if not all_lessons:
        print("📚 No lessons found.")
        return
    
    print(f"📚 {len(all_lessons)} lesson(s):\n")
    for item in all_lessons:
        tags_str = ", ".join(item.get("tags", []))
        print(f"💡 [{tags_str}] {item['lesson']}")
        if item.get("task"):
            print(f"   From: {item['task']}")
        print()


def cmd_stats(args):
    """Show experiment statistics."""
    experiments = load_experiments()
    if not experiments:
        print("📊 No experiments recorded yet.")
        return
    
    total = len(experiments)
    success = sum(1 for e in experiments if e["outcome"] == "success")
    failure = sum(1 for e in experiments if e["outcome"] == "failure")
    partial = sum(1 for e in experiments if e["outcome"] == "partial")
    
    # Tag frequency
    tag_counts = {}
    for exp in experiments:
        for tag in exp.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Recent activity
    recent = experiments[-5:]
    
    print(f"📊 Experiment Statistics\n")
    print(f"Total:    {total}")
    print(f"✅ Success:  {success} ({success/total*100:.0f}%)")
    print(f"❌ Failure:  {failure} ({failure/total*100:.0f}%)")
    print(f"⚠️ Partial:  {partial} ({partial/total*100:.0f}%)")
    
    if top_tags:
        print(f"\nTop Tags:")
        for tag, count in top_tags:
            print(f"  #{tag}: {count}")
    
    lessons_count = sum(1 for e in experiments if e.get("lesson"))
    print(f"\nLessons captured: {lessons_count}")
    
    print(f"\nRecent:")
    for exp in recent:
        icon = {"success": "✅", "failure": "❌", "partial": "⚠️"}.get(exp["outcome"], "❓")
        print(f"  {icon} {exp['timestamp'][:10]} {exp['task'][:50]}")


def cmd_distill(args):
    """Save a distilled lesson from multiple experiments."""
    now = datetime.now(timezone(timedelta(hours=8)))
    lesson = {
        "id": gen_id(),
        "timestamp": now.isoformat(),
        "lesson": args.lesson,
        "tags": [t.strip() for t in args.tags.split(",")] if args.tags else [],
        "source": "distilled",
    }
    save_lesson(lesson)
    print(f"📚 Lesson saved: {args.lesson}")


def main():
    parser = argparse.ArgumentParser(
        prog="expnote",
        description="Experiment Notes System for AI Agents",
    )
    sub = parser.add_subparsers(dest="command")
    
    # log
    p_log = sub.add_parser("log", help="Log an experiment")
    p_log.add_argument("--task", required=True, help="What were you trying to do?")
    p_log.add_argument("--outcome", required=True, choices=["success", "failure", "partial"])
    p_log.add_argument("--tags", default="", help="Comma-separated tags")
    p_log.add_argument("--cmd", default="", help="Command or action attempted")
    p_log.add_argument("--description", default="", help="Detailed description")
    p_log.add_argument("--error", default="", help="Error encountered (if any)")
    p_log.add_argument("--fix", default="", help="How it was fixed")
    p_log.add_argument("--lesson", default="", help="Key takeaway")
    
    # search
    p_search = sub.add_parser("search", help="Search experiments")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--limit", type=int, default=10)
    
    # similar
    p_similar = sub.add_parser("similar", help="Find similar experiments")
    p_similar.add_argument("task", help="Task description to match")
    p_similar.add_argument("--limit", type=int, default=5)
    
    # lessons
    p_lessons = sub.add_parser("lessons", help="Show lessons learned")
    p_lessons.add_argument("--tag", default=None)
    p_lessons.add_argument("--limit", type=int, default=20)
    
    # stats
    sub.add_parser("stats", help="Show statistics")
    
    # distill
    p_distill = sub.add_parser("distill", help="Save a distilled lesson")
    p_distill.add_argument("--tags", required=True, help="Comma-separated tags")
    p_distill.add_argument("--lesson", required=True, help="The lesson")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cmds = {
        "log": cmd_log,
        "search": cmd_search,
        "similar": cmd_similar,
        "lessons": cmd_lessons,
        "stats": cmd_stats,
        "distill": cmd_distill,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
