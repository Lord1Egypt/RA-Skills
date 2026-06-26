#!/usr/bin/env python3
"""Search anime releases from Nyaa.si RSS and return ranked results."""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

# ---- Release quality tiers (best to worst) ----
RELEASE_TIERS = {
    "BDMV": 100,
    "BD-BOX": 100,
    "BluRay BOX": 100,
    "REMUX": 95,
    "BDRip": 90,
    "BDRIP": 90,
    "BD-Rip": 90,
    "Blu-ray": 90,
    "BD": 90,
    "x265 10bit": 85,
    "HEVC": 85,
    "WEB-DL": 80,
    "WEBDL": 80,
    "WEB-DLP": 80,
    "NF": 78,
    "Netflix": 78,
    "WEBRip": 75,
    "webrip": 75,
    "WEB": 72,
    "HDTV": 65,
    "TV-Rip": 60,
    "TVRip": 60,
    "DVDRip": 70,
    "DVD": 70,
    "DVD-R": 70,
    "XviD": 50,
    "DivX": 45,
    "MP4": 40,
    "3GP": 20,
}

SUBTITLE_SCORES = {
    "内置简体": 100,
    "内封简体": 95,
    "简繁": 95,
    "简体": 90,
    "chs": 90,
    "CHS": 90,
    "中文字幕": 85,
    "内嵌": 85,
    "内封": 85,
    "Simplified": 85,
    "][GB]": 85,
    "/GB]": 85,
    "[GB]": 85,
    "繁体": 60,
    "cht": 55,
    "CHT": 55,
    "外挂": 50,
    "Traditional": 50,
    "chinese": 40,
    "中文": 35,
}

RESOLUTION_IDEAL_MB = {
    "2160p": {"ideal": 3000, "label": "4K"},
    "1080p": {"ideal": 1500, "label": "1080P"},
    "720p": {"ideal": 800, "label": "720P"},
    "480p": {"ideal": 400, "label": "480P"},
    "360p": {"ideal": 250, "label": "360P"},
}

RES_KEYWORDS = {
    "2160p": ["2160", "4K", "UHD"],
    "1080p": ["1080", "FHD"],
    "720p": ["720"],
    "480p": ["480", "SD"],
    "360p": ["360"],
}

EXCLUDE_KEYWORDS = [
    "巻",
    "卷",
    "漫画",
    "manga",
    "raw",
    "更新",
    "character",
    "song",
    "ost",
    "ed",
    "op",
    "pv",
    "cm",
    "ncop",
    "nced",
    "menu",
    "teaser",
    "trailer",
]

COLLECTION_KEYWORDS = [
    "complete",
    "全集",
    "合集",
    "collection",
    "batch",
    "season pack",
    "part 1-",
    "part1-",
    "vol.",
    "vol ",
]

NON_VIDEO_KEYWORDS = [
    "artbook",
    "chapter ",
    "chapter-",
    "comic",
    "comics",
    "digitalmangafan",
    "game",
    "manga",
    "pdf",
    "rpcs3",
    "subs only",
    "subtitle only",
    "trial to full game",
]

EPISODE_CONTEXT_PATTERNS = [
    r"\bS\d{1,2}E(\d{1,4})\b",
    r"(?:^|[\s\[\(_-])(?:EP|E)\s*0*(\d{1,4})(?:v\d+)?(?:[\s\]\)_\-.]|$)",
    r"第\s*0*(\d{1,4})\s*(?:集|话|話|回|期)",
    r"(?:^|[\]\)])\s*-\s*0*(\d{1,4})(?:v\d+)?(?:[\s\[\(._-]|$)",
    r"(?:^|[\s\[\(_-])\[(\d{1,4})\](?:[\s\]\)_\-.]|$)",
]

EXPLICIT_SEASON_PATTERNS = [
    r"\bS(\d{1,2})E\d{1,4}\b",
    r"\bSeason\s*0*(\d{1,2})\b",
    r"第\s*0*(\d{1,2})\s*(?:季|部|篇)",
]

PART_SEASON_PATTERNS = [
    r"\bPart\s*0*(\d{1,2})\b",
]

BATCH_RANGE_PATTERNS = [
    r"(?:^|[\s\[\(_-])0*(\d+)\s*[-~至到]+\s*0*(\d+)(?:[\s\]\)_-]|$)",
    r"(?:^|[\s\[\(_-])第?0*(\d+)[\s话集期]*(?:合集|全集合集|全)(?:[\s\]\)_-]|$)",
    r"(?:^|[\s\[\(_-])(?:合集|全)\s*0*(\d+)(?:[\s\]\)_-]|$)",
]

