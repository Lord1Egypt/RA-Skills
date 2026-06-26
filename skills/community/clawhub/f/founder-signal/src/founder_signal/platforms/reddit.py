"""Reddit platform adapter backed by Eddrit discovery and evidence reads."""

from __future__ import annotations

import html
import re
import sys
from typing import Any
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from ..models import FounderSignalConfig
from ..reddit_fetcher import fetch_reddit_evidence, is_placeholder_reddit_url, persist_verified_text_snapshot, to_eddrit_url

_EDDRIT_LINK_RE = re.compile(
    r'href="(?P<href>(?:https://eddrit\.com)?/r/[^"/]+/comments/[^"#?]+(?:/[^"#?]+)?/?)"',
    re.IGNORECASE,
)
_MAX_DISCOVERY_PAGES = 12
PLATFORM = "reddit"


def discover_candidates(
    config: FounderSignalConfig,
    *,
    excluded_source_ids: set[str] | None = None,
    opener=urlopen,
    timeout_seconds: float = 20.0,
) -> list[dict[str, Any]]:
    """Return deterministic Reddit candidates from Eddrit, hints, and snapshots."""
    candidates: list[dict[str, Any]] = []
    seen_ids = {source_id for source_id in (excluded_source_ids or set()) if source_id.strip()}

    for reddit_url, discovery_url in _discover_from_eddrit(
        config,
        excluded_source_ids=seen_ids,
        opener=opener,
        timeout_seconds=timeout_seconds,
    ):
        _append_candidate(
            candidates=candidates,
            seen_ids=seen_ids,
            source_url=reddit_url,
            source_type="eddrit_discovery",
            discovery_method="eddrit_search",
            discovery_url=discovery_url,
            max_candidates=config.max_candidates,
        )
        if len(candidates) >= config.max_candidates:
            return candidates

    for reddit_url in config.seed_reddit_urls:
        normalized = reddit_url.strip()
        if not normalized or is_placeholder_reddit_url(normalized):
            continue
        if not to_eddrit_url(normalized):
            continue
        _append_candidate(
            candidates=candidates,
            seen_ids=seen_ids,
            source_url=normalized,
            source_type="configured_reddit_hint",
            discovery_method="configured_hint_after_discovery",
            discovery_url="",
            max_candidates=config.max_candidates,
        )
        if len(candidates) >= config.max_candidates:
            return candidates

    for snapshot in config.verified_evidence_snapshots:
        if snapshot.platform != PLATFORM:
            continue
        normalized = snapshot.source_url.strip()
        if not normalized or is_placeholder_reddit_url(normalized):
            continue
        _append_candidate(
            candidates=candidates,
            seen_ids=seen_ids,
            source_url=normalized,
            source_type="verified_evidence_snapshot",
            discovery_method=snapshot.verification_method or "agent_browser",
            discovery_url="",
            max_candidates=config.max_candidates,
            extra={
                "text_snapshot": snapshot.text_snapshot,
                "verification_method": snapshot.verification_method or "agent_browser",
                "verified_by": snapshot.verified_by,
            },
        )
        if len(candidates) >= config.max_candidates:
            return candidates

    return candidates


def hydrate_candidate(candidate: dict[str, Any], run_dir):
    if str(candidate.get("source_type") or "") == "verified_evidence_snapshot":
        persister = _public_override("persist_verified_text_snapshot", persist_verified_text_snapshot)
        return persister(
            candidate_id=str(candidate["candidate_id"]),
            reddit_url=str(candidate["source_url"]),
            text_snapshot=str(candidate.get("text_snapshot") or ""),
            run_dir=run_dir,
            verification_method=str(candidate.get("verification_method") or "agent_browser"),
        )
    fetcher = _public_override("fetch_reddit_evidence", fetch_reddit_evidence)
    return fetcher(
        candidate_id=str(candidate["candidate_id"]),
        reddit_url=str(candidate["source_url"]),
        run_dir=run_dir,
    )


def _public_override(name: str, fallback):
    """Respect legacy tests/callers that monkeypatch top-level package exports."""
    package = sys.modules.get("founder_signal")
    if package is None:
        return fallback
    return getattr(package, name, fallback)


