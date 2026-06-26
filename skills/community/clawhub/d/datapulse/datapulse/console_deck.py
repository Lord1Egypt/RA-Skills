"""Mission deck suggestion helpers for the browser console."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from datapulse.reader import DataPulseReader

_STOPWORDS = {
    "a",
    "an",
    "and",
    "at",
    "for",
    "from",
    "in",
    "into",
    "is",
    "launch",
    "launches",
    "of",
    "on",
    "or",
    "the",
    "to",
    "watch",
    "with",
}
_URGENT_TERMS = {
    "alert",
    "breach",
    "breaking",
    "earnings",
    "incident",
    "launch",
    "outage",
    "recall",
    "release",
    "rumor",
    "security",
    "ship",
}
_RISK_TERMS = {"breach", "incident", "outage", "recall", "security"}
_PLATFORM_HINTS = {
    "twitter": {"twitter", "tweet", "tweets", "x"},
    "reddit": {"reddit", "subreddit"},
    "news": {"earnings", "guidance", "merger", "launch", "release"},
    "web": {"docs", "site", "website", "blog"},
}


def _tokenize(*parts: Any) -> set[str]:
    text = " ".join(str(part or "") for part in parts)
    return {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9._-]{1,}", text.casefold())
        if token and token not in _STOPWORDS
    }


def _similarity(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    overlap = left & right
    return len(overlap) / max(len(left), len(right), 1)


def _pick_route(route_health: list[dict[str, Any]], routes: list[dict[str, Any]]) -> tuple[str, str]:
    healthy = [
        route
        for route in route_health
        if str(route.get("status", "")).strip().lower() in {"healthy", "idle"}
    ]
    ranked = healthy or route_health or routes
    if not ranked:
        return "", "No named alert route is configured yet."
    ranked = sorted(
        ranked,
        key=lambda route: (
            0 if str(route.get("status", "")).strip().lower() == "healthy" else 1,
            -int(route.get("event_count", 0) or 0),
            str(route.get("name", "")),
        ),
    )
    selected = str(ranked[0].get("name", "")).strip()
    status = str(ranked[0].get("status", "")).strip().lower() or "configured"
    return selected, f"Recommended route `{selected}` is the strongest available delivery sink ({status})."


def _pick_platform(query_tokens: set[str], similar_watches: list[dict[str, Any]]) -> tuple[str, str]:
    platform_votes: Counter[str] = Counter()
    for watch in similar_watches:
        for platform in watch.get("platforms", []) or []:
            normalized = str(platform or "").strip().lower()
            if normalized:
                platform_votes[normalized] += 2
    for platform, hints in _PLATFORM_HINTS.items():
        if query_tokens & hints:
            platform_votes[platform] += 3
    if not platform_votes:
        return "web", "Default to `web` when no platform signal or similar mission precedent exists."
    platform, _ = platform_votes.most_common(1)[0]
    return platform, f"Recommended platform `{platform}` matches the query terms and nearby mission history."


def _pick_schedule(query_tokens: set[str], has_conflict: bool) -> tuple[str, str]:
    if query_tokens & _RISK_TERMS:
        return "interval:15m", "Risk-sensitive language suggests a tight 15-minute mission cadence."
    if query_tokens & _URGENT_TERMS:
        return "@hourly", "Breaking or launch-like language suggests at least hourly polling."
    if has_conflict:
        return "@hourly", "Similar missions already exist, so hourly cadence is a safe review baseline."
    return "interval:30m", "Thirty-minute cadence is a balanced default for a new mission draft."


def _pick_keyword(query_tokens: set[str]) -> tuple[str, str]:
    ranked = [token for token in query_tokens if token not in _STOPWORDS and len(token) > 2]
    if not ranked:
        return "", "No strong keyword extracted from the draft yet."
    for token in ranked:
        if token in _URGENT_TERMS:
            return token, f"Keyword `{token}` was extracted from the high-signal query vocabulary."
    keyword = sorted(ranked, key=lambda token: (-len(token), token))[0]
    return keyword, f"Keyword `{keyword}` is the strongest non-trivial token in the current draft."


def _pick_domain(similar_watches: list[dict[str, Any]], related_stories: list[dict[str, Any]]) -> tuple[str, str]:
    for watch in similar_watches:
        sites = watch.get("sites", []) or []
        if sites:
            site = str(sites[0] or "").strip().lower()
            if site:
                return site, f"Domain `{site}` is reused from a similar existing mission."
    for story in related_stories:
        source_names = story.get("source_names", []) or []
        if source_names:
            source_hint = str(source_names[0] or "").strip()
            if source_hint:
                return "", f"Related story evidence is clustered around `{source_hint}`; no domain pin was inferred."
    return "", "No stable domain hint could be inferred from nearby missions or stories."


def build_mission_deck_suggestions(reader: DataPulseReader, draft: dict[str, Any]) -> dict[str, Any]:
    name = str(draft.get("name", "") or "").strip()
    query = str(draft.get("query", "") or "").strip()
    keyword = str(draft.get("keyword", "") or "").strip()
    domain = str(draft.get("domain", "") or "").strip().lower()
    platform = str(draft.get("platform", "") or "").strip().lower()
    route = str(draft.get("route", "") or "").strip().lower()
    tokens = _tokenize(name, query, keyword, domain, platform)

    watches = reader.list_watches(include_disabled=True)
    routes = reader.list_alert_routes()
    route_health = reader.alert_route_health(limit=20)
    stories = reader.list_stories(limit=6, min_items=2)
    triage_stats = reader.triage_stats()

    similar_watches = []
    for watch in watches:
        score = _similarity(tokens, _tokenize(watch.get("name"), watch.get("query")))
        if score >= 0.34 or (query and str(watch.get("query", "")).strip().casefold() == query.casefold()):
            row = dict(watch)
            row["similarity"] = round(score, 2)
            similar_watches.append(row)
    similar_watches.sort(key=lambda row: (-float(row.get("similarity", 0.0)), str(row.get("name", ""))))

    related_stories = []
    for story in stories:
        score = _similarity(tokens, _tokenize(story.get("title"), *(story.get("entities", []) or [])))
        if score >= 0.28:
            row = dict(story)
            row["similarity"] = round(score, 2)
            related_stories.append(row)
    related_stories.sort(key=lambda row: (-float(row.get("similarity", 0.0)), -int(row.get("item_count", 0) or 0)))

    suggested_route, route_reason = _pick_route(route_health, routes)
    suggested_platform, platform_reason = _pick_platform(tokens, similar_watches)
    suggested_schedule, schedule_reason = _pick_schedule(tokens, bool(similar_watches))
    suggested_keyword, keyword_reason = _pick_keyword(tokens)
    suggested_domain, domain_reason = _pick_domain(similar_watches, related_stories)

    recommended_min_confidence = 0.88 if tokens & _RISK_TERMS else 0.78 if tokens & _URGENT_TERMS else 0.68
    recommended_min_score = 82 if tokens & _RISK_TERMS else 72 if tokens & _URGENT_TERMS else 60

    warnings: list[str] = []
    if similar_watches:
        warnings.append("Similar watch missions already exist; clone or adjust instead of duplicating silently.")
    if route and any(str(item.get("name", "")).strip().lower() == route and str(item.get("status", "")).strip().lower() not in {"healthy", "idle"} for item in route_health):
        warnings.append(f"Selected route `{route}` is not currently healthy; switch or expect delivery risk.")
    if not query:
        warnings.append("Draft query is empty, so recommendations remain low-confidence.")
    if int(triage_stats.get("open_count", 0) or 0) > 20:
        warnings.append("Open triage queue is already elevated; tighter thresholds will help avoid analyst overload.")

    summary = (
        f"Mission deck sees {len(similar_watches)} similar watches, "
        f"{len(related_stories)} related stories, and {len(routes)} named routes."
    )
    return {
        "summary": summary,
        "recommended_schedule": suggested_schedule,
        "schedule_reason": schedule_reason,
        "recommended_platform": suggested_platform,
        "platform_reason": platform_reason,
        "recommended_route": suggested_route,
        "route_reason": route_reason,
        "recommended_keyword": suggested_keyword,
        "keyword_reason": keyword_reason,
        "recommended_domain": suggested_domain,
        "domain_reason": domain_reason,
        "recommended_min_score": recommended_min_score,
        "recommended_min_confidence": recommended_min_confidence,
        "warnings": warnings,
        "similar_watches": [
            {
                "id": str(item.get("id", "")),
                "name": str(item.get("name", "")),
                "similarity": float(item.get("similarity", 0.0) or 0.0),
                "enabled": bool(item.get("enabled", True)),
                "schedule": str(item.get("schedule_label") or item.get("schedule") or "manual"),
            }
            for item in similar_watches[:4]
        ],
        "related_stories": [
            {
                "id": str(item.get("id", "")),
                "title": str(item.get("title", "")),
                "similarity": float(item.get("similarity", 0.0) or 0.0),
                "status": str(item.get("status", "")),
                "item_count": int(item.get("item_count", 0) or 0),
            }
            for item in related_stories[:4]
        ],
        "autofill_patch": {
            "schedule": suggested_schedule,
            "platform": suggested_platform,
            "route": suggested_route,
            "keyword": suggested_keyword,
            "domain": suggested_domain,
            "min_score": str(recommended_min_score),
            "min_confidence": f"{recommended_min_confidence:.2f}",
        },
    }
