#!/usr/bin/env python3
"""
POST content to Eir Content API.
Only used when Eir mode is enabled.

Usage:
  python3 -m pipeline.eir_post <task_file.json>
  python3 -m pipeline.eir_post --from-dir data/v9/tasks/
"""

import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from .config import POSTED_DIR, PUSHED_TITLES_FILE, V9_DIR, ensure_dirs
from .workspace import get_api_url, get_api_key

TIMEOUT = 60
REQUEST_INTERVAL = 0.5


def api_request(method, url, data=None, api_key=""):
    """Make API request with retry."""
    body = json.dumps(data, ensure_ascii=False).encode() if data else None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url, method=method, data=body,
                headers={
                    "Authorization": "Bearer " + api_key,
                    "Content-Type": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.status, json.loads(resp.read())
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            try:
                return e.code, {"error": str(e)}
            except AttributeError:
                return 0, {"error": str(e)}
    return 0, {"error": "max retries"}


def post_content(content_data, api_key):
    """POST content to Eir Content API. Returns (content_id, contentGroup) or raises."""
    item = {
        "lang": content_data["lang"],
        "slug": content_data["slug"],
        "topicSlug": content_data.get("topicSlug", content_data["slug"]),
        "dot": content_data["dot"],
        "l1": content_data["l1"],
        "l2": content_data["l2"],
        "sources": content_data.get("sources", []),
    }
    # publishTime at top level (accept both camelCase and snake_case input)
    pt = content_data.get("publishTime") or content_data.get("publish_time", "")
    if not pt and item["sources"]:
        # Fall back to first source's publishTime
        pt = item["sources"][0].get("publishTime", item["sources"][0].get("publish_time", ""))
    if pt:
        item["publishTime"] = pt
    if content_data.get("interests"):
        interests = content_data["interests"]
        # Validate anchor: must be clean topic slugs, not content_slugs with hashes
        anchors = interests.get("anchor", [])
        topic_slug = content_data.get("topicSlug", "")
        if anchors and topic_slug:
            # Fix: if anchor looks like content_slug (too long or has hash), replace with topicSlug
            cleaned = []
            for a in anchors:
                if a == topic_slug:
                    cleaned.append(a)
                elif len(a) > len(topic_slug) + 10:
                    print("  ⚠️  Fixing anchor '%s' → '%s' (was content_slug?)" % (a, topic_slug))
                    cleaned.append(topic_slug)
                else:
                    cleaned.append(a)
            interests["anchor"] = cleaned
        item["interests"] = interests
    if content_data.get("contentGroup"):
        item["contentGroup"] = content_data["contentGroup"]

    payload = {"items": [item]}

    time.sleep(REQUEST_INTERVAL)
    status, resp = api_request("POST", get_api_url() + "/api/oc/content", payload, api_key)

    if status not in (200, 201):
        raise RuntimeError("POST failed: %d %s" % (status, json.dumps(resp, ensure_ascii=False)[:300]))

    results = resp.get("results", [])
    if not results or results[0].get("status") != "accepted":
        reason = results[0].get("reason", "unknown") if results else "empty"
        # If rejected for duplicate, refresh source cache
        if "duplicate" in reason.lower() or "exists" in reason.lower():
            try:
                from .eir_sync import sync_sources
                print("  🔄 Duplicate detected, refreshing source cache...")
                sync_sources(force=True)
            except Exception as e:
                print("  ⚠️ sync_sources failed: %s" % e)
        raise RuntimeError("POST rejected: %s" % reason)

    content_id = results[0].get("id", "")
    content_group = results[0].get("contentGroup", "")
    return content_id, content_group


def record_posted(content_data, content_id, content_group):
    """Record posted content in pushed_titles.json and run state."""
    ensure_dirs()
    
    # Update pushed_titles.json
    try:
        pushed = json.loads(PUSHED_TITLES_FILE.read_text()) if PUSHED_TITLES_FILE.exists() else []
    except (FileNotFoundError, json.JSONDecodeError):
        pushed = []
    if not isinstance(pushed, list):
        pushed = []
    
    pushed.append({
        "slug": content_data["slug"],
        "title": content_data.get("l1", {}).get("title", ""),
        "lang": content_data["lang"],
        "content_id": content_id,
        "content_group": content_group,
        "topic_slug": content_data.get("topicSlug", ""),
        "pushed_at": datetime.now(timezone.utc).isoformat(),
        "source_urls": [s.get("url", "") for s in content_data.get("sources", [])],
    })
    PUSHED_TITLES_FILE.write_text(json.dumps(pushed, ensure_ascii=False, indent=2), encoding="utf-8")

    # Also update run state for cross-step dedup
    try:
        from .run_state import record_posted_url, record_posted_id, persist_used_urls, load_state
        state = load_state()
        for s in content_data.get("sources", []):
            url = s.get("url", "")
            if url:
                record_posted_url(state, url)
        record_posted_id(
            state,
            content_id, content_group,
            content_data["slug"],
            content_data.get("topicSlug", ""),
        )
        # Persist to used_source_urls.json
        all_urls = [s.get("url", "") for s in content_data.get("sources", []) if s.get("url")]
        persist_used_urls(all_urls)
    except Exception:
        pass  # non-critical: dedup state update failure shouldn't block posting


def save_posted(content_data, content_id, content_group):
    """Save posted content to posted dir."""
    ensure_dirs()
    slug = content_data.get("slug", "unknown")
    lang = content_data.get("lang", "zh")
    content_data["_posted"] = {
        "content_id": content_id,
        "content_group": content_group,
        "posted_at": datetime.now(timezone.utc).isoformat(),
    }
    name = "%s_%s.json" % (slug, lang)
    path = POSTED_DIR / name
    path.write_text(json.dumps(content_data, indent=2, ensure_ascii=False))
    return path


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Post content to Eir API")
    parser.add_argument("file", nargs="?", help="Generated content JSON file to post")
    parser.add_argument("--from-dir", help="Post all JSON files from directory")
    parser.add_argument("--dry-run", action="store_true", help="Validate without posting")
    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key and not args.dry_run:
        print("Error: No API key. Run connect.py first or set EIR_API_KEY.", file=sys.stderr)
        sys.exit(1)

    def post_file(filepath):
        data = json.loads(Path(filepath).read_text())
        if args.dry_run:
            print("  [dry-run] Would POST: %s" % data.get("slug", data.get("content_slug", "?")))
            return
        cid, cg = post_content(data, api_key)
        record_posted(data, cid, cg)
        print("  ✅ Posted: %s → %s" % (data.get("slug", "?"), cid))

    if args.file:
        fpath = Path(args.file)
        if not fpath.exists():
            print("Error: File not found: %s" % fpath, file=sys.stderr)
            sys.exit(1)
        try:
            post_file(fpath)
        except Exception as e:
            print("Error: %s" % e, file=sys.stderr)
            sys.exit(1)
    elif args.from_dir:
        d = Path(args.from_dir)
        if not d.is_dir():
            print("Error: Directory not found: %s" % d, file=sys.stderr)
            sys.exit(1)
        files = sorted(d.glob("*.json"))
        print("Found %d files in %s" % (len(files), d))
        ok, fail = 0, 0
        for f in files:
            try:
                post_file(f)
                ok += 1
            except Exception as e:
                print("  ❌ %s: %s" % (f.name, e), file=sys.stderr)
                fail += 1
        print("Done: %d posted, %d failed" % (ok, fail))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()