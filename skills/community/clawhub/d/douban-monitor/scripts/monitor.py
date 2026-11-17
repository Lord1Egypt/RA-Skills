from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import tomllib
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

CST = timezone(timedelta(hours=8))


def now_cst() -> datetime:
    return datetime.now(CST)


def iso(dt: datetime | None) -> str | None:
    return dt.isoformat() if dt else None


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)


def log_step(title: str) -> None:
    print(title, flush=True)


def log_kv(label: str, value: Any) -> None:
    print(f"  - {label}: {value}", flush=True)


@dataclass
class Candidate:
    title: str
    category: str
    source: str
    douban_id: str | None = None
    tmdb_id: int | None = None
    imdb_id: str | None = None
    url: str | None = None
    year: int | None = None
    rating: float | None = None
    rating_count: int | None = None


@dataclass
class LibraryItem:
    key: str
    title: str
    category: str
    sources: list[str]
    watch_status: str
    watch_tier: str
    admission_reason: str
    first_discovered_at: str
    last_discovered_at: str
    watch_started_at: str
    watch_expires_at: str
    last_seen_in_sources_at: str
    resolution_failures: int = 0
    douban_id: str | None = None
    tmdb_id: int | None = None
    imdb_id: str | None = None
    original_title: str | None = None
    url: str | None = None
    year: int | None = None
    last_rating: float | None = None
    last_rating_count: int | None = None
    last_checked_at: str | None = None
    qualified: bool = False
    qualified_at: str | None = None
    archived_at: str | None = None
    archive_reason: str | None = None


@dataclass
class StateItem:
    douban_id: str | None
    title: str
    category: str
    url: str | None
    first_seen_at: str
    last_seen_at: str
    first_qualified_at: str | None = None
    last_notified_at: str | None = None
    last_rating: float | None = None
    last_rating_count: int | None = None
    peak_rating: float | None = None
    peak_rating_count: int | None = None
    notified_stage: str | None = None
    qualified: bool = False
    milestones_notified: list[int] = field(default_factory=list)


DEFAULT_CONFIG = {
    "min_rating": 8.0,
    "min_rating_count": 3000,
    "admission_min_rating": 7.5,
    "admission_min_rating_count": 1000,
    "drop_rating_threshold": 7.5,
    "realert_cooldown_days": 7,
    "high_watch_days": 30,
    "medium_watch_days": 14,
    "low_watch_days": 7,
    "rating_delta_for_realert": 0.3,
    "rating_count_delta_for_realert": 5000,
    "milestone_counts": [10000, 30000, 100000],
    "tmdb_base_url": "https://api.themoviedb.org/3",
    "tmdb_language": "zh-CN",
    "tmdb_region": "CN",
    "tmdb_movie_pages": 1,
    "tmdb_tv_pages": 1,
    "douban_collection_urls": [
        "https://m.douban.com/subject_collection/movie_weekly_best",
        "https://m.douban.com/subject_collection/tv_chinese_best_weekly",
        "https://m.douban.com/subject_collection/tv_global_best_weekly",
        "https://m.douban.com/subject_collection/show_domestic_best_weekly",
        "https://m.douban.com/subject_collection/show_global_best_weekly",
    ],
    "request_timeout_seconds": 20,
    # 模式 A（纯本地）设为 false，跳过第 8 步 git 同步；模式 B（托管 GitHub）保持 true。
    # 也可用环境变量 DOUBAN_MONITOR_NO_PUSH=1 临时关闭，优先级高于配置。
    "auto_git_push": True,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0 Safari/537.36",
}


def load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("rb") as f:
        return tomllib.load(f)


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def candidate_key(candidate: Candidate) -> str:
    if candidate.douban_id:
        return candidate.douban_id
    if candidate.imdb_id:
        return candidate.imdb_id
    if candidate.tmdb_id is not None:
        return f"tmdb:{candidate.tmdb_id}"
    title = candidate.title.strip().lower()
    year = candidate.year or 0
    return f"{title}:{candidate.category}:{year}"


def get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    return value.strip()


# ---------------------------------------------------------------------------
# Rexxar API（m.douban.com 移动网页版内部接口）
# 不需要签名和 apiKey，是当前豆瓣抓取的唯一通道。
# ---------------------------------------------------------------------------

