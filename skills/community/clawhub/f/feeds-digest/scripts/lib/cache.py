"""Cache for seen feed items (deduplication)."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_CACHE_DIR = Path.home() / ".cache" / "feeds-digest"


def get_cache_path(source_name: str) -> Path:
    """Get cache file path for a given source."""
    cache_dir = DEFAULT_CACHE_DIR
    cache_dir.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in source_name)
    return cache_dir / f"{safe_name}.json"


def load_seen_guids(source_name: str) -> set[str]:
    """Load seen GUIDs for a source."""
    path = get_cache_path(source_name)
    if not path.exists():
        return set()
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return set(data.get("guids", []))
    except (json.JSONDecodeError, OSError):
        return set()


def save_seen_guids(source_name: str, guids: list[str], max_keep: int = 1000) -> None:
    """Save seen GUIDs for a source (keep only last N)."""
    path = get_cache_path(source_name)
    # Keep only the most recent max_keep guids
    guids_to_keep = list(guids)[-max_keep:]
    data = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "guids": guids_to_keep,
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError:
        pass  # Cache is best-effort


def append_to_history(source_name: str, items: list) -> None:
    """Append items to a daily history file."""
    history_dir = DEFAULT_CACHE_DIR / "history"
    history_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = history_dir / f"{today}.jsonl"

    with open(path, "a", encoding="utf-8") as f:
        for item in items:
            record = {
                "source": source_name,
                "title": item.title,
                "link": item.link,
                "published": item.published.isoformat() if item.published else None,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
