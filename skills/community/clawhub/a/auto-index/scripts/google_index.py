#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-auth>=2.0.0",
#     "google-auth-httplib2>=0.2.0",
#     "google-api-python-client>=2.0.0",
#     "httpx>=0.27.0",
# ]
# ///
"""
Google Indexing API tool — submit URLs for indexing.

Subcommands:
    auto-index  Fetch sitemap, diff against cache, submit new/changed URLs
    index-now   Submit a single URL immediately

Usage:
    uv run google_index.py auto-index --sitemap "https://example.com/sitemap.xml" [--sa-key KEY.json]
    uv run google_index.py index-now --url "https://example.com/page" [--sa-key KEY.json]
"""

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "auto-index"
CACHE_FILE = CACHE_DIR / "sitemap-cache.json"

INDEXING_API_SCOPE = "https://www.googleapis.com/auth/indexing"
INDEXING_ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

# Max 200 requests/day per Google Indexing API quota
DAILY_QUOTA = 200


def get_sa_key_path(provided_key: str | None) -> str | None:
    """Get service account key path from argument or environment."""
    if provided_key:
        return provided_key
    return os.environ.get("GOOGLE_INDEX_SA_KEY")


def build_indexing_service(sa_key_path: str):
    """Build an authenticated Google Indexing API service."""
    from google.oauth2 import service_account
    import httplib2
    import google_auth_httplib2

    credentials = service_account.Credentials.from_service_account_file(
        sa_key_path,
        scopes=[INDEXING_API_SCOPE],
    )
    http = google_auth_httplib2.AuthorizedHttp(credentials, http=httplib2.Http())
    return http


def publish_url(http, url: str, action: str = "URL_UPDATED") -> dict:
    """Publish a URL notification to the Indexing API.

    Args:
        http: Authenticated httplib2.Http instance
        url: The URL to submit
        action: URL_UPDATED or URL_DELETED
    Returns:
        dict with url, status, and response or error
    """
    body = json.dumps({"url": url, "type": action})

    try:
        response, content = http.request(
            INDEXING_ENDPOINT,
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"},
        )
        status_code = int(response["status"])

        result = {
            "url": url,
            "status": status_code,
        }
        
        if status_code == 429:
            result["rateLimited"] = True

        try:
            parsed = json.loads(content)
            if status_code == 200:
                result["notifyTime"] = parsed.get(
                    "urlNotificationMetadata", {}
                ).get("latestUpdate", {}).get("notifyTime", "")
            else:
                result["error"] = parsed.get("error", {}).get(
                    "message", str(content)
                )
        except (json.JSONDecodeError, AttributeError):
            result["response"] = content.decode("utf-8", errors="replace")

        return result
    except Exception as e:
        return {"url": url, "status": -1, "error": str(e)}


def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    """Fetch and parse a sitemap XML, returning all <loc> URLs.
    Handles both regular sitemaps and sitemap index files.
    """
    import httpx

    urls: list[str] = []

    try:
        resp = httpx.get(sitemap_url, timeout=30, follow_redirects=True)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching sitemap {sitemap_url}: {e}", file=sys.stderr)
        return urls

    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        print(f"Error parsing sitemap XML: {e}", file=sys.stderr)
        return urls

    # Strip namespace for easier parsing
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"

    # Check if it's a sitemap index
    sitemap_tags = root.findall(f"{ns}sitemap")
    if sitemap_tags:
        # It's a sitemap index — recurse into each child sitemap
        for sm in sitemap_tags:
            loc = sm.find(f"{ns}loc")
            if loc is not None and loc.text:
                child_urls = fetch_sitemap_urls(loc.text.strip())
                urls.extend(child_urls)
    else:
        # Regular sitemap — extract <loc> URLs
        for url_elem in root.findall(f".//{ns}url"):
            loc = url_elem.find(f"{ns}loc")
            if loc is not None and loc.text:
                urls.append(loc.text.strip())

    return urls


