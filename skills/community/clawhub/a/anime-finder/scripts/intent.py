#!/usr/bin/env python3
"""Normalize user wording into a stable anime-finder intent payload."""

from __future__ import annotations

import argparse
import json
import re
import sys

TITLE_EPISODE_PATTERNS = [
    re.compile(r"第\s*0*(\d{1,4})\s*(?:集|话|話|回|期)"),
    re.compile(r"第\s*([零一二三四五六七八九十百两]+)\s*(?:集|话|話|回|期)"),
    re.compile(r"\bEP?\s*0*(\d{1,4})\b", re.IGNORECASE),
    re.compile(r"\bE0*(\d{1,4})\b", re.IGNORECASE),
]

TITLE_SEASON_PATTERNS = [
    re.compile(r"第\s*0*(\d{1,2})\s*(?:季|部|篇)"),
    re.compile(r"第\s*([零一二三四五六七八九十百两]+)\s*(?:季|部|篇)"),
    re.compile(r"\bS0*(\d{1,2})\b", re.IGNORECASE),
    re.compile(r"\bSeason\s*0*(\d{1,2})\b", re.IGNORECASE),
    re.compile(r"\bPart\s*0*(\d{1,2})\b", re.IGNORECASE),
]

LATEST_EPISODE_PATTERN = re.compile(
    r"(最新[一1]集|最新[一1]话|最新更新|追更|最新一话|latest\s+episode|latest\s+ep)",
    re.IGNORECASE,
)
LATEST_SEASON_PATTERN = re.compile(
    r"(最新[一1]季|新[一1]季|新作第一集|新季度|latest\s+season|new\s+season)",
    re.IGNORECASE,
)
STATUS_PATTERN = re.compile(
    r"(刚才那个下载|刚才那个任务|下载怎么样|有进度吗|下载进度|下好了没|下载好了没|status|progress)",
    re.IGNORECASE,
)
MAGNET_PATTERN = re.compile(
    r"(只要磁力|只要种子|只给我?磁力|磁力链接|磁力|magnet|torrent link|只要链接|不要下载只给链接)",
    re.IGNORECASE,
)
DOWNLOAD_PATTERN = re.compile(
    r"(下载下来|帮我下载|帮我下|直接下|给我下|queue|\bdownload\b|抓下来|收下来|保存下来|下载)",
    re.IGNORECASE,
)
WATCH_PATTERN = re.compile(
    r"(想追更|想看|要看|想追|追更|开看|直接来|来一集|来最新的|给我来|我想补|\bwatch\b)",
    re.IGNORECASE,
)
SEARCH_ONLY_PATTERN = re.compile(
    r"(先找|先搜|先看资源|先别下载|别下载|不要下载|search only|search-only|先看一下|\bsearch\b|\bfind\b)",
    re.IGNORECASE,
)
PERSISTENCE_PATTERN = re.compile(r"(以后|默认|记住|今后|从现在开始|一律|都给我|长期)")
SIMPLE_SUB_PATTERN = re.compile(r"(简中|简体|中字|中文字幕|内置简体|内封简体|chs|simplified)", re.IGNORECASE)
TRAD_SUB_PATTERN = re.compile(r"(繁中|繁体|cht|traditional)", re.IGNORECASE)
NO_SUB_PATTERN = re.compile(r"(无字幕|不要字幕|raw|no subs?)", re.IGNORECASE)
SIZE_CAP_PATTERN = re.compile(r"(?:不超过|别超过|小于|最多)\s*(\d+(?:\.\d+)?)\s*(gib|gb|g)", re.IGNORECASE)
DOWNLOAD_NOW_PATTERN = re.compile(r"(直接下|别问我|自动下|高置信.*直接下)")

