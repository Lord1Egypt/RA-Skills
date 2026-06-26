#!/usr/bin/env python3
"""
Build event candidates from normalized source_item records.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional

STOPWORDS = {
    "the",
    "a",
    "an",
    "for",
    "to",
    "of",
    "and",
    "in",
    "on",
    "with",
    "ai",
    "news",
}

TOKEN_NORMALIZATION = {
    "costs": "cost",
    "pricing": "price",
    "prices": "price",
    "agents": "agent",
    "models": "model",
    "announces": "announce",
    "announced": "announce",
    "launches": "launch",
    "launched": "launch",
    "cuts": "cut",
    "lowers": "cut",
}


def clean_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value.lower()).strip("-")


def parse_time(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None


def source_items_from_payload(payload: object) -> List[Dict[str, object]]:
    if isinstance(payload, dict) and "source_items" in payload:
        return payload["source_items"]
    if isinstance(payload, list):
        return payload
    raise ValueError("Expected either a list of source_items or a payload containing source_items.")


def title_tokens(title: str) -> List[str]:
    normalized = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", title.lower())
    tokens = []
    for token in normalized.split():
        if not token or token in STOPWORDS or len(token) <= 1:
            continue
        normalized_token = TOKEN_NORMALIZATION.get(token, token)
        if normalized_token.endswith("s") and len(normalized_token) > 3 and normalized_token.isascii():
            normalized_token = normalized_token[:-1]
        tokens.append(normalized_token)
    return tokens


def published_day(item: Dict[str, object]) -> str:
    published_at = clean_text(str(item.get("published_at", "")))
    return published_at[:10] if published_at else ""


def primary_entity(item: Dict[str, object]) -> str:
    entities = item.get("entities") or []
    return clean_text(str(entities[0])) if entities else ""


def similarity(left: Dict[str, object], right: Dict[str, object]) -> float:
    left_tokens = set(title_tokens(clean_text(str(left.get("title", "")))))
    right_tokens = set(title_tokens(clean_text(str(right.get("title", "")))))
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def should_merge(left: Dict[str, object], right: Dict[str, object]) -> bool:
    if primary_entity(left) != primary_entity(right):
        return False
    if clean_text(str(left.get("theme_guess", ""))) != clean_text(str(right.get("theme_guess", ""))):
        return False
    if published_day(left) != published_day(right):
        return False
    return similarity(left, right) >= 0.3


def group_key(item: Dict[str, object]) -> str:
    event_key = clean_text(str(item.get("event_key_guess", "")))
    if event_key:
        return event_key

    theme = clean_text(str(item.get("theme_guess", ""))) or "unknown-theme"
    entities = item.get("entities") or []
    first_entity = slugify(str(entities[0])) if entities else "unknown-entity"
    title = slugify(clean_text(str(item.get("title", ""))))[:40] or "untitled"
    published_at = clean_text(str(item.get("published_at", "")))[:10] or "unknown-date"
    return f"{first_entity}--{theme}--{published_at}--{title}"


def choose_event_title(items: List[Dict[str, object]]) -> str:
    ranked = sorted(
        items,
        key=lambda item: (
            len(item.get("entities") or []),
            len(clean_text(str(item.get("title", "")))),
        ),
        reverse=True,
    )
    return clean_text(str(ranked[0].get("title", ""))) if ranked else ""


def choose_theme(items: List[Dict[str, object]]) -> str:
    counts = defaultdict(int)
    for item in items:
        theme = clean_text(str(item.get("theme_guess", "")))
        if theme:
            counts[theme] += 1
    return max(counts, key=counts.get) if counts else ""


def merge_entities(items: Iterable[Dict[str, object]]) -> List[str]:
    merged = []
    seen = set()
    for item in items:
        for entity in item.get("entities") or []:
            if entity in seen:
                continue
            seen.add(entity)
            merged.append(entity)
    return merged


def build_summary(items: List[Dict[str, object]], theme: str) -> str:
    title = choose_event_title(items)
    count = len(items)
    if theme:
        return f"{title}。该事件当前汇总到 {count} 条原始新闻，主主题判断为“{theme}”。"
    return f"{title}。该事件当前汇总到 {count} 条原始新闻。"


def build_event(items: List[Dict[str, object]], key: str) -> Dict[str, object]:
    published_times = [parse_time(clean_text(str(item.get("published_at", "")))) for item in items]
    published_times = [item for item in published_times if item is not None]
    first_seen = min(published_times).astimezone(timezone.utc).isoformat().replace("+00:00", "Z") if published_times else ""
    last_seen = max(published_times).astimezone(timezone.utc).isoformat().replace("+00:00", "Z") if published_times else ""
    theme = choose_theme(items)
    title = choose_event_title(items)
    entities = merge_entities(items)

    return {
        "event_id": slugify(key)[:48] or "event",
        "event_key": key,
        "event_title": title,
        "summary": build_summary(items, theme),
        "theme": theme,
        "companies": entities,
        "products": [],
        "topics": [theme] if theme else [],
        "first_seen_at": first_seen,
        "last_seen_at": last_seen,
        "source_item_ids": [item.get("source_item_id") for item in items],
        "source_count": len(items),
        "status": "active",
    }


def build_events(source_items: List[Dict[str, object]]) -> Dict[str, object]:
    grouped = defaultdict(list)
    for item in source_items:
        grouped[group_key(item)].append(item)

    merged_groups: List[List[Dict[str, object]]] = []
    for items in grouped.values():
        for item in items:
            target_group = None
            for candidate_group in merged_groups:
                if any(should_merge(item, candidate) for candidate in candidate_group):
                    target_group = candidate_group
                    break
            if target_group is None:
                merged_groups.append([item])
            else:
                target_group.append(item)

    events = []
    for items in merged_groups:
        keys = [group_key(item) for item in items]
        chosen_key = min(keys, key=len)
        events.append(build_event(items, chosen_key))
    events.sort(key=lambda event: event.get("last_seen_at", ""), reverse=True)
    return {
        "total_events": len(events),
        "events": events,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build event candidates from source_item records.")
    parser.add_argument("--input", help="Path to source_item JSON. Reads stdin when omitted.")
    return parser.parse_args()


def read_payload(path: Optional[str]) -> object:
    if path:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.load(sys.stdin)


def main() -> int:
    args = parse_args()
    payload = read_payload(args.input)
    source_items = source_items_from_payload(payload)
    print(json.dumps(build_events(source_items), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
