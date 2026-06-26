#!/usr/bin/env python3
"""Fetch Wikipedia DYK hooks and write them untagged (tags=null) to the cache."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from helpers import (
    collect_hooks,
    load_store,
    now_utc,
    refresh_due,
    save_store,
    stored_urls,
    to_iso_z,
    trim_store,
)


def fetch_and_stage(store: dict) -> None:
    """Fetch new hooks and append them untagged to the store."""
    now = now_utc()
    collections = store.setdefault("collections", [])
    if not refresh_due(store, now):
        return
    try:
        hooks = collect_hooks(exclude_urls=stored_urls(store))
    except Exception as exc:
        print(f"DYK fetch failed: {exc}", file=sys.stderr)
        store["last_checked_at"] = to_iso_z(now)
        if collections:
            return
        raise
    store["last_checked_at"] = to_iso_z(now)
    if not hooks:
        return
    for hook in hooks:
        hook["tags"] = None
    # Backfill seen_urls from existing collections before trimming so that
    # legacy caches (written before this field existed) don't lose history
    # when trim_store removes the oldest entry.
    seen = store.setdefault("seen_urls", [])
    seen_set = set(seen)
    for col in collections:
        for hook in col.get("hooks", []):
            for url in hook.get("urls", []):
                if url not in seen_set:
                    seen.append(url)
                    seen_set.add(url)
    collections.append({
        "date": now.date().isoformat(),
        "fetched_at": to_iso_z(now),
        "hooks": hooks,
    })
    for hook in hooks:
        for url in hook.get("urls", []):
            if url not in seen_set:
                seen.append(url)
                seen_set.add(url)
    trim_store(store, now)


def main() -> int:
    """Entrypoint: refresh cache with untagged hooks if due."""
    store = load_store()
    try:
        fetch_and_stage(store)
    except Exception as exc:
        print(f"DYK fetch error: {exc}", file=sys.stderr)
        try:
            save_store(store)
        except Exception:
            pass
        return 1
    save_store(store)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
