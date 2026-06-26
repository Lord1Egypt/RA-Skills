#!/usr/bin/env python3
"""
mem_status.py — Show memory system health summary

Usage:
  python3 mem_status.py
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
MEMORY_DIR = WORKSPACE / "memory"
LEARNINGS_DIR = MEMORY_DIR / "learnings"
PATTERNS_FILE = MEMORY_DIR / "learnings" / "patterns.md"


def get_file_stats(path: Path) -> dict:
    if not path.exists():
        return {"exists": False, "size": 0, "lines": 0, "modified": None}
    
    stat = path.stat()
    content = path.read_text(encoding="utf-8", errors="ignore")
    return {
        "exists": True,
        "size": stat.st_size,
        "lines": len(content.split("\n")),
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
    }


def count_recent_daily_logs(days: int = 7) -> int:
    if not MEMORY_DIR.exists():
        return 0
    today = datetime.now()
    count = 0
    for d in range(days):
        date = today - timedelta(days=d)
        if (MEMORY_DIR / f"{date.strftime('%Y-%m-%d')}.md").exists():
            count += 1
    return count


def count_learnings() -> int:
    if not LEARNINGS_DIR.exists():
        return 0
    return len(list(LEARNINGS_DIR.glob("*.md")))


def count_patterns() -> int:
    if not PATTERNS_FILE.exists():
        return 0
    content = PATTERNS_FILE.read_text(encoding="utf-8", errors="ignore")
    return content.count("## Pattern")


def main():
    print("## Memory System Status\n")
    
    memory = get_file_stats(MEMORY_FILE)
    print(f"**MEMORY.md**: {'✓' if memory['exists'] else '✗'} {memory['modified'] or 'missing'} — {memory['lines']} lines\n")
    
    recent_logs = count_recent_daily_logs(7)
    print(f"**Daily logs**: {recent_logs}/7 days covered (last week)\n")
    
    learnings = count_learnings()
    print(f"**Learnings**: {learnings} captured\n")
    
    patterns = count_patterns()
    print(f"**Patterns**: {patterns} identified\n")
    
    # Health indicators
    print("**Health:**")
    if memory['exists'] and memory['lines'] > 50:
        print("  ✓ MEMORY.md is well-developed")
    elif memory['exists']:
        print("  △ MEMORY.md is thin — consider adding more context")
    else:
        print("  ✗ MEMORY.md missing — create it to enable long-term memory")
    
    if recent_logs >= 5:
        print(f"  ✓ Good daily log coverage ({recent_logs}/7)")
    elif recent_logs > 0:
        print(f"  △ Sparse daily logs ({recent_logs}/7)")
    else:
        print("  ✗ No daily logs — start capturing session context")
    
    if learnings >= 5:
        print(f"  ✓ Rich learnings corpus ({learnings})")
    elif learnings > 0:
        print(f"  △ {learnings} learnings — will grow with feedback")
    else:
        print("  △ No learnings yet — use mem_learn.py when you get feedback")
    
    if patterns > 0:
        print(f"  ✓ {patterns} patterns identified — behavioral guidelines improving")
    
    print()


if __name__ == "__main__":
    main()
