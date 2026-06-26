#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Inbox JSONL to archive")
    ap.add_argument("--archive-dir", default=".learnings/archive", help="Archive directory")
    ap.add_argument("--keep-original", action="store_true", help="Copy instead of move")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        raise SystemExit(f"input not found: {src}")

    archive_dir = Path(args.archive_dir)
    archive_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    dst = archive_dir / f"{ts}-{src.name}"

    if args.keep_original:
        shutil.copy2(src, dst)
        action = "copied"
    else:
        shutil.move(str(src), str(dst))
        action = "moved"

    print(f"{action}: {src} -> {dst}")


if __name__ == "__main__":
    main()