HEADER_SETS = [
    {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "application/rss+xml",
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept": "application/rss+xml",
        "Accept-Language": "en-US,en;q=0.5",
    },
    {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"
        ),
        "Accept": "application/rss+xml",
    },
]


def _add_unique(items: list[str], value: str | None) -> None:
    if not value:
        return
    value = value.strip()
    if value and value not in items:
        items.append(value)


def _normalize_match_text(text: str) -> str:
    text = html.unescape(text).lower()
    text = text.replace("’", "'")
    text = text.replace("'", "")
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", text)


def _query_tokens(query: str) -> list[str]:
    query = html.unescape(query).lower()
    query = query.replace("’", "'").replace("'", "")
    return [token for token in re.split(r"[^0-9a-z\u4e00-\u9fff]+", query) if len(token) >= 2]


def _is_year_like(value: int) -> bool:
    return 1900 <= value <= 2099


def _is_collection_release(title: str) -> bool:
    lowered = title.lower()
    return any(keyword in lowered for keyword in COLLECTION_KEYWORDS)


def _is_probable_video_release(title: str) -> bool:
    lowered = title.lower()
    if any(keyword in lowered for keyword in NON_VIDEO_KEYWORDS):
        return False

    video_indicators = [
        ".mkv",
        ".mp4",
        ".avi",
        "1080p",
        "720p",
        "2160p",
        "480p",
        "webrip",
        "web-dl",
        "bluray",
        "bdrip",
        "dvdrip",
        "hdtv",
        "hevc",
        "x264",
        "x265",
        "aac",
        "flac",
        "opus",
        "remux",
    ]
    if any(indicator in lowered for indicator in video_indicators):
        return True
    if re.search(r"\bS\d{1,2}E\d{1,4}\b", title, re.IGNORECASE):
        return True
    return False


def _parse_episode_range(title: str) -> tuple[int, int] | None:
    title = html.unescape(title)
    for pattern in BATCH_RANGE_PATTERNS:
        match = re.search(pattern, title, re.IGNORECASE)
        if not match:
            continue

        prefix = title[max(0, match.start() - 16):match.start()].lower()
        if re.search(r"(part|season)\s*$", prefix):
            continue

        start = int(match.group(1))
        end = int(match.group(2)) if match.lastindex and match.lastindex >= 2 else start

        if _is_year_like(start) or _is_year_like(end):
            continue
        if start < 1 or end < 1 or start > 9999 or end > 9999:
            continue
        if end < start:
            start, end = end, start
        return start, end

    return None


def extract_episode_numbers(title: str) -> list[int]:
    title = html.unescape(title)
    numbers: set[int] = set()

    batch_range = _parse_episode_range(title)
    if batch_range:
        start, end = batch_range
        numbers.update(range(start, end + 1))

    for pattern in EPISODE_CONTEXT_PATTERNS:
        for match in re.finditer(pattern, title, re.IGNORECASE):
            value = int(match.group(1))
            if value < 1 or value > 9999 or _is_year_like(value):
                continue
            numbers.add(value)

    return sorted(numbers)


def extract_season_numbers(title: str) -> list[int]:
    title = html.unescape(title)
    numbers: set[int] = set()

    for pattern in EXPLICIT_SEASON_PATTERNS:
        for match in re.finditer(pattern, title, re.IGNORECASE):
            value = int(match.group(1))
            if 1 <= value <= 99:
                numbers.add(value)

    if numbers:
        return sorted(numbers)

    for pattern in PART_SEASON_PATTERNS:
        for match in re.finditer(pattern, title, re.IGNORECASE):
            value = int(match.group(1))
            if 1 <= value <= 99:
                numbers.add(value)

    return sorted(numbers)


def _parse_size_to_mb(text: str) -> float:
    match = re.search(r"([\d.]+)\s*(GiB|MiB|GB|MB|KB)", text, re.IGNORECASE)
    if not match:
        return 0.0

    num = float(match.group(1))
    unit = match.group(2).upper()
    if unit in ("GIB", "GB"):
        return num * 1024
    if unit in ("MIB", "MB"):
        return num
    if unit in ("KIB", "KB"):
        return num / 1024
    return 0.0


def _detect_resolution(title: str) -> tuple[str, str]:
    for res_key, keywords in RES_KEYWORDS.items():
        if any(keyword in title for keyword in keywords):
            return res_key, RESOLUTION_IDEAL_MB[res_key]["label"]
    return "unknown", "未知"


