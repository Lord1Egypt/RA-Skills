"""
sync_vault_memory.py — Sync vault markdown files to workspace/memory/

Makes vault content searchable via memory_search.
Only syncs .md files, skips archives and large files.

Usage: python scripts/sync_vault_memory.py
"""
import os
import shutil
from pathlib import Path

from shared_config import VAULT_DIR, MEMORY_DIR, SYNC_DIRS, MAX_FILE_SIZE_KB

MAX_SIZE = MAX_FILE_SIZE_KB * 1024

SKIP_PATTERNS = ["-backup-", "cache-"]

def should_skip(filename):
    for p in SKIP_PATTERNS:
        if p in filename:
            return True
    return False

def sync():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    synced = 0
    skipped = 0

    for dir_name in SYNC_DIRS:
        src_dir = VAULT_DIR / dir_name
        if not src_dir.exists():
            continue

        for md_file in src_dir.rglob("*.md"):
            rel = md_file.relative_to(VAULT_DIR)
            dest = MEMORY_DIR / str(rel).replace(os.sep, "_")

            if should_skip(md_file.name):
                skipped += 1
                continue

            if md_file.stat().st_size > MAX_SIZE:
                skipped += 1
                continue

            if dest.exists():
                if dest.stat().st_mtime >= md_file.stat().st_mtime:
                    continue

            shutil.copy2(md_file, dest)
            synced += 1

    print(f"Sync complete: {synced} files, {skipped} skipped")
    print(f"memory dir: {MEMORY_DIR}")

if __name__ == "__main__":
    sync()
