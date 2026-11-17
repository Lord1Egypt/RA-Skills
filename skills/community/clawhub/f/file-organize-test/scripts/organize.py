#!/usr/bin/env python3
"""Organize files in a directory into subfolders.

Usage:
    python organize.py <directory> [--by type|ext|date] [--dry-run] [--recursive]

Grouping:
    type -> images, documents, videos, audio, archives, other (by extension)
    ext  -> one subfolder per extension (pdf/, jpg/, ...)
    date -> one subfolder per YYYY-MM (last-modified time)
"""

import argparse
import os
import shutil
import sys
from datetime import datetime

CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico", ".tiff"},
    "documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt",
                  ".md", ".csv", ".json", ".xml", ".yaml", ".yml", ".rtf", ".odt"},
    "videos": {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm"},
    "audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
}


def category_for(ext):
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "other"


def plan(root_dir, by, recursive):
    """Return a list of (source, destination) move actions."""
    actions = []
    for root, dirs, files in os.walk(root_dir):
        if not recursive and root != root_dir:
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in files:
            if name.startswith("."):
                continue
            src = os.path.join(root, name)
            if os.path.islink(src):
                continue
            if name == os.path.basename(os.path.abspath(__file__)):
                continue
            ext = os.path.splitext(name)[1].lower()
            if by == "ext":
                group = ext.lstrip(".") or "no-extension"
            elif by == "date":
                mtime = datetime.fromtimestamp(os.path.getmtime(src))
                group = mtime.strftime("%Y-%m")
            else:
                group = category_for(ext)
            dst_dir = os.path.join(root_dir, group)
            dst = os.path.join(dst_dir, name)
            if os.path.abspath(src) == os.path.abspath(dst):
                continue
            actions.append((src, dst))
    return actions


def unique_dst(dst):
    """Append a numeric suffix instead of overwriting an existing file."""
    if not os.path.exists(dst):
        return dst
    base, ext = os.path.splitext(dst)
    i = 1
    while True:
        candidate = f"{base}_{i}{ext}"
        if not os.path.exists(candidate):
            return candidate
        i += 1


def main():
    parser = argparse.ArgumentParser(description="Organize files into subfolders")
    parser.add_argument("directory", help="folder to organize")
    parser.add_argument("--by", choices=["type", "ext", "date"], default="type")
    parser.add_argument("--dry-run", action="store_true", help="only print the plan")
    parser.add_argument("--recursive", action="store_true", help="include subdirectories")
    args = parser.parse_args()

    root_dir = os.path.abspath(args.directory)
    if not os.path.isdir(root_dir):
        print(f"Not a directory: {args.directory}", file=sys.stderr)
        return 2

    actions = plan(root_dir, args.by, args.recursive)
    if not actions:
        print("Nothing to organize.")
        return 0

    moved = 0
    for src, dst in actions:
        rel_src = os.path.relpath(src, root_dir)
        rel_dst = os.path.relpath(dst, root_dir)
        if args.dry_run:
            print(f"[dry-run] {rel_src} -> {rel_dst}")
            continue
        dst = unique_dst(dst)
        rel_dst = os.path.relpath(dst, root_dir)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
        print(f"[moved] {rel_src} -> {rel_dst}")
        moved += 1

    total = len(actions) if args.dry_run else moved
    suffix = " (dry-run)" if args.dry_run else ""
    print(f"Summary: {total} file{'s' if total != 1 else ''}{suffix}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