def _detect_release_quality(title: str) -> tuple[int, str]:
    upper_title = title.upper()
    for label, score in RELEASE_TIERS.items():
        if label.upper() in upper_title:
            return score, label
    return 50, "未知"


def _score_size_for_resolution(size_mb: float, res_key: str) -> float:
    if res_key not in RESOLUTION_IDEAL_MB:
        if size_mb == 0:
            return 0
        return max(0, min(100, 50 + 30 * math.tanh(math.log2(size_mb) - 8)))

    ideal = RESOLUTION_IDEAL_MB[res_key]["ideal"]
    if size_mb == 0:
        return 5

    ratio = size_mb / ideal
    log_ratio = math.log2(ratio)
    score = 100 * math.exp(-(log_ratio**2) / 0.5)
    return max(5, score)


def _score_query_match(title: str, candidate_queries: list[str] | None) -> float:
    if not candidate_queries:
        return 0.0

    normalized_title = _normalize_match_text(title)
    best = 0.0

    for query in candidate_queries:
        normalized_query = _normalize_match_text(query)
        if len(normalized_query) >= 2 and normalized_query in normalized_title:
            best = max(best, 45.0)
            continue

        tokens = _query_tokens(query)
        if not tokens:
            continue
        matched = sum(1 for token in tokens if token in normalized_title)
        if matched == len(tokens):
            best = max(best, 30.0)
        elif matched > 0:
            best = max(best, 12.0 + matched * 4.0)

    return best


def score_title(
    title: str,
    size_str: str,
    seeders: int,
    leechers: int = 0,
    downloads: int = 0,
    prefer_4k: bool = False,
    candidate_queries: list[str] | None = None,
) -> tuple[int, list[str]]:
    score = 0.0
    tags: list[str] = []

    size_mb = _parse_size_to_mb(size_str)
    res_key, res_label = _detect_resolution(title)

    sub_score = 0
    for label, points in SUBTITLE_SCORES.items():
        if label.lower() in title.lower():
            sub_score = max(sub_score, points)
            break
    score += sub_score * 2.5
    if sub_score >= 85:
        tags.append("中字")
    elif sub_score >= 50:
        tags.append("繁字")
    elif sub_score > 0:
        tags.append("字幕")

    res_scores = {
        "2160p": 100,
        "1080p": 85,
        "720p": 60,
        "480p": 30,
        "360p": 15,
    }
    res_base = res_scores.get(res_key, 40)
    if prefer_4k and res_key == "2160p":
        res_base = 100
    elif prefer_4k and res_key == "1080p":
        res_base = 60
    elif not prefer_4k and res_key == "2160p":
        res_base = 50
    score += res_base * 1.5
    if res_key != "unknown":
        tags.append(res_label)

    size_score = _score_size_for_resolution(size_mb, res_key)
    score += size_score
    if size_mb > 2000:
        tags.append("体积大")
    elif size_mb > 1200:
        tags.append("大")
    elif size_mb > 700:
        tags.append("适中")
    elif size_mb > 300:
        tags.append("较小")
    else:
        tags.append("小")

    rel_score, rel_label = _detect_release_quality(title)
    score += rel_score * 1.5
    if rel_label != "未知":
        tags.append(rel_label)

    seeder_score = min(60, 20 * math.log10(max(1, seeders)))
    if seeders > 0:
        ratio = leechers / seeders
        if ratio > 1:
            leech_ratio_score = 20
        elif ratio > 0.5:
            leech_ratio_score = 15
        elif ratio > 0.1:
            leech_ratio_score = 10
        else:
            leech_ratio_score = 5
    elif leechers > 0:
        leech_ratio_score = 0
    else:
        leech_ratio_score = 5

    score += min(seeder_score + leech_ratio_score, 80) * 0.5
    if seeders > 50:
        tags.append("热")
    elif seeders > 10:
        tags.append("活")

    score += _score_query_match(title, candidate_queries)

    if _is_collection_release(title):
        score -= 20
        tags.append("合集风险")

    return int(score), tags


