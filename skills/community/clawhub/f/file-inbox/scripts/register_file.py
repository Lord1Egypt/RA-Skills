#!/usr/bin/env python3
"""
register_file.py — Register a file in the inbox index.

Usage:
  python3 register_file.py --path <file> --direction in|out [options]

Options:
  --path PATH         Path to the file to register (required)
  --direction DIR     'in' (received from user) or 'out' (sent to user) (required)
  --sender NAME       Sender name or channel (for inbound files)
  --dest NAME         Destination name or channel (for outbound files)
  --tags TAGS         Space-separated tags with # prefix, e.g. "#research #논문"
  --notes TEXT        Brief description or context for the file
  --copy              Copy the file instead of moving it (default: move)
  --inbox DIR         Inbox root directory (default: inbox/)
"""

import argparse
import json
import mimetypes
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


# ── Auto-tagging rules ────────────────────────────────────────────────────────

EXT_TAGS = {
    # Documents
    ".pdf": "#pdf #document",
    ".doc": "#doc #document",
    ".docx": "#docx #document",
    ".pptx": "#pptx #slides",
    ".ppt": "#ppt #slides",
    ".xlsx": "#xlsx #spreadsheet",
    ".xls": "#xls #spreadsheet",
    ".txt": "#text",
    ".md": "#markdown",
    ".rst": "#docs",
    # Data
    ".csv": "#csv #data",
    ".tsv": "#tsv #data",
    ".json": "#json #data",
    ".jsonl": "#jsonl #data",
    ".parquet": "#parquet #data",
    ".feather": "#feather #data",
    ".pkl": "#pickle #data",
    ".npy": "#numpy #data",
    ".npz": "#numpy #data",
    # Images
    ".png": "#image",
    ".jpg": "#image",
    ".jpeg": "#image",
    ".gif": "#image",
    ".svg": "#svg #image",
    ".webp": "#image",
    # Code
    ".py": "#python #code",
    ".js": "#javascript #code",
    ".ts": "#typescript #code",
    ".sh": "#shell #code",
    ".r": "#r #code",
    ".ipynb": "#notebook #code",
    # Archives
    ".zip": "#archive",
    ".tar": "#archive",
    ".gz": "#archive",
    ".7z": "#archive",
    # Other
    ".mp4": "#video",
    ".mp3": "#audio",
    ".wav": "#audio",
    ".xml": "#xml",
    ".yaml": "#yaml",
    ".yml": "#yaml",
    ".toml": "#toml",
}


def auto_tags(filepath: Path) -> str:
    ext = filepath.suffix.lower()
    return EXT_TAGS.get(ext, "")


# ── Helpers ───────────────────────────────────────────────────────────────────

def find_workspace_root(start: Path) -> Path:
    """Walk up from start to find the workspace root (contains inbox/ or skills/)."""
    current = start.resolve()
    for _ in range(10):
        if (current / "skills").is_dir() or (current / "inbox").is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    # Fallback: use cwd
    return Path.cwd()


def load_meta(meta_path: Path) -> dict:
    with open(meta_path) as f:
        return json.load(f)


def save_meta(meta_path: Path, meta: dict):
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        f.write("\n")


def merge_tags(auto: str, user: str) -> str:
    """Merge auto and user tags, deduplicate."""
    all_tags = []
    seen = set()
    for tag in (auto + " " + user).split():
        tag = tag.strip()
        if tag and tag not in seen:
            seen.add(tag)
            all_tags.append(tag)
    return " ".join(all_tags)


def sanitize_filename(name: str) -> str:
    """Remove characters unsafe for filenames."""
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)


