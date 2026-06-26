#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sqlite3
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path

from industry_chain import enrich_event_payload_with_chain_focus
from runtime_config import load_runtime_env, require_em_api_key


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "assets" / "news_iterator_config.json"
DEFAULT_WATCHLIST = ROOT / "assets" / "default_watchlists.json"
DEFAULT_STATE_DIR = Path.home() / ".uwillberich" / "news-iterator"
DEFAULT_DB = DEFAULT_STATE_DIR / "news_iterator.sqlite3"
DEFAULT_MARKDOWN = DEFAULT_STATE_DIR / "latest_alerts.md"
DEFAULT_JSONL = DEFAULT_STATE_DIR / "alerts.jsonl"
DEFAULT_EVENT_WATCHLIST = DEFAULT_STATE_DIR / "event_watchlists.json"
DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0"}
EVENT_CATEGORY_ORDER = ["huge_conflict", "huge_future", "huge_name_release"]
CATEGORY_LABELS = {
    "huge_conflict": "巨大冲突",
    "huge_future": "巨大前景",
    "huge_name_release": "巨头名人",
}
SIGNAL_LABELS = {"high": "高", "medium": "中", "low": "低"}
KEYWORD_LABELS = {
    "war": "战争",
    "oil": "原油",
    "energy": "能源",
    "chips": "芯片",
    "chip": "芯片",
    "robots": "机器人",
    "robot": "机器人",
    "launch": "发布",
    "launches": "发布",
    "announces": "宣布",
    "announce": "宣布",
    "unveils": "亮相",
    "unveil": "亮相",
    "data center": "数据中心",
}


load_runtime_env()
require_em_api_key(script_hint="python3 skill/uwillberich/scripts/runtime_config.py set-em-key --stdin")


@dataclass
class FeedItem:
    item_key: str
    feed_key: str
    feed_label: str
    source: str
    title: str
    link: str
    summary: str
    published_at: str