def canonical_source_id(source_url: str) -> str:
    return f"{PLATFORM}:{source_url.strip()}"


def _discover_from_eddrit(
    config: FounderSignalConfig,
    *,
    excluded_source_ids: set[str],
    opener,
    timeout_seconds: float,
) -> list[tuple[str, str]]:
    discovered: list[tuple[str, str]] = []
    seen: set[str] = set()
    for discovery_url in _build_discovery_urls(config):
        try:
            request = Request(
                discovery_url,
                headers={"User-Agent": "FounderSignal/0.1 (+eddrit deterministic discovery)"},
            )
            with opener(request, timeout=timeout_seconds) as response:
                body = response.read()
                charset = getattr(response.headers, "get_content_charset", lambda default=None: default)(
                    "utf-8"
                )
            raw_html = body.decode(charset or "utf-8", errors="replace")
        except Exception:
            continue

        for reddit_url in extract_reddit_urls_from_eddrit_html(raw_html):
            source_id = canonical_source_id(reddit_url)
            if source_id in seen or source_id in excluded_source_ids or reddit_url in excluded_source_ids:
                continue
            seen.add(source_id)
            discovered.append((reddit_url, discovery_url))
            if len(discovered) >= config.max_candidates:
                return discovered
    return discovered


def _build_discovery_urls(config: FounderSignalConfig) -> list[str]:
    urls: list[str] = []
    subreddits = [item.strip().strip("/") for item in config.subreddits if item.strip()]
    terms = [item.strip() for item in config.keywords if item.strip()]
    terms.extend(item.strip() for item in config.scoring_terms if item.strip())
    terms.append(config.product_name.strip())

    seen_queries: set[str] = set()
    for subreddit in subreddits:
        for term in terms:
            query = f"subreddit:{subreddit} {term}".strip()
            normalized = query.lower()
            if normalized in seen_queries:
                continue
            seen_queries.add(normalized)
            urls.append(f"https://eddrit.com/search?q={quote_plus(query)}")
            if len(urls) >= _MAX_DISCOVERY_PAGES:
                return urls

    for subreddit in subreddits:
        urls.append(f"https://eddrit.com/r/{quote_plus(subreddit)}")
        if len(urls) >= _MAX_DISCOVERY_PAGES:
            return urls

    return urls


def extract_reddit_urls_from_eddrit_html(raw_html: str) -> list[str]:
    """Extract Reddit comments URLs from Eddrit listing or search HTML."""
    urls: list[str] = []
    seen: set[str] = set()
    for match in _EDDRIT_LINK_RE.finditer(raw_html):
        href = html.unescape(match.group("href"))
        if href.startswith("https://eddrit.com"):
            path = href.removeprefix("https://eddrit.com")
        else:
            path = href
        reddit_url = f"https://www.reddit.com{path}"
        if is_placeholder_reddit_url(reddit_url):
            continue
        if reddit_url in seen:
            continue
        seen.add(reddit_url)
        urls.append(reddit_url)
    return urls


def _append_candidate(
    *,
    candidates: list[dict[str, Any]],
    seen_ids: set[str],
    source_url: str,
    source_type: str,
    discovery_method: str,
    discovery_url: str,
    max_candidates: int,
    extra: dict[str, Any] | None = None,
) -> None:
    normalized = source_url.strip()
    source_id = canonical_source_id(normalized)
    if not normalized or source_id in seen_ids or normalized in seen_ids or len(candidates) >= max_candidates:
        return
    seen_ids.add(source_id)
    candidate_id = f"cand-{len(candidates) + 1:03d}"
    payload: dict[str, Any] = {
        "candidate_id": candidate_id,
        "platform": PLATFORM,
        "source_platform": PLATFORM,
        "source_id": source_id,
        "source_url": normalized,
        "reddit_url": normalized,
        "source_type": source_type,
        "discovery_method": discovery_method,
    }
    if discovery_url:
        payload["discovery_url"] = discovery_url
    if extra:
        payload.update(extra)
    candidates.append(payload)
