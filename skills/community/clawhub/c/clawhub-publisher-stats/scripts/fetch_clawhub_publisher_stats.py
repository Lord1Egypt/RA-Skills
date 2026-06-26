#!/usr/bin/env python3
"""Fetch live ClawHub publisher metrics from public pages."""

from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from typing import Any


USER_AGENT = "Mozilla/5.0 (Codex ClawHub Publisher Stats)"
AUTHOR_TABLE_URL = "https://topclawhubskills.com/"
SEARCH_API_URL = "https://topclawhubskills.com/api/search?q={query}&limit={limit}"
SKILL_PAGE_URL = "https://clawhub.ai/{handle}/{slug}"
STAT_PATTERN = re.compile(
    r"(comments|downloads|installsAllTime|installsCurrent|stars):(\d+)"
)
AUTHOR_ROW_PATTERN = re.compile(
    r'<tr data-search="(?P<handle>[^"]+)">\s*'
    r'<td class="rank[^"]*">(?P<rank>\d+)</td>\s*'
    r'<td><a href="https://github\.com/[^"]+" target="_blank" class="skill-name">@(?P=handle)</a></td>\s*'
    r'<td class="num">(?P<skills>[^<]+)</td>\s*'
    r'<td class="num">(?P<downloads>[^<]+)</td>\s*'
    r'<td class="num">(?P<stars>[^<]+)</td>',
    re.IGNORECASE,
)


@dataclass
class AuthorStats:
    handle: str
    rank: int | None
    skills: int | None
    downloads_text: str | None
    stars: int | None


def fetch_text(url: str, timeout: int = 20) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "replace")


def parse_int(value: str | int | None) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    cleaned = value.strip().upper().replace(",", "")
    multiplier = 1
    if cleaned.endswith("K"):
        multiplier = 1000
        cleaned = cleaned[:-1]
    elif cleaned.endswith("M"):
        multiplier = 1_000_000
        cleaned = cleaned[:-1]
    try:
        return int(float(cleaned) * multiplier)
    except ValueError:
        return None


def parse_author_stats(page_html: str, handle: str) -> AuthorStats:
    for match in AUTHOR_ROW_PATTERN.finditer(page_html):
        if match.group("handle").lower() != handle.lower():
            continue
        return AuthorStats(
            handle=handle,
            rank=parse_int(match.group("rank")),
            skills=parse_int(match.group("skills")),
            downloads_text=match.group("downloads").strip(),
            stars=parse_int(match.group("stars")),
        )
    return AuthorStats(handle=handle, rank=None, skills=None, downloads_text=None, stars=None)


def fetch_author_stats(handle: str) -> AuthorStats:
    page_html = fetch_text(AUTHOR_TABLE_URL)
    return parse_author_stats(page_html, handle)


def fetch_search_results(handle: str, limit: int) -> dict[str, Any]:
    url = SEARCH_API_URL.format(
        query=urllib.parse.quote(handle),
        limit=limit,
    )
    payload = json.loads(fetch_text(url))
    rows = payload.get("data", [])
    filtered = [row for row in rows if row.get("owner_handle", "").lower() == handle.lower()]
    return {
        "query_total": payload.get("total"),
        "returned": len(filtered),
        "rows": filtered,
        "generated_at": payload.get("generated_at"),
    }


def fetch_skill_page_stats(handle: str, slug: str) -> dict[str, Any]:
    url = SKILL_PAGE_URL.format(
        handle=urllib.parse.quote(handle),
        slug=urllib.parse.quote(slug),
    )
    page_html = fetch_text(url)
    stats = {name: int(value) for name, value in STAT_PATTERN.findall(page_html)}
    stats["url"] = url
    return stats


def enrich_rows(handle: str, rows: list[dict[str, Any]], workers: int) -> list[dict[str, Any]]:
    enriched = [dict(row) for row in rows]
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_map = {
            executor.submit(fetch_skill_page_stats, handle, row["slug"]): index
            for index, row in enumerate(enriched)
        }
        for future in concurrent.futures.as_completed(future_map):
            index = future_map[future]
            row = enriched[index]
            try:
                page_stats = future.result()
            except Exception as exc:  # noqa: BLE001
                row["skill_page_error"] = str(exc)
                row["url"] = SKILL_PAGE_URL.format(handle=handle, slug=row["slug"])
                continue

            row["downloads"] = page_stats.get("downloads", row.get("downloads"))
            row["stars"] = page_stats.get("stars", row.get("stars"))
            row["comments"] = page_stats.get("comments")
            row["installs_current"] = page_stats.get("installsCurrent")
            row["installs_all_time"] = page_stats.get("installsAllTime")
            row["url"] = page_stats["url"]
    return enriched


