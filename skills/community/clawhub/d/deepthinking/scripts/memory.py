#!/usr/bin/env python3
"""
DeepThinking Long-Term Memory
==============================
Append-only memory log stored as plain text lines.
Each entry is a timestamped, tagged line — searchable via grep.
The agent uses this to connect ideas across sessions over time.

Storage: ~/.deepthinking/memory/engrams.log
Format:  YYYY-MM-DDTHH:MM:SS | <tags> | <content>

Design: append-only flat file. No DB. Grep is the query engine.
The agent calls `search` and gets back matching lines with context.
Over time, patterns emerge that no single session could reveal.
"""
import sys
import os
import re
import json
import subprocess
from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path.home() / ".deepthinking" / "memory"
ENGRAMS_FILE = MEMORY_DIR / "engrams.log"
INDEX_FILE = MEMORY_DIR / "tags.idx"


def ensure_dir():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    if not ENGRAMS_FILE.exists():
        ENGRAMS_FILE.touch()


def cmd_store(args):
    """Store a new engram. Usage: memory.py store <tags> <content>
    Tags are comma-separated. Example: memory.py store "fear,career" "User afraid of leaving stable job"
    """
    if len(args) < 2:
        print(json.dumps({"error": "usage: store <tags> <content>"}))
        return
    tags = args[0]
    content = " ".join(args[1:])
    ensure_dir()
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    line = f"{ts} | {tags} | {content}\n"
    with open(ENGRAMS_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    _update_index(tags)
    count = sum(1 for _ in open(ENGRAMS_FILE, encoding="utf-8"))
    print(json.dumps({"stored": True, "tags": tags, "total_engrams": count}))


def cmd_search(args):
    """Search engrams using grep. Returns matching lines with context.
    Usage: memory.py search <query> [--tags <tag>] [--after <date>] [--limit <n>]
    """
    if not args:
        print(json.dumps({"error": "usage: search <query> [--tags tag] [--after date] [--limit n]"}))
        return
    ensure_dir()
    if not ENGRAMS_FILE.exists() or ENGRAMS_FILE.stat().st_size == 0:
        print(json.dumps({"results": [], "count": 0}))
        return

    query = args[0]
    tags_filter = None
    after_date = None
    limit = 20

    i = 1
    while i < len(args):
        if args[i] == "--tags" and i + 1 < len(args):
            tags_filter = args[i + 1]
            i += 2
        elif args[i] == "--after" and i + 1 < len(args):
            after_date = args[i + 1]
            i += 2
        elif args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        else:
            i += 1

    # Use grep for speed on large files
    try:
        cmd = ["grep", "-i", "-n", query, str(ENGRAMS_FILE)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception:
        # Fallback to python
        lines = []
        with open(ENGRAMS_FILE, encoding="utf-8") as f:
            for num, line in enumerate(f, 1):
                if query.lower() in line.lower():
                    lines.append(f"{num}:{line.rstrip()}")

    # Apply filters
    filtered = []
    for raw in lines:
        parts = raw.split(":", 1)
        if len(parts) < 2:
            continue
        line_content = parts[1]
        # Tags filter
        if tags_filter:
            tag_section = line_content.split("|")[1].strip() if "|" in line_content else ""
            if tags_filter.lower() not in tag_section.lower():
                continue
        # Date filter
        if after_date:
            line_date = line_content[:10]
            if line_date < after_date:
                continue
        filtered.append(line_content.strip())

    results = filtered[:limit]
    print(json.dumps({"results": results, "count": len(results), "total_matches": len(filtered)}, ensure_ascii=False))


def cmd_themes(args):
    """Extract recurring themes from memory. Analyzes tag frequency and co-occurrence."""
    ensure_dir()
    if not ENGRAMS_FILE.exists():
        print(json.dumps({"themes": {}, "count": 0}))
        return

    tag_counts = {}
    cooccurrence = {}
    total = 0

    with open(ENGRAMS_FILE, encoding="utf-8") as f:
        for line in f:
            total += 1
            parts = line.split("|")
            if len(parts) < 3:
                continue
            tags = [t.strip().lower() for t in parts[1].split(",")]
            for t in tags:
                tag_counts[t] = tag_counts.get(t, 0) + 1
            # Co-occurrence pairs
            for j in range(len(tags)):
                for k in range(j + 1, len(tags)):
                    pair = tuple(sorted([tags[j], tags[k]]))
                    cooccurrence[pair] = cooccurrence.get(pair, 0) + 1

    # Sort by frequency
    sorted_tags = sorted(tag_counts.items(), key=lambda x: -x[1])[:15]
    sorted_pairs = sorted(cooccurrence.items(), key=lambda x: -x[1])[:10]

    print(json.dumps({
        "total_engrams": total,
        "top_tags": {t: c for t, c in sorted_tags},
        "co_occurring": {f"{a}+{b}": c for (a, b), c in sorted_pairs}
    }, ensure_ascii=False))


def cmd_recent(args):
    """Show most recent N engrams. Usage: memory.py recent [n]"""
    n = int(args[0]) if args else 10
    ensure_dir()
    if not ENGRAMS_FILE.exists():
        print(json.dumps({"results": [], "count": 0}))
        return
    try:
        result = subprocess.run(["tail", f"-{n}", str(ENGRAMS_FILE)],
                                capture_output=True, text=True, timeout=5)
        lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
    except Exception:
        with open(ENGRAMS_FILE, encoding="utf-8") as f:
            all_lines = f.readlines()
        lines = [l.strip() for l in all_lines[-n:]]
    print(json.dumps({"results": lines, "count": len(lines)}, ensure_ascii=False))


def cmd_connect(args):
    """Find connections between two concepts. Searches for engrams containing both."""
    if len(args) < 2:
        print(json.dumps({"error": "usage: connect <concept1> <concept2>"}))
        return
    ensure_dir()
    c1, c2 = args[0].lower(), args[1].lower()
    matches = []
    with open(ENGRAMS_FILE, encoding="utf-8") as f:
        for line in f:
            low = line.lower()
            if c1 in low and c2 in low:
                matches.append(line.strip())
    # Also find bridge concepts: lines with c1 sharing tags with lines with c2
    c1_tags = set()
    c2_tags = set()
    with open(ENGRAMS_FILE, encoding="utf-8") as f:
        for line in f:
            low = line.lower()
            parts = line.split("|")
            if len(parts) >= 3:
                tags = {t.strip().lower() for t in parts[1].split(",")}
                if c1 in low:
                    c1_tags.update(tags)
                if c2 in low:
                    c2_tags.update(tags)
    shared_tags = c1_tags & c2_tags
    print(json.dumps({
        "direct_matches": matches[:10],
        "shared_tags": list(shared_tags),
        "bridge_strength": len(shared_tags)
    }, ensure_ascii=False))


def cmd_stats(args):
    """Memory stats."""
    ensure_dir()
    if not ENGRAMS_FILE.exists():
        print(json.dumps({"total": 0, "size_bytes": 0}))
        return
    total = sum(1 for _ in open(ENGRAMS_FILE, encoding="utf-8"))
    size = ENGRAMS_FILE.stat().st_size
    # Date range
    first = last = ""
    with open(ENGRAMS_FILE, encoding="utf-8") as f:
        for line in f:
            if not first:
                first = line[:10]
            last = line[:10]
    print(json.dumps({
        "total_engrams": total,
        "size_bytes": size,
        "first_entry": first,
        "last_entry": last,
        "file": str(ENGRAMS_FILE)
    }))


def _update_index(tags):
    """Lightweight tag index for fast tag listing."""
    existing = set()
    if INDEX_FILE.exists():
        existing = set(INDEX_FILE.read_text().strip().split("\n"))
    new_tags = {t.strip().lower() for t in tags.split(",")}
    all_tags = existing | new_tags
    INDEX_FILE.write_text("\n".join(sorted(all_tags)))


COMMANDS = {
    "store": cmd_store,
    "search": cmd_search,
    "themes": cmd_themes,
    "recent": cmd_recent,
    "connect": cmd_connect,
    "stats": cmd_stats,
}


def main():
    if len(sys.argv) < 2:
        print("Usage: memory.py <command> [args...]")
        print(f"Commands: {', '.join(COMMANDS.keys())}")
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd in COMMANDS:
        COMMANDS[cmd](args)
    else:
        print(json.dumps({"error": f"unknown command: {cmd}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
