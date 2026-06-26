#!/usr/bin/env python3
"""
mem_evolve.py — Review learnings, identify patterns, evolve behavioral guidelines

Usage:
  python3 mem_evolve.py [--dry-run]

This is the self-evolution loop:
1. Read recent learnings (last 30 days)
2. Identify patterns (recurring mistakes or effective strategies)
3. Generate behavioral updates for SOUL.md or AGENTS.md
4. Archive old learnings to patterns.md
"""
import argparse
import re
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
LEARNINGS_DIR = MEMORY_DIR / "learnings"
PATTERNS_FILE = MEMORY_DIR / "learnings" / "patterns.md"
SOUL_FILE = WORKSPACE / "SOUL.md"
AGENTS_FILE = WORKSPACE / "AGENTS.md"


def ensure_dirs():
    MEMORY_DIR.mkdir(exist_ok=True)
    LEARNINGS_DIR.mkdir(exist_ok=True)


def get_recent_learnings(days: int = 30) -> list[dict]:
    """Read all learnings from the last N days."""
    learnings = []
    if not LEARNINGS_DIR.exists():
        return learnings
    
    cutoff = datetime.now() - timedelta(days=days)
    
    for f in sorted(LEARNINGS_DIR.glob("*.md"), reverse=True):
        try:
            date_str = f.stem
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            if file_date < cutoff:
                break
            content = f.read_text(encoding="utf-8", errors="ignore")
            learnings.append({"date": date_str, "content": content, "file": f})
        except Exception:
            continue
    
    return learnings


def parse_learnings(learnings: list[dict]) -> list[dict]:
    """Parse structured learnings from raw content."""
    parsed = []
    
    for lr in learnings:
        # Extract sections from markdown
        content = lr["content"]
        
        incident = extract_section(content, "### Incident", "### Lesson")
        lesson = extract_section(content, "### Lesson", "### Context")
        tags = extract_tags(content)
        
        if lesson:
            parsed.append({
                "date": lr["date"],
                "incident": incident,
                "lesson": lesson,
                "tags": tags,
                "file": lr["file"],
            })
    
    return parsed


def extract_section(content: str, start_marker: str, end_marker: str) -> str:
    """Extract a section between two markdown headers."""
    pattern = re.escape(start_marker) + r"\s*\n(.*?)(?=\n##|###|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_tags(content: str) -> list[str]:
    """Extract hashtags from content."""
    return re.findall(r"#(\w+)", content)


def identify_patterns(learnings: list[dict]) -> list[dict]:
    """Find recurring themes in learnings."""
    # Count tag occurrences
    all_tags = []
    for lr in learnings:
        all_tags.extend(lr.get("tags", []))
    
    tag_counts = Counter(all_tags)
    recurring_tags = {tag for tag, count in tag_counts.items() if count >= 2}
    
    # Find lessons with recurring tags
    patterns = []
    for tag in recurring_tags:
        related = [lr for lr in learnings if tag in lr.get("tags", [])]
        if len(related) >= 2:
            patterns.append({
                "tag": tag,
                "count": len(related),
                "lessons": [lr["lesson"][:100] for lr in related[:3]],
            })
    
    return sorted(patterns, key=lambda x: x["count"], reverse=True)


def generate_evolution(patterns: list[dict], learnings: list[dict]) -> str:
    """Generate evolution report and suggested updates."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    lines = [f"# Evolution Report — {today}\n"]
    lines.append(f"Reviewed {len(learnings)} learnings, found {len(patterns)} patterns.\n")
    
    if patterns:
        lines.append("## Recurring Patterns\n")
        for p in patterns:
            lines.append(f"### #{p['tag']} ({p['count']} occurrences)\n")
            for lesson in p['lessons']:
                lines.append(f"- {lesson}...\n")
            lines.append("\n")
    
    # Suggested behavioral updates
    if patterns:
        lines.append("## Suggested Behavioral Updates\n")
        lines.append("Consider adding to SOUL.md or AGENTS.md:\n\n")
        for p in patterns[:3]:
            lines.append(f"**When handling #{p['tag']}:**\n")
            lines.append(f"- {p['lessons'][0]}\n\n")
    
    return "".join(lines)


def archive_old_learnings(learnings: list[dict], patterns: list[dict], days: int = 30):
    """Archive learnings older than N days to patterns.md."""
    if not patterns:
        return 0
    
    cutoff = datetime.now() - timedelta(days=days)
    archived = 0
    
    with open(PATTERNS_FILE, "a", encoding="utf-8") as pf:
        pf.write(f"\n## Archive: {datetime.now().strftime('%Y-%m-%d')}\n")
        
        for lr in learnings:
            try:
                file_date = datetime.strptime(lr["date"], "%Y-%m-%d")
                if file_date < cutoff:
                    # Archive this learning
                    pf.write(f"\n### {lr['date']}\n")
                    pf.write(f"**Incident:** {lr.get('incident', 'N/A')[:200]}\n")
                    pf.write(f"**Lesson:** {lr['lesson'][:200]}\n")
                    # Remove original file
                    lr["file"].unlink(missing_ok=True)
                    archived += 1
            except Exception:
                continue
    
    return archived


def main():
    parser = argparse.ArgumentParser(description="Self-evolution review")
    parser.add_argument("--dry-run", action="store_true", help="Show report without applying changes")
    parser.add_argument("--days", type=int, default=30, help="Review learnings from last N days")
    args = parser.parse_args()
    
    ensure_dirs()
    
    learnings = get_recent_learnings(args.days)
    if not learnings:
        print("No learnings found. Run mem_learn.py to capture lessons.")
        sys.exit(0)
    
    parsed = parse_learnings(learnings)
    patterns = identify_patterns(parsed)
    report = generate_evolution(patterns, parsed)
    
    print(report)
    
    if args.dry_run:
        print("\n[Dry run — no changes applied]")
    else:
        if patterns and len(learnings) >= 5:
            # Archive old learnings and apply updates
            archived = archive_old_learnings(parsed, patterns, args.days)
            if archived:
                print(f"\n✓ Archived {archived} old learnings to {PATTERNS_FILE.name}")
            print("\nReview the report above and manually update SOUL.md/AGENTS.md as needed.")


if __name__ == "__main__":
    main()
