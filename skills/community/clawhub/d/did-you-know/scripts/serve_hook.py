#!/usr/bin/env python3
"""Serve the next DYK hook, refreshing the cache if needed."""

from __future__ import annotations

import random
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from helpers import (
    collect_hooks,
    last_served_domains,
    load_prefs,
    load_store,
    now_utc,
    save_store,
    score_hook,
    stored_urls,
    to_iso_z,
    trim_store,
    refresh_due,
)

# Output format constants.
MSG_PREFIX = "Did you know that "
MSG_SUFFIX = "?"
MSG_URL_SEPARATOR = "\n"
MSG_BODY_SEPARATOR = "\n\n"


def ensure_fresh(store: dict) -> None:
    """Ensure a fresh collection exists, refreshing from the network if needed."""
    now = now_utc()
    collections = store.setdefault("collections", [])
    if not refresh_due(store, now):
        return
    try:
        hooks = collect_hooks(exclude_urls=stored_urls(store))
    except Exception as exc:
        print(f"DYK refresh failed: {exc}", file=sys.stderr)
        store["last_checked_at"] = to_iso_z(now)
        if collections:
            return
        raise
    store["last_checked_at"] = to_iso_z(now)
    if not hooks:
        # All hooks were duplicates of ones we already have.  DYK sets
        # rotate once or twice per day, so the template may not have
        # changed yet.  By leaving fetched_at stale, refresh_due stays
        # True and we re-check on the next invocation after cooldown.
        return
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
    collections.append(
        {
            "date": now.date().isoformat(),
            "fetched_at": to_iso_z(now),
            "hooks": hooks,
        }
    )
    # Accumulate the new hooks' URLs in the persistent history so trim_store
    # cannot cause already-seen hooks to be re-fetched from Wikipedia.
    for hook in hooks:
        for url in hook.get("urls", []):
            if url not in seen_set:
                seen.append(url)
                seen_set.add(url)
    trim_store(store, now)


def format_hook(hook: dict) -> str:
    """Format a hook with prefix, trailing '?', and one URL per line."""
    text = hook.get("text", "")
    urls = [urllib.parse.unquote(url) for url in hook.get("urls", [])]
    message = f"{MSG_PREFIX}{text}"
    if not message.endswith(MSG_SUFFIX):
        message += MSG_SUFFIX
    if not urls:
        return message
    return message + MSG_BODY_SEPARATOR + MSG_URL_SEPARATOR.join(urls)


def next_hook(store: dict, prefs: dict | None = None) -> str:
    """Return the next unserved hook by score, or the exhausted message.

    Scoring is delegated to score_hook() — see its docstring for the full model.
    The freshness bonus (+0.1) is applied here for hooks in the most recently
    fetched collection (coll_idx 0 in reversed order), before passing to score_hook.

    Serving priority (highest to lowest):
      1. Score descending (see score_hook for full breakdown)
      2. Most recently fetched collection first
      3. Shortest display text (character count)
      4. Random selection among remaining ties

    Score storage (written to the cache on every call):
      candidate_score  Written to every evaluated (unserved) hook. Reflects the
                       score at the time of this call. Overwritten on subsequent
                       calls — may be stale if prefs or prev_domains have changed.
      served_score     Written only to the winning hook, alongside returned_at.
                       Never overwritten. Definitive record of why this hook was
                       chosen at the moment it was served.
    """
    if prefs is None:
        prefs = {}
    collections = store.get("collections", [])
    # Domains of the last served hook, used to apply the repetition penalty in score_hook.
    prev_domains = last_served_domains(store)
    candidates = []
    for coll_idx, coll in enumerate(reversed(collections)):  # coll_idx 0 = newest
        freshness_bonus = 0.1 if coll_idx == 0 else 0.0
        for hook in coll.get("hooks", []):
            if not hook.get("returned"):
                char_count = len(hook.get("text") or "")
                breakdown = score_hook(hook, prefs, freshness_bonus, prev_domains)
                hook["candidate_score"] = breakdown
                candidates.append((breakdown["total"], coll_idx, char_count, hook, breakdown))
    if not candidates:
        return "No more facts to share today; check back tomorrow!"
    # Primary sort. Ties after this are broken by steps 2–4 above.
    candidates.sort(key=lambda x: (-x[0], x[1], x[2]))
    top_score, top_coll_idx, top_chars = candidates[0][0], candidates[0][1], candidates[0][2]
    tied = [c for c in candidates if c[0] == top_score and c[1] == top_coll_idx and c[2] == top_chars]
    chosen = random.choice(tied)
    hook = chosen[3]
    hook["returned"] = True
    hook["returned_at"] = to_iso_z(now_utc())
    hook["served_score"] = chosen[4]
    return format_hook(hook)


def main() -> int:
    """Script entrypoint: refresh cache if needed and print the next hook."""
    store = load_store()
    try:
        ensure_fresh(store)
    except Exception as exc:
        print(f"DYK error: {exc}", file=sys.stderr)
        try:
            save_store(store)
        except Exception:
            pass
        print("Something went wrong with the fact-fetching; please try again later.")
        return 1
    prefs = load_prefs()
    result = next_hook(store, prefs)
    save_store(store)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
