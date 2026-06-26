from __future__ import annotations

import hashlib
import json
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from review_delivery_schema import (
    normalize_categories,
    normalize_focus_marks,
    normalize_sentiment,
    normalize_space,
    normalize_tags,
)


def dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


ALLOWED_CATEGORIES = [
    "Praise on product",
    "Questions/Worrying",
    "Negative emotions",
    "Suggestion",
    "Nothing particular",
    "Being supportive to the brand",
    "Expecting",
    "Being Sarcastic",
    "Competitor comparison",
    "Status update",
]

FOCUS_MARK_OPTIONS = [
    "性价比",
    "质量",
    "功能改进建议",
    "竞品/型号",
    "软件/设置",
    "安装/适配",
    "品牌/售后",
    "物流/包装",
    "配件/兼容性",
]

NESTED_RECORD_KEYS = (
    "machine",
    "delivery",
    "fields",
    "analysis",
    "semantic",
    "payload",
    "data",
    "row",
    "record",
)

LABEL_OUTPUT_KEYS = (
    "评论概括",
    "summary",
    "summary_cn",
    "情感倾向",
    "sentiment",
    "类别分类",
    "category",
    "categories",
    "标签",
    "tag",
    "tags",
    "tags_cn",
    "重点标记",
    "focus_mark",
    "focus_marks",
    "priority_mark",
)