STRIP_PATTERNS = [
    STATUS_PATTERN,
    MAGNET_PATTERN,
    DOWNLOAD_PATTERN,
    WATCH_PATTERN,
    SEARCH_ONLY_PATTERN,
    PERSISTENCE_PATTERN,
    LATEST_EPISODE_PATTERN,
    LATEST_SEASON_PATTERN,
    SIMPLE_SUB_PATTERN,
    TRAD_SUB_PATTERN,
    NO_SUB_PATTERN,
    re.compile(r"(2160p|4k|uhd|1080p|720p|480p|360p)", re.IGNORECASE),
    re.compile(r"(transmission|daemon|cli-only)", re.IGNORECASE),
    SIZE_CAP_PATTERN,
    re.compile(r"(番剧|番|动漫|动画片|动画|资源|磁力|种子|链接|torrent|nyaa|bt)", re.IGNORECASE),
    re.compile(r"(帮我|给我|麻烦|请|一下|然后|再|顺便|看看|找一下|搜一下|想要|我要)", re.IGNORECASE),
    re.compile(r"(顺手|只给|只要|优先\s+[A-Za-z0-9 ._\-]{1,32}|不要\s+[A-Za-z0-9 ._\-]{1,32})", re.IGNORECASE),
]

FILLER_ONLY_PATTERN = re.compile(r"^[\s,，。.!！？:：/\-_=+~·]*$")
TRAILING_POSSESSIVE_PATTERN = re.compile(r"(?:的|之)+$")
POSITIVE_ANIME_HINTS = [
    "番",
    "新番",
    "追更",
    "最新一集",
    "最新一季",
    "动画",
    "动漫",
    "ep",
    "第",
    "磁力",
    "torrent",
    "nyaa",
]
NEGATIVE_NON_ANIME_HINTS = [
    "bt 链接",
    "pdf",
    "电影",
    "美剧",
    "电视剧",
    "linux iso",
    "ubuntu",
    "windows",
    "游戏",
    "switch",
    "ps5",
    "steam",
    "漫画",
    "纪录片",
]
GENERIC_NON_TITLE_HINTS = ["这个", "那个", "链接", "资源", "任务", "下载", "磁力"]

DEFAULT_RESOLUTION_ORDER = ["1080p", "720p", "2160p", "480p", "360p"]
RESOLUTION_ORDER_MAP = {
    "2160p": ["2160p", "1080p", "720p", "480p", "360p"],
    "1080p": ["1080p", "720p", "2160p", "480p", "360p"],
    "720p": ["720p", "1080p", "480p", "360p", "2160p"],
    "480p": ["480p", "720p", "1080p", "360p", "2160p"],
    "360p": ["360p", "480p", "720p", "1080p", "2160p"],
}


def _add_reason(reasons: list[str], code: str) -> None:
    if code not in reasons:
        reasons.append(code)


def _normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _ordered_resolution(value: str | None) -> list[str]:
    if not value:
        return list(DEFAULT_RESOLUTION_ORDER)
    return list(RESOLUTION_ORDER_MAP.get(value, DEFAULT_RESOLUTION_ORDER))


def _parse_numeric_fragment(value: str) -> int | None:
    if value.isdigit():
        return int(value)

    chinese_map = {
        "零": 0,
        "一": 1,
        "二": 2,
        "两": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
    }
    if value == "十":
        return 10

    total = 0
    current = 0
    for char in value:
        if char == "十":
            current = max(current, 1)
            total += current * 10
            current = 0
            continue
        if char == "百":
            current = max(current, 1)
            total += current * 100
            current = 0
            continue
        if char not in chinese_map:
            return None
        current += chinese_map[char]

    total += current
    return total or None


def _extract_first_int(patterns: list[re.Pattern[str]], text: str) -> int | None:
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            return _parse_numeric_fragment(match.group(1))
    return None


def _detect_quality_pref(text: str) -> str | None:
    lowered = text.lower()
    if "2160p" in lowered or "4k" in lowered or "uhd" in lowered:
        return "2160p"
    if "1080p" in lowered:
        return "1080p"
    if "720p" in lowered:
        return "720p"
    if "480p" in lowered:
        return "480p"
    if "360p" in lowered:
        return "360p"
    return None


def _detect_subtitle_pref(text: str) -> str | None:
    if SIMPLE_SUB_PATTERN.search(text):
        return "simplified"
    if TRAD_SUB_PATTERN.search(text):
        return "traditional"
    if NO_SUB_PATTERN.search(text):
        return "none"
    return None


def _detect_downloader_pref(text: str, action: str) -> str | None:
    lowered = text.lower()
    if action == "magnet":
        return "cli-only"
    if "cli-only" in lowered:
        return "cli-only"
    if "transmission" in lowered or "daemon" in lowered:
        return "transmission"
    return None


