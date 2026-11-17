#!/usr/bin/env python3
"""Plan, fetch, normalize, prepare, validate, and render Amazon review reports."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from reveyes_client import DEFAULT_BASE_URL, ReveyesClient, ReveyesError, load_api_key


SCHEMA_VERSION = 1
STAR_FILTERS = ["one_star", "two_star", "three_star", "four_star", "five_star"]
FILTER_STAR_CHOICES = [
    "all_stars",
    *STAR_FILTERS,
    "positive",
    "critical",
]
DEFAULT_FILTERS = {
    "filter_star": "all_stars",
    "filter_sort_by": "recent",
    "filter_reviewer_type": "all_reviews",
    "filter_media_type": "all_contents",
    "filter_variant": "all_formats",
}


def _star_specs(pages: int) -> list[dict[str, Any]]:
    labels = {
        "one_star": "1 星评论",
        "two_star": "2 星评论",
        "three_star": "3 星评论",
        "four_star": "4 星评论",
        "five_star": "5 星评论",
    }
    return [
        {
            "id": star.replace("_star", "-star"),
            "label": labels[star],
            "purpose": "按星级比较主题、情绪和体验差异",
            "pages": pages,
            "filter_star": star,
        }
        for star in STAR_FILTERS
    ]


SCENARIOS: dict[str, dict[str, Any]] = {
    "quick": {
        "label": "快速口碑概览",
        "description": "用近期综合评论快速了解产品现状。",
        "specs": [
            {
                "id": "recent-overview",
                "label": "近期综合评论",
                "purpose": "快速了解近期样本中的星级、主题和情绪",
                "pages": 3,
                "filter_star": "all_stars",
            }
        ],
    },
    "health": {
        "label": "产品健康诊断",
        "description": "结合近期综合样本与近期差评，兼顾概览和问题发现。",
        "specs": [
            {
                "id": "recent-overview",
                "label": "近期综合评论",
                "purpose": "建立近期基线样本",
                "pages": 5,
                "filter_star": "all_stars",
            },
            {
                "id": "recent-critical",
                "label": "近期差评",
                "purpose": "扩大产品问题和退货风险的发现范围",
                "pages": 5,
                "filter_star": "critical",
            },
        ],
    },
    "pain-points": {
        "label": "质量问题与退货原因",
        "description": "重点分析 1～3 星评论中的故障、落差和售后问题。",
        "specs": [
            {**_star_specs(10)[0], "purpose": "识别严重故障和强烈不满"},
            {**_star_specs(10)[1], "purpose": "识别明显缺陷和退货诱因"},
            {**_star_specs(5)[2], "purpose": "识别可改进但未完全失败的体验"},
        ],
    },
    "selling-points": {
        "label": "卖点与用户语言",
        "description": "从 4～5 星评论提炼购买动机、使用场景和营销表达。",
        "specs": [
            {**_star_specs(5)[3], "purpose": "识别满意但仍有保留的体验"},
            {**_star_specs(10)[4], "purpose": "提炼强购买驱动、核心卖点和用户原话"},
        ],
    },
    "listing": {
        "label": "Listing 优化",
        "description": "均匀抽取五个星级，寻找预期差、卖点和常见疑问。",
        "specs": _star_specs(5),
    },
    "media": {
        "label": "图片与实物缺陷分析",
        "description": "聚焦带图片或视频的差评，提取可视化缺陷证据。",
        "specs": [
            {
                "id": "critical-media",
                "label": "带媒体的差评",
                "purpose": "识别包装、破损、做工和实物不符等可视化问题",
                "pages": 10,
                "filter_star": "critical",
                "filter_media_type": "media_reviews_only",
            }
        ],
    },
    "competitor": {
        "label": "多 ASIN 竞品对比",
        "description": "每个 ASIN、每个星级抽取 2 页，控制横向比较成本。",
        "specs": _star_specs(2),
    },
    "deep": {
        "label": "最深度完整分析",
        "description": "1～5 星每个星级抓取 10 页，生成完整分层分析。",
        "specs": _star_specs(10),
    },
}


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def fingerprint(value: Any) -> str:
    return hashlib.sha256(json_bytes(value)).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def display_number(value: float | int) -> float | int:
    number = float(value)
    return int(number) if number.is_integer() else round(number, 4)


def validate_asin(asin: str) -> str:
    normalized = asin.strip().upper()
    if not re.fullmatch(r"[A-Z0-9]{10}", normalized):
        raise ValueError(f"无效 ASIN: {asin!r}（应为 10 位字母或数字）")
    return normalized


def safe_slug(value: str, *, fallback: str = "run") -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-._").lower()
    return slug or fallback


def build_plan(
    *,
    asins: list[str],
    marketplace: str,
    scenario: str,
    points_per_page: float,
    pages_override: int | None = None,
    sort_by: str | None = None,
    reviewer_type: str = "all_reviews",
    media_type: str = "all_contents",
    variant: str = "all_formats",
    custom_filter_star: str | None = None,
    report_language: str = "zh-CN",
    report_title: str | None = None,
) -> dict[str, Any]:
    normalized_asins = list(dict.fromkeys(validate_asin(asin) for asin in asins))
    if not normalized_asins:
        raise ValueError("至少需要一个 ASIN")
    marketplace = marketplace.strip().upper()
    if not re.fullmatch(r"[A-Z]{2,5}", marketplace):
        raise ValueError(f"无效 marketplace: {marketplace!r}")
    if points_per_page <= 0:
        raise ValueError("每页积分必须大于 0")
    if pages_override is not None and not 1 <= pages_override <= 10:
        raise ValueError("--pages 必须在 1～10 之间")

    if scenario == "custom":
        if custom_filter_star not in FILTER_STAR_CHOICES:
            raise ValueError("custom 场景必须提供有效的 --filter-star")
        specs = [
            {
                "id": safe_slug(custom_filter_star),
                "label": f"自定义 {custom_filter_star}",
                "purpose": "执行用户明确指定的评论采样",
                "pages": pages_override or 1,
                "filter_star": custom_filter_star,
            }
        ]
        scenario_meta = {
            "label": "自定义采样",
            "description": "按用户明确指定的过滤条件采样。",
        }
    else:
        if scenario not in SCENARIOS:
            raise ValueError(f"未知场景: {scenario}")
        scenario_meta = SCENARIOS[scenario]
        specs = [dict(spec) for spec in scenario_meta["specs"]]

    requests: list[dict[str, Any]] = []
    for spec in specs:
        pages = pages_override or int(spec["pages"])
        filters = dict(DEFAULT_FILTERS)
        filters.update(
            {
                "filter_star": spec.get("filter_star", "all_stars"),
                "filter_sort_by": sort_by or spec.get("filter_sort_by", "recent"),
                "filter_reviewer_type": reviewer_type,
                "filter_media_type": spec.get("filter_media_type", media_type),
                "filter_variant": variant,
            }
        )
        items = [
            {
                "asin": asin,
                "marketplace": marketplace,
                "pages": pages,
                **filters,
            }
            for asin in normalized_asins
        ]
        request_payload = {"asins": items}
        requested_pages = pages * len(items)
        requests.append(
            {
                "id": spec["id"],
                "label": spec["label"],
                "purpose": spec["purpose"],
                "requested_pages": requested_pages,
                "estimated_max_points": display_number(requested_pages * points_per_page),
                "request_fingerprint": fingerprint(request_payload),
                "payload": request_payload,
            }
        )

    total_pages = sum(int(request["requested_pages"]) for request in requests)
    plan = {
        "schema_version": SCHEMA_VERSION,
        "created_at": now_iso(),
        "scenario": scenario,
        "scenario_label": scenario_meta["label"],
        "scenario_description": scenario_meta["description"],
        "asins": normalized_asins,
        "marketplace": marketplace,
        "report_language": report_language,
        "report_title": report_title,
        "points_per_page_at_plan": display_number(points_per_page),
        "requested_pages": total_pages,
        "estimated_max_points": display_number(total_pages * points_per_page),
        "sampling_notice": (
            "这是有意设计的评论样本。分星级样本不得合并推断商品真实星级分布；"
            "只有获得外部真实星级权重时才能计算总体加权比例。"
        ),
        "requests": requests,
    }
    plan["plan_fingerprint"] = fingerprint({key: value for key, value in plan.items() if key != "created_at"})
    return plan


def create_run_dir(output_root: Path, *, scenario: str, asins: list[str], explicit: str | None = None) -> Path:
    if explicit:
        run_dir = Path(explicit).expanduser().resolve()
        if run_dir.exists() and any(run_dir.iterdir()):
            raise ValueError(f"运行目录已存在且非空: {run_dir}")
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir
    output_root = output_root.expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    asin_part = "-".join(asins[:3]) if asins else "task"
    base = safe_slug(f"{timestamp}-{scenario}-{asin_part}")
    candidate = output_root / base
    counter = 2
    while candidate.exists():
        candidate = output_root / f"{base}-{counter}"
        counter += 1
    candidate.mkdir(parents=True)
    return candidate


def load_reviews(path: Path) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number} 不是有效 JSON") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number} 必须是 JSON 对象")
        reviews.append(value)
    return reviews


def write_reviews(path: Path, reviews: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for review in reviews:
            handle.write(json.dumps(review, ensure_ascii=False, separators=(",", ":")) + "\n")
    temporary.replace(path)


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _as_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def normalize_results(
    raw_results: list[tuple[dict[str, Any], dict[str, Any], str]],
) -> list[dict[str, Any]]:
    """Normalize result rows and merge duplicate review IDs while retaining provenance."""
    merged: dict[str, dict[str, Any]] = {}
    for request_entry, result, task_id in raw_results:
        rows = result.get("data", {}).get("reviews", {}).get("data", [])
        if not isinstance(rows, list):
            raise ValueError(f"任务 {task_id} 的评论数据不是数组")
        requested_items = request_entry.get("payload", {}).get("asins", [])
        by_asin = {item.get("asin"): item for item in requested_items if isinstance(item, dict)}
        for raw in rows:
            if not isinstance(raw, dict):
                continue
            asin = _as_text(raw.get("asin")).upper()
            marketplace = _as_text(raw.get("marketplace")).upper()
            review_id = _as_text(raw.get("review_id"))
            if not review_id:
                review_id = "generated-" + fingerprint(
                    [asin, marketplace, raw.get("title"), raw.get("review_date"), raw.get("review_content")]
                )[:20]
            source_filter = by_asin.get(asin, {})
            source = {
                "request_id": request_entry.get("id"),
                "label": request_entry.get("label"),
                "task_id": str(task_id),
                "filter_star": source_filter.get("filter_star", "unknown"),
                "filter_sort_by": source_filter.get("filter_sort_by", "unknown"),
                "filter_reviewer_type": source_filter.get("filter_reviewer_type", "unknown"),
                "filter_media_type": source_filter.get("filter_media_type", "unknown"),
                "filter_variant": source_filter.get("filter_variant", "unknown"),
                "page": _as_int(raw.get("page"), 0),
            }
            normalized = {
                "asin": asin,
                "marketplace": marketplace,
                "review_id": review_id,
                "user_name": _as_text(raw.get("user_name")),
                "profile_url": _as_text(raw.get("profile_url")),
                "rating": max(1, min(5, _as_int(raw.get("rating"), 0))),
                "title": _as_text(raw.get("title")),
                "review_date": _as_text(raw.get("review_date")),
                "review_content": _as_text(raw.get("review_content")),
                "verified_purchase": 1 if _as_int(raw.get("verified_purchase")) else 0,
                "helpful_votes": max(0, _as_int(raw.get("helpful_votes"))),
                "product_variant": _as_text(raw.get("product_variant")),
                "images": _as_string_list(raw.get("images")),
                "videos": _as_string_list(raw.get("videos")),
                "sources": [source],
            }
            key = f"{marketplace}:{asin}:{review_id}"
            if key not in merged:
                merged[key] = normalized
                continue
            existing = merged[key]
            existing_source_ids = {
                (item.get("request_id"), item.get("task_id"), item.get("page"))
                for item in existing["sources"]
            }
            source_id = (source.get("request_id"), source.get("task_id"), source.get("page"))
            if source_id not in existing_source_ids:
                existing["sources"].append(source)
            existing["verified_purchase"] = max(existing["verified_purchase"], normalized["verified_purchase"])
            existing["helpful_votes"] = max(existing["helpful_votes"], normalized["helpful_votes"])
            existing["images"] = list(dict.fromkeys(existing["images"] + normalized["images"]))
            existing["videos"] = list(dict.fromkeys(existing["videos"] + normalized["videos"]))
            for field in ("title", "review_content", "product_variant", "review_date", "user_name", "profile_url"):
                if len(str(normalized[field])) > len(str(existing[field])):
                    existing[field] = normalized[field]

    reviews = list(merged.values())
    reviews.sort(key=lambda review: (review["asin"], review["rating"], review["review_id"]))
    return reviews


def _year_from_review_date(value: str) -> str | None:
    matches = re.findall(r"\b(20\d{2})\b", value or "")
    return matches[-1] if matches else None


def compute_statistics(reviews: list[dict[str, Any]], manifest: dict[str, Any]) -> dict[str, Any]:
    rating_counts = Counter(str(review.get("rating")) for review in reviews)
    total = len(reviews)
    ratings = [int(review["rating"]) for review in reviews if review.get("rating")]
    helpful_values = [int(review.get("helpful_votes", 0)) for review in reviews]
    verified = sum(int(review.get("verified_purchase", 0)) for review in reviews)
    media_reviews = sum(bool(review.get("images") or review.get("videos")) for review in reviews)
    variants = Counter(review.get("product_variant") or "未标注规格" for review in reviews)
    years = Counter(
        year
        for year in (_year_from_review_date(str(review.get("review_date", ""))) for review in reviews)
        if year
    )

    by_asin: dict[str, Any] = {}
    for asin in sorted({review.get("asin", "") for review in reviews}):
        subset = [review for review in reviews if review.get("asin") == asin]
        subset_ratings = [int(review["rating"]) for review in subset if review.get("rating")]
        by_asin[asin] = {
            "reviews": len(subset),
            "sample_average_rating": round(statistics.fmean(subset_ratings), 3) if subset_ratings else None,
            "rating_counts": {str(star): sum(review.get("rating") == star for review in subset) for star in range(1, 6)},
            "verified_reviews": sum(int(review.get("verified_purchase", 0)) for review in subset),
            "media_reviews": sum(bool(review.get("images") or review.get("videos")) for review in subset),
        }

    source_counts: dict[str, set[str]] = defaultdict(set)
    for review in reviews:
        for source in review.get("sources", []):
            source_counts[str(source.get("request_id", "unknown"))].add(review["review_id"])

    tasks = manifest.get("tasks", [])
    actual_pages = 0
    pre_deduct = 0.0
    actual_deduct = 0.0
    for task in tasks:
        pre_deduct += float(task.get("pre_deduct") or 0)
        actual_deduct += float(task.get("actual_deduct") or 0)
        actual_pages += sum(_as_int(item.get("actual_pages")) for item in task.get("items_summary", []))

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": now_iso(),
        "sample_notice": manifest.get("plan", {}).get("sampling_notice"),
        "unique_reviews": total,
        "sample_average_rating": round(statistics.fmean(ratings), 3) if ratings else None,
        "rating_counts": {str(star): rating_counts.get(str(star), 0) for star in range(1, 6)},
        "verified_reviews": verified,
        "verified_rate": round(verified / total, 4) if total else 0,
        "media_reviews": media_reviews,
        "media_rate": round(media_reviews / total, 4) if total else 0,
        "helpful_votes_total": sum(helpful_values),
        "helpful_votes_median": statistics.median(helpful_values) if helpful_values else 0,
        "requested_pages": manifest.get("plan", {}).get("requested_pages"),
        "actual_pages": actual_pages,
        "pre_deduct": display_number(pre_deduct),
        "actual_deduct": display_number(actual_deduct),
        "source_unique_reviews": {key: len(value) for key, value in sorted(source_counts.items())},
        "top_variants": [{"variant": name, "reviews": count} for name, count in variants.most_common(20)],
        "review_year_counts": dict(sorted(years.items())),
        "by_asin": by_asin,
    }


def _analysis_review(review: dict[str, Any]) -> dict[str, Any]:
    return {
        "review_id": review["review_id"],
        "asin": review["asin"],
        "marketplace": review["marketplace"],
        "rating": review["rating"],
        "title": review["title"],
        "review_date": review["review_date"],
        "review_content": review["review_content"],
        "verified_purchase": review["verified_purchase"],
        "helpful_votes": review["helpful_votes"],
        "product_variant": review["product_variant"],
        "image_count": len(review.get("images", [])),
        "video_count": len(review.get("videos", [])),
        "source_filters": [
            {
                "request_id": source.get("request_id"),
                "filter_star": source.get("filter_star"),
                "filter_sort_by": source.get("filter_sort_by"),
                "filter_media_type": source.get("filter_media_type"),
            }
            for source in review.get("sources", [])
        ],
    }


def prepare_analysis(
    run_dir: Path,
    *,
    max_reviews_per_batch: int = 35,
    max_chars_per_batch: int = 24000,
) -> dict[str, Any]:
    reviews = load_reviews(run_dir / "reviews.jsonl")
    manifest = read_json(run_dir / "manifest.json")
    stats_path = run_dir / "statistics.json"
    stats = read_json(stats_path) if stats_path.exists() else compute_statistics(reviews, manifest)
    write_json(stats_path, stats)

    analysis_dir = run_dir / "analysis"
    batches_dir = analysis_dir / "batches"
    batches_dir.mkdir(parents=True, exist_ok=True)
    grouped: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for review in reviews:
        grouped[(review.get("asin", "unknown"), int(review.get("rating", 0)))].append(review)

    batch_entries: list[dict[str, Any]] = []
    for (asin, rating), group in sorted(grouped.items()):
        current: list[dict[str, Any]] = []
        current_chars = 0
        part = 1
        for review in group:
            prepared = _analysis_review(review)
            size = len(prepared["title"]) + len(prepared["review_content"]) + 200
            if current and (len(current) >= max_reviews_per_batch or current_chars + size > max_chars_per_batch):
                batch_entries.append(_write_batch(batches_dir, asin, rating, part, current, manifest))
                part += 1
                current = []
                current_chars = 0
            current.append(prepared)
            current_chars += size
        if current:
            batch_entries.append(_write_batch(batches_dir, asin, rating, part, current, manifest))

    index = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": now_iso(),
        "scenario": manifest.get("plan", {}).get("scenario"),
        "scenario_label": manifest.get("plan", {}).get("scenario_label"),
        "report_language": manifest.get("plan", {}).get("report_language", "zh-CN"),
        "review_count": len(reviews),
        "batch_count": len(batch_entries),
        "statistics_path": "../statistics.json",
        "constraints": [
            "只根据批次中的评论形成结论，不补充评论中不存在的产品事实。",
            "任何主题、洞察和建议都必须绑定有效 review_id。",
            "引用必须是对应评论标题或正文中的连续原文，不得改写后放入 quote。",
            "按星级抓取的分层样本不能用于推断商品真实总体星级比例。",
            "区分基线样本和定向样本，不把定向差评样本的占比表述为总体买家占比。",
        ],
        "batches": batch_entries,
    }
    write_json(analysis_dir / "index.json", index)
    template_path = analysis_dir / "final-analysis.template.json"
    if not template_path.exists():
        write_json(template_path, final_analysis_template(manifest, stats))
    return index


def _write_batch(
    batches_dir: Path,
    asin: str,
    rating: int,
    part: int,
    reviews: list[dict[str, Any]],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    batch_id = safe_slug(f"{asin}-{rating}-star-{part:02d}")
    path = batches_dir / f"{batch_id}.json"
    payload = {
        "schema_version": SCHEMA_VERSION,
        "batch_id": batch_id,
        "asin": asin,
        "rating": rating,
        "scenario": manifest.get("plan", {}).get("scenario"),
        "reviews": reviews,
    }
    write_json(path, payload)
    return {
        "batch_id": batch_id,
        "asin": asin,
        "rating": rating,
        "review_count": len(reviews),
        "path": f"batches/{path.name}",
    }


def final_analysis_template(manifest: dict[str, Any], stats: dict[str, Any]) -> dict[str, Any]:
    plan = manifest.get("plan", {})
    default_title = plan.get("report_title") or f"Amazon 评论分析：{', '.join(plan.get('asins', []))}"
    return {
        "schema_version": SCHEMA_VERSION,
        "language": plan.get("report_language", "zh-CN"),
        "report_title": default_title,
        "executive_summary": [],
        "themes": [],
        "pain_points": [],
        "positive_drivers": [],
        "use_cases": [],
        "listing_gaps": [],
        "recommendations": [],
        "competitor_comparison": [],
        "limitations": [
            stats.get("sample_notice")
            or "本报告基于有限、定向抽取的评论样本，不代表全部购买者。"
        ],
    }


def _all_review_id_values(value: Any, path: str = "$") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key == "review_id" and isinstance(child, str):
                yield child_path, child
            elif key == "review_ids" or key.endswith("_review_ids"):
                if isinstance(child, list):
                    for index, item in enumerate(child):
                        if isinstance(item, str):
                            yield f"{child_path}[{index}]", item
            yield from _all_review_id_values(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _all_review_id_values(child, f"{path}[{index}]")


def _normalize_quote(value: str) -> str:
    value = value.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", value).strip().casefold()


def validate_analysis(run_dir: Path, analysis_path: Path) -> dict[str, Any]:
    analysis = read_json(analysis_path)
    reviews = load_reviews(run_dir / "reviews.jsonl")
    review_map = {review["review_id"]: review for review in reviews}
    errors: list[str] = []
    warnings: list[str] = []

    required_types = {
        "report_title": str,
        "executive_summary": list,
        "themes": list,
        "pain_points": list,
        "positive_drivers": list,
        "use_cases": list,
        "listing_gaps": list,
        "recommendations": list,
        "limitations": list,
    }
    if not isinstance(analysis, dict):
        errors.append("分析文件顶层必须是 JSON 对象")
    else:
        for key, expected in required_types.items():
            if key not in analysis:
                errors.append(f"缺少必填字段: {key}")
            elif not isinstance(analysis[key], expected):
                errors.append(f"字段 {key} 必须是 {expected.__name__}")

    if isinstance(analysis, dict):
        for path, review_id in _all_review_id_values(analysis):
            if review_id not in review_map:
                errors.append(f"{path} 引用了不存在的 review_id: {review_id}")

        theme_ids: set[str] = set()
        for index, theme in enumerate(analysis.get("themes", [])):
            path = f"$.themes[{index}]"
            if not isinstance(theme, dict):
                errors.append(f"{path} 必须是对象")
                continue
            theme_id = theme.get("id")
            if not isinstance(theme_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", theme_id):
                errors.append(f"{path}.id 必须是小写英文、数字和连字符组成的稳定 ID")
            elif theme_id in theme_ids:
                errors.append(f"重复主题 ID: {theme_id}")
            else:
                theme_ids.add(theme_id)
            ids = theme.get("review_ids", [])
            if not isinstance(ids, list) or not ids:
                warnings.append(f"{path} 没有 review_ids，将无法展示可信提及量")
            elif len(ids) != len(set(ids)):
                errors.append(f"{path}.review_ids 含重复值")
            for subset_key in ("positive_review_ids", "negative_review_ids", "mixed_review_ids", "neutral_review_ids"):
                subset = theme.get(subset_key, [])
                if subset and (not isinstance(subset, list) or not set(subset).issubset(set(ids))):
                    errors.append(f"{path}.{subset_key} 必须是 review_ids 的子集")
            severity = theme.get("severity")
            if severity is not None and (not isinstance(severity, (int, float)) or not 1 <= severity <= 5):
                errors.append(f"{path}.severity 必须在 1～5 之间")
            opportunity = theme.get("opportunity_score")
            if opportunity is not None and (
                not isinstance(opportunity, (int, float)) or not 0 <= opportunity <= 100
            ):
                errors.append(f"{path}.opportunity_score 必须在 0～100 之间")

        def inspect_evidence(value: Any, path: str = "$") -> None:
            if isinstance(value, dict):
                if "quote" in value:
                    quote = value.get("quote")
                    review_id = value.get("review_id")
                    if not isinstance(quote, str) or not quote.strip():
                        errors.append(f"{path}.quote 必须是非空字符串")
                    elif not isinstance(review_id, str) or review_id not in review_map:
                        errors.append(f"{path}.quote 缺少有效 review_id")
                    else:
                        review = review_map[review_id]
                        source = _normalize_quote(f"{review.get('title', '')} {review.get('review_content', '')}")
                        if _normalize_quote(quote) not in source:
                            errors.append(f"{path}.quote 不是评论 {review_id} 中的连续原文")
                for key, child in value.items():
                    inspect_evidence(child, f"{path}.{key}")
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    inspect_evidence(child, f"{path}[{index}]")

        inspect_evidence(analysis)

    if not analysis.get("themes") if isinstance(analysis, dict) else True:
        warnings.append("没有语义主题，报告仍可生成，但只包含确定性统计")
    if isinstance(analysis, dict) and not analysis.get("limitations"):
        warnings.append("建议明确写出采样限制")

    result = {
        "valid": not errors,
        "validated_at": now_iso(),
        "analysis_path": str(analysis_path),
        "review_count": len(reviews),
        "errors": errors,
        "warnings": warnings,
    }
    write_json(run_dir / "analysis" / "validation.json", result)
    return result


def _manifest_base(plan: dict[str, Any], run_dir: Path, mode: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "mode": mode,
        "run_dir": str(run_dir),
        "plan": plan,
        "tasks": [],
        "status": "created",
    }


def _task_record(
    request_entry: dict[str, Any],
    task_id: str,
    *,
    submission: dict[str, Any] | None,
    result: dict[str, Any] | None,
) -> dict[str, Any]:
    submit_data = (submission or {}).get("data", {})
    result_data = (result or {}).get("data", {})
    return {
        "request_id": request_entry.get("id"),
        "request_fingerprint": request_entry.get("request_fingerprint"),
        "task_id": str(task_id),
        "status": result_data.get("status") or submit_data.get("status"),
        "pre_deduct": submit_data.get("pre_deduct", result_data.get("pre_deduct")),
        "actual_deduct": result_data.get("actual_deduct"),
        "created_at": submit_data.get("created_at", result_data.get("created_at")),
        "finished_at": result_data.get("finished_at"),
        "items_summary": result_data.get("items_summary", []),
    }


def _update_task_index(output_root: Path, manifest: dict[str, Any]) -> None:
    path = output_root / "task-index.json"
    if path.exists():
        try:
            index = read_json(path)
        except (OSError, json.JSONDecodeError):
            index = {"schema_version": SCHEMA_VERSION, "tasks": []}
    else:
        index = {"schema_version": SCHEMA_VERSION, "tasks": []}
    existing = {str(item.get("task_id")): item for item in index.get("tasks", []) if item.get("task_id")}
    plan = manifest.get("plan", {})
    for task in manifest.get("tasks", []):
        existing[str(task["task_id"])] = {
            **task,
            "scenario": plan.get("scenario"),
            "asins": plan.get("asins", []),
            "marketplace": plan.get("marketplace"),
            "run_dir": manifest.get("run_dir"),
            "indexed_at": now_iso(),
        }
    index["updated_at"] = now_iso()
    index["tasks"] = sorted(existing.values(), key=lambda item: str(item.get("created_at") or ""), reverse=True)
    write_json(path, index)


def _finalize_run(
    run_dir: Path,
    manifest: dict[str, Any],
    raw_results: list[tuple[dict[str, Any], dict[str, Any], str]],
    output_root: Path,
) -> None:
    reviews = normalize_results(raw_results)
    write_reviews(run_dir / "reviews.jsonl", reviews)
    stats = compute_statistics(reviews, manifest)
    write_json(run_dir / "statistics.json", stats)
    prepare_analysis(run_dir)
    manifest["status"] = "ready_for_semantic_analysis"
    manifest["updated_at"] = now_iso()
    manifest["unique_reviews"] = len(reviews)
    write_json(run_dir / "manifest.json", manifest)
    _update_task_index(output_root, manifest)


def run_fetch(args: argparse.Namespace) -> Path:
    plan_path = Path(args.plan).expanduser().resolve()
    plan = read_json(plan_path)
    confirmed = float(args.confirm_max_points)
    estimated = float(plan.get("estimated_max_points", 0))
    if confirmed + 1e-9 < estimated:
        raise ValueError(
            f"确认上限 {display_number(confirmed)} 小于计划最大预估 {display_number(estimated)}；拒绝提交付费任务"
        )
    output_root = Path(args.output_root).expanduser().resolve()
    run_dir = create_run_dir(
        output_root,
        scenario=plan.get("scenario", "custom"),
        asins=plan.get("asins", []),
        explicit=args.run_dir,
    )
    write_json(run_dir / "plan.json", plan)
    manifest = _manifest_base(plan, run_dir, "fetch")
    write_json(run_dir / "manifest.json", manifest)

    api_key = load_api_key(env_file=args.env_file, prompt=args.prompt_api_key)
    client = ReveyesClient(
        api_key,
        base_url=args.base_url,
        timeout=args.http_timeout,
        retries=args.retries,
    )
    submissions: list[tuple[dict[str, Any], str, dict[str, Any]]] = []
    cumulative_pre_deduct = 0.0
    total_requested_pages = max(1, int(plan.get("requested_pages", 0)))
    inferred_unit_price: float | None = None
    try:
        for index, request_entry in enumerate(plan.get("requests", [])):
            submission = client.submit(request_entry["payload"])
            data = submission["data"]
            task_id = str(data["task_id"])
            pre_deduct = float(data.get("pre_deduct") or 0)
            cumulative_pre_deduct += pre_deduct
            requested_pages = max(1, int(request_entry.get("requested_pages", 0)))
            if pre_deduct > 0:
                inferred_unit_price = pre_deduct / requested_pages
            record = _task_record(request_entry, task_id, submission=submission, result=None)
            manifest["tasks"].append(record)
            manifest["status"] = "submitted"
            manifest["updated_at"] = now_iso()
            write_json(run_dir / "manifest.json", manifest)
            submissions.append((request_entry, task_id, submission))

            if inferred_unit_price is not None and index + 1 < len(plan.get("requests", [])):
                projected = inferred_unit_price * total_requested_pages
                if projected > confirmed + 1e-9:
                    raise ReveyesError(
                        "服务端当前预扣单价高于计划配置。已停止提交剩余任务；"
                        f"服务端推算最大预扣 {display_number(projected)}，确认上限为 {display_number(confirmed)}。"
                    )
            if cumulative_pre_deduct > confirmed + 1e-9:
                raise ReveyesError(
                    f"累计预扣 {display_number(cumulative_pre_deduct)} 已超过确认上限 "
                    f"{display_number(confirmed)}；已停止提交剩余任务。"
                )

        raw_results: list[tuple[dict[str, Any], dict[str, Any], str]] = []
        for request_entry, task_id, submission in submissions:
            def on_poll(status: str, attempt: int, *, _task_id: str = task_id) -> None:
                print(f"任务 {_task_id}: {status}（轮询 {attempt}）", file=sys.stderr, flush=True)

            result = client.collect_result(
                task_id,
                poll_interval=args.poll_interval,
                max_wait=args.max_wait,
                page_size=args.result_page_size,
                on_poll=on_poll,
            )
            raw_path = run_dir / "raw" / f"{safe_slug(request_entry['id'])}-{task_id}.json"
            write_json(raw_path, result)
            record = _task_record(request_entry, task_id, submission=submission, result=result)
            for position, current in enumerate(manifest["tasks"]):
                if str(current.get("task_id")) == task_id:
                    manifest["tasks"][position] = record
                    break
            manifest["updated_at"] = now_iso()
            write_json(run_dir / "manifest.json", manifest)
            raw_results.append((request_entry, result, task_id))
        _finalize_run(run_dir, manifest, raw_results, output_root)
        return run_dir
    finally:
        del api_key


def run_retrieve(args: argparse.Namespace) -> Path:
    output_root = Path(args.output_root).expanduser().resolve()
    run_dir = create_run_dir(output_root, scenario="existing-task", asins=[], explicit=args.run_dir)
    filters = {
        **DEFAULT_FILTERS,
        "filter_star": args.filter_star,
        "filter_sort_by": args.sort_by,
        "filter_reviewer_type": args.reviewer_type,
        "filter_media_type": args.media_type,
        "filter_variant": args.variant,
    }
    request_entry = {
        "id": args.source_id,
        "label": args.source_label,
        "purpose": "复用永久保存的已有任务",
        "requested_pages": args.known_pages,
        "estimated_max_points": 0,
        "request_fingerprint": None,
        "payload": {"asins": []},
        "known_filters": filters,
    }
    plan = {
        "schema_version": SCHEMA_VERSION,
        "created_at": now_iso(),
        "scenario": "existing-task",
        "scenario_label": "复用已有任务",
        "scenario_description": "读取永久保存的任务结果，不创建新的扣费任务。",
        "asins": [],
        "marketplace": args.marketplace.upper() if args.marketplace else None,
        "report_language": args.report_language,
        "report_title": args.report_title,
        "points_per_page_at_plan": display_number(args.points_per_page),
        "requested_pages": args.known_pages,
        "estimated_max_points": 0,
        "sampling_notice": "任务的原始过滤条件由调用者提供；未知条件不得从结果中臆测。",
        "requests": [request_entry],
    }
    plan["plan_fingerprint"] = fingerprint(plan)
    manifest = _manifest_base(plan, run_dir, "retrieve")
    write_json(run_dir / "plan.json", plan)
    write_json(run_dir / "manifest.json", manifest)

    api_key = load_api_key(env_file=args.env_file, prompt=args.prompt_api_key)
    client = ReveyesClient(api_key, base_url=args.base_url, timeout=args.http_timeout, retries=args.retries)
    try:
        result = client.collect_result(
            str(args.task_id),
            poll_interval=args.poll_interval,
            max_wait=args.max_wait,
            page_size=args.result_page_size,
            on_poll=lambda status, attempt: print(
                f"任务 {args.task_id}: {status}（轮询 {attempt}）", file=sys.stderr, flush=True
            ),
        )
    finally:
        del api_key
    data = result.get("data", {})
    rows = data.get("reviews", {}).get("data", [])
    discovered_asins = sorted({str(row.get("asin", "")).upper() for row in rows if row.get("asin")})
    discovered_marketplace = next((str(row.get("marketplace", "")).upper() for row in rows if row.get("marketplace")), None)
    source_items = []
    for asin in discovered_asins:
        source_items.append(
            {
                "asin": asin,
                "marketplace": args.marketplace.upper() if args.marketplace else discovered_marketplace,
                "pages": args.known_pages,
                **filters,
            }
        )
    request_entry["payload"] = {"asins": source_items}
    request_entry["request_fingerprint"] = fingerprint(request_entry["payload"])
    plan["asins"] = discovered_asins
    plan["marketplace"] = args.marketplace.upper() if args.marketplace else discovered_marketplace
    plan["plan_fingerprint"] = fingerprint({key: value for key, value in plan.items() if key != "created_at"})
    raw_path = run_dir / "raw" / f"{safe_slug(args.source_id)}-{safe_slug(str(args.task_id))}.json"
    write_json(raw_path, result)
    manifest["tasks"] = [
        _task_record(request_entry, str(args.task_id), submission=None, result=result)
    ]
    write_json(run_dir / "plan.json", plan)
    write_json(run_dir / "manifest.json", manifest)
    _finalize_run(run_dir, manifest, [(request_entry, result, str(args.task_id))], output_root)
    return run_dir


def render_run(args: argparse.Namespace) -> Path:
    from report_renderer import render_report

    run_dir = Path(args.run_dir).expanduser().resolve()
    analysis_path = (
        Path(args.analysis).expanduser().resolve()
        if args.analysis
        else run_dir / "analysis" / "final-analysis.json"
    )
    if analysis_path.exists():
        validation = validate_analysis(run_dir, analysis_path)
        if not validation["valid"] and not args.allow_invalid_analysis:
            raise ValueError("语义分析校验失败；查看 analysis/validation.json，或明确使用 --allow-invalid-analysis")
        analysis = read_json(analysis_path)
    else:
        manifest = read_json(run_dir / "manifest.json")
        stats = read_json(run_dir / "statistics.json")
        analysis = final_analysis_template(manifest, stats)
        analysis["limitations"].append("尚未完成语义分析，本报告只展示确定性统计和评论浏览器。")
    output = Path(args.output).expanduser().resolve() if args.output else run_dir / "report.html"
    render_report(
        run_dir=run_dir,
        analysis=analysis,
        output=output,
        title_override=args.title,
        include_media_links=args.include_media_links,
    )
    return output


def add_api_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base-url", default=os.environ.get("REVEYES_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--env-file", help="包含 REVEYES_API_KEY 的 dotenv 文件（不执行其中的 shell 语法）")
    parser.add_argument("--prompt-api-key", action="store_true", help="在终端中隐藏输入 API Key")
    parser.add_argument("--http-timeout", type=float, default=30)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--poll-interval", type=float, default=5)
    parser.add_argument("--max-wait", type=float, default=1800)
    parser.add_argument("--result-page-size", type=int, default=100)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    scenarios = subparsers.add_parser("scenarios", help="列出内置用户场景和最大成本")
    scenarios.add_argument("--points-per-page", type=float, default=float(os.environ.get("REVEYES_POINTS_PER_PAGE", 3)))
    scenarios.add_argument("--asins", type=int, default=1, help="用于估算成本的 ASIN 数量")

    plan = subparsers.add_parser("plan", help="生成抓取计划，不调用付费接口")
    plan.add_argument("--asin", action="append", required=True, help="可重复传入多个 ASIN")
    plan.add_argument("--marketplace", default="US")
    plan.add_argument("--scenario", choices=[*SCENARIOS, "custom"], default="health")
    plan.add_argument("--points-per-page", type=float, default=float(os.environ.get("REVEYES_POINTS_PER_PAGE", 3)))
    plan.add_argument("--pages", type=int, help="覆盖场景中每个过滤组的页数，范围 1～10")
    plan.add_argument("--filter-star", choices=FILTER_STAR_CHOICES, help="custom 场景使用")
    plan.add_argument("--sort-by", choices=["recent", "helpful"])
    plan.add_argument("--reviewer-type", choices=["all_reviews", "avp_only_reviews"], default="all_reviews")
    plan.add_argument("--media-type", choices=["all_contents", "media_reviews_only"], default="all_contents")
    plan.add_argument("--variant", choices=["all_formats", "current_format"], default="all_formats")
    plan.add_argument("--report-language", default="zh-CN")
    plan.add_argument("--report-title")
    plan.add_argument("--output", help="计划 JSON 输出路径；省略则输出到标准输出")

    fetch = subparsers.add_parser("fetch", help="按计划提交付费任务并完整获取结果")
    fetch.add_argument("--plan", required=True)
    fetch.add_argument("--confirm-max-points", required=True, type=float, help="用户确认的最大预扣上限")
    fetch.add_argument("--output-root", default="amazon-review-reports")
    fetch.add_argument("--run-dir")
    add_api_arguments(fetch)

    retrieve = subparsers.add_parser("retrieve", help="复用永久任务，不创建新的扣费任务")
    retrieve.add_argument("--task-id", required=True)
    retrieve.add_argument("--source-id", default="existing-task")
    retrieve.add_argument("--source-label", default="已有永久任务")
    retrieve.add_argument("--known-pages", type=int, default=1)
    retrieve.add_argument("--filter-star", choices=FILTER_STAR_CHOICES, default="all_stars")
    retrieve.add_argument("--sort-by", choices=["recent", "helpful"], default="recent")
    retrieve.add_argument("--reviewer-type", choices=["all_reviews", "avp_only_reviews"], default="all_reviews")
    retrieve.add_argument("--media-type", choices=["all_contents", "media_reviews_only"], default="all_contents")
    retrieve.add_argument("--variant", choices=["all_formats", "current_format"], default="all_formats")
    retrieve.add_argument("--marketplace")
    retrieve.add_argument("--report-language", default="zh-CN")
    retrieve.add_argument("--report-title")
    retrieve.add_argument("--points-per-page", type=float, default=float(os.environ.get("REVEYES_POINTS_PER_PAGE", 3)))
    retrieve.add_argument("--output-root", default="amazon-review-reports")
    retrieve.add_argument("--run-dir")
    add_api_arguments(retrieve)

    prepare = subparsers.add_parser("prepare", help="重新生成统计和语义分析批次")
    prepare.add_argument("--run-dir", required=True)
    prepare.add_argument("--max-reviews-per-batch", type=int, default=35)
    prepare.add_argument("--max-chars-per-batch", type=int, default=24000)

    validate = subparsers.add_parser("validate-analysis", help="校验语义分析结构和引用证据")
    validate.add_argument("--run-dir", required=True)
    validate.add_argument("--analysis", help="默认使用 RUN_DIR/analysis/final-analysis.json")

    render = subparsers.add_parser("render", help="渲染自包含 HTML 报告")
    render.add_argument("--run-dir", required=True)
    render.add_argument("--analysis")
    render.add_argument("--output")
    render.add_argument("--title")
    render.add_argument("--include-media-links", action="store_true")
    render.add_argument("--allow-invalid-analysis", action="store_true")

    tasks = subparsers.add_parser("tasks", help="列出本地登记的永久任务")
    tasks.add_argument("--output-root", default="amazon-review-reports")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "scenarios":
            rows = []
            for key, value in SCENARIOS.items():
                pages = sum(int(spec["pages"]) for spec in value["specs"]) * args.asins
                rows.append(
                    {
                        "scenario": key,
                        "label": value["label"],
                        "asins": args.asins,
                        "requested_pages": pages,
                        "estimated_max_points": display_number(pages * args.points_per_page),
                        "description": value["description"],
                    }
                )
            print(json.dumps(rows, ensure_ascii=False, indent=2))
            return 0
        if args.command == "plan":
            plan_value = build_plan(
                asins=args.asin,
                marketplace=args.marketplace,
                scenario=args.scenario,
                points_per_page=args.points_per_page,
                pages_override=args.pages,
                sort_by=args.sort_by,
                reviewer_type=args.reviewer_type,
                media_type=args.media_type,
                variant=args.variant,
                custom_filter_star=args.filter_star,
                report_language=args.report_language,
                report_title=args.report_title,
            )
            if args.output:
                output = Path(args.output).expanduser().resolve()
                write_json(output, plan_value)
                print(output)
            else:
                print(json.dumps(plan_value, ensure_ascii=False, indent=2))
            return 0
        if args.command == "fetch":
            print(run_fetch(args))
            return 0
        if args.command == "retrieve":
            print(run_retrieve(args))
            return 0
        if args.command == "prepare":
            index = prepare_analysis(
                Path(args.run_dir).expanduser().resolve(),
                max_reviews_per_batch=args.max_reviews_per_batch,
                max_chars_per_batch=args.max_chars_per_batch,
            )
            print(json.dumps(index, ensure_ascii=False, indent=2))
            return 0
        if args.command == "validate-analysis":
            run_dir = Path(args.run_dir).expanduser().resolve()
            analysis_path = (
                Path(args.analysis).expanduser().resolve()
                if args.analysis
                else run_dir / "analysis" / "final-analysis.json"
            )
            result = validate_analysis(run_dir, analysis_path)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["valid"] else 1
        if args.command == "render":
            print(render_run(args))
            return 0
        if args.command == "tasks":
            path = Path(args.output_root).expanduser().resolve() / "task-index.json"
            print(path.read_text(encoding="utf-8") if path.exists() else '{"schema_version":1,"tasks":[]}')
            return 0
        parser.error(f"未知命令: {args.command}")
    except (ReveyesError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        if isinstance(exc, ReveyesError) and exc.api_code is not None:
            print(f"API code: {exc.api_code}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

