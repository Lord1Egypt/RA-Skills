"""Deterministic candidate discovery for Founder Signal."""

from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterator
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from .models import FounderSignalConfig
from .platforms import discover_all_candidates
from .reddit_fetcher import is_placeholder_reddit_url, to_eddrit_url

_EDDRIT_LINK_RE = re.compile(
    r'href="(?P<href>(?:https://eddrit\.com)?/r/[^"/]+/comments/[^"#?]+(?:/[^"#?]+)?/?)"',
    re.IGNORECASE,
)
_MAX_DISCOVERY_PAGES = 12
_LIVE_FEED_LIMIT = 25
_PLACEHOLDER_BODY_RE = re.compile(
    r"^(?:title|same as title|see title|following|bump|help|help me|any advice\??)\.?$",
    re.IGNORECASE,
)
_TERM_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "for",
        "from",
        "how",
        "i",
        "in",
        "is",
        "my",
        "of",
        "on",
        "or",
        "the",
        "to",
        "with",
    }
)
_HARD_NEGATIVE_PATTERNS = (
    "prediction",
    "predict",
    "benchmark",
    "leaderboard",
    "which model",
    "model release",
    "subscription",
    "worth the price",
    "news",
    "announcement",
    "announced",
    "launched",
)


@dataclass(frozen=True)
class DiscoveryResult:
    candidates: list[dict[str, Any]]
    metrics: dict[str, Any]

    def __iter__(self) -> Iterator[dict[str, Any]]:
        return iter(self.candidates)

    def __len__(self) -> int:
        return len(self.candidates)

    def __getitem__(self, index: int) -> dict[str, Any]:
        return self.candidates[index]