_REXXAR_BASE = "https://m.douban.com/rexxar/api/v2"
_REXXAR_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
    "Mobile/15E148 Safari/604.1"
)


def rexxar_get(path: str, params: dict[str, Any] | None = None, config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Call Douban Rexxar API (m.douban.com)."""
    timeout = (config or {}).get("request_timeout_seconds", 20)
    query: dict[str, Any] = dict(params or {})
    query.setdefault("ck", "")
    query.setdefault("for_mobile", 1)
    url = f"{_REXXAR_BASE}{path}?{urllib.parse.urlencode(query)}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": _REXXAR_UA,
            "Accept": "application/json",
            "Referer": "https://m.douban.com/",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))



def _get_collection_max_items(collection_id: str, config: dict[str, Any]) -> int:
    """Get max items limit for a collection from config."""
    max_items_map = config.get("douban_collection_max_items") or {}
    return max_items_map.get(collection_id, 20)  # Default 20

def fetch_douban_collection_via_rexxar(collection_id: str, config: dict[str, Any]) -> list[dict[str, Any]]:
    """通过 Rexxar API 抓取榜单分页。"""
    max_items = _get_collection_max_items(collection_id, config)
    all_items: list[dict[str, Any]] = []
    start = 0
    count = 20
    while True:
        data = rexxar_get(
            f"/subject_collection/{collection_id}/items",
            params={"start": start, "count": count},
            config=config,
        )
        items = data.get("subject_collection_items") or []
        if not items:
            break
        all_items.extend(items)
        if len(all_items) >= max_items:
            all_items = all_items[:max_items]
            break
        total = data.get("total", 0)
        start += count
        if start >= total:
            break
        time.sleep(0.5)
    return all_items


def fetch_douban_subject_detail_via_rexxar(douban_id: str, config: dict[str, Any]) -> dict[str, Any]:
    """Rexxar 版本的影片详情抓取。"""
    for media_type in ("movie", "tv"):
        try:
            return rexxar_get(f"/{media_type}/{douban_id}", config=config)
        except Exception:
            continue
    return {}


def _collection_id_from_url(url: str) -> str:
    """Extract collection id like 'movie_weekly_best' from the full URL."""
    match = re.search(r"subject_collection/([^/?#]+)", url)
    return match.group(1) if match else url


def _category_and_source_from_collection(url_text: str) -> tuple[str, str]:
    """Determine category and source tag from collection URL."""
    if "movie_hot_gaia" in url_text:
        return "movie", "douban_movie_hot_gaia"
    if "tv_hot" in url_text:
        return "tv", "douban_tv_hot"
    if "tv_real_time_hotest" in url_text:
        return "tv", "douban_tv_realtime_hot"
    if "real_time_hotest" in url_text:
        return "movie", "douban_movie_realtime_hot"
    if "movie_" in url_text:
        return "movie", "douban_movie_weekly"
    if "tv_chinese" in url_text:
        return "tv", "douban_tv_chinese_weekly"
    if "tv_global" in url_text:
        return "tv", "douban_tv_global_weekly"
    if "show_domestic" in url_text:
        return "variety", "douban_show_domestic_weekly"
    if "show_global" in url_text:
        return "variety", "douban_show_global_weekly"
    return "unknown", "douban_weekly"


def fetch_douban_weekly_candidates_lite(config: dict[str, Any]) -> list[Candidate]:
    """Fetch weekly candidates via Rexxar API。"""
    candidates: list[Candidate] = []
    collection_urls = config.get("douban_collection_urls") or []
    for collection_url in collection_urls:
        url_text = str(collection_url)
        collection_id = _collection_id_from_url(url_text)
        category, source = _category_and_source_from_collection(url_text)
        items: list[dict[str, Any]] = []
        try:
            items = fetch_douban_collection_via_rexxar(collection_id, config)
            log_kv(f"Rexxar 榜单 {collection_id} 成功", f"{len(items)} 条")
        except Exception as exc:
            log_kv(f"Rexxar 榜单 {collection_id} 失败", str(exc))
            continue
        if not items:
            continue
        for item in items:
            subject = item if "id" in item else item.get("subject") or item
            douban_id = str(subject.get("id", "")).strip() or None
            title = subject.get("title") or ""
            rating_info = subject.get("rating") or {}
            rating_val = rating_info.get("value")
            rating_count = rating_info.get("count")
            year_str = subject.get("year") or ""
            year = int(year_str) if year_str and year_str.isdigit() else None
            url = f"https://movie.douban.com/subject/{douban_id}/" if douban_id else None
            candidates.append(
                Candidate(
                    title=title or f"douban-subject-{douban_id or 'unknown'}",
                    category=category,
                    source=source,
                    douban_id=douban_id,
                    url=url,
                    year=year,
                    rating=float(rating_val) if rating_val else None,
                    rating_count=int(rating_count) if rating_count else None,
                )
            )
        time.sleep(0.5)
    return candidates


def fetch_douban_subject_detail_lite(candidate: Candidate, config: dict[str, Any]) -> Candidate:
    """Fetch subject detail via Rexxar API。"""
    if not candidate.douban_id:
        return candidate
    if not candidate.url:
        candidate.url = f"https://movie.douban.com/subject/{candidate.douban_id}/"
    data = fetch_douban_subject_detail_via_rexxar(candidate.douban_id, config)
    if not data:
        return candidate
    title = data.get("title")
    if title:
        candidate.title = title
    rating_info = data.get("rating") or {}
    rating_val = rating_info.get("value")
    rating_count = rating_info.get("count")
    if rating_val is not None:
        candidate.rating = float(rating_val)
    if rating_count is not None:
        candidate.rating_count = int(rating_count)
    year_str = data.get("year") or ""
    if year_str and year_str.isdigit() and candidate.year is None:
        candidate.year = int(year_str)
    return candidate


def tmdb_get(path: str, config: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    api_key = get_env("TMDB_API_KEY")
    bearer = get_env("TMDB_BEARER_TOKEN")
    if not api_key and not bearer:
        return {}

    query = dict(params)
    headers = {"User-Agent": config["user_agent"], "Accept": "application/json"}
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"
    else:
        query["api_key"] = api_key

    url = f"{config['tmdb_base_url']}{path}?{urllib.parse.urlencode(query)}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=config["request_timeout_seconds"]) as response:
        return json.loads(response.read().decode("utf-8"))


def tmdb_results_to_candidates(media_type: str, payload: dict[str, Any]) -> list[Candidate]:
    results = payload.get("results") or []
    candidates: list[Candidate] = []
    for item in results:
        tmdb_id = item.get("id")
        if tmdb_id is None:
            continue
        title = item.get("title") or item.get("name") or f"tmdb-{media_type}-{tmdb_id}"
        date_value = item.get("release_date") or item.get("first_air_date") or ""
        year = int(date_value[:4]) if len(date_value) >= 4 and date_value[:4].isdigit() else None
        candidates.append(
            Candidate(
                title=title,
                category="movie" if media_type == "movie" else "tv",
                source=f"tmdb_{payload.get('_source_name', 'popular')}",
                tmdb_id=int(tmdb_id),
                year=year,
            )
        )
    return candidates


def fetch_tmdb_hot_candidates_with_config(config: dict[str, Any]) -> list[Candidate]:
    try:
        sources = [
            ("movie", "/trending/movie/week", "trending_movie", config["tmdb_movie_pages"]),
            ("movie", "/movie/popular", "popular_movie", config["tmdb_movie_pages"]),
            ("tv", "/trending/tv/week", "trending_tv", config["tmdb_tv_pages"]),
            ("tv", "/tv/popular", "popular_tv", config["tmdb_tv_pages"]),
        ]
        candidates: list[Candidate] = []
        for media_type, path, source_name, pages in sources:
            for page in range(1, int(pages) + 1):
                payload = tmdb_get(
                    path,
                    config,
                    {"language": config["tmdb_language"], "region": config["tmdb_region"], "page": page},
                )
                if not payload:
                    continue
                payload["_source_name"] = source_name
                candidates.extend(tmdb_results_to_candidates(media_type, payload))
        return candidates
    except Exception as e:
        log_kv("TMDB 异常（将仅使用豆瓣数据）", str(e))
        return []


def enrich_with_tmdb(candidate: Candidate) -> Candidate:
    return candidate


def dedupe_candidates(candidates: list[Candidate]) -> list[Candidate]:
    merged: dict[str, Candidate] = {}
    for candidate in candidates:
        key = candidate_key(candidate)
        existing = merged.get(key)
        if not existing:
            merged[key] = candidate
            continue
        if candidate.title and (not existing.title or existing.title.startswith("douban-subject-")):
            existing.title = candidate.title
        if candidate.rating is not None:
            existing.rating = candidate.rating
        if candidate.rating_count is not None:
            existing.rating_count = candidate.rating_count
        if candidate.url:
            existing.url = candidate.url
        if candidate.douban_id:
            existing.douban_id = candidate.douban_id
    return list(merged.values())


def assign_watch_tier(candidate: Candidate, config: dict[str, Any]) -> str:
    rating = candidate.rating or 0.0
    count = candidate.rating_count or 0
    if rating >= config["min_rating"] and count < config["min_rating_count"]:
        return "high"
    if rating >= 7.8 or count >= 2000:
        return "medium"
    return "low"


def watch_days_for_tier(tier: str, config: dict[str, Any]) -> int:
    return {"high": config["high_watch_days"], "medium": config["medium_watch_days"], "low": config["low_watch_days"]}[tier]


def admission_reason(candidate: Candidate, config: dict[str, Any]) -> str | None:
    rating = candidate.rating or 0.0
    count = candidate.rating_count or 0
    if candidate.source.startswith("douban_"):
        return "appeared_on_douban_weekly"
    if candidate.source.startswith("tmdb"):
        return "appeared_on_tmdb_hot"
    if rating >= config["admission_min_rating"]:
        return "rating_at_least_7_5"
    if count >= config["admission_min_rating_count"]:
        return "rating_count_at_least_1000"
    return None


def should_qualify(candidate: Candidate, config: dict[str, Any]) -> bool:
    return (candidate.rating or 0.0) > config["min_rating"] and (candidate.rating_count or 0) > config["min_rating_count"]


def update_library(library_data: dict[str, Any], candidates: list[Candidate], config: dict[str, Any], now: datetime) -> dict[str, Any]:
    items = library_data.setdefault("items", {})
    for candidate in candidates:
        reason = admission_reason(candidate, config)
        if not reason:
            continue
        key = candidate_key(candidate)
        tier = assign_watch_tier(candidate, config)
        expires_at = now + timedelta(days=watch_days_for_tier(tier, config))
        entry = items.get(key)
        if not entry:
            item = LibraryItem(
                key=key,
                title=candidate.title,
                category=candidate.category,
                sources=[candidate.source],
                watch_status="active",
                watch_tier=tier,
                admission_reason=reason,
                first_discovered_at=iso(now),
                last_discovered_at=iso(now),
                watch_started_at=iso(now),
                watch_expires_at=iso(expires_at),
                last_seen_in_sources_at=iso(now),
                douban_id=candidate.douban_id,
                tmdb_id=candidate.tmdb_id,
                imdb_id=candidate.imdb_id,
                url=candidate.url,
                year=candidate.year,
                last_rating=candidate.rating,
                last_rating_count=candidate.rating_count,
                last_checked_at=iso(now),
                qualified=should_qualify(candidate, config),
                qualified_at=iso(now) if should_qualify(candidate, config) else None,
            )
            items[key] = asdict(item)
            continue
        entry["title"] = candidate.title
        entry["category"] = candidate.category
        entry["url"] = candidate.url
        entry["last_discovered_at"] = iso(now)
        entry["last_seen_in_sources_at"] = iso(now)
        entry["watch_tier"] = tier
        entry["watch_expires_at"] = iso(expires_at)
        entry["last_checked_at"] = iso(now)
        entry["last_rating"] = candidate.rating
        entry["last_rating_count"] = candidate.rating_count
        entry["qualified"] = should_qualify(candidate, config)
        if entry["qualified"] and not entry.get("qualified_at"):
            entry["qualified_at"] = iso(now)
        if candidate.source not in entry["sources"]:
            entry["sources"].append(candidate.source)
    library_data["updated_at"] = iso(now)
    return library_data


def archive_expired_library_items(library_data: dict[str, Any], config: dict[str, Any], now: datetime) -> dict[str, Any]:
    for entry in library_data.get("items", {}).values():
        if entry.get("archived_at"):
            continue
        expires_at = parse_dt(entry.get("watch_expires_at"))
        if expires_at and expires_at < now and not entry.get("qualified"):
            entry["watch_status"] = "archived"
            entry["archived_at"] = iso(now)
            entry["archive_reason"] = "watch_window_expired_without_qualification"
            continue
        rating = entry.get("last_rating") or 0.0
        if rating < config["drop_rating_threshold"]:
            entry["watch_status"] = "archived"
            entry["archived_at"] = iso(now)
            entry["archive_reason"] = "rating_below_threshold"
    library_data["updated_at"] = iso(now)
    return library_data


def update_state(state_data: dict[str, Any], candidates: list[Candidate], config: dict[str, Any], now: datetime) -> tuple[dict[str, Any], list[Candidate], list[tuple[Candidate, str]]]:
    items = state_data.setdefault("items", {})
    new_qualified: list[Candidate] = []
    second_look: list[tuple[Candidate, str]] = []
    for candidate in candidates:
        key = candidate.douban_id or candidate_key(candidate)
        entry = items.get(key)
        qualifies = should_qualify(candidate, config)
        if not entry:
            state_item = StateItem(
                douban_id=candidate.douban_id,
                title=candidate.title,
                category=candidate.category,
                url=candidate.url,
                first_seen_at=iso(now),
                last_seen_at=iso(now),
                first_qualified_at=iso(now) if qualifies else None,
                last_notified_at=iso(now) if qualifies else None,
                last_rating=candidate.rating,
                last_rating_count=candidate.rating_count,
                peak_rating=candidate.rating,
                peak_rating_count=candidate.rating_count,
                notified_stage="initial" if qualifies else None,
                qualified=qualifies,
            )
            items[key] = asdict(state_item)
            if qualifies:
                new_qualified.append(candidate)
            continue

        previous_rating = entry.get("last_rating") or 0.0
        previous_count = entry.get("last_rating_count") or 0
        entry["title"] = candidate.title
        entry["category"] = candidate.category
        entry["url"] = candidate.url
        entry["last_seen_at"] = iso(now)
        entry["last_rating"] = candidate.rating
        entry["last_rating_count"] = candidate.rating_count
        entry["peak_rating"] = max(entry.get("peak_rating") or 0.0, candidate.rating or 0.0)
        entry["peak_rating_count"] = max(entry.get("peak_rating_count") or 0, candidate.rating_count or 0)

        if qualifies and not entry.get("first_qualified_at"):
            entry["first_qualified_at"] = iso(now)
            entry["last_notified_at"] = iso(now)
            entry["notified_stage"] = "initial"
            entry["qualified"] = True
            new_qualified.append(candidate)
            continue
        if not qualifies:
            continue
        cooldown_cutoff = now - timedelta(days=config["realert_cooldown_days"])
        last_notified_at = parse_dt(entry.get("last_notified_at"))
        if last_notified_at and last_notified_at > cooldown_cutoff:
            continue

        trigger: str | None = None
        if (candidate.rating or 0.0) - previous_rating >= config["rating_delta_for_realert"]:
            trigger = f"评分较上次提醒提升 {(candidate.rating or 0.0) - previous_rating:.1f}"
        elif (candidate.rating_count or 0) - previous_count >= config["rating_count_delta_for_realert"]:
            trigger = f"评分人数较上次提醒增加 {(candidate.rating_count or 0) - previous_count}"
        else:
            for milestone in config["milestone_counts"]:
                if previous_count < milestone <= (candidate.rating_count or 0) and milestone not in entry["milestones_notified"]:
                    entry["milestones_notified"].append(milestone)
                    trigger = f"评分人数跨过 {milestone}"
                    break
        if trigger:
            entry["last_notified_at"] = iso(now)
            entry["notified_stage"] = "second_look"
            second_look.append((candidate, trigger))

    state_data["updated_at"] = iso(now)
    return state_data, new_qualified, second_look


def render_report(new_qualified: list[Candidate], second_look: list[tuple[Candidate, str]], observed: list[Candidate], config: dict[str, Any], now: datetime) -> str:
    lines = [
        "# 豆瓣高分监控",
        "",
        f"运行时间: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}",
        f"阈值: 评分 > {config['min_rating']}，评分人数 > {config['min_rating_count']}",
        "",
        "## 新增命中",
    ]
    if not new_qualified:
        lines.append("- 无")
    for item in new_qualified:
        lines.extend([
            f"- 标题: {item.title}",
            f"- 类型: {item.category}",
            f"- 评分: {item.rating}",
            f"- 评分人数: {item.rating_count}",
            f"- 链接: {item.url or 'N/A'}",
            "- 触发原因: 首次达标",
        ])
    lines.extend(["", "## 值得二次关注"])
    if not second_look:
        lines.append("- 无")
    for item, trigger in second_look:
        lines.extend([
            f"- 标题: {item.title}",
            f"- 类型: {item.category}",
            f"- 评分: {item.rating}",
            f"- 评分人数: {item.rating_count}",
            f"- 链接: {item.url or 'N/A'}",
            f"- 触发原因: {trigger}",
        ])
    lines.extend(["", "## 继续观察"])
    pending = [item for item in observed if not should_qualify(item, config)]
    if not pending:
        lines.append("- 无")
    for item in pending:
        lines.extend([
            f"- 标题: {item.title}",
            f"- 评分: {item.rating}",
            f"- 评分人数: {item.rating_count}",
        ])
    return "\n".join(lines) + "\n"


def build_result_json(candidates: list[Candidate], config: dict[str, Any], now: datetime, library_data: dict[str, Any]) -> dict[str, Any]:
    """Build the result.json consumed by the frontend (index.html)."""
    qualified = [
        c for c in candidates if should_qualify(c, config)
    ]
    library_items = library_data.get("items", {})
    items = []
    for c in qualified:
        entry = library_items.get(candidate_key(c)) or {}
        items.append({
            "title": c.title,
            "category": c.category,
            "douban_id": c.douban_id,
            "rating": c.rating,
            "rating_count": c.rating_count,
            "year": str(c.year) if c.year else "",
            "url": c.url or "",
            "qualified_at": entry.get("qualified_at"),
            "first_discovered_at": entry.get("first_discovered_at"),
        })
    return {
        "run_at": iso(now),
        "total": len(candidates),
        "qualified": items,
        "status": "has_qualified" if items else "no_qualified",
    }


def build_posters_json(candidates: list[Candidate], config: dict[str, Any]) -> dict[str, str]:
    """Fetch TMDB poster URLs for qualified candidates, keyed by douban_id."""
    posters: dict[str, str] = {}
    api_key = get_env("TMDB_API_KEY")
    bearer = get_env("TMDB_BEARER_TOKEN")
    if not api_key and not bearer:
        return posters

    for c in candidates:
        if not c.douban_id or not should_qualify(c, config):
            continue
        if not c.tmdb_id:
            # Try searching TMDB by title
            try:
                media_type = "movie" if c.category == "movie" else "tv"
                params: dict[str, Any] = {
                    "query": c.title,
                    "language": config["tmdb_language"],
                }
                if c.year:
                    params["year" if media_type == "movie" else "first_air_date_year"] = c.year
                data = tmdb_get(f"/search/{media_type}", config, params)
                results = data.get("results") or []
                if results:
                    c.tmdb_id = results[0].get("id")
            except Exception:
                continue
        if c.tmdb_id:
            try:
                media_type = "movie" if c.category == "movie" else "tv"
                data = tmdb_get(f"/{media_type}/{c.tmdb_id}", config, {"language": config["tmdb_language"]})
                poster_path = data.get("poster_path")
                if poster_path:
                    posters[c.douban_id] = f"https://image.tmdb.org/t/p/w500{poster_path}"
            except Exception:
                continue
        time.sleep(0.15)
    return posters


def build_metadata_json(candidates: list[Candidate], config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Fetch TMDB metadata for qualified candidates, keyed by douban_id."""
    meta: dict[str, dict[str, Any]] = {}
    api_key = get_env("TMDB_API_KEY")
    bearer = get_env("TMDB_BEARER_TOKEN")
    if not api_key and not bearer:
        return meta

    for c in candidates:
        if not c.douban_id or not should_qualify(c, config):
            continue
        if not c.tmdb_id:
            continue
        try:
            media_type = "movie" if c.category == "movie" else "tv"
            data = tmdb_get(f"/{media_type}/{c.tmdb_id}", config, {"language": config["tmdb_language"]})
            entry: dict[str, Any] = {}
            original_title = data.get("original_title") or data.get("original_name") or ""
            if original_title:
                entry["original_title"] = original_title
            overview = data.get("overview") or ""
            if overview:
                entry["overview"] = overview
            genres = [g.get("name") for g in (data.get("genres") or []) if g.get("name")]
            if genres:
                entry["genres"] = genres
            release_date = data.get("release_date") or data.get("first_air_date") or ""
            if release_date:
                entry["release_date"] = release_date
            if entry:
                meta[c.douban_id] = entry
        except Exception:
            continue
        time.sleep(0.15)
    return meta


def run(base_dir: Path, config: dict[str, Any] | None = None) -> dict[str, Path]:
    project_root = base_dir.parent
    file_config = load_toml(project_root / "config.toml")
    config = {**DEFAULT_CONFIG, **file_config, **(config or {})}
    now = now_cst()

    log_step("运行模式: 豆瓣 Rexxar API")

    state_path = project_root / "data" / "douban-monitor-state.json"
    library_path = project_root / "data" / "douban-monitor-library.json"
    report_path = project_root / "reports" / f"douban-monitor-{now.strftime('%Y%m%d')}.md"

    state_data = load_json(state_path, {"version": 1, "updated_at": None, "items": {}})
    library_data = load_json(library_path, {"version": 1, "updated_at": None, "items": {}})

    log_step("[1/8] 抓取豆瓣榜单候选...")
    douban_candidates = fetch_douban_weekly_candidates_lite(config)
    log_kv("豆瓣榜单候选数", len(douban_candidates))

    log_step("[2/8] 抓取 TMDB 候选...")
    tmdb_candidates = fetch_tmdb_hot_candidates_with_config(config)
    log_kv("TMDB 候选数", len(tmdb_candidates))

    log_step("[3/8] 去重并补详情页...")
    candidates: list[Candidate] = []
    candidates.extend(douban_candidates)
    candidates.extend(tmdb_candidates)
    deduped_candidates = dedupe_candidates(candidates)
    log_kv("去重后候选数", len(deduped_candidates))
    enriched: list[Candidate] = []
    for item in deduped_candidates:
        if item.rating is not None and item.rating_count is not None:
            enriched.append(enrich_with_tmdb(item))
        else:
            enriched.append(enrich_with_tmdb(fetch_douban_subject_detail_lite(item, config)))
            time.sleep(0.3)
    candidates = enriched
    detail_ready = sum(1 for item in candidates if item.url)
    rating_ready = sum(1 for item in candidates if item.rating is not None)
    rating_count_ready = sum(1 for item in candidates if item.rating_count is not None)
    log_kv("已有详情页链接", detail_ready)
    log_kv("已获取评分", rating_ready)
    log_kv("已获取评分人数", rating_count_ready)

    log_step("[4/8] 更新状态与监控库...")
    library_data = update_library(library_data, candidates, config, now)
    library_data = archive_expired_library_items(library_data, config, now)
    state_data, new_qualified, second_look = update_state(state_data, candidates, config, now)
    report = render_report(new_qualified, second_look, candidates, config, now)
    pending_count = sum(1 for item in candidates if not should_qualify(item, config))
    log_kv("新增命中", len(new_qualified))
    log_kv("值得二次关注", len(second_look))
    log_kv("继续观察", pending_count)
    log_kv("监控库条目数", len(library_data.get("items", {})))
    log_kv("状态条目数", len(state_data.get("items", {})))

    # 若本次一条候选都没拉到（豆瓣/TMDB 全挂），跳过日报和前端数据的写入，
    # 保留上一份好数据，避免网页刷新出空列表。state/library 只是 updated_at 微更新，照常写。
    fetch_empty = len(candidates) == 0

    log_step("[5/8] 写入状态与报告...")
    save_json(state_path, state_data)
    save_json(library_path, library_data)
    log_kv("状态文件", state_path)
    log_kv("监控库文件", library_path)
    if fetch_empty:
        log_kv("跳过日报写入", "候选为 0，保留上一份")
    else:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
        log_kv("报告文件", report_path)

    log_step("[6/8] 生成前端数据...")
    result_path = project_root / "data" / "douban-monitor-result.json"
    if fetch_empty:
        log_kv("跳过前端结果写入", "候选为 0，保留上一份")
    else:
        result_data = build_result_json(candidates, config, now, library_data)
        save_json(result_path, result_data)
        log_kv("前端结果文件", result_path)
        log_kv("达标条目数", len(result_data["qualified"]))

    log_step("[7/8] 生成网页数据（封面 + 元数据）...")
    python = sys.executable
    for script_name in ("fetch_favorites.py", "fetch_posters.py", "fetch_metadata.py", "fetch_reviews.py", "generate_detail_pages.py"):
        script_path = base_dir / script_name
        if not script_path.exists():
            continue
        log_kv("运行", script_name)
        result = subprocess.run(
            [python, str(script_path)],
            cwd=str(project_root),
            capture_output=True, text=True,
        )
        if result.stdout:
            print(result.stdout, end="", flush=True)
        if result.returncode != 0:
            log_kv(f"{script_name} 失败 (exit {result.returncode})", "")
            if result.stderr:
                print(result.stderr, end="", flush=True)

    log_step("[8/8] 同步并推送到 GitHub...")

    # 纯本地模式：跳过 git 同步，数据只写在本地，由 skill 在对话中汇报结果。
    no_push_env = (get_env("DOUBAN_MONITOR_NO_PUSH") or "").lower() in ("1", "true", "yes")
    if no_push_env or not config.get("auto_git_push", True):
        log_kv("本地模式", "跳过 git 同步（auto_git_push=false 或 DOUBAN_MONITOR_NO_PUSH）")
        return {"state_path": state_path, "library_path": library_path, "report_path": report_path, "result_path": result_path}

    git_kw = {"cwd": str(project_root), "capture_output": True, "text": True, "encoding": "utf-8", "errors": "replace"}

    # 先拉取远端最新，避免 push 被拒绝
    pull = subprocess.run(["git", "pull", "--rebase", "--autostash"], **git_kw)
    if pull.returncode != 0:
        log_kv("拉取失败（中止提交，避免推送坏数据）", (pull.stderr or pull.stdout or "").strip())
        return {"state_path": state_path, "library_path": library_path, "report_path": report_path, "result_path": result_path}
    log_kv("拉取", "成功")

    subprocess.run(["git", "add", "data/", "detail/", "reports/", "posters/"], **git_kw)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], **git_kw)
    if diff.returncode == 0:
        log_kv("跳过", "数据无变化，无需提交")
        return {"state_path": state_path, "library_path": library_path, "report_path": report_path, "result_path": result_path}

    # 提交前扫一遍待提交文件，防止冲突标记混进去
    staged_diff = subprocess.run(["git", "diff", "--cached"], **git_kw)
    conflict_markers = ("<<<<<<<", "=======", ">>>>>>>")
    suspicious = [m for m in conflict_markers if f"\n+{m}" in (staged_diff.stdout or "")]
    if suspicious:
        log_kv("检测到冲突标记，中止提交", " ".join(suspicious))
        subprocess.run(["git", "reset", "HEAD", "--", "data/", "reports/"], **git_kw)
        return {"state_path": state_path, "library_path": library_path, "report_path": report_path, "result_path": result_path}

    msg = f"data: 更新监控数据 {now.strftime('%Y-%m-%d %H:%M')}"
    subprocess.run(["git", "commit", "-m", msg], **git_kw)
    push = subprocess.run(["git", "push"], **git_kw)
    if push.returncode == 0:
        log_kv("推送", "成功")
    else:
        log_kv("推送失败", (push.stderr or "").strip())

    return {"state_path": state_path, "library_path": library_path, "report_path": report_path, "result_path": result_path}


if __name__ == "__main__":
    run(Path(__file__).resolve().parent)
