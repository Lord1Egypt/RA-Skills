#!/usr/bin/env python3
"""Backup a SKILL.md before structural changes and record a checksum."""

import argparse
import datetime
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
    if backup_arg.suffix:
        backup = backup_arg
    else:
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_arg.mkdir(parents=True, exist_ok=True)
        backup = backup_arg / f"{skill.name}-{stamp}"

    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(skill, backup)
    digest = hashlib.sha256(skill.read_bytes()).hexdigest()
    checksum_path = backup.with_suffix(backup.suffix + ".sha256")
    checksum_path.write_text(digest + "\n", encoding="utf-8")
    print(f"backup={backup}")
    print(f"checksum={digest}")


if __name__ == "__main__":
    main()