def _extract_group_preferences(text: str) -> tuple[list[str], list[str]]:
    preferred: list[str] = []
    blocked: list[str] = []

    for pattern, bucket in (
        (r"(?:只要|优先|prefer)\s+([A-Za-z0-9][A-Za-z0-9 ._\-]{1,32})", preferred),
        (r"(?:不要|屏蔽|排除|block)\s+([A-Za-z0-9][A-Za-z0-9 ._\-]{1,32})", blocked),
    ):
        for match in re.finditer(pattern, text, re.IGNORECASE):
            value = _normalize_spaces(match.group(1))
            value = re.sub(r"(字幕组|发布组|组)$", "", value, flags=re.IGNORECASE).strip()
            if value and value not in bucket:
                bucket.append(value)

    return preferred, blocked


def _extract_title(text: str, action: str) -> str | None:
    if action == "status":
        return None

    cleaned = text
    for pattern in TITLE_EPISODE_PATTERNS + TITLE_SEASON_PATTERNS:
        cleaned = pattern.sub(" ", cleaned)

    for pattern in STRIP_PATTERNS:
        cleaned = pattern.sub(" ", cleaned)

    cleaned = re.sub(r"[“”\"'‘’《》\[\]【】()（）]", " ", cleaned)
    cleaned = re.sub(
        r"\b(?:the|latest|episode|season|anime|download|magnet|status|progress|search|find|watch|for)\b",
        " ",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = _normalize_spaces(cleaned)
    cleaned = re.sub(r"^(?:我|找|搜|下|看|追|用)+", "", cleaned)
    cleaned = re.sub(r"^(?:只|给|来)+", "", cleaned)
    cleaned = _normalize_spaces(cleaned)
    cleaned = TRAILING_POSSESSIVE_PATTERN.sub("", cleaned).strip()
    cleaned = re.sub(r"(?:别|不要)+$", "", cleaned).strip()
    cleaned = cleaned.strip(" ,，。.!！？:：/-_")

    if not cleaned or FILLER_ONLY_PATTERN.match(cleaned):
        return None

    return cleaned


def should_trigger_skill(text: str) -> bool:
    lowered = text.lower()
    if STATUS_PATTERN.search(text):
        return True

    if any(hint in lowered for hint in NEGATIVE_NON_ANIME_HINTS):
        return False

    has_resource_cue = any(
        (
            MAGNET_PATTERN.search(text),
            DOWNLOAD_PATTERN.search(text),
            WATCH_PATTERN.search(text),
            SEARCH_ONLY_PATTERN.search(text),
            LATEST_EPISODE_PATTERN.search(text),
            LATEST_SEASON_PATTERN.search(text),
            re.search(r"[找搜]", text),
            "下载" in text,
            "磁力" in text,
            "想看" in text,
            "追更" in text,
            "torrent" in lowered,
            "bt" in lowered,
            "nyaa" in lowered,
            "latest" in lowered,
            "season" in lowered,
            "episode" in lowered,
        )
    )
    has_anime_cue = any(hint in lowered for hint in POSITIVE_ANIME_HINTS)
    if has_anime_cue and has_resource_cue:
        return True

    if not has_resource_cue:
        return False

    action = "magnet" if MAGNET_PATTERN.search(text) else "search"
    candidate_title = _extract_title(text, action)
    if not candidate_title:
        return False

    normalized_title = _normalize_spaces(candidate_title).lower()
    if normalized_title in GENERIC_NON_TITLE_HINTS:
        return False
    if any(hint == normalized_title for hint in GENERIC_NON_TITLE_HINTS):
        return False
    return len(normalized_title.replace(" ", "")) >= 2


def parse_intent(text: str) -> dict:
    raw = _normalize_spaces(text)
    reasons: list[str] = []

    latest_episode = bool(LATEST_EPISODE_PATTERN.search(raw))
    latest_season = bool(LATEST_SEASON_PATTERN.search(raw))
    episode = _extract_first_int(TITLE_EPISODE_PATTERNS, raw)
    season = _extract_first_int(TITLE_SEASON_PATTERNS, raw)

    watch_intent = bool(WATCH_PATTERN.search(raw))
    explicit_download = bool(DOWNLOAD_PATTERN.search(raw))
    explicit_magnet = bool(MAGNET_PATTERN.search(raw))
    explicit_search_only = bool(SEARCH_ONLY_PATTERN.search(raw))
    status_query = bool(STATUS_PATTERN.search(raw))

    if status_query:
        action = "status"
        action_source = "status_phrase"
        _add_reason(reasons, "status_follow_up")
    elif explicit_magnet:
        action = "magnet"
        action_source = "magnet_phrase"
        _add_reason(reasons, "magnet_only_request")
    elif explicit_search_only:
        action = "search"
        action_source = "search_only_phrase"
        _add_reason(reasons, "search_only_request")
    elif explicit_download:
        action = "download"
        action_source = "download_phrase"
        _add_reason(reasons, "explicit_download_request")
    elif watch_intent:
        action = "download"
        action_source = "watch_phrase"
        _add_reason(reasons, "watch_request")
    else:
        action = "search"
        action_source = "default"
        _add_reason(reasons, "default_search")

    quality_pref = _detect_quality_pref(raw)
    subtitle_pref = _detect_subtitle_pref(raw)
    downloader_pref = _detect_downloader_pref(raw, action)
    title = _extract_title(raw, action)
    missing_fields: list[str] = []

    if action in {"search", "download", "magnet"} and not title:
        missing_fields.append("title")
        _add_reason(reasons, "missing_title")

    profile_updates: dict = {}
    persist_profile = bool(PERSISTENCE_PATTERN.search(raw))
    size_cap = None
    size_match = SIZE_CAP_PATTERN.search(raw)
    if size_match:
        size_cap = float(size_match.group(1))

    preferred_groups, blocked_groups = _extract_group_preferences(raw)

    if persist_profile:
        _add_reason(reasons, "explicit_profile_update")
        if subtitle_pref:
            profile_updates["subtitle_pref"] = subtitle_pref
        if quality_pref:
            profile_updates["resolution_order"] = _ordered_resolution(quality_pref)
        if size_cap is not None:
            profile_updates["file_size_cap_gb"] = size_cap
        if downloader_pref:
            profile_updates["downloader"] = downloader_pref
        if action in {"search", "download", "magnet"} and action_source != "default":
            profile_updates["default_action"] = action
        if preferred_groups:
            profile_updates["preferred_release_groups"] = preferred_groups
        if blocked_groups:
            profile_updates["blocked_release_groups"] = blocked_groups
        if DOWNLOAD_NOW_PATTERN.search(raw):
            profile_updates["auto_download_high_confidence"] = True

    confidence_score = 0.35
    if title:
        confidence_score += 0.35
        _add_reason(reasons, "title_extracted")
    if action_source != "default":
        confidence_score += 0.15
    if latest_episode or latest_season or episode is not None or season is not None:
        confidence_score += 0.1
    if not missing_fields:
        confidence_score += 0.1
    if action == "status":
        confidence_score = 0.9 if status_query else 0.6
    if action in {"download", "magnet"} and title and watch_intent:
        confidence_score = max(confidence_score, 0.88)

    if missing_fields and action != "status":
        confidence_score -= 0.25

    confidence_score = round(max(0.0, min(confidence_score, 1.0)), 2)

    if confidence_score >= 0.8:
        confidence = "high"
    elif confidence_score >= 0.55:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "raw_query": raw,
        "title": title,
        "episode": episode,
        "season": season,
        "latest_episode": latest_episode,
        "latest_season": latest_season,
        "action": action,
        "action_source": action_source,
        "quality_pref": quality_pref,
        "subtitle_pref": subtitle_pref,
        "downloader_pref": downloader_pref,
        "confidence": confidence,
        "confidence_score": confidence_score,
        "missing_fields": missing_fields,
        "watch_intent": watch_intent,
        "should_trigger_skill": should_trigger_skill(raw),
        "profile_updates": profile_updates,
        "should_persist_profile": bool(profile_updates),
        "file_size_cap_gb": size_cap,
        "preferred_release_groups": preferred_groups,
        "blocked_release_groups": blocked_groups,
        "reason_codes": reasons,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize anime-finder natural language intent into JSON.")
    parser.add_argument("query", help="Raw user query or extracted title")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    output = parse_intent(args.query)
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(output)


if __name__ == "__main__":
    main()
