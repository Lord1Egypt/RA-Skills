#!/usr/bin/env python3
"""Restore a SKILL.md from a backup created by backup.py."""

import argparse
import hashlib
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--backup", required=True)
    args = parser.parse_args()

    skill = Path(args.skill)
    backup_arg = Path(args.backup)
    if backup_arg.is_file():
        backup = backup_arg
    else:
        candidates = []
        if backup_arg.exists():
            candidates = [
                p
                for p in backup_arg.iterdir()
                if p.is_file() and p.suffix != ".sha256"
            ]
        backup = max(candidates, key=lambda p: p.stat().st_mtime, default=None)
    if backup is None or not backup.exists():
        raise SystemExit("BACKUP_NOT_FOUND")

    checksum_path = backup.with_suffix(backup.suffix + ".sha256")
    if checksum_path.exists():
        expected = checksum_path.read_text(encoding="utf-8").strip()
        actual = hashlib.sha256(backup.read_bytes()).hexdigest()
        if expected != actual:
            raise SystemExit("BACKUP_CHECKSUM_MISMATCH")

    skill.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup, skill)
    print(f"restored={skill}")


if __name__ == "__main__":
    main()
