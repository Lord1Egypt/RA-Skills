"""
Watch state management for ebay-agent.

Manages a local JSON file of saved searches ("watches") that can be
checked against live eBay listings.  The state file defaults to
~/.ebay-agent/watches.json and can be overridden with --state-file.
"""

import json
import os
import re
import random
import string
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DEFAULT_STATE_DIR = os.path.expanduser("~/.ebay-agent")
DEFAULT_STATE_FILE = os.path.join(DEFAULT_STATE_DIR, "watches.json")


def _state_path(override: Optional[str] = None) -> Path:
    path = Path(override) if override else Path(DEFAULT_STATE_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _load(state_file: Optional[str] = None) -> list[dict]:
    path = _state_path(state_file)
    if not path.exists():
        return []
    return json.loads(path.read_text())


def _save(watches: list[dict], state_file: Optional[str] = None) -> None:
    path = _state_path(state_file)
    path.write_text(json.dumps(watches, indent=2) + "\n")


def _make_id(query: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", query.lower()).strip("-")
    slug = slug[:20]
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{slug}-{suffix}"


def add_watch(
    query: str,
    max_price: float,
    condition: str = "used",
    state_file: Optional[str] = None,
) -> dict:
    watches = _load(state_file)
    watch = {
        "id": _make_id(query),
        "query": query,
        "condition": condition,
        "max_price": max_price,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_checked_at": None,
        "last_best_price": None,
        "trigger_count": 0,
    }
    watches.append(watch)
    _save(watches, state_file)
    return watch


def list_watches(state_file: Optional[str] = None) -> list[dict]:
    return _load(state_file)


def remove_watch(watch_id: str, state_file: Optional[str] = None) -> bool:
    watches = _load(state_file)
    original_len = len(watches)
    watches = [w for w in watches if w["id"] != watch_id]
    if len(watches) == original_len:
        return False
    _save(watches, state_file)
    return True


def check_watches(state_file: Optional[str] = None) -> list[dict]:
    """Check all watches against live eBay data. Returns triggered watches."""
    from .search import search_items
    from .relevance import filter_relevant

    watches = _load(state_file)
    if not watches:
        return []

    triggered = []
    now = datetime.now(timezone.utc).isoformat()

    for watch in watches:
        watch["last_checked_at"] = now
        try:
            items = search_items(
                watch["query"],
                max_price=watch["max_price"],
                condition=watch["condition"],
                limit=20,
            )
            if not items:
                continue
            items = filter_relevant(items, watch["query"])
            if not items:
                continue
            best = min(items, key=lambda x: x["total_price"])
            watch["last_best_price"] = best["total_price"]
            if best["total_price"] <= watch["max_price"]:
                watch["trigger_count"] += 1
                triggered.append({
                    "watch": watch,
                    "listing": {
                        "title": best.get("title", ""),
                        "total_price": best["total_price"],
                        "url": best.get("item_url", ""),
                    },
                })
        except Exception:
            # Search failures shouldn't crash the whole check run
            continue

    _save(watches, state_file)
    return triggered