def parse_nyaa_rss(xml_content: str) -> list[dict]:
    results = []
    items = re.findall(r"<item>(.*?)</item>", xml_content, re.DOTALL)

    for item in items:
        title_match = re.search(r"<title>(.*?)</title>", item)
        size_match = re.search(r"<nyaa:size>(.*?)</nyaa:size>", item)
        seeders_match = re.search(r"<nyaa:seeders>(.*?)</nyaa:seeders>", item)
        leechers_match = re.search(r"<nyaa:leechers>(.*?)</nyaa:leechers>", item)
        downloads_match = re.search(r"<nyaa:downloads>(.*?)</nyaa:downloads>", item)
        infohash_match = re.search(r"<nyaa:infoHash>(.*?)</nyaa:infoHash>", item)
        link_match = re.search(r"<link>https://nyaa\.si/download/(\d+)\.torrent</link>", item)

        if title_match and infohash_match:
            results.append(
                {
                    "title": html.unescape(title_match.group(1)),
                    "size": size_match.group(1) if size_match else "",
                    "seeders": int(seeders_match.group(1)) if seeders_match else 0,
                    "leechers": int(leechers_match.group(1)) if leechers_match else 0,
                    "downloads": int(downloads_match.group(1)) if downloads_match else 0,
                    "infohash": infohash_match.group(1),
                    "torrent_id": link_match.group(1) if link_match else "",
                }
            )

    return results


