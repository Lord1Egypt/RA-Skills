"""GitHub Issues Search API backend for /depradar.

Searches GitHub for issues mentioning a package + breaking change keywords.
Free: 60 req/hr unauth, 5000 req/hr with GITHUB_TOKEN.
"""
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
import importlib.util as _ilu
if "_depradar_http" not in sys.modules:
    _http_spec = _ilu.spec_from_file_location("_depradar_http", str(Path(__file__).parent / "http.py"))
    _http_mod = _ilu.module_from_spec(_http_spec)   # type: ignore[arg-type]
    sys.modules["_depradar_http"] = _http_mod
    _http_spec.loader.exec_module(_http_mod)         # type: ignore[union-attr]
_http_mod = sys.modules["_depradar_http"]
get_json      = _http_mod.get_json
RateLimitError = _http_mod.RateLimitError
NotFoundError  = _http_mod.NotFoundError
HttpError      = _http_mod.HttpError
from schema import GithubIssueItem, SubScores
from dates import recency_score, days_ago, today_utc
import cache


GITHUB_SEARCH_URL = "https://api.github.com/search/issues"

DEPTH_CONFIG = {
    "quick":   {"queries_per_pkg": 1, "results_per_query": 5,  "max_results": 5},
    "default": {"queries_per_pkg": 2, "results_per_query": 10, "max_results": 15},
    "deep":    {"queries_per_pkg": 3, "results_per_query": 20, "max_results": 30},
}


def search_issues(
    packages: List[str],
    repos: Dict[str, str],
    days: int = 30,
    depth: str = "default",
    token: Optional[str] = None,
) -> List[GithubIssueItem]:
    """Search GitHub Issues for breaking change pain reports for each package.

    Runs package searches in parallel. Returns scored + sorted items.
    """
    all_items: List[GithubIssueItem] = []

    with ThreadPoolExecutor(max_workers=min(len(packages), 5)) as executor:
        future_to_pkg = {
            executor.submit(
                _search_package,
                pkg,
                repos.get(pkg),
                days,
                depth,
                token,
            ): pkg
            for pkg in packages
        }
        for future in as_completed(future_to_pkg):
            try:
                items = future.result()
                all_items.extend(items)
            except Exception:
                pass

    deduped = _dedupe(all_items)
    deduped.sort(key=lambda x: x.score, reverse=True)
    return deduped


def _search_package(
    package: str,
    repo: Optional[str],
    days: int,
    depth: str,
    token: Optional[str],
) -> List[GithubIssueItem]:
    """Search issues for a single package. Returns up to max_results items."""
    cfg = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])
    max_results: int = cfg["max_results"]
    results_per_query: int = cfg["results_per_query"]

    since_date = days_ago(days)
    queries = _build_queries(package, repo, since_date, depth)

    cache_key = cache.cache_key("gh_issues", package, repo or "", days, depth)
    cached = cache.load(cache_key, ttl_hours=cache.COMMUNITY_TTL_HOURS, namespace="gh_issues")
    if cached is not None:
        return [GithubIssueItem.from_dict(d) for d in cached]

    seen_urls: set = set()
    items: List[GithubIssueItem] = []
    headers = _github_headers(token)

    for query in queries:
        if len(items) >= max_results:
            break
        try:
            data = get_json(
                GITHUB_SEARCH_URL,
                headers=headers,
                params={
                    "q": query,
                    "sort": "created",
                    "order": "desc",
                    "per_page": results_per_query,
                },
            )
        except RateLimitError:
            break
        except (HttpError, NotFoundError):
            continue

        for idx, raw in enumerate(data.get("items", [])):
            url = raw.get("html_url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            item = _parse_issue(raw, package, len(items) + 1)
            item = _score_issue(item)
            items.append(item)
            if len(items) >= max_results:
                break

    # Reassign sequential IDs after collecting all
    for i, item in enumerate(items, 1):
        item.id = f"GI{i}"

    cache.save(cache_key, [it.to_dict() for it in items], namespace="gh_issues")
    return items


def _build_queries(package: str, repo: Optional[str], since_date: str, depth: str) -> List[str]:
    """Build 1-3 GitHub search query strings."""
    cfg = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])
    queries_per_pkg: int = cfg["queries_per_pkg"]

    queries: List[str] = []

    # Query 1: repo-scoped label search (most precise)
    if repo:
        queries.append(
            f'repo:{repo} label:breaking-change created:>{since_date}'
        )
    else:
        queries.append(
            f'"{package}" "breaking change" is:issue created:>{since_date}'
        )

    if queries_per_pkg >= 2:
        # Query 2: broad breaking change mention
        queries.append(
            f'"{package}" "breaking change" is:issue created:>{since_date}'
        )

    if queries_per_pkg >= 3:
        # Query 3: migration pain
        queries.append(
            f'"{package}" migration is:issue created:>{since_date}'
        )

    return queries[:queries_per_pkg]


def _parse_issue(raw: dict, package: str, idx: int) -> GithubIssueItem:
    """Convert raw GitHub API issue object to GithubIssueItem."""
    labels = [lbl.get("name", "") for lbl in raw.get("labels", [])]
    body = raw.get("body") or ""
    body_snippet = body[:400].strip() if body else None

    # Try to extract version from title / body
    import re
    version = ""
    ver_match = re.search(r"v?(\d+\.\d+[\.\d]*)", raw.get("title", "") + " " + body[:200])
    if ver_match:
        version = ver_match.group(0).lstrip("v")

    return GithubIssueItem(
        id=f"GI{idx}",
        package=package,
        version=version,
        title=raw.get("title", ""),
        url=raw.get("html_url", ""),
        body_snippet=body_snippet,
        comments=raw.get("comments", 0),
        labels=labels,
        state=raw.get("state", "open"),
        resolution_snippet=None,
        created_at=raw.get("created_at"),
        subs=SubScores(),
        score=0,
        cross_refs=[],
    )


def _score_issue(item: GithubIssueItem) -> GithubIssueItem:
    """Apply scoring formula.

    severity: if "breaking" in labels → 80, "bug" → 50, else 40
    recency: recency_score(created_at)
    impact: min(100, comments * 3)
    community: 50
    score = 0.30*severity + 0.30*recency + 0.25*impact + 0.15*community
    """
    label_names = [lbl.lower() for lbl in item.labels]

    severity = 40
    if any("breaking" in lbl for lbl in label_names):
        severity = 80
    elif any("bug" in lbl for lbl in label_names):
        severity = 50

    recency = recency_score(item.created_at)
    impact = min(100, item.comments * 3)
    community = 50

    raw_score = (
        0.30 * severity
        + 0.30 * recency
        + 0.25 * impact
        + 0.15 * community
    )
    item.subs = SubScores(
        severity=severity,
        recency=recency,
        impact=impact,
        community=community,
    )
    item.score = min(100, int(round(raw_score)))
    return item


def _dedupe(items: List[GithubIssueItem]) -> List[GithubIssueItem]:
    """Remove duplicate URLs."""
    seen: set = set()
    result: List[GithubIssueItem] = []
    for item in items:
        if item.url not in seen:
            seen.add(item.url)
            result.append(item)
    return result


def _github_headers(token: Optional[str]) -> Dict[str, str]:
    hdrs = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        hdrs["Authorization"] = f"Bearer {token}"
    return hdrs
