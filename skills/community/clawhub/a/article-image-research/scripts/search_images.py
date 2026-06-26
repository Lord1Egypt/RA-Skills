#!/usr/bin/env python3
"""Search image providers and return normalized candidate JSON."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any


class SearchError(RuntimeError):
    pass


def request_json(url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
    request_headers = {
        "Accept": "application/json",
        "User-Agent": "article-image-research/1.0 (image research for editorial attribution)",
    }
    request_headers.update(headers or {})
    request = urllib.request.Request(url, headers=request_headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SearchError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SearchError(str(exc)) from exc


def build_url(base: str, params: dict[str, Any]) -> str:
    clean = {key: value for key, value in params.items() if value not in (None, "")}
    return base + "?" + urllib.parse.urlencode(clean)


def search_openverse(query: str, limit: int, page: int, include_raw: bool) -> list[dict[str, Any]]:
    url = build_url(
        "https://api.openverse.org/v1/images/",
        {
            "q": query,
            "page_size": limit,
            "page": page,
            "mature": "false",
        },
    )
    data = request_json(url)
    results = []
    for item in data.get("results", []):
        result = {
            "provider": "openverse",
            "title": item.get("title"),
            "image_url": item.get("url"),
            "thumbnail_url": item.get("thumbnail"),
            "landing_url": item.get("foreign_landing_url"),
            "creator": item.get("creator"),
            "creator_url": item.get("creator_url"),
            "license": item.get("license"),
            "license_url": item.get("license_url"),
            "source": item.get("source") or item.get("provider"),
            "attribution": item.get("attribution"),
            "width": item.get("width"),
            "height": item.get("height"),
        }
        if include_raw:
            result["raw"] = item
        results.append(result)
    return results


def search_pexels(query: str, limit: int, page: int, include_raw: bool) -> list[dict[str, Any]]:
    api_key = os.environ.get("PEXELS_API_KEY")
    if not api_key:
        raise SearchError("PEXELS_API_KEY is required for provider=pexels")
    url = build_url(
        "https://api.pexels.com/v1/search",
        {
            "query": query,
            "per_page": limit,
            "page": page,
        },
    )
    data = request_json(url, {"Authorization": api_key})
    results = []
    for item in data.get("photos", []):
        src = item.get("src") or {}
        result = {
            "provider": "pexels",
            "title": item.get("alt"),
            "image_url": src.get("large2x") or src.get("large") or src.get("original"),
            "thumbnail_url": src.get("medium") or src.get("small"),
            "landing_url": item.get("url"),
            "creator": item.get("photographer"),
            "creator_url": item.get("photographer_url"),
            "license": "Pexels License",
            "license_url": "https://www.pexels.com/license/",
            "source": "pexels",
            "attribution": f"Photo by {item.get('photographer')} on Pexels" if item.get("photographer") else None,
            "width": item.get("width"),
            "height": item.get("height"),
        }
        if include_raw:
            result["raw"] = item
        results.append(result)
    return results


def search_unsplash(query: str, limit: int, page: int, include_raw: bool) -> list[dict[str, Any]]:
    api_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not api_key:
        raise SearchError("UNSPLASH_ACCESS_KEY is required for provider=unsplash")
    url = build_url(
        "https://api.unsplash.com/search/photos",
        {
            "query": query,
            "per_page": limit,
            "page": page,
        },
    )
    data = request_json(url, {"Authorization": f"Client-ID {api_key}"})
    results = []
    for item in data.get("results", []):
        user = item.get("user") or {}
        urls = item.get("urls") or {}
        links = item.get("links") or {}
        creator = user.get("name")
        result = {
            "provider": "unsplash",
            "title": item.get("description") or item.get("alt_description"),
            "image_url": urls.get("regular") or urls.get("full"),
            "thumbnail_url": urls.get("thumb") or urls.get("small"),
            "landing_url": links.get("html"),
            "creator": creator,
            "creator_url": (user.get("links") or {}).get("html"),
            "license": "Unsplash License / API Terms",
            "license_url": "https://unsplash.com/license",
            "source": "unsplash",
            "attribution": f"Photo by {creator} on Unsplash" if creator else None,
            "download_location": links.get("download_location"),
            "width": item.get("width"),
            "height": item.get("height"),
        }
        if include_raw:
            result["raw"] = item
        results.append(result)
    return results


def search_brave(query: str, limit: int, page: int, include_raw: bool) -> list[dict[str, Any]]:
    api_key = os.environ.get("BRAVE_SEARCH_API_KEY")
    if not api_key:
        raise SearchError("BRAVE_SEARCH_API_KEY is required for provider=brave")
    offset = max(page - 1, 0) * limit
    url = build_url(
        "https://api.search.brave.com/res/v1/images/search",
        {
            "q": query,
            "count": limit,
            "offset": offset,
            "safesearch": "strict",
            "spellcheck": 1,
        },
    )
    data = request_json(
        url,
        {
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
        },
    )
    results = []
    for item in data.get("results", []):
        image = item.get("properties") or {}
        thumbnail = item.get("thumbnail") or {}
        result = {
            "provider": "brave",
            "title": item.get("title"),
            "image_url": image.get("url") or item.get("url"),
            "thumbnail_url": thumbnail.get("src"),
            "landing_url": item.get("page_url") or item.get("url"),
            "creator": None,
            "creator_url": None,
            "license": None,
            "license_url": None,
            "source": item.get("source"),
            "attribution": None,
            "width": image.get("width"),
            "height": image.get("height"),
        }
        if include_raw:
            result["raw"] = item
        results.append(result)
    return results


PROVIDERS = {
    "openverse": search_openverse,
    "pexels": search_pexels,
    "unsplash": search_unsplash,
    "brave": search_brave,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search image providers and output normalized JSON.")
    parser.add_argument("--query", required=True, help="Search query.")
    parser.add_argument(
        "--provider",
        action="append",
        choices=sorted(PROVIDERS),
        help="Provider to search. Repeat for multiple providers. Defaults to openverse.",
    )
    parser.add_argument("--limit", type=int, default=10, help="Results per provider.")
    parser.add_argument("--page", type=int, default=1, help="Provider result page.")
    parser.add_argument("--include-raw", action="store_true", help="Include raw provider payloads.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    providers = args.provider or ["openverse"]
    output: dict[str, Any] = {
        "query": args.query,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "providers": providers,
        "results": [],
        "errors": [],
    }

    for provider in providers:
        try:
            output["results"].extend(PROVIDERS[provider](args.query, args.limit, args.page, args.include_raw))
        except SearchError as exc:
            output["errors"].append({"provider": provider, "error": str(exc)})

    json.dump(output, sys.stdout, ensure_ascii=False, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 1 if output["errors"] and not output["results"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