def normalize_rows(handle: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for row in rows:
        normalized.append(
            {
                "display_name": row.get("display_name"),
                "slug": row.get("slug"),
                "owner_handle": row.get("owner_handle", handle),
                "downloads": parse_int(row.get("downloads")),
                "stars": parse_int(row.get("stars")),
                "comments": parse_int(row.get("comments")),
                "installs_current": parse_int(row.get("installs_current")),
                "installs_all_time": parse_int(row.get("installs_all_time")),
                "created_at": row.get("created_at"),
                "updated_at": row.get("updated_at"),
                "summary": html.unescape(row.get("summary", "")),
                "is_certified": row.get("is_certified"),
                "is_deleted": row.get("is_deleted"),
                "url": row.get("url") or SKILL_PAGE_URL.format(handle=handle, slug=row.get("slug")),
                "skill_page_error": row.get("skill_page_error"),
            }
        )
    normalized.sort(key=lambda item: (-(item["downloads"] or 0), item["slug"] or ""))
    return normalized


def build_result(
    handle: str,
    limit: int,
    include_skill_pages: bool,
    workers: int,
) -> dict[str, Any]:
    author_stats = fetch_author_stats(handle)
    search_data = fetch_search_results(handle, limit)
    rows = search_data["rows"]
    if include_skill_pages and rows:
        rows = enrich_rows(handle, rows, workers)
    rows = normalize_rows(handle, rows)

    return {
        "handle": handle,
        "fetched_live": True,
        "source_limit": limit,
        "include_skill_pages": include_skill_pages,
        "generated_at": search_data.get("generated_at"),
        "author_stats": asdict(author_stats),
        "search_stats": {
            "returned_skills": len(rows),
            "query_total": search_data.get("query_total"),
            "author_total_skills": author_stats.skills,
            "search_total_may_be_partial": (
                author_stats.skills is not None
                and len(rows) < author_stats.skills
            ),
        },
        "notes": [
            "Author aggregate stats come from the Top Authors table on topclawhubskills.com.",
            "Per-skill rows come from the public search API and are filtered to the exact owner handle.",
            "Current installs, all-time installs, and comments require skill-page fetches.",
            "A separate public user rating field was not detected on sampled ClawHub skill pages.",
        ],
        "skills": rows,
    }


def render_markdown(result: dict[str, Any]) -> str:
    author = result["author_stats"]
    search = result["search_stats"]
    lines = [
        f"# ClawHub Publisher Stats: @{result['handle']}",
        "",
        "## Author Summary",
        f"- Rank: {author['rank'] if author['rank'] is not None else 'unavailable'}",
        f"- Published skills: {author['skills'] if author['skills'] is not None else 'unavailable'}",
        f"- Total downloads: {author['downloads_text'] or 'unavailable'}",
        f"- Total stars: {author['stars'] if author['stars'] is not None else 'unavailable'}",
        "",
        "## Search Coverage",
        f"- Returned per-skill rows: {search['returned_skills']}",
        f"- Search API total: {search['query_total']}",
        f"- Aggregate author skill total: {search['author_total_skills']}",
        f"- Search results may be partial: {'yes' if search['search_total_may_be_partial'] else 'no'}",
        "",
        "## Skills",
        "",
        "| Skill | Downloads | Current Installs | All-time Installs | Stars | Comments |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for skill in result["skills"]:
        lines.append(
            "| [{name}]({url}) | {downloads} | {current} | {all_time} | {stars} | {comments} |".format(
                name=skill["display_name"] or skill["slug"],
                url=skill["url"],
                downloads=skill["downloads"] if skill["downloads"] is not None else "n/a",
                current=(
                    skill["installs_current"]
                    if skill["installs_current"] is not None
                    else "n/a"
                ),
                all_time=(
                    skill["installs_all_time"]
                    if skill["installs_all_time"] is not None
                    else "n/a"
                ),
                stars=skill["stars"] if skill["stars"] is not None else "n/a",
                comments=skill["comments"] if skill["comments"] is not None else "n/a",
            )
        )
    lines.extend(["", "## Notes"])
    lines.extend([f"- {note}" for note in result["notes"]])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch live ClawHub publisher metrics."
    )
    parser.add_argument("--user", required=True, help="Publisher handle, e.g. harrylabsj")
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of search API skill rows to retrieve.",
    )
    parser.add_argument(
        "--include-skill-pages",
        action="store_true",
        help="Fetch each skill page to populate install and comment counts.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=6,
        help="Concurrent skill-page fetch workers.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = build_result(
            handle=args.user,
            limit=max(1, args.limit),
            include_skill_pages=args.include_skill_pages,
            workers=max(1, args.workers),
        )
    except urllib.error.URLError as exc:
        print(f"Network error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to fetch publisher stats: {exc}", file=sys.stderr)
        return 1

    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
