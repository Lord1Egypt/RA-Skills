#!/usr/bin/env python3
"""backup-rotator: Smart backup rotation and retention manager.

Manages backup files with flexible retention policies:
- Daily: keep last N daily backups
- Weekly: keep last N weekly backups
- Monthly: keep last N monthly backups
- Grandpa-Father-Son (GFS) rotation strategy

Usage:
    python3 backup_rotator.py --backup /path/to/source /path/to/backup/dir
    python3 backup_rotator.py --rotate /path/to/backup/dir --name myproject
    python3 backup_rotator.py --dry-run /path/to/backup/dir
    python3 backup_rotator.py --backup /path/to/db.sqlite /backups --compress
    python3 backup_rotator.py --cron /path/to/config.json
"""

import argparse
import json
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path


DEFAULT_CONFIG = {
    "keep_daily": 7,
    "keep_weekly": 4,
    "keep_monthly": 3,
    "compress": False,
    "verify": True,
    "backup_name": "backup",
    "backup_prefix": "",
}


def get_timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def parse_backup_name(filename):
    """Parse a backup filename and extract metadata."""
    # Expected pattern: prefix_YYYYMMDD-HHMMSS.ext or prefix_YYYY-MM-DD.ext
    pattern = re.compile(
        r"(?P<name>.+?)_(?P<date>\d{4}[-]?\d{2}[-]?\d{2})[-_]?\d{0,6}\.(?P<ext>\w+)"
    )
    match = pattern.match(filename)
    if not match:
        return None
    return {
        "filename": filename,
        "name": match.group("name"),
        "date_str": match.group("date"),
        "ext": match.group("ext"),
    }


def classify_backup(date_str, now=None):
    """Classify a backup date as daily/weekly/monthly/other."""
    if now is None:
        now = datetime.now()
    try:
        # Handle YYYYMMDD or YYYY-MM-DD
        date_str_clean = date_str.replace("-", "")
        bd = datetime.strptime(date_str_clean, "%Y%m%d")
    except ValueError:
        return None

    days_ago = (now.date() - bd.date()).days
    if days_ago < 0:
        return "future"

    # Monthly: first backup of each month
    if bd.day <= 7 and bd.month != (now - timedelta(days=days_ago)).month:
        return "monthly"
    # Weekly: Sunday (iso weekday 7)
    if bd.isoweekday() == 7 and days_ago <= 35:
        return "weekly"
    # Daily: any other day
    if days_ago <= 7:
        return "daily"

    return "old"


def compute_checksum(filepath):
    """Compute SHA256 checksum of a file."""
    sha = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha.update(chunk)
        return sha.hexdigest()
    except (FileNotFoundError, PermissionError, OSError) as e:
        return f"error: {e}"


