#!/usr/bin/env python3
"""
Cleanup Manager
Deletes old summaries and archives based on retention policy.
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
SUMMARIES_DIR = PROJECT_DIR / 'summaries'
ARCHIVE_DIR = PROJECT_DIR / 'data' / 'archive'

# Configuration
# Driver cards are read every 28 days → Archive for 10 years (legal retention requirement)
SUMMARY_RETENTION_DAYS = 365  # How long to keep summaries (1 year)
ARCHIVE_RETENTION_DAYS = 3650  # 10 years archive for .ddd files (legal requirement)

DRY_RUN = '--dry-run' in sys.argv


def get_age_days(filepath: Path) -> float:
    """Calculate file age in days."""
    mtime = filepath.stat().st_mtime
    age_seconds = time.time() - mtime
    return age_seconds / (24 * 60 * 60)


def cleanup_summaries():
    """Delete old summary files."""
    if not SUMMARIES_DIR.exists():
        return [], []
    
    deleted = []
    kept = []
    
    for filepath in SUMMARIES_DIR.glob('*.json'):
        age_days = get_age_days(filepath)
        if age_days > SUMMARY_RETENTION_DAYS:
            if DRY_RUN:
                print(f"  [DELETE] {filepath.name} ({age_days:.1f} days old)")
            else:
                filepath.unlink()
                print(f"  [DELETED] {filepath.name} ({age_days:.1f} days old)")
            deleted.append(filepath)
        else:
            kept.append(filepath)
    
    return deleted, kept


def cleanup_archives():
    """Delete old archive files (.ddd in archive/ directory)."""
    if not ARCHIVE_DIR.exists():
        return [], []
    
    deleted = []
    kept = []
    
    for filepath in ARCHIVE_DIR.glob('*.ddd'):
        age_days = get_age_days(filepath)
        if age_days > ARCHIVE_RETENTION_DAYS:
            if DRY_RUN:
                print(f"  [DELETE] archive/{filepath.name} ({age_days:.1f} days old)")
            else:
                filepath.unlink()
                print(f"  [DELETED] archive/{filepath.name} ({age_days:.1f} days old)")
            deleted.append(filepath)
        else:
            kept.append(filepath)
    
    return deleted, kept


def main():
    """Main function: Run all cleanup tasks."""
    print("=" * 50)
    print("Tachograph Cleanup Manager")
    print("=" * 50)
    print(f"Project: {PROJECT_DIR}")
    print(f"Summary Retention: {SUMMARY_RETENTION_DAYS} days (1 year)")
    print(f"Archive Retention: {ARCHIVE_RETENTION_DAYS} days (10 years)")
    if DRY_RUN:
        print("Mode: DRY RUN (no files will be deleted)")
    print()
    
    total_deleted = 0
    total_kept = 0
    
    # Summaries
    print("[1/2] Cleaning up summaries...")
    deleted, kept = cleanup_summaries()
    print(f"  Deleted: {len(deleted)}, Kept: {len(kept)}")
    total_deleted += len(deleted)
    total_kept += len(kept)
    
    # Archives
    print("[2/2] Cleaning up archives (10 years)...")
    deleted, kept = cleanup_archives()
    print(f"  Deleted: {len(deleted)}, Kept: {len(kept)}")
    total_deleted += len(deleted)
    total_kept += len(kept)
    
    print()
    print("=" * 50)
    print(f"Total: {total_deleted} files deleted, {total_kept} files kept")
    
    if DRY_RUN:
        print("NOTE: This was a DRY RUN - no files were actually deleted")
        print("Run without --dry-run to delete files")


if __name__ == '__main__':
    main()
