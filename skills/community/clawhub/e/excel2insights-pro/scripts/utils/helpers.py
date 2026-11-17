"""Common helper functions for Excel2Insights."""

import json
from pathlib import Path


def safe_json(obj):
    """Convert object to JSON-safe format."""
    return json.loads(json.dumps(obj, default=str))


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def file_size_str(size_bytes):
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
