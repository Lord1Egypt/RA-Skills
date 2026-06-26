#!/usr/bin/env python3
"""
Consolidation helper: scan recent daily memory files and suggest
MEMORY.md updates. Run periodically (every 3-7 days) to identify
what deserves promotion from episodic daily notes to semantic memory.

Usage:
    python3 consolidate.py [--days N] [--memory-dir DIR]
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

CATEGORIES = {
    "preference": {
        "patterns": [r"(喜欢|不喜欢|prefer|like|don't like|喜欢|preferred tool|favorite|偏好|习惯)"],
        "label": "PREFERENCE — consider adding to MEMORY.md's User Preferences section",
    },
    "decision": {
        "patterns": [r"(决定|决策|decided|决定|选择|choose|选|settled on|went with)"],
        "label": "DECISION — consider adding to MEMORY.md as a long-term record",
    },
    "lesson": {
        "patterns": [r"(教训|learned|学到|lesson|学到了|下次注意|mistake|error|坑|踩坑)"],
        "label": "LESSON — consider adding to MEMORY.md's Lessons Learned section",
    },
    "project": {
        "patterns": [r"(项目|project|repo|仓库|deployed|上线|发布|release|版本)"],
        "label": "PROJECT — update project context in MEMORY.md",
    },
    "relationship": {
        "patterns": [r"(认识|met|见了|见了|together|co-work|同事|朋友)"],
        "label": "SOCIAL — significant relationship detail",
    },
}


def find_memory_files(memory_dir: Path, days: int) -> list[Path]:
    """Find daily note files within the specified number of days."""
    cutoff = datetime.now() - timedelta(days=days)
    files = []
    for f in sorted(memory_dir.glob("*.md"), reverse=True):
        # Parse date from filename YYYY-MM-DD.md
        m = re.match(r"(\d{4}-\d{2}-\d{2})", f.stem)
        if m:
            try:
                fdate = datetime.strptime(m.group(1), "%Y-%m-%d")
                if fdate >= cutoff:
                    files.append(f)
            except ValueError:
                continue
    return files


def classify_line(line: str) -> str | None:
    """Classify a line into a category if it matches known patterns."""
    for cat, info in CATEGORIES.items():
        for pat in info["patterns"]:
            if re.search(pat, line, re.IGNORECASE):
                return cat
    return None


def scan_files(files: list[Path]) -> dict[str, list[tuple[str, str]]]:
    """Scan files and return categorized items."""
    categorized: dict[str, list[tuple[str, str]]] = {c: [] for c in CATEGORIES}
    for f in files:
        content = f.read_text(encoding="utf-8")
        # Simple line-by-line scan (skip headers and empty lines)
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("<!--"):
                continue
            cat = classify_line(line)
            if cat:
                categorized[cat].append((f.stem, line))
    return categorized


def print_report(categorized: dict[str, list[tuple[str, str]]]):
    """Print a human-readable consolidation suggestion report."""
    print("=" * 60)
    print("Memory Consolidation Report")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    has_content = False
    for cat, label_info in [
        ("preference", CATEGORIES["preference"]["label"]),
        ("decision", CATEGORIES["decision"]["label"]),
        ("lesson", CATEGORIES["lesson"]["label"]),
        ("project", CATEGORIES["project"]["label"]),
        ("relationship", CATEGORIES["relationship"]["label"]),
    ]:
        items = categorized.get(cat, [])
        if items:
            has_content = True
            print(f"\n## {label_info}")
            print("-" * 40)
            for date, line in items:
                # Clean up markdown bullets
                clean = re.sub(r"^[-*+]\s*", "", line)
                print(f"  [{date}] {clean}")

    if not has_content:
        print("\nNo significant items found for promotion.")
        print("Memory is up-to-date or all recent entries are transient.")

    print("\n" + "=" * 60)
    print("Review the items above and decide what to add to MEMORY.md.")
    print("Items already in MEMORY.md can be skipped.")


def main():
    parser = argparse.ArgumentParser(description="Suggest MEMORY.md updates from daily notes")
    parser.add_argument("--days", type=int, default=7, help="Days of history to scan (default: 7)")
    parser.add_argument(
        "--memory-dir",
        type=str,
        default=None,
        help="Path to memory directory (default: <workspace>/memory)",
    )
    args = parser.parse_args()

    # Find memory directory
    if args.memory_dir:
        memory_dir = Path(args.memory_dir)
    else:
        # Try to find workspace from common locations
        candidates = [
            Path.cwd() / "memory",
            Path.home() / ".openclaw" / "workspace" / "memory",
        ]
        memory_dir = None
        for c in candidates:
            if c.exists() and c.is_dir():
                memory_dir = c
                break

    if not memory_dir or not memory_dir.exists():
        print("Error: Could not find memory directory.", file=sys.stderr)
        print("Specify with --memory-dir or run from your workspace.", file=sys.stderr)
        sys.exit(1)

    files = find_memory_files(memory_dir, args.days)
    if not files:
        print(f"No memory files found in the last {args.days} days.")
        sys.exit(0)

    print(f"Scanning {len(files)} memory file(s)...")
    categorized = scan_files(files)
    print_report(categorized)


if __name__ == "__main__":
    main()
