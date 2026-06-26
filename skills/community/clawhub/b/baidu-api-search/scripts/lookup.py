#!/usr/bin/env python3
"""Lightweight Baidu Baike lookup for entity-style questions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from baidu_web_search import DEFAULT_KEY_ENV, key_id, load_keys, search_baidu  # noqa: E402
from run_search_plan import extract_references  # noqa: E402


BAIKE_BASE_URL = "https://appbuilder.baidu.com"
LIST_PATH = "/v2/baike/lemma/get_list_by_title"
CONTENT_PATH = "/v2/baike/lemma/get_content"


def slugify_topic(topic: str) -> str:
    slug = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", topic.strip(), flags=re.UNICODE)
    slug = re.sub(r"-+", "-", slug).strip("-_")
    return (slug or "baike-lookup")[:48]


def default_out_dir(topic: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    return SCRIPT_DIR.parent / "runs" / f"{stamp}-{os.getpid()}-lookup-{slugify_topic(topic)}"


def default_cache_dir() -> Path:
    return SCRIPT_DIR.parent / "cache" / "baike"


def default_web_cache_dir() -> Path:
    return SCRIPT_DIR.parent / "cache" / "web_search"


def clamp_top_k(top_k: int) -> int:
    if top_k < 1:
        raise ValueError("top_k must be >= 1")
    return min(top_k, 100)


def build_headers(key: str, auth_header: str) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    bearer = f"Bearer {key}"
    if auth_header in {"authorization", "both"}:
        headers["Authorization"] = bearer
    if auth_header in {"x-appbuilder", "both"}:
        headers["X-Appbuilder-Authorization"] = bearer
    return headers


def build_url(base_url: str, path: str, params: dict[str, Any]) -> str:
    return f"{base_url.rstrip('/')}{path}?{urllib.parse.urlencode(params)}"


def cache_key(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def read_cache(cache_dir: str | None, url: str, ttl_seconds: int) -> dict[str, Any] | None:
    if not cache_dir or ttl_seconds <= 0:
        return None
    path = Path(cache_dir) / f"{cache_key(url)}.json"
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


def write_cache(cache_dir: str | None, url: str, response: dict[str, Any]) -> None:
    if not cache_dir:
        return
    path = Path(cache_dir) / f"{cache_key(url)}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "cached_at": time.time(),
                "url": url,
                "response": response,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def normalize_response(data: Any) -> dict[str, Any]:
    if isinstance(data, list):
        return {"result": data}
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected JSON response type: {type(data).__name__}")
    return data


def get_json(url: str, key: str, timeout: int, auth_header: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=build_headers(key, auth_header), method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            data = normalize_response(json.loads(raw))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc}") from exc
    if str(data.get("code", "0")) not in {"0", ""}:
        raise RuntimeError(json.dumps({"code": data.get("code"), "message": data.get("message")}, ensure_ascii=False))
    return data


def baike_get(
    url: str,
    keys: list[str],
    timeout: int,
    auth_header: str,
    cache_dir: str | None,
    cache_ttl_seconds: int,
) -> dict[str, Any]:
    cached = read_cache(cache_dir, url, cache_ttl_seconds)
    if cached is not None:
        return {
            "url": url,
            "key_id": "cache",
            "elapsed_ms": 0,
            "cache_hit": True,
            "response": cached,
        }
    if not keys:
        raise RuntimeError(f"No API keys found. Set {DEFAULT_KEY_ENV}.")
    errors: list[dict[str, str]] = []
    for key in keys:
        try:
            started = time.time()
            response = get_json(url, key, timeout=timeout, auth_header=auth_header)
            write_cache(cache_dir, url, response)
            return {
                "url": url,
                "key_id": key_id(key),
                "elapsed_ms": int((time.time() - started) * 1000),
                "cache_hit": False,
                "response": response,
            }
        except Exception as exc:
            errors.append({"key_id": key_id(key), "error": str(exc)})
    raise RuntimeError(json.dumps({"message": "All Baidu Baike API keys failed", "errors": errors}, ensure_ascii=False))


def result_items(response: dict[str, Any]) -> list[dict[str, Any]]:
    result = response.get("result")
    if isinstance(result, list):
        return [item for item in result if isinstance(item, dict)]
    if isinstance(result, dict):
        items = result.get("items")
        if isinstance(items, list):
            return [item for item in items if isinstance(item, dict)]
        return [result]
    return []


def content_result(response: dict[str, Any]) -> dict[str, Any] | None:
    result = response.get("result")
    return result if isinstance(result, dict) else None


def render_lookup_pack(summary: dict[str, Any], candidates: list[dict[str, Any]], contents: list[dict[str, Any]], fallback_refs: list[dict[str, Any]]) -> str:
    lines = [
        f"# Baidu Lookup Pack: {summary['topic']}",
        "",
        "## Summary",
        "",
        f"- Mode: `{summary['mode']}`",
        f"- Candidate count: {summary['candidate_count']}",
        f"- Content count: {summary['content_count']}",
        f"- Fallback search used: `{summary['fallback_search_used']}`",
        f"- Cache hits: {summary['cache_hit_count']}",
        f"- Errors: {summary['error_count']}",
        "",
    ]
    lines.extend(["## Baike Candidates", ""])
    if not candidates:
        lines.append("- None")
    for index, item in enumerate(candidates, start=1):
        title = item.get("lemma_title") or item.get("title") or "Untitled"
        desc = item.get("lemma_desc") or ""
        lemma_id = item.get("lemma_id") or ""
        url = item.get("url") or ""
        default_mark = " default" if item.get("is_default") == 1 else ""
        lines.extend(
            [
                f"### baike_candidate_{index:02d}{default_mark} - {title}",
                "",
                f"- Lemma ID: {lemma_id}",
                f"- Description: {desc}",
                f"- URL: {url}",
                "",
            ]
        )
    lines.extend(["## Baike Content", ""])
    if not contents:
        lines.append("- None")
    for index, item in enumerate(contents, start=1):
        title = item.get("lemma_title") or "Untitled"
        desc = item.get("lemma_desc") or ""
        lemma_id = item.get("lemma_id") or ""
        url = item.get("url") or ""
        summary_text = item.get("summary") or item.get("abstract_plain") or ""
        pic_url = item.get("pic_url") or item.get("square_pic_url") or ""
        lines.extend(
            [
                f"### baike_content_{index:02d} - {title}",
                "",
                f"- Lemma ID: {lemma_id}",
                f"- Description: {desc}",
                f"- URL: {url}",
                f"- Image: {pic_url}",
                "",
                "Summary:",
                "",
                summary_text.strip() or "No summary returned.",
                "",
            ]
        )
        relations = item.get("relations")
        if isinstance(relations, list) and relations:
            lines.extend(["Relations:", ""])
            for rel in relations[:10]:
                if isinstance(rel, dict):
                    rel_name = rel.get("relation_name") or "related"
                    rel_title = rel.get("lemma_title") or ""
                    rel_id = rel.get("lemma_id") or ""
                    lines.append(f"- {rel_name}: {rel_title} ({rel_id})")
            lines.append("")
    lines.extend(["## Fallback Web Results", ""])
    if not fallback_refs:
        lines.append("- None")
    for index, ref in enumerate(fallback_refs, start=1):
        title = ref.get("title") or "Untitled"
        url = ref.get("url") or ""
        snippet = ref.get("snippet") or ref.get("content") or ""
        lines.extend(
            [
                f"### web_fallback_{index:02d} - {title}",
                "",
                f"- URL: {url}",
                f"- Website: {ref.get('website') or ''}",
                f"- Snippet: {snippet}",
                "",
            ]
        )
    lines.extend(
        [
            "## Limitations",
            "",
            "- Baike lookup is best for entity definitions and disambiguation.",
            "- Baike is not a substitute for broad web research, recent news, reviews, complaints, or forum discussion.",
            "- Use web search or research mode when the user asks for current information, opinions, comparison, defects, or coverage across sources.",
            "",
        ]
    )
    return "\n".join(lines)


def run_lookup(args: argparse.Namespace) -> dict[str, Any]:
    topic = (args.topic_opt or args.topic or "").strip()
    if not topic:
        raise RuntimeError("Missing topic.")
    out_dir = Path(args.out_dir) if args.out_dir else default_out_dir(topic)
    out_dir.mkdir(parents=True, exist_ok=True)

    candidates_path = out_dir / "baike_candidates.json"
    contents_path = out_dir / "baike_content.json"
    fallback_path = out_dir / "fallback_web_results.json"
    errors_path = out_dir / "errors.jsonl"
    summary_path = out_dir / "run_summary.json"
    pack_path = out_dir / "lookup_pack.md"
    errors_path.write_text("", encoding="utf-8")

    list_url = build_url(
        args.baike_base_url,
        LIST_PATH,
        {"lemma_title": topic, "top_k": clamp_top_k(args.top_k)},
    )
    if args.dry_run:
        print(
            json.dumps(
                {
                    "mode": "lookup",
                    "topic": topic,
                    "list_url": list_url,
                    "content_url_template": build_url(args.baike_base_url, CONTENT_PATH, {"search_type": "lemmaId", "search_key": "<lemma_id>"}),
                    "fallback_search": args.fallback_search,
                    "out_dir": str(out_dir),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return {"topic": topic, "mode": "lookup", "dry_run": True, "out_dir": str(out_dir)}

    keys = load_keys(args.key_env)
    if not keys:
        raise RuntimeError(f"No API keys found. Set {args.key_env}.")

    started = time.time()
    error_count = 0
    cache_hit_count = 0
    fallback_refs: list[dict[str, Any]] = []
    contents: list[dict[str, Any]] = []

    list_result = baike_get(
        list_url,
        keys=keys,
        timeout=args.timeout,
        auth_header=args.auth_header,
        cache_dir=None if args.no_cache else args.cache_dir,
        cache_ttl_seconds=args.cache_ttl,
    )
    cache_hit_count += 1 if list_result.get("cache_hit") else 0
    candidates = result_items(list_result["response"])

    if not args.no_content:
        for candidate in candidates[: max(args.content_limit, 0)]:
            lemma_id = candidate.get("lemma_id")
            if lemma_id:
                content_params = {"search_type": "lemmaId", "search_key": str(lemma_id)}
            else:
                content_params = {"search_type": "lemmaTitle", "search_key": str(candidate.get("lemma_title") or topic)}
            content_url = build_url(args.baike_base_url, CONTENT_PATH, content_params)
            try:
                content_call = baike_get(
                    content_url,
                    keys=keys,
                    timeout=args.timeout,
                    auth_header=args.auth_header,
                    cache_dir=None if args.no_cache else args.cache_dir,
                    cache_ttl_seconds=args.cache_ttl,
                )
                cache_hit_count += 1 if content_call.get("cache_hit") else 0
                content = content_result(content_call["response"])
                if content:
                    contents.append(content)
            except Exception as exc:
                error_count += 1
                with errors_path.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps({"stage": "content", "candidate": candidate, "error": str(exc)}, ensure_ascii=False) + "\n")

    fallback_used = False
    if args.fallback_search and not candidates:
        fallback_used = True
        try:
            fallback = search_baidu(
                query=topic,
                top_k=args.fallback_top_k,
                keys=keys,
                edition="lite",
                timeout=args.timeout,
                auth_header=args.auth_header,
                cache_dir=None if args.no_cache else str(default_web_cache_dir()),
                cache_ttl_seconds=args.cache_ttl,
            )
            cache_hit_count += 1 if fallback.get("cache_hit") else 0
            fallback_refs = extract_references(fallback)
        except Exception as exc:
            error_count += 1
            with errors_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps({"stage": "fallback_search", "error": str(exc)}, ensure_ascii=False) + "\n")

    candidates_path.write_text(json.dumps({"topic": topic, "items": candidates, "raw": list_result["response"]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    contents_path.write_text(json.dumps({"topic": topic, "items": contents}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fallback_path.write_text(json.dumps({"topic": topic, "items": fallback_refs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = {
        "topic": topic,
        "mode": "lookup",
        "candidate_count": len(candidates),
        "content_count": len(contents),
        "fallback_search_used": fallback_used,
        "fallback_result_count": len(fallback_refs),
        "error_count": error_count,
        "cache_hit_count": cache_hit_count,
        "cache_enabled": not args.no_cache,
        "cache_dir": None if args.no_cache else args.cache_dir,
        "cache_ttl": args.cache_ttl,
        "elapsed_seconds": round(time.time() - started, 2),
        "out_dir": str(out_dir),
        "baike_candidates": str(candidates_path),
        "baike_content": str(contents_path),
        "fallback_web_results": str(fallback_path),
        "lookup_pack": str(pack_path),
        "errors": str(errors_path),
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pack_path.write_text(render_lookup_pack(summary, candidates, contents, fallback_refs), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", nargs="?")
    parser.add_argument("--topic", dest="topic_opt")
    parser.add_argument("--top-k", type=int, default=5, help="Baike candidate count, 1-100.")
    parser.add_argument("--content-limit", type=int, default=1, help="Fetch full content for the first N candidates.")
    parser.add_argument("--no-content", action="store_true", help="Only fetch candidate list.")
    parser.add_argument("--fallback-search", action="store_true", help="Run one lite web search if Baike returns no candidates.")
    parser.add_argument("--fallback-top-k", type=int, default=10)
    parser.add_argument("--out-dir")
    parser.add_argument("--key-env", default=DEFAULT_KEY_ENV)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--auth-header", choices=["authorization", "x-appbuilder", "both"], default="authorization")
    parser.add_argument("--baike-base-url", default=BAIKE_BASE_URL)
    parser.add_argument("--cache-dir", default=str(default_cache_dir()), help="Baike cache directory. API keys are never written.")
    parser.add_argument("--cache-ttl", type=int, default=86400)
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        result = run_lookup(args)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if not args.dry_run:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
