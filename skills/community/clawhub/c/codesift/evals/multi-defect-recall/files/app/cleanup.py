"""Remove export files older than the retention window."""

import time
from pathlib import Path

RETENTION_SECONDS = 7 * 24 * 3600


def run(directory: Path) -> int:
    """Delete expired export files in directory and return how many were removed."""
    removed = 0
    cutoff = time.time() - RETENTION_SECONDS
    for path in directory.glob("*.json"):
        if path.stat().st_mtime < cutoff:
            path.unlink()
            removed += 1
    return removed