def load_cache() -> dict:
    """Load sitemap cache from disk."""
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_cache(cache: dict):
    """Save sitemap cache to disk."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2))


def cmd_auto_index(args):
    """Auto-index: fetch sitemap, diff against cache, submit new URLs."""
    sa_key = get_sa_key_path(args.sa_key)
    if not sa_key:
        print("Error: No service account key provided.", file=sys.stderr)
        print("  Use --sa-key or set GOOGLE_INDEX_SA_KEY env var.", file=sys.stderr)
        sys.exit(1)

    if not Path(sa_key).is_file():
        print(f"Error: Service account key file not found: {sa_key}", file=sys.stderr)
        sys.exit(1)

    # Fetch sitemap
    print(f"Fetching sitemap: {args.sitemap}", file=sys.stderr)
    current_urls = fetch_sitemap_urls(args.sitemap)
    if not current_urls:
        output = {
            "meta": {
                "action": "auto-index",
                "sitemap": args.sitemap,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            "error": "No URLs found in sitemap",
        }
        print(json.dumps(output, indent=2))
        sys.exit(1)

    print(f"Found {len(current_urls)} URLs in sitemap", file=sys.stderr)

    # Load cache and diff
    cache = load_cache()
    cached_urls = set(cache.get(args.sitemap, {}).get("urls", []))
    current_set = set(current_urls)

    new_urls = current_set - cached_urls
    removed_urls = cached_urls - current_set

    if not new_urls and not args.force:
        output = {
            "meta": {
                "action": "auto-index",
                "sitemap": args.sitemap,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "total_in_sitemap": len(current_urls),
                "new_urls": 0,
                "removed_urls": len(removed_urls),
            },
            "results": [],
            "message": "No new URLs to index. Use --force to re-index all.",
        }
        print(json.dumps(output, indent=2))
        return

    urls_to_submit = list(new_urls) if not args.force else current_urls

    if len(urls_to_submit) > DAILY_QUOTA:
        print(
            f"Warning: {len(urls_to_submit)} URLs exceed daily quota of {DAILY_QUOTA}. "
            f"Only first {DAILY_QUOTA} will be submitted.",
            file=sys.stderr,
        )
        urls_to_submit = urls_to_submit[:DAILY_QUOTA]

    # Build service and submit
    http = build_indexing_service(sa_key)
    results = []
    success_count = 0
    fail_count = 0
    successfully_indexed_urls = set()

    for i, url in enumerate(urls_to_submit, 1):
        print(f"[{i}/{len(urls_to_submit)}] Indexing: {url}", file=sys.stderr)
        result = publish_url(http, url)
        results.append(result)
        if result["status"] == 200:
            success_count += 1
            successfully_indexed_urls.add(url)
        else:
            fail_count += 1
            if result.get("rateLimited"):
                remaining = len(urls_to_submit) - i
                print(
                    f"Rate limit hit. Stopping immediately. "
                    f"{remaining} URLs skipped.",
                    file=sys.stderr,
                )
                break

    # Update cache
    if args.sitemap not in cache:
        cache[args.sitemap] = {}
    
    # Only store URLs that were successfully indexed and still exist in the sitemap
    # Keep previously cached URLs that are still in the sitemap
    # Add newly successful URLs
    updated_cache_set = (cached_urls | successfully_indexed_urls) & current_set
    
    cache[args.sitemap]["urls"] = list(updated_cache_set)
    cache[args.sitemap]["last_indexed"] = datetime.now(timezone.utc).isoformat()
    save_cache(cache)

    output = {
        "meta": {
            "action": "auto-index",
            "sitemap": args.sitemap,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_in_sitemap": len(current_urls),
            "new_urls": len(new_urls),
            "removed_urls": len(removed_urls),
            "submitted": len(urls_to_submit),
            "success": success_count,
            "failed": fail_count,
        },
        "results": results,
    }
    print(json.dumps(output, indent=2))


def cmd_index_now(args):
    """Index-now: submit a single URL immediately."""
    sa_key = get_sa_key_path(args.sa_key)
    if not sa_key:
        print("Error: No service account key provided.", file=sys.stderr)
        print("  Use --sa-key or set GOOGLE_INDEX_SA_KEY env var.", file=sys.stderr)
        sys.exit(1)

    if not Path(sa_key).is_file():
        print(f"Error: Service account key file not found: {sa_key}", file=sys.stderr)
        sys.exit(1)

    action = "URL_DELETED" if args.delete else "URL_UPDATED"
    http = build_indexing_service(sa_key)

    urls = args.url  # list of URLs
    results = []
    success_count = 0
    fail_count = 0

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Submitting {action}: {url}", file=sys.stderr)
        result = publish_url(http, url, action)
        results.append(result)
        if result["status"] == 200:
            success_count += 1
        else:
            fail_count += 1
            if result.get("rateLimited"):
                remaining = len(urls) - i
                print(
                    f"Rate limit hit. Stopping immediately. "
                    f"{remaining} URLs skipped.",
                    file=sys.stderr,
                )
                break

    output = {
        "meta": {
            "action": "index-now",
            "type": action,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "submitted": len(urls),
            "success": success_count,
            "failed": fail_count,
        },
        "results": results,
    }
    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Google Indexing API — submit URLs for indexing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # auto-index subcommand
    auto_parser = subparsers.add_parser(
        "auto-index",
        help="Fetch sitemap, diff against cache, submit new URLs",
    )
    auto_parser.add_argument(
        "--sitemap", "-s",
        required=True,
        help="Sitemap URL to fetch (e.g. https://example.com/sitemap.xml)",
    )
    auto_parser.add_argument(
        "--sa-key", "-k",
        help="Path to service account JSON key (or set GOOGLE_INDEX_SA_KEY env)",
    )
    auto_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force re-index all URLs, ignoring cache",
    )
    auto_parser.set_defaults(func=cmd_auto_index)

    # index-now subcommand
    now_parser = subparsers.add_parser(
        "index-now",
        help="Submit URL(s) for immediate indexing",
    )
    now_parser.add_argument(
        "--url", "-u",
        required=True,
        action="append",
        help="URL to submit (can be specified multiple times)",
    )
    now_parser.add_argument(
        "--sa-key", "-k",
        help="Path to service account JSON key (or set GOOGLE_INDEX_SA_KEY env)",
    )
    now_parser.add_argument(
        "--delete", "-d",
        action="store_true",
        help="Notify URL deletion instead of update",
    )
    now_parser.set_defaults(func=cmd_index_now)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
