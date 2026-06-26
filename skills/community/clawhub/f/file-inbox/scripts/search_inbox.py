#!/usr/bin/env python3
"""
search_inbox.py — Search files registered in the inbox.

Usage:
  python3 search_inbox.py [options]

Options:
  --tag TAG           Filter by tag (e.g. research, #논문)
  --type TYPE         Filter by file type (e.g. pdf, csv, png)
  --direction DIR     Filter by direction: in | out
  --date-from DATE    Start date (YYYY-MM-DD)
  --date-to DATE      End date (YYYY-MM-DD)
  --query TEXT        Free-text search across ID, filename, tags, sender, notes
  --inbox DIR         Inbox root directory (default: inbox/)
  --limit N           Max results to show (default: 20)
"""

import argparse
import re
import sys
from pathlib import Path


def find_workspace_root(start: Path) -> Path:
    current = start.resolve()
    for _ in range(10):
        if (current / "skills").is_dir() or (current / "inbox").is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return Path.cwd()


def parse_index(index_path: Path) -> list[dict]:
    """Parse INDEX.md table rows into dicts."""
    if not index_path.exists():
        return []

    content = index_path.read_text(encoding="utf-8")
    rows = []
    in_table = False

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("| ID |"):
            in_table = True
            continue
        if in_table and stripped.startswith("|---"):
            continue
        if in_table and stripped.startswith("|"):
            parts = [p.strip() for p in stripped.strip("|").split("|")]
            if len(parts) >= 7:
                direction_raw = parts[1]
                direction = "in" if "in" in direction_raw else "out"
                rows.append({
                    "id": parts[0],
                    "direction": direction,
                    "filename": parts[2],
                    "type": parts[3],
                    "tags": parts[4],
                    "sender_dest": parts[5],
                    "date": parts[6],
                    "notes": parts[7] if len(parts) > 7 else "",
                    "_raw": stripped,
                })
        elif in_table and not stripped.startswith("|"):
            if stripped:  # non-empty non-table line ends the table
                in_table = False

    return rows


def matches(row: dict, args: argparse.Namespace) -> bool:
    # Direction filter
    if args.direction and row["direction"] != args.direction:
        return False

    # Type filter
    if args.type:
        ftype = args.type.lstrip(".")
        if row["type"].lower() != ftype.lower():
            return False

    # Tag filter
    if args.tag:
        tag = args.tag if args.tag.startswith("#") else f"#{args.tag}"
        if tag.lower() not in row["tags"].lower():
            return False

    # Date range filter
    if args.date_from and row["date"] < args.date_from:
        return False
    if args.date_to and row["date"] > args.date_to:
        return False

    # Free-text query (searches all fields)
    if args.query:
        query = args.query.lower()
        searchable = " ".join([
            row["id"], row["filename"], row["tags"],
            row["sender_dest"], row["notes"], row["type"]
        ]).lower()
        if query not in searchable:
            return False

    return True


def format_results(rows: list[dict]) -> str:
    if not rows:
        return "No files found."

    header = f"Found {len(rows)} file(s):\n"
    sep = "-" * 80
    lines = [header, sep]
    for r in rows:
        direction_icon = "⬇️ IN " if r["direction"] == "in" else "⬆️ OUT"
        lines.append(
            f"{r['id']}  {direction_icon}  {r['filename']}"
        )
        lines.append(
            f"     Type: {r['type']}  |  Date: {r['date']}  |  {r['sender_dest']}"
        )
        if r["tags"]:
            lines.append(f"     Tags: {r['tags']}")
        if r["notes"]:
            lines.append(f"     Notes: {r['notes']}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Search the file inbox")
    parser.add_argument("--tag", default="", help="Filter by tag")
    parser.add_argument("--type", default="", help="Filter by file type")
    parser.add_argument("--direction", default="", choices=["", "in", "out"])
    parser.add_argument("--date-from", default="", dest="date_from")
    parser.add_argument("--date-to", default="", dest="date_to")
    parser.add_argument("--query", default="", help="Free-text search")
    parser.add_argument("--inbox", default="inbox", help="Inbox root directory")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    # At least one filter required
    if not any([args.tag, args.type, args.direction, args.date_from, args.date_to, args.query]):
        print("Please specify at least one filter. Use --help for options.")
        sys.exit(1)

    workspace = find_workspace_root(Path(__file__))
    inbox_root = workspace / args.inbox
    index_path = inbox_root / "INDEX.md"

    if not index_path.exists():
        print(f"Error: INDEX.md not found at {index_path}. Run init_inbox.sh first.")
        sys.exit(1)

    rows = parse_index(index_path)
    matched = [r for r in rows if matches(r, args)]
    matched = matched[:args.limit]

    print(format_results(matched))


if __name__ == "__main__":
    main()