def fetch_rss(query: str) -> str:
    rss_url = f"https://nyaa.si/?page=rss&q={urllib.parse.quote(query)}"
    last_error: Exception | None = None

    for headers in HEADER_SETS:
        try:
            req = urllib.request.Request(rss_url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                return response.read().decode()
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code == 403:
                continue
            raise RuntimeError(f"Nyaa.si 请求失败：HTTP {exc.code}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            continue

    error_name = type(last_error).__name__ if last_error else "UnknownError"
    raise RuntimeError(f"Nyaa.si 无法访问（{error_name}），可能触发了反爬限制")


def search_nyaa_once(query: str) -> list[dict]:
    return parse_nyaa_rss(fetch_rss(query))


def merge_results(query_results: dict[str, list[dict]]) -> list[dict]:
    merged: dict[str, dict] = {}

    for query, results in query_results.items():
        for result in results:
            key = result.get("infohash") or result.get("torrent_id") or result["title"]
            current = merged.get(key)
            if current is None:
                current = dict(result)
                current["matched_queries"] = [query]
                merged[key] = current
            else:
                _add_unique(current["matched_queries"], query)

    return list(merged.values())


def filter_episode(results: list[dict], episode: int) -> list[dict]:
    filtered = []

    for result in results:
        title = result["title"]
        if any(keyword in title.lower() for keyword in EXCLUDE_KEYWORDS):
            continue

        batch_range = _parse_episode_range(title)
        if batch_range and batch_range[0] <= episode <= batch_range[1]:
            filtered.append(result)
            continue

        if episode in extract_episode_numbers(title):
            filtered.append(result)

    return filtered


def filter_latest_season(results: list[dict]) -> tuple[list[dict], int | None]:
    seasons = sorted(
        {
            season
            for result in results
            for season in extract_season_numbers(result["title"])
        }
    )
    if not seasons:
        return results, None

    latest_season = max(seasons)
    filtered = [
        result
        for result in results
        if latest_season in extract_season_numbers(result["title"])
    ]
    return filtered or results, latest_season


def infer_latest_episode(results: list[dict]) -> int | None:
    max_episode = 0

    for result in results:
        batch_range = _parse_episode_range(result["title"])
        if batch_range:
            max_episode = max(max_episode, batch_range[1])

        episode_numbers = extract_episode_numbers(result["title"])
        if episode_numbers:
            max_episode = max(max_episode, max(episode_numbers))

    return max_episode or None


def run_search(
    query: str,
    *,
    aliases: list[str] | None = None,
    episode: int | None = None,
    latest_season: bool = False,
    prefer_4k: bool = False,
) -> dict:
    search_queries: list[str] = []
    _add_unique(search_queries, query)
    for alias in aliases or []:
        _add_unique(search_queries, alias)

    query_results: dict[str, list[dict]] = {}
    warnings: list[str] = []
    network_success = False
    last_error: str | None = None

    for search_query in search_queries:
        try:
            query_results[search_query] = search_nyaa_once(search_query)
            network_success = True
        except RuntimeError as exc:
            warnings.append(f"搜索「{search_query}」失败：{exc}")
            last_error = str(exc)

    if not network_success:
        return {
            "error": last_error or "Nyaa.si 无法访问",
            "fallback_suggestion": "请稍后重试，或改用 --downloader cli-only 仅返回磁力链接",
            "query": query,
            "search_queries": search_queries,
            "warnings": warnings,
        }

    results = merge_results(query_results)
    results = [result for result in results if _is_probable_video_release(result["title"])]
    if not results:
        return {
            "query": query,
            "search_queries": search_queries,
            "episode": episode,
            "latest_season_requested": latest_season,
            "total": 0,
            "results": [],
            "warnings": warnings,
        }

    available_seasons = sorted(
        {
            season
            for result in results
            for season in extract_season_numbers(result["title"])
        }
    )

    if episode is not None:
        results = filter_episode(results, episode)

    resolved_latest_season = None
    if latest_season and results:
        results, resolved_latest_season = filter_latest_season(results)
        if resolved_latest_season is None:
            warnings.append("结果中没有明确季号，无法严格按“最新一季”过滤。")

    if not results:
        return {
            "query": query,
            "search_queries": search_queries,
            "episode": episode,
            "latest_season_requested": latest_season,
            "resolved_latest_season": resolved_latest_season,
            "available_seasons": available_seasons,
            "total": 0,
            "results": [],
            "warnings": warnings,
        }

    for result in results:
        candidate_queries = search_queries + result.get("matched_queries", [])
        score, tags = score_title(
            result["title"],
            result["size"],
            result["seeders"],
            result.get("leechers", 0),
            result.get("downloads", 0),
            prefer_4k,
            candidate_queries=candidate_queries,
        )
        result["score"] = score
        result["tags"] = tags
        season_numbers = extract_season_numbers(result["title"])
        if season_numbers:
            result["season_numbers"] = season_numbers
        episode_numbers = extract_episode_numbers(result["title"])
        if episode_numbers:
            result["episode_numbers"] = episode_numbers

    results.sort(key=lambda item: (-item["score"], -item["seeders"], item["title"]))

    latest_episode = None if episode is not None else infer_latest_episode(results)
    has_chinese_subtitle = any("中字" in result.get("tags", []) for result in results)

    output = {
        "query": query,
        "search_queries": search_queries,
        "episode": episode,
        "latest_season_requested": latest_season,
        "resolved_latest_season": resolved_latest_season,
        "available_seasons": available_seasons,
        "total": len(results),
        "results": results,
        "has_chinese_subtitle": has_chinese_subtitle,
        "warnings": warnings,
    }
    if latest_episode is not None:
        output["latest_episode"] = latest_episode
    return output


def _print_human(output: dict) -> None:
    if "error" in output:
        print(f"❌ {output['error']}")
        suggestion = output.get("fallback_suggestion")
        if suggestion:
            print(f"💡 建议：{suggestion}")
        return

    print(f"🔍 搜索：{output['query']}")
    if output.get("latest_season_requested"):
        if output.get("resolved_latest_season") is not None:
            print(f"📺 已按最新一季过滤：S{output['resolved_latest_season']:02d}")
        else:
            print("📺 请求了最新一季，但结果中没有明确季号")
    if output.get("episode") is not None:
        print(f"📺 指定集数：第 {output['episode']} 集")
    if output.get("latest_episode") is not None:
        print(f"📺 最新已到第 {output['latest_episode']} 集")
    if not output.get("has_chinese_subtitle"):
        print("⚠️  所有结果均暂无中文字幕")
    if output.get("warnings"):
        for warning in output["warnings"]:
            print(f"⚠️  {warning}")
    print(f"📋 找到 {output['total']} 个结果\n")

    for index, result in enumerate(output["results"][:10], 1):
        tags_str = " ".join(f"[{tag}]" for tag in result["tags"])
        print(f"  {index}. {tags_str} {result['title']}")
        print(f"     评分：{result['score']} | 大小：{result['size']} | 种子：{result['seeders']}")

    best = output["results"][0]
    print(f"\n✅ 最佳匹配：{best['title']} (评分：{best['score']})")
    print(f"🔗 磁力：magnet:?xt=urn:btih:{best['infohash']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Search anime releases on Nyaa.si RSS.")
    parser.add_argument("query", help="Primary search query")
    parser.add_argument("--alias", action="append", default=[], help="Additional search alias")
    parser.add_argument("--episode", type=int, help="Target episode number")
    parser.add_argument("--latest-season", action="store_true", help="Filter to the latest detected season")
    parser.add_argument("--prefer-4k", action="store_true", help="Prefer 4K releases")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    output = run_search(
        args.query,
        aliases=args.alias,
        episode=args.episode,
        latest_season=args.latest_season,
        prefer_4k=args.prefer_4k,
    )

    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        _print_human(output)

    sys.exit(1 if "error" in output else 0)


if __name__ == "__main__":
    main()
