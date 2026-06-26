#!/usr/bin/env python3
"""Call Baidu AI Search web_search, or print the request with --dry-run."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ENDPOINT = "https://qianfan.baidubce.com/v2/ai_search/web_search"
DEFAULT_KEY_ENV = "BAIDU_AI_SEARCH_API_KEYS"
RECENCY_VALUES = ("week", "month", "semiyear", "year")


@dataclass
class SearchRequest:
    query: str
    top_k: int
    edition: str = "standard"
    freshness: str | None = None
    include_domains: list[str] | None = None
    block_domains: list[str] | None = None


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.replace(";", ",").split(",") if item.strip()]


def load_keys(env_name: str) -> list[str]:
    return split_csv(os.getenv(env_name))


def key_id(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def clamp_top_k(top_k: int) -> int:
    if top_k < 1:
        raise ValueError("top_k must be >= 1")
    return min(top_k, 50)


def build_payload(req: SearchRequest) -> dict[str, Any]:
    if req.freshness and req.freshness not in RECENCY_VALUES:
        raise ValueError(f"freshness must be one of: {', '.join(RECENCY_VALUES)}")
    payload: dict[str, Any] = {
        "messages": [{"role": "user", "content": req.query}],
        "search_source": "baidu_search_v2",
        "resource_type_filter": [{"type": "web", "top_k": clamp_top_k(req.top_k)}],
    }
    if req.edition != "standard":
        payload["edition"] = req.edition
    search_filter: dict[str, Any] = {}
    if req.include_domains:
        search_filter.setdefault("match", {})["site"] = req.include_domains
    if req.block_domains:
        search_filter.setdefault("items", {})["block_websites"] = req.block_domains
    if search_filter:
        payload["search_filter"] = search_filter
    if req.freshness:
        payload["search_recency_filter"] = req.freshness
    return payload


def build_headers(key: str, auth_header: str) -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    bearer = f"Bearer {key}"
    if auth_header in {"authorization", "both"}:
        headers["Authorization"] = bearer
    if auth_header in {"x-appbuilder", "both"}:
        headers["X-Appbuilder-Authorization"] = bearer
    return headers


def post_json(payload: dict[str, Any], key: str, timeout: int, auth_header: str) -> dict[str, Any]:
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=build_headers(key, auth_header),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc}") from exc


def cache_key(payload: dict[str, Any]) -> str:
    cache_input = json.dumps({"endpoint": ENDPOINT, "payload": payload}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(cache_input.encode("utf-8")).hexdigest()


def read_cache(cache_dir: str | None, payload: dict[str, Any], ttl_seconds: int) -> dict[str, Any] | None:
    if not cache_dir or ttl_seconds <= 0:
        return None
    path = Path(cache_dir) / f"{cache_key(payload)}.json"
    if not path.exists():
        return None
    try:
        cached = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    cached_at = float(cached.get("cached_at") or 0)
    if time.time() - cached_at > ttl_seconds:
        return None
    return cached.get("response")


def write_cache(cache_dir: str | None, payload: dict[str, Any], response: dict[str, Any]) -> None:
    if not cache_dir:
        return
    path = Path(cache_dir) / f"{cache_key(payload)}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "cached_at": time.time(),
                "endpoint": ENDPOINT,
                "payload": payload,
                "response": response,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def search_baidu(
    query: str,
    top_k: int,
    keys: list[str],
    edition: str = "standard",
    freshness: str | None = None,
    include_domains: list[str] | None = None,
    block_domains: list[str] | None = None,
    timeout: int = 30,
    auth_header: str = "both",
    cache_dir: str | None = None,
    cache_ttl_seconds: int = 86400,
) -> dict[str, Any]:
    payload = build_payload(
        SearchRequest(
            query=query,
            top_k=top_k,
            edition=edition,
            freshness=freshness,
            include_domains=include_domains,
            block_domains=block_domains,
        )
    )
    cached_response = read_cache(cache_dir, payload, cache_ttl_seconds)
    if cached_response is not None:
        return {
            "query": query,
            "top_k": clamp_top_k(top_k),
            "key_id": "cache",
            "elapsed_ms": 0,
            "cache_hit": True,
            "payload": payload,
            "response": cached_response,
        }

    if not keys:
        raise RuntimeError(f"No API keys found. Set {DEFAULT_KEY_ENV}.")

    errors: list[dict[str, str]] = []
    for key in keys:
        try:
            started = time.time()
            response = post_json(payload, key, timeout=timeout, auth_header=auth_header)
            write_cache(cache_dir, payload, response)
            return {
                "query": query,
                "top_k": clamp_top_k(top_k),
                "key_id": key_id(key),
                "elapsed_ms": int((time.time() - started) * 1000),
                "cache_hit": False,
                "payload": payload,
                "response": response,
            }
        except Exception as exc:  # try next key
            errors.append({"key_id": key_id(key), "error": str(exc)})
    raise RuntimeError(json.dumps({"message": "All Baidu API keys failed", "errors": errors}, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--edition", choices=["standard", "lite"], default="standard")
    parser.add_argument("--freshness", choices=RECENCY_VALUES)
    parser.add_argument("--include-domains", help="Comma-separated domain allowlist.")
    parser.add_argument("--block-domains", help="Comma-separated domain blocklist.")
    parser.add_argument("--key-env", default=DEFAULT_KEY_ENV)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--auth-header", choices=["authorization", "x-appbuilder", "both"], default="both")
    parser.add_argument("--cache-dir", help="Optional query-level cache directory. API keys are never written.")
    parser.add_argument("--cache-ttl", type=int, default=86400, help="Cache TTL in seconds when --cache-dir is used.")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--output")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    req = SearchRequest(
        query=args.query,
        top_k=args.top_k,
        edition=args.edition,
        freshness=args.freshness,
        include_domains=split_csv(args.include_domains),
        block_domains=split_csv(args.block_domains),
    )
    payload = build_payload(req)
    if args.dry_run:
        print(json.dumps({"endpoint": ENDPOINT, "payload": payload}, ensure_ascii=False, indent=2))
        return 0

    keys = load_keys(args.key_env)
    result = search_baidu(
        query=args.query,
        top_k=args.top_k,
        keys=keys,
        edition=args.edition,
        freshness=args.freshness,
        include_domains=split_csv(args.include_domains),
        block_domains=split_csv(args.block_domains),
        timeout=args.timeout,
        auth_header=args.auth_header,
        cache_dir=None if args.no_cache else args.cache_dir,
        cache_ttl_seconds=args.cache_ttl,
    )
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