def create_backup(source, backup_dir, name="backup", compress=False, verify=True):
    """Create a new backup file."""
    source = Path(source).resolve()
    backup_dir = Path(backup_dir).resolve()
    backup_dir.mkdir(parents=True, exist_ok=True)

    if not source.exists():
        print(f"Error: source not found: {source}")
        return False

    ts = get_timestamp()
    src_name = source.name if source.is_file() else name

    if source.is_dir() and compress:
        # Compress directory to tar.gz
        backup_path = backup_dir / f"{src_name}_{ts}.tar.gz"
        print(f"  Compressing {source} → {backup_path} ...")
        result = subprocess.run(
            ["tar", "-czf", str(backup_path), "-C", str(source.parent), source.name],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  Error creating tar: {result.stderr}")
            return False
        print(f"  Created: {backup_path}")
    elif source.is_file():
        # Copy single file
        suffix = source.suffix or ".bak"
        backup_path = backup_dir / f"{src_name}_{ts}{suffix}"
        shutil.copy2(source, backup_path)
        print(f"  Copied: {backup_path}")
    elif source.is_dir():
        # Copy directory recursively
        backup_path = backup_dir / f"{src_name}_{ts}"
        shutil.copytree(source, backup_path)
        print(f"  Copied: {backup_path}")
    else:
        print(f"Error: unsupported source type: {source}")
        return False

    # Verify
    if verify and backup_path.exists():
        csum = compute_checksum(backup_path)
        file_size = os.path.getsize(backup_path)
        print(f"  Size:    {_format_size(file_size)}")
        print(f"  SHA256:  {csum[:16]}...{csum[-16:]}")

    return True


def _format_size(bytes_):
    for unit in ("B", "K", "M", "G", "T"):
        if bytes_ < 1024:
            return f"{bytes_:.1f}{unit}"
        bytes_ /= 1024
    return f"{bytes_:.1f}P"


def get_backup_files(backup_dir, backup_name=None):
    """List all backup files in a directory, sorted by date (newest first)."""
    backup_dir = Path(backup_dir)
    if not backup_dir.is_dir():
        print(f"Error: backup directory not found: {backup_dir}")
        return []

    backups = []
    for f in sorted(backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if not f.is_file():
            continue
        info = parse_backup_name(f.name)
        if info:
            if backup_name and backup_name not in info["name"]:
                continue
            info["path"] = str(f)
            info["size"] = os.path.getsize(f)
            backups.append(info)

    return backups


def plan_rotation(backups, config):
    """Plan which backups to keep and which to delete."""
    now = datetime.now()
    classify = {}
    keep = []
    delete = []

    for b in backups:
        cat = classify_backup(b["date_str"], now)
        if cat:
            b["category"] = cat
            if cat not in classify:
                classify[cat] = []
            classify[cat].append(b)

    # Keep most recent daily
    keep_count = 0
    for b in classify.get("daily", []):
        if keep_count < config.get("keep_daily", 7):
            keep.append(b)
            b["action"] = "keep (daily)"
            keep_count += 1
        else:
            delete.append(b)
            b["action"] = "delete (excess daily)"

    # Keep most recent weekly
    keep_count = 0
    for b in classify.get("weekly", []):
        if keep_count < config.get("keep_weekly", 4):
            keep.append(b)
            b["action"] = "keep (weekly)"
            keep_count += 1
        else:
            delete.append(b)
            b["action"] = "delete (excess weekly)"

    # Keep most recent monthly
    keep_count = 0
    for b in classify.get("monthly", []):
        if keep_count < config.get("keep_monthly", 3):
            keep.append(b)
            b["action"] = "keep (monthly)"
            keep_count += 1
        else:
            delete.append(b)
            b["action"] = "delete (excess monthly)"

    # Old backups beyond all retention
    for b in classify.get("old", []):
        delete.append(b)
        b["action"] = "delete (past retention)"

    # Sort keep by date (newest first), delete by date (oldest first)
    keep.sort(key=lambda x: x["date_str"], reverse=True)
    delete.sort(key=lambda x: x["date_str"])

    return keep, delete, classify


def execute_rotation(backup_dir, config, dry_run=False):
    """Execute backup rotation according to retention policy."""
    backups = get_backup_files(backup_dir, config.get("backup_name"))
    if not backups:
        print("  No backup files found.")
        return [], []

    keep, delete, classify = plan_rotation(backups, config)

    print(f"\n  Summary: {len(keep)} keep, {len(delete)} delete")
    print(f"  Categories: {', '.join(f'{k}: {len(v)}' for k, v in classify.items())}")

    if keep:
        print(f"\n  Keeping:")
        for b in keep:
            print(f"    ✅ {b['filename']} ({_format_size(b['size'])}) - {b['action']}")

    if delete:
        print(f"\n  Deleting:")
        for b in delete:
            if dry_run:
                print(f"    🔄 {b['filename']} ({_format_size(b['size'])}) - {b['action']} (dry run)")
            else:
                print(f"    🗑  {b['filename']} ({_format_size(b['size'])}) - {b['action']}")
                try:
                    os.remove(b["path"])
                except OSError as e:
                    print(f"    ⚠️  Error deleting {b['filename']}: {e}")

    return keep, delete


def verify_backups(backup_dir, backup_name=None):
    """Verify integrity of backup files in directory."""
    backups = get_backup_files(backup_dir, backup_name)
    if not backups:
        print("  No backup files to verify.")
        return

    print(f"\n  Verifying {len(backups)} backup files...")
    for b in backups:
        path = b["path"]
        file_size = os.path.getsize(path)
        if file_size == 0:
            print(f"    ⚠️  EMPTY: {b['filename']}")
            continue
        csum = compute_checksum(path)
        print(f"    ✅ {b['filename']} ({_format_size(file_size)}) SHA256: {csum[:16]}...{csum[-16:]}")


def list_backups(backup_dir, backup_name=None, detail=False):
    """List all backups with details."""
    backups = get_backup_files(backup_dir, backup_name)
    if not backups:
        print("  No backup files found.")
        return

    now = datetime.now()
    total_size = sum(b["size"] for b in backups)
    print(f"\n  Found {len(backups)} backup(s), total: {_format_size(total_size)}")
    print()

    for b in backups:
        cat = classify_backup(b["date_str"], now)
        age_days = (now.date() - _parse_date(b["date_str"])).days
        cat_icon = {"daily": "📅", "weekly": "📆", "monthly": "📦", "old": "🗄", "future": "🔮"}.get(cat, "📄")
        print(f"  {cat_icon} {b['filename']}")
        print(f"     Size: {_format_size(b['size'])} | Age: {age_days}d | Type: {cat}")


def _parse_date(date_str):
    try:
        return datetime.strptime(date_str.replace("-", ""), "%Y%m%d").date()
    except ValueError:
        return datetime.now().date()


def load_config(config_path):
    """Load configuration from JSON file."""
    try:
        with open(config_path) as f:
            cfg = json.load(f)
        merged = {**DEFAULT_CONFIG, **cfg}
        return merged
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config: {e}")
        return None


def print_config(config):
    """Print current configuration."""
    print("\n  Backup Rotation Configuration:")
    print(f"  {'='*40}")
    for k, v in config.items():
        if k == "backup_name":
            print(f"  Name prefix:       {v}")
        elif k == "backup_prefix":
            print(f"  Directory prefix:  {v or '(none)'}")
        elif k == "keep_daily":
            print(f"  Keep daily:        {v}")
        elif k == "keep_weekly":
            print(f"  Keep weekly:       {v}")
        elif k == "keep_monthly":
            print(f"  Keep monthly:      {v}")
        elif k == "compress":
            print(f"  Compress:          {'yes' if v else 'no'}")
        elif k == "verify":
            print(f"  Verify:            {'yes' if v else 'no'}")


def main():
    parser = argparse.ArgumentParser(description="Backup Rotation Manager")
    parser.add_argument("--backup", nargs=2, metavar=("SOURCE", "DEST"), help="Create backup from SOURCE to DEST dir")
    parser.add_argument("--name", help="Backup name prefix")
    parser.add_argument("--compress", action="store_true", help="Compress directory backups to tar.gz")
    parser.add_argument("--no-verify", action="store_true", help="Skip backup verification")
    parser.add_argument("--rotate", metavar="DIR", help="Rotate backups in DIR")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted without deleting")
    parser.add_argument("--list", metavar="DIR", help="List backups in DIR")
    parser.add_argument("--verify", metavar="DIR", help="Verify integrity of backups in DIR")
    parser.add_argument("--cron", metavar="CONFIG", help="Run with config file (backup + rotate)")
    parser.add_argument("--config", metavar="CONFIG", help="Show config from file")
    args = parser.parse_args()

    # --cron mode: load config and run backup + rotate
    if args.cron:
        config = load_config(args.cron)
        if not config:
            sys.exit(1)

        backup_source = config.get("backup_source")
        backup_dest = config.get("backup_dest")
        if not backup_source or not backup_dest:
            print("Error: config must include backup_source and backup_dest")
            sys.exit(1)

        print(f"  Backup Rotator — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  {'='*50}")
        print_config(config)

        # Step 1: Create backup
        print(f"\n  📦 Creating backup...")
        success = create_backup(
            config.get("backup_source"),
            config.get("backup_dest"),
            name=config.get("backup_name", "backup"),
            compress=config.get("compress", False),
            verify=config.get("verify", True),
        )
        if not success:
            print("  ⚠️  Backup creation failed, skipping rotation.")
            sys.exit(1)

        # Step 2: Rotate old backups
        print(f"\n  🔄 Rotating old backups...")
        execute_rotation(config.get("backup_dest"), config, dry_run=False)

        # Step 3: Verify
        if config.get("verify", True):
            print(f"\n  ✅ Verifying remaining backups...")
            verify_backups(config.get("backup_dest"), config.get("backup_name"))
        else:
            print(f"\n  ✅ Rotation complete.")

        return

    # --config: just show config
    if args.config:
        config = load_config(args.config)
        if config:
            print_config(config)
        return

    # --backup SOURCE DEST
    if args.backup:
        source, dest = args.backup
        print(f"  Backup: {source} → {dest}")
        create_backup(source, dest, name=args.name or "backup", compress=args.compress, verify=not args.no_verify)

    # --rotate DIR
    if args.rotate:
        if args.name:
            config = {**DEFAULT_CONFIG, "backup_name": args.name}
        else:
            config = DEFAULT_CONFIG
        print(f"  Rotating backups in: {args.rotate}")
        if args.dry_run:
            execute_rotation(args.rotate, config, dry_run=True)
        else:
            execute_rotation(args.rotate, config, dry_run=False)

    # --list DIR
    if args.list:
        list_backups(args.list, args.name, detail=True)

    # --verify DIR
    if args.verify:
        verify_backups(args.verify, args.name)


if __name__ == "__main__":
    main()