def flatten_record(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {}

    flattened: dict[str, Any] = {}
    for nested_key in NESTED_RECORD_KEYS:
        nested = raw.get(nested_key)
        if isinstance(nested, dict):
            flattened.update(flatten_record(nested))

    for key, value in raw.items():
        if key in NESTED_RECORD_KEYS and isinstance(value, dict):
            continue
        flattened[key] = value

    return flattened


def first_nonempty(source: Any, *names: str) -> str:
    record = flatten_record(source)
    for name in names:
        value = normalize_space(record.get(name))
        if value:
            return value
    return ""


def has_semantic_output(source: Any) -> bool:
    record = flatten_record(source)
    return any(normalize_space(record.get(key)) for key in LABEL_OUTPUT_KEYS)


def normalize_text_for_cache(text: Any) -> str:
    value = normalize_space(text).lower()
    value = re.sub(r"\s+", " ", value)
    return value


def build_cache_key(review_id: Any, review_text: Any, taxonomy_version: str) -> str:
    raw = f"{normalize_space(review_id)}\n{normalize_text_for_cache(review_text)}\n{normalize_space(taxonomy_version)}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def default_cache_path(output_dir: Path) -> Path:
    return output_dir.expanduser() / "label_cache.jsonl"


def load_cache(path: Path, *, ttl_hours: float = 0) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    mapping: dict[str, dict[str, Any]] = {}
    cutoff = time.time() - (ttl_hours * 3600) if ttl_hours > 0 else 0
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(item, dict) or not item.get("cache_key"):
            continue
        if cutoff > 0:
            cached_at = item.get("cached_at", 0)
            if isinstance(cached_at, (int, float)) and cached_at < cutoff:
                continue
        mapping[str(item["cache_key"])] = item
    return mapping


def save_cache(path: Path, entries: dict[str, dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(entries[key], ensure_ascii=False) for key in sorted(entries)]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def heuristic_sentiment(review_text: str, rating: str) -> tuple[str | None, bool]:
    text = normalize_text_for_cache(review_text)
    try:
        numeric_rating = float(rating) if rating else None
    except ValueError:
        numeric_rating = None

    positive_tokens = (
        "great",
        "excellent",
        "love",
        "perfect",
        "amazing",
        "good",
        "fantastic",
        "easy",
        "recommend",
    )
    negative_tokens = (
        "bad",
        "poor",
        "terrible",
        "worst",
        "awful",
        "broken",
        "refund",
        "problem",
        "issue",
        "disappointed",
    )
    suggestion_tokens = ("should", "wish", "suggest", "could", "希望", "建议", "改进")

    if numeric_rating is not None:
        if (
            numeric_rating >= 4.5
            and any(token in text for token in positive_tokens)
            and not any(token in text for token in negative_tokens)
        ):
            return "Positive", True
        if numeric_rating <= 2.5 and any(token in text for token in negative_tokens):
            return "Negative", True
        if numeric_rating == 3 and any(token in text for token in suggestion_tokens):
            return "Neutral", False
    return None, False


def heuristic_category(review_text: str, rating: str) -> tuple[str | None, bool]:
    text = normalize_text_for_cache(review_text)
    if "?" in review_text or any(
        token in text
        for token in ("anyone", "wonder", "question", "how do", "can i", "whether")
    ):
        return "Questions/Worrying", True
    if any(
        token in text for token in ("should", "wish", "suggest", "希望", "建议", "改进")
    ):
        return "Suggestion", True
    if any(
        token in text
        for token in ("competitor", "vs ", "compared", "better than", "比", "型号")
    ):
        return "Competitor comparison", True
    sentiment, confident = heuristic_sentiment(review_text, rating)
    if confident and sentiment == "Positive":
        return "Praise on product", True
    if confident and sentiment == "Negative":
        return "Negative emotions", True
    return None, False


def heuristic_focus_marks(
    review_text: str, translated_text: str = ""
) -> tuple[str, bool]:
    text = normalize_text_for_cache(" ".join([review_text, translated_text]))
    marks: list[str] = []
    if any(
        token in text for token in ("price", "value", "worth", "性价比", "贵", "便宜")
    ):
        marks.append("性价比")
    if any(token in text for token in ("quality", "durable", "build", "质量", "做工")):
        marks.append("质量")
    if any(
        token in text for token in ("suggest", "should", "wish", "希望", "建议", "改进")
    ):
        marks.append("功能改进建议")
    if any(token in text for token in ("compare", "vs", "competitor", "型号", "竞品")):
        marks.append("竞品/型号")
    if any(token in text for token in ("app", "software", "setup", "设置", "软件")):
        marks.append("软件/设置")
    if any(token in text for token in ("install", "fit", "mount", "安装", "适配")):
        marks.append("安装/适配")
    if any(
        token in text
        for token in ("support", "service", "brand", "售后", "客服", "品牌")
    ):
        marks.append("品牌/售后")
    if any(
        token in text for token in ("delivery", "package", "packaging", "物流", "包装")
    ):
        marks.append("物流/包装")
    if any(
        token in text
        for token in ("accessory", "compatible", "compatibility", "配件", "兼容")
    ):
        marks.append("配件/兼容性")
    return "；".join(dict.fromkeys(marks)), bool(marks)


def lightweight_row(record: dict[str, Any]) -> dict[str, Any]:
    record = flatten_record(record)
    review_text = first_nonempty(
        record,
        "评论原文",
        "review_text",
        "body",
        "content",
        "review_body",
        "title",
        "review_title",
    )
    translated = first_nonempty(
        record, "评论中文版", "translated_text", "translated_cn"
    )
    rating = first_nonempty(record, "星级评分", "rating", "star_rating", "rating_text")
    sentiment, sentiment_confident = heuristic_sentiment(review_text, rating)
    category, category_confident = heuristic_category(review_text, rating)
    focus_marks, focus_confident = heuristic_focus_marks(review_text, translated)
    return {
        "seq": first_nonempty(record, "序号", "seq", "index"),
        "review_id": first_nonempty(record, "review_id", "reviewId"),
        "review_text": review_text,
        "translated_text": translated,
        "rating": rating,
        "country": first_nonempty(
            record, "国家", "country", "country_cn", "region", "market"
        ),
        "prefilled_sentiment": sentiment or "",
        "prefilled_category": category or "",
        "prefilled_focus_marks": focus_marks,
        "heuristic_confidence": {
            "sentiment": sentiment_confident,
            "category": category_confident,
            "focus_marks": focus_confident,
        },
    }


def load_canonical_tags(path: Path | None) -> list[str]:
    if path is None or not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return dedupe_preserve_order(
            [normalize_space(item) for item in payload if normalize_space(item)]
        )
    if isinstance(payload, dict):
        values = payload.get("canonical_tags") or payload.get("tags") or []
        if isinstance(values, list):
            return dedupe_preserve_order(
                [normalize_space(item) for item in values if normalize_space(item)]
            )
    return []


def prepare_tagging_payload(
    records: list[dict[str, Any]],
    *,
    taxonomy_version: str,
    cache_entries: dict[str, dict[str, Any]],
    canonical_tags: list[str],
) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    cached_rows: list[dict[str, Any]] = []
    for record in records:
        record = flatten_record(record)
        seq = first_nonempty(record, "序号", "seq", "index")
        review_id = first_nonempty(record, "review_id", "reviewId")
        review_text = first_nonempty(
            record,
            "评论原文",
            "review_text",
            "body",
            "content",
            "review_body",
            "title",
            "review_title",
        )
        cache_key = build_cache_key(review_id or seq, review_text, taxonomy_version)
        cached = cache_entries.get(cache_key)
        if cached:
            cached_rows.append(
                {
                    "seq": seq,
                    "review_id": review_id,
                    "cache_key": cache_key,
                }
            )
            continue

        item = lightweight_row(record)
        item["cache_key"] = cache_key
        item["allowed_categories"] = ALLOWED_CATEGORIES
        item["allowed_focus_marks"] = FOCUS_MARK_OPTIONS
        item["canonical_tags"] = canonical_tags
        items.append(item)

    return {
        "metadata": {
            "taxonomy_version": taxonomy_version,
            "total_rows": len(records),
            "pending_rows": len(items),
            "cached_rows": len(cached_rows),
        },
        "allowed_categories": ALLOWED_CATEGORIES,
        "allowed_focus_marks": FOCUS_MARK_OPTIONS,
        "canonical_tags": canonical_tags,
        "items": items,
        "cached_rows": cached_rows,
    }


def representative_sample(
    records: list[dict[str, Any]], sample_size: int
) -> list[dict[str, Any]]:
    records = [flatten_record(record) for record in records]
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        rating = (
            first_nonempty(record, "星级评分", "rating", "star_rating", "rating_text")
            or "unknown"
        )
        buckets[rating].append(record)

    sample: list[dict[str, Any]] = []
    for bucket in sorted(buckets):
        rows = sorted(
            buckets[bucket],
            key=lambda item: len(
                first_nonempty(
                    item,
                    "评论原文",
                    "review_text",
                    "body",
                    "content",
                    "review_body",
                    "title",
                    "review_title",
                )
            ),
            reverse=True,
        )
        if rows:
            sample.append(rows[0])

    if len(sample) >= sample_size:
        return sample[:sample_size]

    remaining = [row for row in records if row not in sample]
    remaining = sorted(
        remaining,
        key=lambda item: len(
            first_nonempty(
                item,
                "评论原文",
                "review_text",
                "body",
                "content",
                "review_body",
                "title",
                "review_title",
            )
        ),
        reverse=True,
    )
    for row in remaining:
        if len(sample) >= sample_size:
            break
        sample.append(row)
    return sample


def seed_tags(records: list[dict[str, Any]], limit: int = 20) -> list[str]:
    counter: Counter[str] = Counter()
    for record in records:
        record = flatten_record(record)
        text = normalize_text_for_cache(
            first_nonempty(
                record,
                "评论原文",
                "review_text",
                "body",
                "content",
                "review_body",
                "title",
                "review_title",
            )
        )
        for token in re.findall(r"[a-z]{4,}", text):
            if token in {
                "this",
                "that",
                "with",
                "have",
                "been",
                "very",
                "easy",
                "good",
            }:
                continue
            counter[token] += 1
    return [token for token, _ in counter.most_common(limit)]


def build_taxonomy_bootstrap(
    records: list[dict[str, Any]],
    *,
    taxonomy_version: str,
    sample_size: int,
) -> dict[str, Any]:
    records = [flatten_record(record) for record in records]
    sample = representative_sample(records, sample_size)
    sample_rows = []
    for record in sample:
        sample_rows.append(
            {
                "seq": first_nonempty(record, "序号", "seq", "index"),
                "review_id": first_nonempty(record, "review_id", "reviewId"),
                "review_text": first_nonempty(
                    record,
                    "评论原文",
                    "review_text",
                    "body",
                    "content",
                    "review_body",
                    "title",
                    "review_title",
                ),
                "translated_text": first_nonempty(
                    record, "评论中文版", "translated_text", "translated_cn"
                ),
                "rating": first_nonempty(
                    record, "星级评分", "rating", "star_rating", "rating_text"
                ),
                "country": first_nonempty(
                    record, "国家", "country", "country_cn", "region", "market"
                ),
            }
        )
    return {
        "metadata": {
            "taxonomy_version": taxonomy_version,
            "sample_size": len(sample_rows),
            "source_rows": len(records),
        },
        "allowed_categories": ALLOWED_CATEGORIES,
        "allowed_focus_marks": FOCUS_MARK_OPTIONS,
        "suggested_seed_tags": seed_tags(sample),
        "sample_rows": sample_rows,
        "instructions": {
            "goal": "Read sample_rows and produce a canonical tag vocabulary for this batch.",
            "output": "Write canonical_tags as a short stable Chinese tag list, then use it in prepare-tagging output.",
        },
    }


def parse_labels_payload(payload: Any) -> dict[str, dict[str, Any]]:
    if isinstance(payload, dict):
        items = payload.get("items") if isinstance(payload.get("items"), list) else None
        if items is None:
            items = (
                payload.get("labels")
                if isinstance(payload.get("labels"), list)
                else None
            )
        if items is None:
            items = (
                payload.get("rows") if isinstance(payload.get("rows"), list) else None
            )
        if items is None:
            items = (
                payload.get("records")
                if isinstance(payload.get("records"), list)
                else None
            )
        if items is None:
            items = [payload]
    elif isinstance(payload, list):
        items = payload
    else:
        items = []

    mapping: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        item = flatten_record(item)
        if not has_semantic_output(item):
            continue
        seq = first_nonempty(item, "seq", "序号", "index")
        review_id = first_nonempty(item, "review_id", "reviewId")
        key = review_id or seq
        if key:
            mapping[key] = item
    return mapping


def merged_semantic_fields(source: dict[str, Any]) -> dict[str, str]:
    source = flatten_record(source)
    return {
        "评论中文版": normalize_space(
            source.get("评论中文版")
            or source.get("translated_text")
            or source.get("translated_cn")
        ),
        "评论概括": normalize_space(
            source.get("评论概括") or source.get("summary") or source.get("summary_cn")
        ),
        "情感倾向": normalize_sentiment(
            source.get("情感倾向") or source.get("sentiment")
        ),
        "类别分类": normalize_categories(
            source.get("类别分类") or source.get("category") or source.get("categories")
        ),
        "标签": normalize_tags(
            source.get("标签")
            or source.get("tag")
            or source.get("tags")
            or source.get("tags_cn")
        ),
        "重点标记": normalize_focus_marks(
            source.get("重点标记")
            or source.get("focus_marks")
            or source.get("focus_mark")
        ),
    }


def combine_semantic_fields(
    base: dict[str, Any], override: dict[str, Any]
) -> dict[str, str]:
    base_fields = merged_semantic_fields(base)
    override_fields = merged_semantic_fields(override)
    combined: dict[str, str] = {}
    for key, base_value in base_fields.items():
        combined[key] = override_fields.get(key) or base_value
    return combined


def merge_records_with_labels(
    base_records: list[dict[str, Any]],
    *,
    labels_payload: Any,
    taxonomy_version: str,
    cache_entries: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, int]]:
    label_mapping = parse_labels_payload(labels_payload)
    merged: list[dict[str, Any]] = []
    updated_cache = dict(cache_entries)
    stats = {"cache_hits": 0, "label_hits": 0, "unresolved": 0}

    for record in base_records:
        row = flatten_record(record)
        seq = first_nonempty(row, "序号", "seq", "index")
        review_id = first_nonempty(row, "review_id", "reviewId")
        review_text = first_nonempty(
            row,
            "评论原文",
            "review_text",
            "body",
            "content",
            "review_body",
            "title",
            "review_title",
        )
        cache_key = build_cache_key(review_id or seq, review_text, taxonomy_version)
        source = None
        if review_id and review_id in label_mapping:
            source = label_mapping[review_id]
            stats["label_hits"] += 1
        elif seq and seq in label_mapping:
            source = label_mapping[seq]
            stats["label_hits"] += 1
        elif cache_key in cache_entries:
            source = cache_entries[cache_key].get("fields")
            stats["cache_hits"] += 1

        if source:
            combined_fields = combine_semantic_fields(row, source)
            row.update(combined_fields)
            updated_cache[cache_key] = {
                "cache_key": cache_key,
                "taxonomy_version": taxonomy_version,
                "review_id": review_id,
                "cached_at": time.time(),
                "fields": combined_fields,
            }
        else:
            stats["unresolved"] += 1
        merged.append(row)

    return merged, updated_cache, stats
