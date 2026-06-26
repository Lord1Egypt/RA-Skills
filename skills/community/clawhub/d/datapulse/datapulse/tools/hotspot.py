"""Unified hotspot evidence pack workflow for Reddit/X/Web + GitHub verification."""

from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any
from urllib.parse import urlparse

from datapulse.collectors.github import GitHubCollector
from datapulse.core.models import DataPulseItem, SourceType
from datapulse.core.utils import extract_urls
from datapulse.reader import DataPulseReader


def extract_repo_slug(url: str) -> str:
    parsed = urlparse(str(url or "").strip())
    host = (parsed.hostname or "").lower()
    if host not in {"github.com", "www.github.com"}:
        return ""
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return ""
    owner = parts[0].strip()
    repo = parts[1].strip()
    if repo.endswith(".git"):
        repo = repo[:-4]
    if not owner or not repo:
        return ""
    return f"{owner.lower()}/{repo.lower()}"


def extract_repo_candidates(item: DataPulseItem) -> list[str]:
    repos: list[str] = []
    if direct := extract_repo_slug(item.url):
        repos.append(direct)

    text_blob = " ".join(
        value for value in [
            item.title,
            item.excerpt if hasattr(item, "excerpt") else "",
            item.content[:1000],
        ]
        if value
    )
    for url in extract_urls(text_blob):
        if repo := extract_repo_slug(url):
            repos.append(repo)

    extra = item.extra if isinstance(item.extra, dict) else {}
    for repo in extra.get("github_repos", []) if isinstance(extra.get("github_repos"), list) else []:
        normalized = str(repo).strip().lower()
        if normalized and "/" in normalized:
            repos.append(normalized)
    for url in extra.get("comment_links", []) if isinstance(extra.get("comment_links"), list) else []:
        if repo := extract_repo_slug(str(url)):
            repos.append(repo)

    out: list[str] = []
    seen: set[str] = set()
    for repo in repos:
        if repo in seen:
            continue
        seen.add(repo)
        out.append(repo)
    return out


async def build_hotspot_evidence_pack(
    *,
    query: str,
    platform: str = "reddit",
    provider: str = "auto",
    time_range: str = "month",
    limit: int = 12,
    min_confidence: float = 0.75,
    read_reddit_thread: bool = True,
) -> list[dict[str, Any]]:
    reader = DataPulseReader()
    github = GitHubCollector()

    search_items = await reader.search(
        query,
        platform=None if platform == "web" else platform,
        provider=provider,
        time_range=time_range,
        limit=limit,
        fetch_content=False,
        min_confidence=0.0,
    )

    best_by_repo: dict[str, dict[str, Any]] = {}

    for item in search_items:
        repo_candidates = extract_repo_candidates(item)
        if (
            read_reddit_thread
            and item.source_type == SourceType.REDDIT
            and not repo_candidates
        ):
            try:
                enriched = await reader.read(item.url, min_confidence=0.0)
                repo_candidates.extend(extract_repo_candidates(enriched))
            except Exception:
                pass

        for repo in repo_candidates:
            gh_result = await asyncio.to_thread(github.parse, f"https://github.com/{repo}")
            repo_meta = gh_result.extra if gh_result.success else {}
            repo_degraded = bool(repo_meta.get("api_degraded", not gh_result.success))

            confidence = float(item.confidence)
            factors = list(item.confidence_factors)
            if repo_degraded:
                confidence = max(0.01, confidence - 0.20)
                factors.append("github_repo_degraded")
            else:
                factors.append("github_repo_verified")
                stars = int(repo_meta.get("stars") or 0)
                if stars >= 200:
                    confidence = min(0.99, confidence + 0.03)

            confidence = round(confidence, 4)
            if confidence < min_confidence:
                continue

            record = {
                "topic": query,
                "source_url": item.url,
                "source_title": item.title,
                "source_type": item.source_type.value,
                "github_repo": repo,
                "github_url": f"https://github.com/{repo}",
                "confidence": confidence,
                "factors": list(dict.fromkeys(factors)),
                "fetched_at": item.fetched_at,
                "cross_validation": (
                    item.extra.get("search_cross_validation")
                    or item.extra.get("search_consistency")
                    or {}
                ),
                "repo_stars": int(repo_meta.get("stars") or 0),
                "repo_forks": int(repo_meta.get("forks") or 0),
                "repo_open_issues": int(repo_meta.get("open_issues") or 0),
                "repo_pushed_at": repo_meta.get("pushed_at", ""),
                "repo_release": repo_meta.get("release") or {},
                "repo_api_degraded": repo_degraded,
            }

            prev = best_by_repo.get(repo)
            if prev is None:
                best_by_repo[repo] = record
                continue
            if (
                record["confidence"] > prev["confidence"]
                or (
                    record["confidence"] == prev["confidence"]
                    and record["repo_stars"] > prev["repo_stars"]
                )
            ):
                best_by_repo[repo] = record

    ranked = list(best_by_repo.values())
    ranked.sort(key=lambda row: (row["confidence"], row["repo_stars"]), reverse=True)
    return ranked


def main() -> None:
    parser = argparse.ArgumentParser(description="Build hotspot evidence pack with GitHub cross-validation.")
    parser.add_argument("--query", required=True, help="Search query, e.g. 'data governance open source'")
    parser.add_argument("--platform", default="reddit", choices=["reddit", "twitter", "web"], help="Search platform")
    parser.add_argument("--provider", default="auto", choices=["auto", "tavily", "jina", "multi"], help="Search provider")
    parser.add_argument("--time-range", default="month", choices=["day", "week", "month", "year", "all"], help="Freshness window")
    parser.add_argument("--limit", type=int, default=12, help="Search candidate limit")
    parser.add_argument("--min-confidence", type=float, default=0.75, help="Output confidence threshold")
    parser.add_argument("--no-reddit-read", action="store_true", help="Skip secondary read() enrichment for reddit hits")
    args = parser.parse_args()

    records = asyncio.run(
        build_hotspot_evidence_pack(
            query=args.query,
            platform=args.platform,
            provider=args.provider,
            time_range=args.time_range,
            limit=max(1, int(args.limit)),
            min_confidence=max(0.0, min(1.0, float(args.min_confidence))),
            read_reddit_thread=not args.no_reddit_read,
        )
    )
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
