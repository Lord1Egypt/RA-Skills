#!/usr/bin/env python3
"""
Eir API read operations - fetch directives and report misses.
Only used when Eir mode is enabled.

Usage:
  python3 -m pipeline.eir_sync fetch     # Fetch directives from API
  python3 -m pipeline.eir_sync miss      # Report missed topic slugs
"""

import json
import sys
import urllib.request
from datetime import datetime, timezone

from .config import DIRECTIVES_FILE, USED_SOURCE_URLS_FILE, PUSHED_TITLES_FILE, load_json
from .workspace import get_api_url, get_api_key


def _fetch_interests_as_directives():
    """Fallback: build directives from /oc/interests when /oc/curation is unavailable.
    Assigns default tier/freshness based on heat score."""
    api_key = get_api_key()
    req = urllib.request.Request(
        "%s/api/oc/interests" % get_api_url(),
        headers={"Authorization": "Bearer %s" % api_key},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = json.loads(resp.read())
    interests = raw.get("interests", raw) if isinstance(raw, dict) else raw

    # Sort by heat desc, take top N (avoid too many searches)
    interests = [i for i in interests if isinstance(i, dict) and i.get("status") == "active"]
    interests.sort(key=lambda i: i.get("heat", 0), reverse=True)
    top = interests[:40]  # reasonable daily search budget

    directives = []
    tracked = []
    for idx, i in enumerate(top):
        heat = i.get("heat", 0)
        # Assign tier based on heat
        if heat >= 80:
            tier = "tracked"
        elif heat >= 30:
            tier = "focus"
        else:
            tier = "explore"
        # Default freshness by tier
        freshness_map = {"tracked": "3d", "focus": "7d", "explore": "7d"}
        label = i.get("label", "")
        if isinstance(label, list):
            label = label[0] if label else i.get("slug", "")
        d = {
            "slug": i.get("slug", ""),
            "label": label,
            "tier": tier,
            "freshness": freshness_map.get(tier, "7d"),
            "searchHints": [],  # no hints available from interests API
        }
        if tier == "tracked":
            tracked.append(d)
        else:
            directives.append(d)

    data = {
        "directives": directives + tracked,
        "tracked": [],
        "_source": "interests_fallback",
        "_fetched_at": datetime.now(timezone.utc).isoformat(),
    }
    DIRECTIVES_FILE.parent.mkdir(parents=True, exist_ok=True)
    DIRECTIVES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    n = len(directives) + len(tracked)
    print("⚠️  /oc/curation unavailable — built %d directives from /oc/interests (fallback)" % n)
    return data


def fetch_directives():
    """Fetch fresh directives from Eir API.
    Falls back to building directives from /oc/interests if /oc/curation fails."""
    # Preflight
    from .config import preflight_check
    errors = preflight_check(require_eir=True)
    if errors:
        for e in errors:
            print("❌ %s" % e, file=sys.stderr)
        return None

    api_key = get_api_key()
    # Try /oc/curation first
    try:
        req = urllib.request.Request(
            "%s/api/oc/curation" % get_api_url(),
            headers={"Authorization": "Bearer %s" % api_key},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        data["_fetched_at"] = datetime.now(timezone.utc).isoformat()
        DIRECTIVES_FILE.parent.mkdir(parents=True, exist_ok=True)
        DIRECTIVES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        n = len(data.get("directives", [])) + len(data.get("tracked", []))
        print("✅ Fetched %d directives from API" % n)

        # Sync source dedup data (uses cache, won't re-call if fresh)
        sync_sources()

        return data
    except Exception as e:
        print("⚠️  /oc/curation failed (%s), trying interests fallback..." % e, file=sys.stderr)

    # Fallback: build from interests
    try:
        return _fetch_interests_as_directives()
    except Exception as e2:
        print("❌ Both /oc/curation and /oc/interests failed: %s" % e2, file=sys.stderr)
        raise


def _normalize_title(title):
    """Normalize title for fuzzy dedup.
    Strip quotes, punctuation variants, source suffixes, whitespace."""
    import re
    t = title.strip().lower()
    # Strip source suffixes: "| TechCrunch", "- CSDN博客", "_ 新浪网"
    t = re.sub(r'\s*[|_\-–—]\s*[^|_\-–—]{2,30}$', '', t)
    # Normalize quotes
    t = t.replace('\u201c', '"').replace('\u201d', '"')  # smart double
    t = t.replace('\u2018', "'").replace('\u2019', "'")  # smart single
    t = t.replace('\u300c', '"').replace('\u300d', '"')  # CJK corner
    t = t.replace('\u300e', '"').replace('\u300f', '"')  # CJK white corner
    t = t.replace('\uff08', '(').replace('\uff09', ')')  # fullwidth parens
    # Strip all remaining punctuation and collapse whitespace
    t = re.sub(r'[\s]+', ' ', t).strip()
    return t


def _sources_cache_path():
    """Return path to local sources cache."""
    from .config import DATA_DIR
    return DATA_DIR / "sources_cache.json"


def sync_sources(force=False):
    """Sync source URLs and titles from Eir API to local dedup files.
    Uses local cache — only calls API if cache is stale (>6h) or force=True.
    Returns (url_count, title_count) synced."""
    import os
    cache_path = _sources_cache_path()

    # Check cache freshness
    if not force and cache_path.exists():
        import time
        age_hours = (time.time() - os.path.getmtime(str(cache_path))) / 3600
        if age_hours < 6:
            # Load from cache instead of API
            try:
                cached = json.loads(cache_path.read_text(encoding='utf-8'))
                return _apply_sources_to_dedup(cached)
            except Exception:
                pass  # Cache corrupt, fetch fresh

    # Fetch from API
    try:
        api_key = get_api_key()
        req = urllib.request.Request(
            "%s/api/oc/sources" % get_api_url(),
            headers={"Authorization": "Bearer %s" % api_key},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())

        items = data.get("items", data) if isinstance(data, dict) else data
        if not isinstance(items, list):
            items = []

        # Write cache
        cache_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
        result = _apply_sources_to_dedup(items)
        print("📡 Synced sources from Eir: %d URLs, %d titles" % result)
        return result

    except Exception as e:
        print("⚠️ Failed to sync sources: %s" % e)
        # Try cache as fallback
        if cache_path.exists():
            try:
                cached = json.loads(cache_path.read_text(encoding='utf-8'))
                return _apply_sources_to_dedup(cached)
            except Exception:
                pass
        return (0, 0)


def _apply_sources_to_dedup(items):
    """Extract URLs and titles from source items, merge into local dedup files."""
    urls = set()
    titles = []

    for item in items:
        sources = item.get("sources", [])
        content_group = item.get("contentGroup", "")
        for s in sources:
            url = s.get("url", "")
            title = s.get("title", "")
            if url:
                urls.add(url)
            if title:
                titles.append({
                    "title": title,
                    "normalized": _normalize_title(title),
                    "content_group": content_group,
                    "url": url,
                })

    # Merge into used_source_urls.json
    existing_urls = set(load_json(USED_SOURCE_URLS_FILE, []))
    merged_urls = sorted(existing_urls | urls)
    USED_SOURCE_URLS_FILE.write_text(json.dumps(merged_urls, indent=2), encoding='utf-8')

    # Merge into pushed_titles.json (add normalized field)
    existing_titles = load_json(PUSHED_TITLES_FILE, [])
    if not isinstance(existing_titles, list):
        existing_titles = []
    # Add normalized field to existing entries that lack it
    for entry in existing_titles:
        if "normalized" not in entry and "title" in entry:
            entry["normalized"] = _normalize_title(entry["title"])
    # Merge new titles (skip if URL already exists)
    existing_url_set = set()
    for e in existing_titles:
        for u in e.get("source_urls", []):
            if u:
                existing_url_set.add(u)
        url_field = e.get("url", "")
        if url_field:
            existing_url_set.add(url_field)
    for t in titles:
        if t["url"] and t["url"] not in existing_url_set:
            existing_titles.append({
                "title": t["title"],
                "normalized": t["normalized"],
                "content_group": t["content_group"],
                "source_urls": [t["url"]],
                "synced_from_api": True,
            })
    PUSHED_TITLES_FILE.write_text(
        json.dumps(existing_titles, ensure_ascii=False, indent=2), encoding='utf-8'
    )

    return (len(merged_urls), len(existing_titles))


def report_misses(misses):
    """Report missed topic slugs to POST /oc/curation/miss.
    
    Args:
        misses: list of {slug, reason} dicts, or list of slug strings (legacy)
    """
    if not misses:
        return
    # Normalize to [{slug, reason}]
    normalized = []
    for m in misses:
        if isinstance(m, str):
            normalized.append({"slug": m, "reason": "no usable content"})
        else:
            normalized.append({"slug": m.get("slug", ""), "reason": m.get("reason", "no usable content")})
    normalized = [m for m in normalized if m["slug"]]
    if not normalized:
        return
    try:
        api_url = get_api_url()
        api_key = get_api_key()
        payload = json.dumps({
            "slugs": [m["slug"] for m in normalized],
            "details": normalized,
        }).encode()
        req = urllib.request.Request(
            "%s/api/oc/curation/miss" % api_url,
            data=payload,
            headers={
                "Authorization": "Bearer %s" % api_key,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        slugs_str = ", ".join(m["slug"] for m in normalized)
        print("📡 Reported %d missed topics: %s" % (len(normalized), slugs_str))
    except Exception as e:
        print("⚠️ Failed to report misses: %s" % e)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Eir sync operations")
    parser.add_argument("action", choices=["fetch", "miss", "sync-sources"], help="Action to perform")
    parser.add_argument("--slugs", nargs="+", help="Topic slugs for miss reporting")
    parser.add_argument("--reason", default="manual", help="Reason for miss")
    args = parser.parse_args()

    if args.action == "fetch":
        fetch_directives()
    elif args.action == "sync-sources":
        sync_sources(force=True)
    elif args.action == "miss":
        if not args.slugs:
            print("Error: --slugs required for miss action", file=sys.stderr)
            sys.exit(1)
        misses = [{"slug": slug, "reason": args.reason} for slug in args.slugs]
        report_misses(misses)


if __name__ == "__main__":
    main()