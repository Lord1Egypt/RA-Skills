#!/usr/bin/env python3
"""
mem_learn.py — Capture a learning from feedback, mistakes, or experience

Usage:
  python3 mem_learn.py --incident "what happened" --lesson "what to do differently" [--tags tag1,tag2] [--confidence high]

Stores the learning in memory/learnings/YYYY-MM-DD.md
Every 5 learnings, prompts for evolution review.
"""
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
LEARNINGS_DIR = MEMORY_DIR / "learnings"
PATTERNS_FILE = MEMORY_DIR / "learnings" / "patterns.md"


def ensure_dirs():
    MEMORY_DIR.mkdir(exist_ok=True)
    LEARNINGS_DIR.mkdir(exist_ok=True)


def count_learnings() -> int:
    """Count total learnings."""
    if not LEARNINGS_DIR.exists():
        return 0
    return len(list(LEARNINGS_DIR.glob("*.md")))


def save_learning(incident: str, lesson: str, context: str, tags: list[str], confidence: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    learning_file = LEARNINGS_DIR / f"{today}.md"
    
    # Append to today's file (or create it)
    entry = f"""
## Learning: {today}

### Incident
{incident}

### Lesson
{lesson}

### Context
{context or "General situation"}

### Tags
{' '.join(f'#{t.strip()}' for t in tags if t.strip())}

### Confidence
{confidence}

---
"""
    
    with open(learning_file, "a", encoding="utf-8") as f:
        f.write(entry)
    
    return learning_file.name


def check_evolve_needed() -> bool:
    """Every 5 learnings, flag for evolution review."""
    return count_learnings() % 5 == 0


def record_pattern(incident: str, lesson: str, tags: list[str]):
    """Record a recurring pattern."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    pattern_entry = f"""
## Pattern detected: {today}

### Recurring Issue
{incident}

### Adopted Response
{lesson}

### Tags
{' '.join(f'#{t.strip()}' for t in tags if t.strip())}

"""
    
    PATTERNS_FILE.parent.mkdir(exist_ok=True)
    with open(PATTERNS_FILE, "a", encoding="utf-8") as f:
        f.write(pattern_entry)


def main():
    parser = argparse.ArgumentParser(description="Capture a learning")
    parser.add_argument("--incident", "-i", required=True, help="What happened")
    parser.add_argument("--lesson", "-l", required=True, help="What to do differently")
    parser.add_argument("--context", "-c", default="", help="When does this apply")
    parser.add_argument("--tags", "-t", default="", help="Comma-separated tags")
    parser.add_argument("--confidence", "-d", default="medium",
                        choices=["high", "medium", "low"], help="Confidence level")
    parser.add_argument("--pattern", "-p", action="store_true", help="Mark as recurring pattern")
    args = parser.parse_args()
    
    ensure_dirs()
    
    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
    if not tags:
        tags = ["general"]
    
    file_name = save_learning(args.incident, args.lesson, args.context, tags, args.confidence)
    
    if args.pattern:
        record_pattern(args.incident, args.lesson, tags)
        print(f"✓ Pattern recorded in {PATTERNS_FILE.name}")
    
    evolve_needed = check_evolve_needed()
    total = count_learnings()
    
    print(f"✓ Learning saved ({total} total)")
    if evolve_needed:
        print(f"⚠ Evolution review recommended — {total} learnings stored")
        print("  Run: python3 mem_evolve.py")


if __name__ == "__main__":
    main()
