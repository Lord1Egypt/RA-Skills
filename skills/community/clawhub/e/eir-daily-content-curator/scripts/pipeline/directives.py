#!/usr/bin/env python3
"""
Pure local directive/interests loading for standalone mode.
Extracted from search.py to separate network-free operations.
"""

import json
from pathlib import Path

from .config import CONFIG_DIR, DIRECTIVES_FILE, load_json


def _label_to_slug(label: str) -> str:
    """Convert a human-readable label to a kebab-case slug.
    Handles CJK by transliterating common terms; falls back to
    stripping non-ASCII and lowercasing."""
    import re
    # If already looks like a slug (lowercase ASCII + hyphens), keep it
    if re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', label):
        return label
    # Try: lowercase, replace spaces/underscores with hyphens, strip non-slug chars
    slug = label.lower().strip()
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    # Require meaningful content (multi-word or long enough)
    if slug and '-' in slug and len(slug) >= 5:
        return slug
    # Fallback for CJK-heavy labels: use hash
    import hashlib
    return 'topic-' + hashlib.md5(label.encode()).hexdigest()[:8]


def load_local_interests():
    """Load interests from local config/interests.json (standalone mode).
    Converts to directive format for pipeline compatibility."""
    interests_file = CONFIG_DIR / "interests.json"
    if not interests_file.exists():
        return None
    try:
        data = json.loads(interests_file.read_text())
        topics = data.get("topics", [])
        if not topics:
            return None
        directives = []
        for t in topics:
            directives.append({
                "slug": t.get("slug", "") or _label_to_slug(t.get("label", "")),
                "label": t.get("label", ""),
                "topic": t.get("label", ""),
                "description": ", ".join(t.get("keywords", [])),
                "keywords": t.get("keywords", []),
                "freshness": t.get("freshness", "7d"),
                "tier": t.get("tier", "tracked"),
                "searchHints": t.get("search_hints", []),
            })
        return {"directives": directives, "tracked": []}
    except Exception:
        return None


def load_directives():
    """Load directives with staleness check.

    Resolution order:
      1. Cached directives.json — if < 24h old, use directly
      2. Fresh fetch from API (with interests fallback)
      3. Stale cache (if fetch fails)
      4. Local interests.json (standalone mode)
    """
    import os
    from datetime import datetime, timezone

    stale_threshold = 24 * 3600  # 24 hours in seconds
    cache_exists = DIRECTIVES_FILE.exists()
    is_stale = True

    if cache_exists:
        try:
            age = datetime.now(timezone.utc).timestamp() - os.path.getmtime(DIRECTIVES_FILE)
            is_stale = age > stale_threshold
        except OSError:
            pass

    if cache_exists and not is_stale:
        data = load_json(DIRECTIVES_FILE)
        n = len(data.get("directives", []))
        print("  Using cached directives.json (%d topics)" % n)
        return data

    # Cache is stale or missing — try fresh fetch
    if is_stale:
        try:
            from .eir_sync import fetch_directives
            data = fetch_directives()
            return data
        except Exception as e:
            print("  ⚠️  Failed to refresh directives: %s" % e)
            # Fall through to stale cache

    if cache_exists:
        data = load_json(DIRECTIVES_FILE)
        n = len(data.get("directives", []))
        print("  ⚠️  Using STALE directives.json (%d topics, >24h old)" % n)
        return data

    # Fallback: local interests (standalone mode)
    local = load_local_interests()
    if local:
        n = len(local.get("directives", []))
        print("  ✅ Loaded %d topics from local interests.json" % n)
        return local

    raise RuntimeError("No directives available. Create config/interests.json or run pipeline.eir_sync fetch")