def update_index(index_path: Path, row: dict, meta: dict):
    """Insert a new row at the top of the Recent Files table in INDEX.md."""
    content = index_path.read_text(encoding="utf-8") if index_path.exists() else ""

    direction_icon = "⬇️ in" if row["direction"] == "in" else "⬆️ out"
    sender_dest = row.get("sender") or f"→ {row.get('dest', '')}"
    notes = row.get("notes", "").replace("|", "\\|")
    tags = row.get("tags", "")

    new_row = (
        f"| {row['id']} | {direction_icon} | {row['filename']} | {row['filetype']} "
        f"| {tags} | {sender_dest} | {row['date']} | {notes} |"
    )

    # Find the table header separator line and insert after it
    table_header_re = re.compile(
        r"(\| ID \| Direction \|.*\n\|[-| ]+\|\n)", re.MULTILINE
    )
    match = table_header_re.search(content)
    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + new_row + "\n" + content[insert_pos:]
    else:
        # No table yet — append
        content += f"\n{new_row}\n"

    # Update stats header
    total = meta["total"]
    inbound = meta["inbound"]
    outbound = meta["outbound"]
    today = row["date"]

    stats_line = f"> Total: {total} files | Inbound: {inbound} | Outbound: {outbound}"
    updated_line = f"> Last updated: {today}"

    content = re.sub(r"> Total:.*", stats_line, content)
    content = re.sub(r"> Last updated:.*", updated_line, content)

    index_path.write_text(content, encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Register a file in the inbox")
    parser.add_argument("--path", required=True, help="Path to the file")
    parser.add_argument("--direction", required=True, choices=["in", "out"])
    parser.add_argument("--sender", default="", help="Sender name/channel (inbound)")
    parser.add_argument("--dest", default="", help="Destination name/channel (outbound)")
    parser.add_argument("--tags", default="", help="Space-separated #tags")
    parser.add_argument("--notes", default="", help="Brief description")
    parser.add_argument("--copy", action="store_true", help="Copy instead of move")
    parser.add_argument("--inbox", default="inbox", help="Inbox root directory")
    args = parser.parse_args()

    src = Path(args.path).resolve()
    if not src.exists():
        print(f"Error: file not found: {src}", file=sys.stderr)
        sys.exit(1)

    workspace = find_workspace_root(src)
    inbox_root = workspace / args.inbox

    if not inbox_root.exists():
        print(f"Error: inbox not initialized at {inbox_root}. Run init_inbox.sh first.", file=sys.stderr)
        sys.exit(1)

    meta_path = inbox_root / ".meta.json"
    index_path = inbox_root / "INDEX.md"
    meta = load_meta(meta_path)

    # Assign ID
    file_id = f"F-{meta['nextId']:03d}"
    today = datetime.today().strftime("%Y-%m-%d")
    year_month = datetime.today().strftime("%Y-%m")

    # Determine destination subdir
    subdir_name = "inbound" if args.direction == "in" else "outbound"
    dest_dir = inbox_root / subdir_name / year_month
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Build destination filename: F-NNN_original-name
    safe_name = sanitize_filename(src.name)
    dest_filename = f"{file_id}_{safe_name}"
    dest_path = dest_dir / dest_filename

    # Move or copy
    if args.copy:
        shutil.copy2(str(src), str(dest_path))
        action = "Copied"
    else:
        shutil.move(str(src), str(dest_path))
        action = "Moved"

    # Determine file type from extension
    filetype = src.suffix.lstrip(".").lower() or "file"

    # Merge tags
    tags = merge_tags(auto_tags(src), args.tags)

    # Update meta
    meta["nextId"] += 1
    meta["total"] += 1
    if args.direction == "in":
        meta["inbound"] += 1
    else:
        meta["outbound"] += 1
    meta["lastUpdated"] = today
    save_meta(meta_path, meta)

    # Build row data
    row = {
        "id": file_id,
        "direction": args.direction,
        "filename": dest_filename,
        "filetype": filetype,
        "tags": tags,
        "sender": args.sender,
        "dest": args.dest,
        "date": today,
        "notes": args.notes,
    }

    update_index(index_path, row, meta)

    print(f"{action} to: {dest_path}")
    print(f"Registered as {file_id} | {filetype} | {tags}")
    print(f"INDEX.md updated.")


if __name__ == "__main__":
    main()
