#!/usr/bin/env python3
"""Build an analysis-ready summary from one or more normalized Douban JSON files.

Usage:
  python scripts/build_taste_profile.py collection.json [more.json ...]
  python scripts/build_taste_profile.py --focus-type book collection.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

BOOK_CREATOR_BLOCKLIST = (
    "出版",
    "出版社",
    "书店",
    "发行",
    "策划",
    "出品",
    "有限责任公司",
    "有限公司",
    "股份有限公司",
    "图书",
    "工作室",
)

MOVIE_NOISE_TOKENS = {
    "中国大陆",
    "中国台湾",
    "中国香港",
    "美国",
    "英国",
    "日本",
    "韩国",
    "法国",
    "德国",
    "意大利",
    "西班牙",
    "俄罗斯",
    "印度",
    "加拿大",
    "澳大利亚",
    "英语",
    "汉语普通话",
    "日语",
    "韩语",
    "法语",
    "粤语",
    "58分钟",
    "60分钟",
    "90分钟",
    "105分钟",
    "156分钟",
}

GAME_TAG_STOPWORDS = {
    "pc",
    "mac",
    "lin",
    "ios",
    "iphn",
    "ipad",
    "andr",
    "ps",
    "ps2",
    "ps3",
    "ps4",
    "ps5",
    "psp",
    "psv",
    "xsx",
    "xone",
    "x360",
    "xbox",
    "ns",
    "ns 2",
    "wii",
    "wiiu",
    "sd",
    "vr",
    "stadia",
    "2023-12-07",
}

DATE_TOKEN_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def top_counter(counter: Counter, limit: int = 20) -> list[dict[str, Any]]:
    return [{"name": k, "count": v} for k, v in counter.most_common(limit)]


def normalize_comment(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def sort_recent(items: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    dated = [x for x in items if x.get("date")]
    dated.sort(key=lambda x: str(x.get("date")), reverse=True)
    return dated[:limit]


def rating_value(item: dict[str, Any]) -> int | float | None:
    rating = item.get("rating")
    return rating if isinstance(rating, (int, float)) else None


def select_extreme_rated(items: list[dict[str, Any]], *, mode: str, limit: int = 20) -> tuple[int | float | None, list[dict[str, Any]]]:
    rated_items = [x for x in items if rating_value(x) is not None]
    if not rated_items:
        return None, []

    ratings = [rating_value(x) for x in rated_items]
    if mode == "high":
        target = max(r for r in ratings if r is not None)
    elif mode == "low":
        target = min(r for r in ratings if r is not None)
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    selected = [x for x in rated_items if rating_value(x) == target]
    selected.sort(key=lambda x: (str(x.get("date") or ""), str(x.get("title") or "")), reverse=True)
    return target, selected[:limit]


def select_commented(items: list[dict[str, Any]], limit: int = 20) -> list[dict[str, Any]]:
    out = [x for x in items if normalize_comment(x.get("comment"))]
    out.sort(key=lambda x: str(x.get("date") or ""), reverse=True)
    return out[:limit]


def normalize_game_tag_piece(piece: str) -> str | None:
    value = piece.strip()
    if not value:
        return None
    lowered = value.lower()
    if lowered in GAME_TAG_STOPWORDS:
        return None
    if DATE_TOKEN_RE.match(value):
        return None
    if YEAR_RE.fullmatch(value):
        return None
    if len(value) > 40:
        return None
    return value


def extract_game_tags(raw_tags: list[str]) -> list[str]:
    result: list[str] = []
    for raw in raw_tags:
        for piece in re.split(r"/|｜|\||，|、", str(raw)):
            tag = normalize_game_tag_piece(piece)
            if tag:
                result.append(tag)
    return result


def is_book_creator_noise(value: str) -> bool:
    return any(token in value for token in BOOK_CREATOR_BLOCKLIST)


def normalize_book_creator(value: str) -> str | None:
    text = value.strip()
    if not text or len(text) > 40:
        return None
    if any(ch.isdigit() for ch in text):
        return None
    if is_book_creator_noise(text):
        return None
    return text


def normalize_movie_creator(value: str) -> str | None:
    text = value.strip().strip("()（）[]")
    if not text or len(text) > 40:
        return None
    if any(ch.isdigit() for ch in text):
        return None
    if text in MOVIE_NOISE_TOKENS:
        return None
    if text.endswith("分钟") or text.endswith("(平均)"):
        return None
    if "/" in text:
        return None
    if any(token in text for token in ("中国", "美国", "英国", "英语", "日语", "韩语")):
        return None
    return text


def candidate_book_creators(item: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for raw in item.get("creators", []) or []:
        text = normalize_book_creator(str(raw))
        if text:
            result.append(text)
    return result


def extract_movie_tags(item: dict[str, Any]) -> list[str]:
    tags: list[str] = []
    title = str(item.get("title") or "").strip()
    for raw in item.get("tags", []) or []:
        for piece in re.split(r"/|｜|\|", str(raw)):
            value = piece.strip().strip("()（）[]")
            if not value:
                continue
            if DATE_TOKEN_RE.match(value):
                continue
            if YEAR_RE.fullmatch(value):
                continue
            if value in MOVIE_NOISE_TOKENS:
                continue
            if value == title:
                continue
            if value.endswith("分钟") or value.endswith("(平均)"):
                continue
            if len(value) > 30:
                continue
            tags.append(value)
    return tags


def extract_book_tags(item: dict[str, Any]) -> list[str]:
    return []


def extract_music_tags(item: dict[str, Any]) -> list[str]:
    tags: list[str] = []
    for raw in item.get("tags", []) or []:
        raw_text = str(raw).strip()
        if raw_text and len(raw_text) <= 80:
            tags.append(raw_text)
    return tags


def tags_for_item(item: dict[str, Any], focus_type: str) -> list[str]:
    if focus_type == "game":
        return extract_game_tags(item.get("tags", []) or [])
    if focus_type == "book":
        return extract_book_tags(item)
    if focus_type == "movie":
        return extract_movie_tags(item)
    if focus_type == "music":
        return extract_music_tags(item)
    tags: list[str] = []
    for raw in item.get("tags", []) or []:
        raw_text = str(raw).strip()
        if raw_text and len(raw_text) <= 80:
            tags.append(raw_text)
    return tags


def creators_for_item(item: dict[str, Any], focus_type: str) -> list[str]:
    if focus_type == "book":
        return candidate_book_creators(item)
    if focus_type == "game":
        return []
    result: list[str] = []
    for raw in item.get("creators", []) or []:
        text = str(raw).strip()
        if focus_type == "movie":
            text = normalize_movie_creator(text) or ""
        if text and len(text) <= 40 and not any(ch.isdigit() for ch in text):
            result.append(text)
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--focus-type", choices=["movie", "book", "music", "game", "all"], default="all")
    p.add_argument("paths", nargs="+")
    return p.parse_args(argv[1:])


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    items: list[dict[str, Any]] = []
    source_files: list[str] = []
    for raw in args.paths:
        path = Path(raw)
        if not path.exists():
            print(f"Missing file: {path}", file=sys.stderr)
            return 2
        data = load_json(path)
        source_files.append(str(path))
        items.extend([x for x in data.get("items", []) if isinstance(x, dict)])

    focus_type = args.focus_type
    focused_items = items if focus_type == "all" else [x for x in items if x.get("subject_type") == focus_type]

    by_type = Counter()
    by_status = Counter()
    ratings = Counter()
    tags = Counter()
    creators = Counter()
    years = Counter()
    comments: list[str] = []
    latest_dates: list[str] = []

    for item in focused_items:
        subject_type = item.get("subject_type") or "unknown"
        by_type[subject_type] += 1

        status = item.get("status") or "unknown"
        by_status[status] += 1

        rating = rating_value(item)
        if rating is not None:
            ratings[str(rating)] += 1

        effective_type = focus_type if focus_type != "all" else str(subject_type)

        for tag in tags_for_item(item, effective_type):
            tags[tag] += 1

        for creator in creators_for_item(item, effective_type):
            creators[creator] += 1

        year = item.get("year")
        if year:
            years[str(year)] += 1

        comment = normalize_comment(item.get("comment"))
        if comment:
            comments.append(comment)

        date = item.get("date")
        if date:
            latest_dates.append(str(date))

    high_rating_value, high_rated_items = select_extreme_rated(focused_items, mode="high", limit=20)
    low_rating_value, low_rated_items = select_extreme_rated(focused_items, mode="low", limit=20)

    preference_hints: list[str] = []
    for tag, count in tags.most_common(10):
        if count >= 3:
            preference_hints.append(f"高频标签：{tag}（{count}）")
    for creator, count in creators.most_common(10):
        if count >= 2:
            preference_hints.append(f"重复出现的创作者：{creator}（{count}）")

    output = {
        "platform": "douban",
        "owner": "self",
        "focus_type": focus_type,
        "source_files": source_files,
        "stats": {
            "total_items": len(focused_items),
            "by_type": dict(by_type),
            "by_status": dict(by_status),
            "ratings": dict(ratings),
            "date_range": {
                "from": min(latest_dates) if latest_dates else None,
                "to": max(latest_dates) if latest_dates else None,
            },
        },
        "top_tags": top_counter(tags),
        "top_creators": top_counter(creators),
        "top_years": top_counter(years),
        "high_rated_items": high_rated_items,
        "high_rating_value": high_rating_value,
        "low_rated_items": low_rated_items,
        "low_rating_value": low_rating_value,
        "commented_items": select_commented(focused_items, limit=20),
        "recent_items": sort_recent(focused_items, limit=20),
        "recent_comments": comments[-20:],
        "preference_hints": preference_hints,
    }

    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
