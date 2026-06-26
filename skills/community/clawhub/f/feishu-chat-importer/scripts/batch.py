#!/usr/bin/env python3
"""
Batch driver for feishu-chat-importer skill.

Usage:
  python3 scripts/batch.py --dir <feishu_chat_dir> [--since YYYY-MM-DD] [--dry-run] [--verbose]

Reads feishu_chat_YYYYMMDD.json files from the source directory,
parses messages, groups by date, and writes episodic summaries to:
  memory/episodic/YYYY-MM-DD.md
"""

import argparse
import json
import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime

SCRIPTS_DIR = Path(__file__).parent


def parse_export(json_path: Path) -> list[dict]:
    """Run the feishu parser and yield episodic entry dicts."""
    parser_script = SCRIPTS_DIR / "parse_feishu.py"
    proc = subprocess.run(
        ["python", str(parser_script), str(json_path)],
        capture_output=True, text=True
    )
    if proc.returncode != 0:
        print(f"  Error parsing {json_path.name}: {proc.stderr.strip()}", file=sys.stderr)
        return []
    entries = []
    for line in proc.stdout.strip().splitlines():
        if line:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return entries


def main():
    parser = argparse.ArgumentParser(description="Import Feishu chat history into OpenClaw episodic memory")
    parser.add_argument("--dir", required=True, help="Directory containing feishu_chat_YYYYMMDD.json files")
    parser.add_argument("--since", help="Only process chats on or after this date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing anything")
    parser.add_argument("--verbose", action="store_true", help="Show message count and preview per chat")
    args = parser.parse_args()

    # Workspace and episodic output directory
    workspace = Path(os.environ.get("OPENCLAW_WORKSPACE", str(Path.home() / ".openclaw/workspace")))
    episodic_dir = workspace / "memory/episodic"

    base_dir = Path(args.dir).expanduser()
    if not base_dir.is_dir():
        print(f"Error: directory not found: {base_dir}", file=sys.stderr)
        sys.exit(1)

    since_date = None
    if args.since:
        since_date = datetime.strptime(args.since, "%Y-%m-%d").date()

    # Find all feishu_chat_YYYYMMDD.json files
    feishu_files = sorted(base_dir.glob("feishu_chat_*.json"))
    if not feishu_files:
        print(f"No feishu_chat_*.json files found in {base_dir}")
        return

    total_entries = 0
    written_entries = 0

    for json_file in feishu_files:
        print(f"Processing {json_file.name} (format: feishu)...")
        entries = parse_export(json_file)

        for entry in entries:
            entry_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
            if since_date and entry_date < since_date:
                continue

            total_entries += 1
            msg_count = entry.get("message_count", 0)
            source = entry.get("source", "")

            print(f"  • {entry['date']} — {msg_count} messages from {source}")
            if args.verbose:
                # Show first 120 chars of first message as preview
                content = entry.get("content", "")
                first_line = content.split("\n")[3] if "\n" in content else content
                preview = first_line[:120].replace("\n", " ").strip()
                if preview:
                    print(f"    └─ {preview}...")

            if not args.dry_run:
                episodic_dir.mkdir(parents=True, exist_ok=True)
                mem_file = episodic_dir / f"{entry['date']}.md"

                # Check if this source+date combo already exists
                marker = f"Source: `{source}`"
                already_in_episodic = (
                    mem_file.exists() and marker in mem_file.read_text(encoding="utf-8")
                )

                if not already_in_episodic:
                    entry_content = entry["content"]
                    # If file exists, append; if not, create with header
                    if mem_file.exists():
                        existing = mem_file.read_text(encoding="utf-8")
                        # Avoid double headers if already has episodic content
                        entry_content = "\n\n---\n\n" + entry_content
                    else:
                        entry_content = (
                            f"# Episodic Memory — {entry['date']}\n\n"
                            + "> Imported from Feishu chat history via feishu-chat-importer\n\n"
                            + entry_content
                        )

                    with open(mem_file, "a", encoding="utf-8") as f:
                        f.write(entry_content)
                    written_entries += 1
                    print(f"    Wrote episodic entry to {mem_file.name}")
                else:
                    print(f"    (episodic entry already exists, skipping)")
            else:
                print(f"    (dry run, no writes)")

    print(f"\n{'Previewed' if args.dry_run else 'Imported'} {total_entries} episodic entries", end="")
    if not args.dry_run and written_entries > 0:
        print(f" ({written_entries} new writes)", end="")
    print(".")
    print(f"\nEpisodic files written to: {episodic_dir}")
    print("These will be processed by Dreaming and appear in Imported Insights / Memory Palace.")


if __name__ == "__main__":
    main()
