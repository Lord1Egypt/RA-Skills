#!/usr/bin/env python3
"""
timeline_manager.py — Manage the document processing timeline.

The timeline is stored at ~/.doc-process-timeline.json.

Commands:
  add     Add a new entry
  show    Display the timeline (optionally filtered)
  save    Export to a Markdown file
  export  Export to JSON
  delete  Delete an entry by ID
  clear   Remove all entries
  stats   Show summary statistics

Usage:
  python timeline_manager.py add --type "Receipt Scanner" --source "receipt.jpg" --summary "Coffee $13.12"
  python timeline_manager.py show
  python timeline_manager.py show --type "Contract Analyzer"
  python timeline_manager.py save --output ~/Documents/doc-process-timeline.md
  python timeline_manager.py export --output timeline.json
  python timeline_manager.py delete --id abc123
  python timeline_manager.py clear
  python timeline_manager.py stats
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import uuid


TIMELINE_PATH = Path.home() / ".doc-process-timeline.json"


# ---------------------------------------------------------------------------
# Storage helpers
# ---------------------------------------------------------------------------

def _load() -> list[dict]:
    if not TIMELINE_PATH.exists():
        return []
    try:
        with TIMELINE_PATH.open(encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _save(entries: list[dict]) -> None:
    TIMELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TIMELINE_PATH.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _display_dt(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return iso


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_add(args: argparse.Namespace) -> int:
    entries = _load()
    entry = {
        "id": uuid.uuid4().hex[:8],
        "timestamp": _now_iso(),
        "type": args.type,
        "source": args.source,
        "summary": args.summary,
    }
    entries.append(entry)
    _save(entries)
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    entries = _load()
    filter_type = getattr(args, "type", None)

    if filter_type:
        entries = [e for e in entries if e.get("type", "").lower() == filter_type.lower()]

    if not entries:
        if filter_type:
            print(f"No entries found for type: {filter_type}")
        else:
            print("No documents have been processed yet. Your timeline will appear here after you process your first document.")
        return 0

    print("#### Document Processing History\n")
    print(f"| # | Date & Time | Mode | Document | Summary |")
    print("|---|---|---|---|---|")
    for i, e in enumerate(entries, 1):
        print(
            f"| {i} "
            f"| {_display_dt(e.get('timestamp', ''))} "
            f"| {e.get('type', '')} "
            f"| {e.get('source', '')} "
            f"| {e.get('summary', '')} |"
        )
    print(f"\n**Total documents processed: {len(entries)}**")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    entries = _load()
    if not entries:
        print("No entries in timeline.")
        return 0

    from collections import Counter
    type_counts = Counter(e.get("type", "Unknown") for e in entries)
    most_common_type, most_common_count = type_counts.most_common(1)[0]

    timestamps = [e.get("timestamp", "") for e in entries if e.get("timestamp")]
    timestamps.sort()
    date_from = _display_dt(timestamps[0]) if timestamps else "?"
    date_to = _display_dt(timestamps[-1]) if timestamps else "?"

    distinct_types = sorted(type_counts.keys())

    print("#### Timeline Statistics\n")
    print(f"| Stat | Value |")
    print("|---|---|")
    print(f"| Total Documents Processed | {len(entries)} |")
    print(f"| Most Used Mode | {most_common_type} ({most_common_count}×) |")
    print(f"| Date Range | {date_from} → {date_to} |")
    print(f"| Document Types | {', '.join(distinct_types)} |")
    return 0


def cmd_save(args: argparse.Namespace) -> int:
    entries = _load()
    output_path = Path(args.output).expanduser()

    lines = []
    lines.append("# Document Processing Timeline")
    lines.append("")
    lines.append(f"*Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    lines.append("")

    if not entries:
        lines.append("No documents processed yet.")
    else:
        lines.append(f"**Total entries: {len(entries)}**")
        lines.append("")
        lines.append("| # | Date & Time | Mode | Document | Summary |")
        lines.append("|---|---|---|---|---|")
        for i, e in enumerate(entries, 1):
            lines.append(
                f"| {i} "
                f"| {_display_dt(e.get('timestamp', ''))} "
                f"| {e.get('type', '')} "
                f"| {e.get('source', '')} "
                f"| {e.get('summary', '')} |"
            )

        # Stats
        from collections import Counter
        type_counts = Counter(e.get("type", "Unknown") for e in entries)
        lines.append("")
        lines.append("## Statistics")
        lines.append("")
        lines.append("| Mode | Count |")
        lines.append("|---|---|")
        for mode, count in type_counts.most_common():
            lines.append(f"| {mode} | {count} |")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Timeline saved to {output_path} ({len(entries)} entries).")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    entries = _load()
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    print(f"Timeline exported to {output_path} ({len(entries)} entries).")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    entries = _load()
    original_count = len(entries)
    entries = [e for e in entries if e.get("id") != args.id]
    if len(entries) == original_count:
        print(f"No entry found with id: {args.id}", file=sys.stderr)
        return 1
    _save(entries)
    print(f"Entry {args.id} deleted. ({len(entries)} entries remain)")
    return 0


def cmd_clear(args: argparse.Namespace) -> int:
    confirm = getattr(args, "yes", False)
    if not confirm:
        answer = input("Are you sure you want to clear all timeline entries? [y/N] ")
        if answer.strip().lower() != "y":
            print("Cancelled.")
            return 0
    _save([])
    print("Timeline cleared.")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="timeline_manager",
        description="Manage the document processing timeline.",
    )
    sub = parser.add_subparsers(dest="command")

    # add
    p_add = sub.add_parser("add", help="Add a new entry")
    p_add.add_argument("--type", required=True, help="Mode name (e.g. 'Receipt Scanner')")
    p_add.add_argument("--source", required=True, help="Filename or description")
    p_add.add_argument("--summary", required=True, help="One-line summary of findings")

    # show
    p_show = sub.add_parser("show", help="Display timeline")
    p_show.add_argument("--type", help="Filter by mode name")

    # stats
    sub.add_parser("stats", help="Show summary statistics")

    # save
    p_save = sub.add_parser("save", help="Export timeline to Markdown")
    p_save.add_argument("--output", default="~/Documents/doc-process-timeline.md")

    # export
    p_export = sub.add_parser("export", help="Export timeline to JSON")
    p_export.add_argument("--output", required=True)

    # delete
    p_del = sub.add_parser("delete", help="Delete an entry by ID")
    p_del.add_argument("--id", required=True)

    # clear
    p_clear = sub.add_parser("clear", help="Remove all entries")
    p_clear.add_argument("--yes", action="store_true", help="Skip confirmation prompt")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "add": cmd_add,
        "show": cmd_show,
        "stats": cmd_stats,
        "save": cmd_save,
        "export": cmd_export,
        "delete": cmd_delete,
        "clear": cmd_clear,
    }

    if not args.command:
        parser.print_help()
        return 0

    fn = commands.get(args.command)
    if not fn:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1

    return fn(args)


if __name__ == "__main__":
    sys.exit(main())
