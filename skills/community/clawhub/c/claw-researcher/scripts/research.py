#!/usr/bin/env python3
"""
research.py — Research index manager for the deep-research skill.

Manages a lightweight index of research reports at ~/research/index.json.
Tracks reports, their metadata, and enables quick retrieval of past research.

Usage:
    python research.py init                          # Initialize ~/research/ and index
    python research.py add <slug> <title> [--depth D] [--confidence C] [--tags t1,t2]
    python research.py list [--tag TAG] [--since YYYY-MM-DD]
    python research.py show <slug>                   # Print report metadata
    python research.py search <query>                # Full-text search across reports
    python research.py cite <slug>                   # Extract citations from a report
    python research.py stats                         # Research stats summary
    python research.py link <slug> <related_slug>    # Link related reports
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

RESEARCH_DIR = Path.home() / "research"
INDEX_FILE = RESEARCH_DIR / "index.json"


def load_index() -> dict:
    if INDEX_FILE.exists():
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": 1, "reports": {}, "tags": {}, "links": []}


def save_index(index: dict):
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def cmd_init(_args):
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    index = load_index()
    save_index(index)
    print(f"Research directory initialized at {RESEARCH_DIR}")
    print(f"Index: {INDEX_FILE}")


def cmd_add(args):
    index = load_index()
    now = datetime.now(timezone.utc).isoformat()
    slug = args.slug

    report_path = RESEARCH_DIR / f"{slug}.md"
    entry = {
        "title": args.title,
        "slug": slug,
        "depth": args.depth or "standard",
        "confidence": args.confidence or "MEDIUM",
        "tags": [t.strip() for t in args.tags.split(",")] if args.tags else [],
        "created": now,
        "updated": now,
        "file": str(report_path),
        "sources_count": 0,
        "related": [],
    }

    # Count sources if report file already exists
    if report_path.exists():
        content = report_path.read_text(encoding="utf-8")
        sources = re.findall(r"^\[(\d+)\]", content, re.MULTILINE)
        entry["sources_count"] = len(sources)

    index["reports"][slug] = entry

    # Update tag index
    for tag in entry["tags"]:
        if tag not in index["tags"]:
            index["tags"][tag] = []
        if slug not in index["tags"][tag]:
            index["tags"][tag].append(slug)

    save_index(index)
    print(f"Added: {slug} — {args.title}")
    print(f"  Depth: {entry['depth']} | Confidence: {entry['confidence']}")
    if entry["tags"]:
        print(f"  Tags: {', '.join(entry['tags'])}")


def cmd_list(args):
    index = load_index()
    reports = index.get("reports", {})

    if not reports:
        print("No research reports found. Run 'research.py init' to get started.")
        return

    # Filter by tag
    if args.tag:
        slugs = index.get("tags", {}).get(args.tag, [])
        reports = {k: v for k, v in reports.items() if k in slugs}

    # Filter by date
    if args.since:
        since = datetime.fromisoformat(args.since).replace(tzinfo=timezone.utc)
        reports = {
            k: v
            for k, v in reports.items()
            if datetime.fromisoformat(v["created"]) >= since
        }

    if not reports:
        print("No matching reports.")
        return

    # Sort by created date descending
    sorted_reports = sorted(
        reports.values(), key=lambda r: r["created"], reverse=True
    )

    print(f"{'Slug':<30} {'Depth':<12} {'Conf':<8} {'Sources':<8} {'Date':<12} Title")
    print("-" * 100)
    for r in sorted_reports:
        date = r["created"][:10]
        print(
            f"{r['slug']:<30} {r['depth']:<12} {r['confidence']:<8} "
            f"{r['sources_count']:<8} {date:<12} {r['title']}"
        )


def cmd_show(args):
    index = load_index()
    report = index.get("reports", {}).get(args.slug)
    if not report:
        print(f"Report '{args.slug}' not found.")
        sys.exit(1)

    print(json.dumps(report, indent=2, ensure_ascii=False))


def cmd_search(args):
    query = args.query.lower()
    results = []

    for md_file in RESEARCH_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        if query in content.lower():
            # Find matching lines for context
            lines = content.split("\n")
            matches = [
                (i + 1, line.strip())
                for i, line in enumerate(lines)
                if query in line.lower()
            ]
            results.append((md_file.stem, matches[:3]))  # Top 3 matches per file

    if not results:
        print(f"No results for '{args.query}'")
        return

    print(f"Found '{args.query}' in {len(results)} report(s):\n")
    for slug, matches in results:
        print(f"  {slug}:")
        for line_no, line in matches:
            # Truncate long lines
            display = line[:120] + "..." if len(line) > 120 else line
            print(f"    L{line_no}: {display}")
        print()


def cmd_cite(args):
    report_path = RESEARCH_DIR / f"{args.slug}.md"
    if not report_path.exists():
        print(f"Report file not found: {report_path}")
        sys.exit(1)

    content = report_path.read_text(encoding="utf-8")

    # Extract citation lines (lines starting with [n])
    citations = re.findall(r"^\[(\d+)\]\s+(.+)$", content, re.MULTILINE)

    if not citations:
        print("No citations found in report.")
        return

    print(f"Citations from '{args.slug}' ({len(citations)} sources):\n")
    for num, text in citations:
        print(f"  [{num}] {text}")


def cmd_stats(_args):
    index = load_index()
    reports = index.get("reports", {})

    if not reports:
        print("No research reports yet.")
        return

    total = len(reports)
    total_sources = sum(r.get("sources_count", 0) for r in reports.values())
    depths = {}
    confidences = {}
    tags = {}

    for r in reports.values():
        d = r.get("depth", "unknown")
        depths[d] = depths.get(d, 0) + 1
        c = r.get("confidence", "unknown")
        confidences[c] = confidences.get(c, 0) + 1
        for t in r.get("tags", []):
            tags[t] = tags.get(t, 0) + 1

    print(f"Research Stats")
    print(f"{'='*40}")
    print(f"Total reports:    {total}")
    print(f"Total sources:    {total_sources}")
    print(f"Avg sources/report: {total_sources / total:.1f}")
    print()
    print("By depth:")
    for d, count in sorted(depths.items()):
        print(f"  {d:<15} {count}")
    print()
    print("By confidence:")
    for c, count in sorted(confidences.items()):
        print(f"  {c:<15} {count}")
    if tags:
        print()
        print("Top tags:")
        for t, count in sorted(tags.items(), key=lambda x: -x[1])[:10]:
            print(f"  {t:<20} {count}")


def cmd_link(args):
    index = load_index()
    reports = index.get("reports", {})

    if args.slug not in reports:
        print(f"Report '{args.slug}' not found.")
        sys.exit(1)
    if args.related not in reports:
        print(f"Report '{args.related}' not found.")
        sys.exit(1)

    # Add bidirectional link
    if args.related not in reports[args.slug].get("related", []):
        reports[args.slug].setdefault("related", []).append(args.related)
    if args.slug not in reports[args.related].get("related", []):
        reports[args.related].setdefault("related", []).append(args.slug)

    link_entry = {"a": args.slug, "b": args.related}
    if link_entry not in index.get("links", []):
        index.setdefault("links", []).append(link_entry)

    save_index(index)
    print(f"Linked: {args.slug} <-> {args.related}")


def main():
    parser = argparse.ArgumentParser(
        description="Research index manager for deep-research skill"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", help="Initialize research directory and index")

    add_p = sub.add_parser("add", help="Add/update a report in the index")
    add_p.add_argument("slug", help="Report slug (filename without .md)")
    add_p.add_argument("title", help="Report title")
    add_p.add_argument("--depth", choices=["quick", "standard", "deep", "exhaustive"])
    add_p.add_argument("--confidence", choices=["HIGH", "MEDIUM", "LOW"])
    add_p.add_argument("--tags", help="Comma-separated tags")

    list_p = sub.add_parser("list", help="List research reports")
    list_p.add_argument("--tag", help="Filter by tag")
    list_p.add_argument("--since", help="Filter by date (YYYY-MM-DD)")

    show_p = sub.add_parser("show", help="Show report metadata")
    show_p.add_argument("slug", help="Report slug")

    search_p = sub.add_parser("search", help="Full-text search across reports")
    search_p.add_argument("query", help="Search query")

    cite_p = sub.add_parser("cite", help="Extract citations from a report")
    cite_p.add_argument("slug", help="Report slug")

    sub.add_parser("stats", help="Show research statistics")

    link_p = sub.add_parser("link", help="Link related reports")
    link_p.add_argument("slug", help="First report slug")
    link_p.add_argument("related", help="Related report slug")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "init": cmd_init,
        "add": cmd_add,
        "list": cmd_list,
        "show": cmd_show,
        "search": cmd_search,
        "cite": cmd_cite,
        "stats": cmd_stats,
        "link": cmd_link,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