def load_config(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def ensure_state_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def open_db(path: Path) -> sqlite3.Connection:
    ensure_state_dir(path.parent)
    conn = sqlite3.connect(path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            item_key TEXT PRIMARY KEY,
            feed_key TEXT NOT NULL,
            feed_label TEXT NOT NULL,
            source TEXT,
            title TEXT NOT NULL,
            link TEXT NOT NULL,
            summary TEXT,
            published_at TEXT,
            inserted_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS alerts (
            alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_key TEXT NOT NULL,
            category TEXT NOT NULL,
            score INTEGER NOT NULL,
            signal TEXT NOT NULL,
            impacted_watchlists_json TEXT NOT NULL,
            watchlist_scores_json TEXT NOT NULL DEFAULT '{}',
            matched_entities_json TEXT NOT NULL,
            matched_keywords_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(item_key, category)
        )
        """
    )
    columns = {row[1] for row in conn.execute("PRAGMA table_info(alerts)").fetchall()}
    if "watchlist_scores_json" not in columns:
        conn.execute("ALTER TABLE alerts ADD COLUMN watchlist_scores_json TEXT NOT NULL DEFAULT '{}'")
    return conn


def normalize_text(value: str) -> str:
    cleaned = value or ""
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = html.unescape(cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def normalize_match_text(value: str) -> str:
    cleaned = normalize_text(value)
    cleaned = re.sub(r"https?://\S+", " ", cleaned)
    cleaned = re.sub(r"\bnews\.google\.com\b", " ", cleaned, flags=re.IGNORECASE)
    return cleaned.lower()


def category_display_name(category: str) -> str:
    return CATEGORY_LABELS.get(category, category)


def signal_display_name(signal: str) -> str:
    return SIGNAL_LABELS.get(signal, signal)


def keyword_display_name(keyword: str) -> str:
    return KEYWORD_LABELS.get(keyword, keyword)


def format_keyword_list(keywords: list[str]) -> str:
    if not keywords:
        return "n/a"
    return ", ".join(keyword_display_name(keyword) for keyword in keywords)


def term_pattern(term: str) -> re.Pattern[str]:
    escaped = re.escape(normalize_match_text(term))
    return re.compile(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])")


def text_contains_term(text: str, term: str) -> bool:
    return bool(term_pattern(term).search(normalize_match_text(text)))


def parse_datetime(raw: str) -> str:
    if not raw:
        return ""
    try:
        parsed = parsedate_to_datetime(raw)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC).isoformat()
    except Exception:
        return raw


def fetch_url(url: str) -> bytes:
    request = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def build_item_key(feed_key: str, guid: str, link: str, title: str) -> str:
    base = guid or link or title
    return hashlib.sha256(f"{feed_key}|{base}".encode("utf-8")).hexdigest()


def parse_feed(feed: dict) -> list[FeedItem]:
    payload = fetch_url(feed["url"])
    root = ET.fromstring(payload)
    items: list[FeedItem] = []

    channel = root.find("channel")
    if channel is not None:
        for item in channel.findall("item"):
            title = normalize_text(item.findtext("title"))
            link = normalize_text(item.findtext("link"))
            summary = normalize_text(item.findtext("description"))
            source = normalize_text(item.findtext("source")) or feed["label"]
            guid = normalize_text(item.findtext("guid"))
            published = parse_datetime(normalize_text(item.findtext("pubDate")))
            items.append(
                FeedItem(
                    item_key=build_item_key(feed["key"], guid, link, title),
                    feed_key=feed["key"],
                    feed_label=feed["label"],
                    source=source,
                    title=title,
                    link=link,
                    summary=summary,
                    published_at=published,
                )
            )
        return items

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("atom:entry", ns):
        title = normalize_text(entry.findtext("atom:title", default="", namespaces=ns))
        link_el = entry.find("atom:link", ns)
        link = normalize_text(link_el.attrib.get("href", "")) if link_el is not None else ""
        summary = normalize_text(entry.findtext("atom:summary", default="", namespaces=ns))
        source = feed["label"]
        guid = normalize_text(entry.findtext("atom:id", default="", namespaces=ns))
        published = parse_datetime(
            normalize_text(entry.findtext("atom:updated", default="", namespaces=ns))
        )
        items.append(
            FeedItem(
                item_key=build_item_key(feed["key"], guid, link, title),
                feed_key=feed["key"],
                feed_label=feed["label"],
                source=source,
                title=title,
                link=link,
                summary=summary,
                published_at=published,
            )
        )
    return items


def match_terms(text: str, terms: list[str]) -> list[str]:
    return sorted({term for term in terms if text_contains_term(text, term)})


def bump_watchlist_scores(scores: dict[str, int], groups: list[str], points: int) -> None:
    for group in groups:
        scores[group] = scores.get(group, 0) + points


def derive_watchlist_scores(
    text: str,
    matched_entities: list[str],
    config: dict,
    categories: list[str],
) -> dict[str, int]:
    watchlist_scores: dict[str, int] = {}

    for entity in matched_entities:
        bump_watchlist_scores(
            watchlist_scores,
            config.get("entity_watchlists", {}).get(entity.lower(), []),
            points=2,
        )

    for keyword, groups in config.get("keyword_watchlists", {}).items():
        if text_contains_term(text, keyword):
            bump_watchlist_scores(watchlist_scores, groups, points=2)

    if "huge_future" in categories:
        bump_watchlist_scores(
            watchlist_scores,
            [
                "cross_cycle_anchor12",
                "cross_cycle_ai_hardware",
                "cross_cycle_semis",
                "cross_cycle_software_platforms",
            ],
            points=1,
        )
    if "huge_name_release" in categories:
        bump_watchlist_scores(watchlist_scores, ["cross_cycle_anchor12"], points=1)
    if "huge_conflict" in categories:
        bump_watchlist_scores(
            watchlist_scores,
            [
                "war_shock_core12",
                "defensive_gauge",
            ]
            ,
            points=1,
        )
        bump_watchlist_scores(watchlist_scores, ["war_benefit_oil_coal"], points=1)
        bump_watchlist_scores(watchlist_scores, ["war_headwind_compute_power"], points=1)
    return watchlist_scores


def score_to_signal(score: int) -> str:
    if score >= 10:
        return "high"
    if score >= 6:
        return "medium"
    return "low"


def classify_item(item: FeedItem, config: dict) -> list[dict]:
    title_text = item.title.strip()
    text = f"{item.title} {item.summary}".strip()
    matched_entities = match_terms(title_text, config.get("big_name_entities", []))
    matched_conflict_entities = match_terms(text, config.get("conflict_entities", []))
    matched_future = match_terms(text, config.get("future_keywords", []))
    matched_release = match_terms(title_text, config.get("release_verbs", []))
    matched_conflict = match_terms(text, config.get("conflict_keywords", []))
    matched_energy = match_terms(text, config.get("energy_keywords", []))
    matched_compute_power = match_terms(text, config.get("compute_power_keywords", []))

    alerts: list[dict] = []

    if matched_future and not matched_conflict and not matched_conflict_entities:
        score = len(matched_future) * 2 + (2 if matched_entities else 0)
        categories = ["huge_future"]
        watchlist_scores = derive_watchlist_scores(text, matched_entities, config, categories)
        alerts.append(
            {
                "category": "huge_future",
                "score": score,
                "signal": score_to_signal(score),
                "matched_entities": matched_entities,
                "matched_keywords": matched_future,
                "impacted_watchlists": sorted(
                    watchlist_scores,
                    key=lambda group: (-watchlist_scores[group], group),
                ),
                "watchlist_scores": watchlist_scores,
            }
        )

    if matched_entities and matched_release:
        score = len(matched_entities) * 3 + len(matched_release) * 2
        categories = ["huge_name_release"]
        watchlist_scores = derive_watchlist_scores(text, matched_entities, config, categories)
        alerts.append(
            {
                "category": "huge_name_release",
                "score": score,
                "signal": score_to_signal(score),
                "matched_entities": matched_entities,
                "matched_keywords": matched_release,
                "impacted_watchlists": sorted(
                    watchlist_scores,
                    key=lambda group: (-watchlist_scores[group], group),
                ),
                "watchlist_scores": watchlist_scores,
            }
        )

    if matched_conflict or matched_conflict_entities:
        score = len(matched_conflict) * 3 + len(matched_conflict_entities) * 3
        if matched_energy:
            score += 2
        if matched_compute_power:
            score += 1
        categories = ["huge_conflict"]
        all_entities = sorted(set(matched_conflict_entities + matched_entities))
        watchlist_scores = derive_watchlist_scores(text, all_entities, config, categories)
        alerts.append(
            {
                "category": "huge_conflict",
                "score": score,
                "signal": score_to_signal(score),
                "matched_entities": all_entities,
                "matched_keywords": sorted(set(matched_conflict + matched_energy + matched_compute_power)),
                "impacted_watchlists": sorted(
                    watchlist_scores,
                    key=lambda group: (-watchlist_scores[group], group),
                ),
                "watchlist_scores": watchlist_scores,
            }
        )

    return [alert for alert in alerts if alert["score"] >= 4]


def item_exists(conn: sqlite3.Connection, item_key: str) -> bool:
    row = conn.execute("SELECT 1 FROM items WHERE item_key = ?", (item_key,)).fetchone()
    return row is not None


def insert_item(conn: sqlite3.Connection, item: FeedItem) -> None:
    conn.execute(
        """
        INSERT OR IGNORE INTO items (
            item_key, feed_key, feed_label, source, title, link, summary, published_at, inserted_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            item.item_key,
            item.feed_key,
            item.feed_label,
            item.source,
            item.title,
            item.link,
            item.summary,
            item.published_at,
            datetime.now(UTC).isoformat(),
        ),
    )


def insert_alert(conn: sqlite3.Connection, item: FeedItem, alert: dict) -> bool:
    cursor = conn.execute(
        """
        INSERT OR IGNORE INTO alerts (
            item_key, category, score, signal, impacted_watchlists_json, matched_entities_json,
            matched_keywords_json, watchlist_scores_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            item.item_key,
            alert["category"],
            alert["score"],
            alert["signal"],
            json.dumps(alert["impacted_watchlists"], ensure_ascii=False),
            json.dumps(alert["matched_entities"], ensure_ascii=False),
            json.dumps(alert["matched_keywords"], ensure_ascii=False),
            json.dumps(alert.get("watchlist_scores", {}), ensure_ascii=False),
            datetime.now(UTC).isoformat(),
        ),
    )
    return cursor.rowcount > 0


def fetch_and_classify(conn: sqlite3.Connection, config: dict) -> list[dict]:
    new_alerts: list[dict] = []
    for feed in config.get("feeds", []):
        try:
            items = parse_feed(feed)
        except Exception as exc:
            new_alerts.append(
                {
                    "system_error": True,
                    "feed_key": feed["key"],
                    "feed_label": feed["label"],
                    "error": str(exc),
                }
            )
            continue

        for item in items:
            is_new_item = not item_exists(conn, item.item_key)
            if is_new_item:
                insert_item(conn, item)
            alerts = classify_item(item, config)
            for alert in alerts:
                if insert_alert(conn, item, alert):
                    row = {"item": item, "alert": alert}
                    new_alerts.append(row)
    conn.commit()
    return new_alerts


def row_to_markdown(row: dict) -> str:
    item: FeedItem = row["item"]
    alert = row["alert"]
    return (
        f"- [{item.title}]({item.link})\n"
        f"  source: {item.source}\n"
        f"  category: `{alert['category']}` | signal: `{alert['signal']}` | score: `{alert['score']}`\n"
        f"  watchlists: {', '.join(alert['impacted_watchlists']) or 'n/a'}\n"
        f"  entities: {', '.join(alert['matched_entities']) or 'n/a'}\n"
        f"  keywords: {', '.join(alert['matched_keywords']) or 'n/a'}"
    )


def append_jsonl(new_alerts: list[dict], jsonl_path: Path) -> None:
    ensure_state_dir(jsonl_path.parent)
    json_lines: list[str] = []

    for row in new_alerts:
        if row.get("system_error"):
            json_lines.append(json.dumps(row, ensure_ascii=False))
        else:
            item = row["item"]
            alert = row["alert"]
            json_lines.append(
                json.dumps(
                    {
                        "item_key": item.item_key,
                        "title": item.title,
                        "link": item.link,
                        "source": item.source,
                        "published_at": item.published_at,
                        "category": alert["category"],
                        "score": alert["score"],
                        "signal": alert["signal"],
                        "impacted_watchlists": alert["impacted_watchlists"],
                        "watchlist_scores": alert.get("watchlist_scores", {}),
                        "matched_entities": alert["matched_entities"],
                        "matched_keywords": alert["matched_keywords"],
                    },
                    ensure_ascii=False,
                )
            )
    with jsonl_path.open("a", encoding="utf-8") as handle:
        for line in json_lines:
            handle.write(line + "\n")


def fetch_recent_alerts(conn: sqlite3.Connection, hours: int) -> list[dict]:
    cutoff = (datetime.now(UTC) - timedelta(hours=hours)).isoformat()
    rows = conn.execute(
        """
        SELECT
            a.category,
            a.score,
            a.signal,
            a.impacted_watchlists_json,
            a.watchlist_scores_json,
            a.matched_entities_json,
            a.matched_keywords_json,
            i.title,
            i.link,
            i.source,
            i.published_at
        FROM alerts a
        JOIN items i ON i.item_key = a.item_key
        WHERE a.created_at >= ?
        ORDER BY a.score DESC, a.created_at DESC
        """,
        (cutoff,),
    ).fetchall()

    result = []
    for row in rows:
        result.append(
            {
                "category": row[0],
                "score": row[1],
                "signal": row[2],
                "watchlists": json.loads(row[3]),
                "watchlist_scores": json.loads(row[4] or "{}"),
                "entities": json.loads(row[5]),
                "keywords": json.loads(row[6]),
                "title": row[7],
                "link": row[8],
                "source": row[9],
                "published_at": row[10],
            }
        )
    return result


def top_alerts_by_category(alerts: list[dict], limit: int = 10) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for category in EVENT_CATEGORY_ORDER:
        ranked = sorted(
            [alert for alert in alerts if alert["category"] == category],
            key=lambda item: (
                item["score"],
                item.get("published_at") or "",
                item.get("title") or item.get("headline") or "",
            ),
            reverse=True,
        )
        if ranked:
            deduped: list[dict] = []
            seen_links: set[str] = set()
            for item in ranked:
                link = item.get("link") or item.get("title")
                if link in seen_links:
                    continue
                seen_links.add(link)
                deduped.append(item)
                if len(deduped) >= limit:
                    break
            grouped[category] = deduped
    return grouped


def render_report(alerts: list[dict], hours: int) -> str:
    lines = [f"# News Iterator Report", f"", f"Window: last {hours} hours"]
    if not alerts:
        lines.append("\nNo alerts in the selected window.")
        return "\n".join(lines) + "\n"

    summary = summarize_alert_categories(alerts)
    if summary:
        lines.append("")
        lines.append("## Event Summary")
        lines.append("")
        lines.append("| 类别 | 条数 | 总分 | 高频关键词 |")
        lines.append("| --- | ---: | ---: | --- |")
        for item in summary:
            lines.append(
                f"| {category_display_name(item['category'])} | {item['alert_count']} | {item['total_score']} | {format_keyword_list(item.get('top_keywords', []))} |"
            )

    grouped = top_alerts_by_category(alerts, limit=10)
    for category in EVENT_CATEGORY_ORDER:
        items = grouped.get(category, [])
        if not items:
            continue
        lines.append(f"\n## {category_display_name(category)} Top 10 信息源")
        for index, alert in enumerate(items, start=1):
            lines.append(f"{index}. [{alert['title']}]({alert['link']})")
            lines.append(
                f"   - 来源: {alert['source']} | 信号: `{signal_display_name(alert['signal'])}` | 分值: `{alert['score']}`"
            )
            lines.append(f"   - 实体: {', '.join(alert['entities']) or 'n/a'}")
            lines.append(f"   - 关键词: {format_keyword_list(alert['keywords'])}")
    return "\n".join(lines) + "\n"


def render_system_errors(rows: list[dict]) -> str:
    if not rows:
        return ""
    lines = ["\n## system_error"]
    for row in rows:
        lines.append(f"- feed: `{row['feed_key']}` ({row['feed_label']}) | error: {row['error']}")
    return "\n".join(lines) + "\n"


def load_base_watchlists(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def merge_item_details(existing: dict, incoming: dict) -> dict:
    merged = dict(existing)
    for key, value in incoming.items():
        if not merged.get(key) and value:
            merged[key] = value
    return merged


def build_base_item_index(base_watchlists: dict) -> tuple[dict[str, dict], dict[str, list[dict]]]:
    symbol_index: dict[str, dict] = {}
    group_index: dict[str, list[dict]] = {}
    for group, items in base_watchlists.items():
        group_index[group] = []
        for item in items:
            symbol = item["symbol"]
            if symbol in symbol_index:
                symbol_index[symbol] = merge_item_details(symbol_index[symbol], item)
            else:
                symbol_index[symbol] = dict(item)
            group_index[group].append(symbol_index[symbol])
    return symbol_index, group_index


def shorten_driver(category: str, keywords: Counter[str], entities: Counter[str]) -> str:
    top_terms = [term for term, _ in keywords.most_common(3)]
    top_entities = [entity for entity, _ in entities.most_common(2)]
    parts = [category]
    if top_terms:
        parts.append("/".join(top_terms))
    if top_entities:
        parts.append(",".join(top_entities))
    return " | ".join(parts)


def build_event_item(category: str, item: dict, stats: dict) -> dict:
    category_label = category.replace("event_focus_", "") if category.startswith("event_focus_") else category
    role = item.get("role", "")
    strong_signal = item.get("strong_signal") or "消息驱动仍在扩散时，优先看它能否领涨并放量。"
    weak_signal = item.get("weak_signal") or "消息很多但股价不跟，说明事件交易开始钝化。"
    return {
        "symbol": item["symbol"],
        "name": item.get("name", ""),
        "role": role,
        "event_score": stats["event_score"],
        "trigger_count": stats["trigger_count"],
        "event_driver": shorten_driver(category_label, stats["keywords"], stats["entities"]),
        "source_groups": sorted(stats["source_groups"]),
        "trigger_categories": sorted(stats["categories"]),
        "strong_signal": strong_signal,
        "weak_signal": weak_signal,
    }


def aggregate_alerts_into_pool(
    alerts: list[dict],
    group_index: dict[str, list[dict]],
    symbol_index: dict[str, dict],
    allowed_groups: set[str] | None = None,
) -> dict[str, dict]:
    symbol_stats: dict[str, dict] = {}
    for alert in alerts:
        symbol_weights: dict[str, int] = {}
        symbol_source_groups: dict[str, set[str]] = {}
        watchlist_scores = alert.get("watchlist_scores") or {group: 1 for group in alert.get("watchlists", [])}
        for group, group_weight in watchlist_scores.items():
            if group not in group_index:
                continue
            if allowed_groups is not None and group not in allowed_groups:
                continue
            for item in group_index[group]:
                symbol = item["symbol"]
                symbol_weights[symbol] = max(symbol_weights.get(symbol, 0), group_weight)
                symbol_source_groups.setdefault(symbol, set()).add(group)
        if not symbol_weights:
            continue
        for symbol, weight in symbol_weights.items():
            if symbol not in symbol_stats:
                symbol_stats[symbol] = {
                    "event_score": 0,
                    "trigger_count": 0,
                    "keywords": Counter(),
                    "entities": Counter(),
                    "categories": set(),
                    "source_groups": set(),
                }
            stats = symbol_stats[symbol]
            stats["event_score"] += alert["score"] * weight
            stats["trigger_count"] += 1
            stats["keywords"].update(alert.get("keywords", []))
            stats["entities"].update(alert.get("entities", []))
            stats["categories"].add(alert["category"])
            stats["source_groups"].update(symbol_source_groups.get(symbol, set()))
    return symbol_stats


def rank_pool_items(symbol_stats: dict[str, dict], symbol_index: dict[str, dict], limit: int, category: str) -> list[dict]:
    ranked = sorted(
        symbol_stats.items(),
        key=lambda pair: (-pair[1]["event_score"], -pair[1]["trigger_count"], pair[0]),
    )
    items: list[dict] = []
    for symbol, stats in ranked[:limit]:
        if symbol not in symbol_index:
            continue
        items.append(build_event_item(category, symbol_index[symbol], stats))
    return items


def summarize_alert_categories(alerts: list[dict]) -> list[dict]:
    category_map: dict[str, dict] = {}
    for alert in alerts:
        bucket = category_map.setdefault(
            alert["category"],
            {"category": alert["category"], "alert_count": 0, "total_score": 0, "top_keywords": Counter()},
        )
        bucket["alert_count"] += 1
        bucket["total_score"] += alert["score"]
        bucket["top_keywords"].update(alert.get("keywords", []))
    summary = []
    for bucket in category_map.values():
        summary.append(
            {
                "category": bucket["category"],
                "alert_count": bucket["alert_count"],
                "total_score": bucket["total_score"],
                "top_keywords": [term for term, _ in bucket["top_keywords"].most_common(3)],
            }
        )
    return sorted(summary, key=lambda item: (-item["total_score"], -item["alert_count"], item["category"]))


def build_event_watchlists_payload(alerts: list[dict], base_watchlists: dict, hours: int) -> dict:
    symbol_index, group_index = build_base_item_index(base_watchlists)
    groups: dict[str, list[dict]] = {}

    all_stats = aggregate_alerts_into_pool(alerts, group_index, symbol_index)
    groups["event_focus_core"] = rank_pool_items(all_stats, symbol_index, limit=12, category="event_focus_core")

    category_summary = summarize_alert_categories(alerts)
    for category in EVENT_CATEGORY_ORDER:
        category_alerts = [alert for alert in alerts if alert["category"] == category]
        if not category_alerts:
            continue
        stats = aggregate_alerts_into_pool(category_alerts, group_index, symbol_index)
        groups[f"event_focus_{category}"] = rank_pool_items(
            stats,
            symbol_index,
            limit=10,
            category=f"event_focus_{category}",
        )

    conflict_alerts = [alert for alert in alerts if alert["category"] == "huge_conflict"]
    if conflict_alerts:
        benefit_stats = aggregate_alerts_into_pool(
            conflict_alerts,
            group_index,
            symbol_index,
            allowed_groups={"war_benefit_oil_coal"},
        )
        headwind_stats = aggregate_alerts_into_pool(
            conflict_alerts,
            group_index,
            symbol_index,
            allowed_groups={"war_headwind_compute_power"},
        )
        defensive_stats = aggregate_alerts_into_pool(
            conflict_alerts,
            group_index,
            symbol_index,
            allowed_groups={"defensive_gauge"},
        )
        groups["event_focus_huge_conflict_benefit"] = rank_pool_items(
            benefit_stats,
            symbol_index,
            limit=8,
            category="event_focus_huge_conflict_benefit",
        )
        groups["event_focus_huge_conflict_headwind"] = rank_pool_items(
            headwind_stats,
            symbol_index,
            limit=8,
            category="event_focus_huge_conflict_headwind",
        )
        groups["event_focus_huge_conflict_defensive"] = rank_pool_items(
            defensive_stats,
            symbol_index,
            limit=6,
            category="event_focus_huge_conflict_defensive",
        )

    default_report_groups: list[str] = []
    for item in category_summary[:2]:
        if item["category"] == "huge_conflict":
            for group_name in [
                "event_focus_huge_conflict_benefit",
                "event_focus_huge_conflict_headwind",
                "event_focus_huge_conflict_defensive",
            ]:
                if group_name in groups:
                    default_report_groups.append(group_name)
            continue
        group_name = f"event_focus_{item['category']}"
        if group_name in groups:
            default_report_groups.append(group_name)
    if not default_report_groups and groups.get("event_focus_core"):
        default_report_groups.append("event_focus_core")

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "lookback_hours": hours,
        "summary": category_summary,
        "top_alerts": top_alerts_by_category(alerts, limit=10),
        "default_report_groups": list(dict.fromkeys(default_report_groups)),
        "groups": {name: items for name, items in groups.items() if items},
    }


def write_event_watchlists(payload: dict, path: Path) -> None:
    ensure_state_dir(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_event_watchlists(payload: dict) -> str:
    groups = payload.get("groups", {})
    if not groups:
        return ""

    lines = ["\n## Event Pools"]
    for group_name in payload.get("default_report_groups", []):
        items = groups.get(group_name, [])
        if not items:
            continue
        lines.append(f"\n### {group_name}")
        for item in items[:6]:
            lines.append(
                f"- {item['name']} `{item['symbol'][2:]}` | score `{item['event_score']}` | triggers `{item['trigger_count']}` | {item['event_driver']}"
            )
    chain_summary = payload.get("chain_summary", [])
    if chain_summary:
        lines.append("\n## Industry Chain Focus")
        lines.append("")
        lines.append("| Theme | Score | Group | Reasons |")
        lines.append("| --- | ---: | --- | --- |")
        for item in chain_summary:
            reasons = " / ".join(item.get("reasons", [])[:3]) or "n/a"
            lines.append(f"| {item['theme']} | {item['score']} | {item['group']} | {reasons} |")
    for error in payload.get("chain_errors", []):
        lines.append(f"- chain_error: `{error['theme']}` | {error['error']}")
    return "\n".join(lines) + "\n"


def run_poll(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    conn = open_db(Path(args.db_path))
    try:
        new_alerts = fetch_and_classify(conn, config)
        append_jsonl(new_alerts, Path(args.jsonl_path))
        recent_alerts = fetch_recent_alerts(conn, args.report_hours)
        event_payload = build_event_watchlists_payload(
            recent_alerts,
            load_base_watchlists(args.watchlist_path),
            args.report_hours,
        )
        event_payload = enrich_event_payload_with_chain_focus(
            event_payload,
            load_base_watchlists(args.watchlist_path),
        )
        write_event_watchlists(event_payload, Path(args.event_watchlist_path))
        markdown = render_report(recent_alerts, args.report_hours)
        markdown += render_event_watchlists(event_payload)
        system_errors = [row for row in new_alerts if row.get("system_error")]
        markdown += render_system_errors(system_errors)
        Path(args.markdown_path).write_text(markdown, encoding="utf-8")
        if args.format == "json":
            serializable = []
            for row in new_alerts:
                if row.get("system_error"):
                    serializable.append(row)
                    continue
                item: FeedItem = row["item"]
                serializable.append(
                    {
                        "title": item.title,
                        "link": item.link,
                        "source": item.source,
                        "published_at": item.published_at,
                        **row["alert"],
                    }
                )
            print(json.dumps(serializable, ensure_ascii=False, indent=2))
        else:
            print(markdown)
        return 0
    finally:
        conn.close()


def run_loop(args: argparse.Namespace) -> int:
    interval = max(args.interval_seconds, 30)
    while True:
        run_poll(args)
        time.sleep(interval)


def run_report(args: argparse.Namespace) -> int:
    conn = open_db(Path(args.db_path))
    try:
        alerts = fetch_recent_alerts(conn, args.hours)
        report = render_report(alerts, args.hours)
        event_payload = build_event_watchlists_payload(
            alerts,
            load_base_watchlists(args.watchlist_path),
            args.hours,
        )
        event_payload = enrich_event_payload_with_chain_focus(
            event_payload,
            load_base_watchlists(args.watchlist_path),
        )
        report += render_event_watchlists(event_payload)
        if args.event_watchlist_path:
            write_event_watchlists(event_payload, Path(args.event_watchlist_path))
        print(report)
        return 0
    finally:
        conn.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Persistent RSS-based news iterator for A-share idea intake.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to news iterator config JSON.")
    parser.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR), help="State directory for reports and DB.")
    parser.add_argument(
        "--watchlist-path",
        default=str(DEFAULT_WATCHLIST),
        help="Base watchlist JSON used to build dynamic event-driven stock pools.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common_io(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument(
            "--db-path",
            default=str(DEFAULT_DB),
            help="SQLite database path. Defaults under the state directory.",
        )
        subparser.add_argument(
            "--markdown-path",
            default=str(DEFAULT_MARKDOWN),
            help="Markdown alert output path.",
        )
        subparser.add_argument(
            "--jsonl-path",
            default=str(DEFAULT_JSONL),
            help="JSONL alert output path.",
        )
        subparser.add_argument(
            "--event-watchlist-path",
            default=str(DEFAULT_EVENT_WATCHLIST),
            help="Output path for the dynamic event-driven watchlists JSON.",
        )
        subparser.add_argument(
            "--report-hours",
            type=int,
            default=24,
            help="Lookback window for the markdown snapshot report.",
        )
        subparser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    poll = subparsers.add_parser("poll", help="Fetch feeds once and store new alerts.")
    add_common_io(poll)
    poll.set_defaults(func=run_poll)

    loop = subparsers.add_parser("loop", help="Continuously fetch feeds on an interval.")
    add_common_io(loop)
    loop.add_argument("--interval-seconds", type=int, default=300, help="Polling interval in seconds.")
    loop.set_defaults(func=run_loop)

    report = subparsers.add_parser("report", help="Render a report from stored alerts.")
    report.add_argument(
        "--db-path",
        default=str(DEFAULT_DB),
        help="SQLite database path. Defaults under the state directory.",
    )
    report.add_argument(
        "--event-watchlist-path",
        default=str(DEFAULT_EVENT_WATCHLIST),
        help="Optional output path for the dynamic event-driven watchlists JSON.",
    )
    report.add_argument("--hours", type=int, default=12, help="Lookback window in hours.")
    report.set_defaults(func=run_report)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    state_dir = Path(args.state_dir)
    ensure_state_dir(state_dir)

    if getattr(args, "db_path", None) == str(DEFAULT_DB):
        args.db_path = str(state_dir / DEFAULT_DB.name)
    if getattr(args, "markdown_path", None) == str(DEFAULT_MARKDOWN):
        args.markdown_path = str(state_dir / DEFAULT_MARKDOWN.name)
    if getattr(args, "jsonl_path", None) == str(DEFAULT_JSONL):
        args.jsonl_path = str(state_dir / DEFAULT_JSONL.name)
    if getattr(args, "event_watchlist_path", None) == str(DEFAULT_EVENT_WATCHLIST):
        args.event_watchlist_path = str(state_dir / DEFAULT_EVENT_WATCHLIST.name)

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