def discover_candidates(
    config: FounderSignalConfig,
    *,
    excluded_reddit_urls: set[str] | None = None,
    profile_excluded_reddit_urls: set[str] | None = None,
    history_excluded_reddit_urls: set[str] | None = None,
    excluded_source_ids: set[str] | None = None,
    opener=urlopen,
    timeout_seconds: float = 20.0,
) -> DiscoveryResult:
    """Return deterministic candidates from Reddit live/research or federated adapters."""
    active_platforms = sorted(config.platforms)
    if active_platforms and active_platforms != ["reddit"]:
        exclusions = {item for item in (excluded_source_ids or set()) if item.strip()}
        for url in excluded_reddit_urls or set():
            normalized = url.strip()
            if normalized:
                exclusions.add(normalized)
                exclusions.add(f"reddit:{normalized}")
        candidates = discover_all_candidates(
            config,
            excluded_source_ids=exclusions,
            opener=opener,
            timeout_seconds=timeout_seconds,
        )
        metrics = _new_discovery_metrics()
        metrics["fresh_candidates_found"] = len(candidates)
        return DiscoveryResult(candidates=candidates, metrics=metrics)

    candidates: list[dict[str, Any]] = []
    seen_urls: set[str] = {
        url.strip() for url in (excluded_reddit_urls or set()) if url.strip()
    }
    profile_excluded = {
        url.strip() for url in (profile_excluded_reddit_urls or set()) if url.strip()
    }
    history_excluded = {
        url.strip() for url in (history_excluded_reddit_urls or set()) if url.strip()
    }
    metrics = _new_discovery_metrics()

    if config.discovery_mode == "live":
        for payload in _discover_from_live_feeds(
            config,
            excluded_reddit_urls=seen_urls,
            profile_excluded_reddit_urls=profile_excluded,
            history_excluded_reddit_urls=history_excluded,
            opener=opener,
            timeout_seconds=timeout_seconds,
            metrics=metrics,
        ):
            _append_candidate(
                candidates=candidates,
                seen_urls=seen_urls,
                reddit_url=str(payload["reddit_url"]),
                source_type="live_reddit_feed",
                discovery_method="reddit_new_json",
                discovery_url=str(payload.get("discovery_url") or ""),
                max_candidates=config.max_candidates,
                extra={key: value for key, value in payload.items() if key != "reddit_url"},
            )
            if len(candidates) >= config.max_candidates:
                break

        metrics["fresh_candidates_found"] = len(candidates)
        metrics["no_live_candidate_found"] = len(candidates) == 0
        metrics["discovery_exhausted"] = bool(metrics["live_feed_requests"])
        return DiscoveryResult(candidates=candidates, metrics=metrics)

    for reddit_url, discovery_url in _discover_from_eddrit(
        config,
        excluded_reddit_urls=seen_urls,
        profile_excluded_reddit_urls=profile_excluded,
        history_excluded_reddit_urls=history_excluded,
        opener=opener,
        timeout_seconds=timeout_seconds,
        metrics=metrics,
    ):
        _append_candidate(
            candidates=candidates,
            seen_urls=seen_urls,
            reddit_url=reddit_url,
            source_type="eddrit_discovery",
            discovery_method="eddrit_search",
            discovery_url=discovery_url,
            max_candidates=config.max_candidates,
        )
        if len(candidates) >= config.max_candidates:
            metrics["fresh_candidates_found"] = len(candidates)
            return DiscoveryResult(candidates=candidates, metrics=metrics)

    metrics["fresh_candidates_found"] = len(candidates)
    metrics["discovery_exhausted"] = (
        metrics["searched_pages"] >= metrics["discovery_budget_pages"]
        and len(candidates) < config.max_candidates
    )

    for reddit_url in config.seed_reddit_urls:
        normalized = reddit_url.strip()
        if not normalized or is_placeholder_reddit_url(normalized):
            continue
        if not to_eddrit_url(normalized):
            continue
        _append_candidate(
            candidates=candidates,
            seen_urls=seen_urls,
            reddit_url=normalized,
            source_type="configured_reddit_hint",
            discovery_method="configured_hint_after_discovery",
            discovery_url="",
            max_candidates=config.max_candidates,
        )
        if len(candidates) >= config.max_candidates:
            return DiscoveryResult(candidates=candidates, metrics=metrics)

    for snapshot in config.verified_evidence_snapshots:
        if snapshot.platform != "reddit":
            continue
        normalized = snapshot.source_url.strip()
        if not normalized or is_placeholder_reddit_url(normalized):
            continue
        _append_candidate(
            candidates=candidates,
            seen_urls=seen_urls,
            reddit_url=normalized,
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
            return DiscoveryResult(candidates=candidates, metrics=metrics)

    return DiscoveryResult(candidates=candidates, metrics=metrics)


def _discover_from_eddrit(
    config: FounderSignalConfig,
    *,
    excluded_reddit_urls: set[str],
    profile_excluded_reddit_urls: set[str],
    history_excluded_reddit_urls: set[str],
    opener,
    timeout_seconds: float,
    metrics: dict[str, Any],
) -> list[tuple[str, str]]:
    discovered: list[tuple[str, str]] = []
    seen: set[str] = set()
    for discovery_url in _build_discovery_urls(config):
        metrics["searched_pages"] += 1
        metrics["searched_urls"].append(discovery_url)
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
            if reddit_url in seen:
                continue
            seen.add(reddit_url)
            if reddit_url in excluded_reddit_urls:
                if reddit_url in profile_excluded_reddit_urls:
                    metrics["excluded_by_profile"] += 1
                elif reddit_url in history_excluded_reddit_urls:
                    metrics["excluded_by_history"] += 1
                metrics["total_excluded"] += 1
                continue
            discovered.append((reddit_url, discovery_url))
            if len(discovered) >= config.max_candidates:
                return discovered
    return discovered


def _build_discovery_urls(config: FounderSignalConfig) -> list[str]:
    base_urls: list[str] = []
    subreddits = [item.strip().strip("/") for item in config.subreddits if item.strip()]
    terms = [item.strip() for item in config.keywords if item.strip()]
    if config.research_terms:
        terms.extend(item.strip() for item in config.research_terms if item.strip())
    elif config.discovery_terms:
        terms.extend(item.strip() for item in config.discovery_terms if item.strip())
    else:
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
            base_urls.append(f"https://eddrit.com/search?q={quote_plus(query)}")

    for subreddit in subreddits:
        base_urls.append(f"https://eddrit.com/r/{quote_plus(subreddit)}")

    if not base_urls:
        return []

    urls: list[str] = []
    page_number = 1
    while len(urls) < _MAX_DISCOVERY_PAGES:
        for base_url in base_urls:
            if page_number == 1:
                urls.append(base_url)
            elif "?" in base_url:
                urls.append(f"{base_url}&page={page_number}")
            else:
                urls.append(f"{base_url}?page={page_number}")
            if len(urls) >= _MAX_DISCOVERY_PAGES:
                return urls
        page_number += 1
    return urls


def _new_discovery_metrics() -> dict[str, Any]:
    return {
        "searched_pages": 0,
        "searched_urls": [],
        "live_feed_requests": 0,
        "live_feed_failures": 0,
        "live_feed_items_seen": 0,
        "filtered_candidates": 0,
        "filter_reason_counts": {},
        "excluded_by_history": 0,
        "excluded_by_profile": 0,
        "total_excluded": 0,
        "fresh_candidates_found": 0,
        "discovery_budget_pages": _MAX_DISCOVERY_PAGES,
        "discovery_exhausted": False,
        "no_live_candidate_found": False,
    }


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
    seen_urls: set[str],
    reddit_url: str,
    source_type: str,
    discovery_method: str,
    discovery_url: str,
    max_candidates: int,
    extra: dict[str, Any] | None = None,
) -> None:
    normalized = reddit_url.strip()
    if not normalized or normalized in seen_urls or len(candidates) >= max_candidates:
        return
    seen_urls.add(normalized)
    candidate_id = f"cand-{len(candidates) + 1:03d}"
    payload: dict[str, Any] = {
        "candidate_id": candidate_id,
        "platform": "reddit",
        "source_platform": "reddit",
        "source_id": f"reddit:{normalized}",
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


def _discover_from_live_feeds(
    config: FounderSignalConfig,
    *,
    excluded_reddit_urls: set[str],
    profile_excluded_reddit_urls: set[str],
    history_excluded_reddit_urls: set[str],
    opener,
    timeout_seconds: float,
    metrics: dict[str, Any],
) -> list[dict[str, Any]]:
    discovered: list[dict[str, Any]] = []
    seen: set[str] = set()
    now = datetime.now(timezone.utc)
    for subreddit in [item.strip().strip("/") for item in config.subreddits if item.strip()]:
        discovery_url = f"https://www.reddit.com/r/{quote_plus(subreddit)}/new.json?limit={_LIVE_FEED_LIMIT}"
        metrics["live_feed_requests"] += 1
        metrics["searched_pages"] += 1
        metrics["searched_urls"].append(discovery_url)
        try:
            request = Request(
                discovery_url,
                headers={
                    "User-Agent": "FounderSignal/0.1 (+live reddit discovery)",
                    "Accept": "application/json",
                },
            )
            with opener(request, timeout=timeout_seconds) as response:
                body = response.read()
                charset = getattr(response.headers, "get_content_charset", lambda default=None: default)(
                    "utf-8"
                )
            payload = json.loads(body.decode(charset or "utf-8", errors="replace"))
        except Exception:
            metrics["live_feed_failures"] += 1
            continue

        feed_candidates = extract_candidates_from_reddit_json(payload, now=now)
        metrics["live_feed_items_seen"] += len(feed_candidates)
        for candidate in feed_candidates:
            reddit_url = str(candidate["reddit_url"])
            if reddit_url in seen:
                continue
            seen.add(reddit_url)
            if reddit_url in excluded_reddit_urls:
                if reddit_url in profile_excluded_reddit_urls:
                    metrics["excluded_by_profile"] += 1
                elif reddit_url in history_excluded_reddit_urls:
                    metrics["excluded_by_history"] += 1
                metrics["total_excluded"] += 1
                continue

            reasons = _live_filter_reasons(candidate, config)
            if reasons:
                metrics["filtered_candidates"] += 1
                for reason in reasons:
                    counts = metrics.setdefault("filter_reason_counts", {})
                    counts[reason] = int(counts.get(reason) or 0) + 1
                continue

            candidate["discovery_url"] = discovery_url
            candidate["live_filter_reasons"] = []
            candidate["within_preferred_age_window"] = bool(
                float(candidate.get("post_age_hours") or 0.0) <= config.preferred_post_age_hours
            )
            discovered.append(candidate)

    discovered.sort(key=_live_candidate_sort_key, reverse=True)
    return discovered[: config.max_candidates]


def extract_candidates_from_reddit_json(
    payload: dict[str, Any],
    *,
    now: datetime | None = None,
) -> list[dict[str, Any]]:
    current_time = now or datetime.now(timezone.utc)
    children = payload.get("data", {}).get("children", [])
    if not isinstance(children, list):
        return []

    candidates: list[dict[str, Any]] = []
    for child in children:
        post = child.get("data", {}) if isinstance(child, dict) else {}
        permalink = str(post.get("permalink") or "").strip()
        if not permalink.startswith("/r/") or "/comments/" not in permalink:
            continue
        reddit_url = f"https://www.reddit.com{permalink.split('?')[0]}"
        created_utc = _to_float(post.get("created_utc"))
        if created_utc is None:
            continue
        age_hours = max(0.0, (current_time.timestamp() - created_utc) / 3600.0)
        candidates.append(
            {
                "platform": "reddit",
                "source_platform": "reddit",
                "source_id": f"reddit:{reddit_url}",
                "source_url": reddit_url,
                "reddit_url": reddit_url,
                "post_title": str(post.get("title") or "").strip(),
                "post_body": str(post.get("selftext") or "").strip(),
                "subreddit": str(post.get("subreddit") or "").strip(),
                "post_permalink": permalink,
                "post_url": str(post.get("url_overridden_by_dest") or post.get("url") or "").strip(),
                "created_utc": created_utc,
                "post_age_hours": round(age_hours, 2),
                "post_age_days": round(age_hours / 24.0, 2),
                "score": int(post.get("score") or 0),
                "comment_count": int(post.get("num_comments") or 0),
            }
        )
    return candidates


def _live_filter_reasons(candidate: dict[str, Any], config: FounderSignalConfig) -> list[str]:
    reasons: list[str] = []
    post_age_hours = float(candidate.get("post_age_hours") or 0.0)
    if post_age_hours > float(config.max_post_age_days * 24):
        reasons.append("post_too_old_for_live_discovery")

    comment_count = int(candidate.get("comment_count") or 0)
    if comment_count < config.min_comment_count:
        reasons.append("comment_count_below_min")
    if comment_count > config.max_comment_count:
        reasons.append("comment_count_above_max")

    title = str(candidate.get("post_title") or "").strip()
    body = str(candidate.get("post_body") or "").strip()
    combined = "\n\n".join(part for part in (title, body) if part).strip()
    if len(title) < 12 or len(_meaningful_tokens(title)) < 3:
        reasons.append("title_not_usable")
    if len(combined) < 24 or _PLACEHOLDER_BODY_RE.match(body or title):
        reasons.append("body_not_usable")

    if not _has_product_term_overlap(combined or title, config):
        reasons.append("insufficient_product_term_overlap")
    if _contains_any_marker(combined, tuple(config.negative_scoring_terms) + _HARD_NEGATIVE_PATTERNS):
        reasons.append("hard_negative_or_off_topic_match")
    return reasons


def _live_candidate_sort_key(candidate: dict[str, Any]) -> tuple[int, float, int, str]:
    return (
        1 if candidate.get("within_preferred_age_window") else 0,
        -float(candidate.get("post_age_hours") or 0.0),
        int(candidate.get("comment_count") or 0),
        str(candidate.get("reddit_url") or ""),
    )


def _has_product_term_overlap(text: str, config: FounderSignalConfig) -> bool:
    lowered = text.lower()
    overlap_terms = [
        *config.keywords,
        *config.live_discovery_terms,
        config.product_name,
    ]
    for term in overlap_terms:
        normalized = str(term).strip().lower()
        if not normalized:
            continue
        if normalized in lowered:
            return True
        tokens = _meaningful_tokens(normalized)
        if tokens and len(tokens.intersection(_meaningful_tokens(lowered))) >= min(2, len(tokens)):
            return True
    return False


def _contains_any_marker(text: str, markers: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(marker.strip().lower() in lowered for marker in markers if marker.strip())


def _meaningful_tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) >= 3 and token not in _TERM_STOPWORDS
    }


def _to_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
