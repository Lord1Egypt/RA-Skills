#!/usr/bin/env python3
"""Render a safe, self-contained HTML report from one prepared review run."""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_reviews(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _safe_json(value: Any) -> str:
    """Serialize data for an inline script without allowing a </script> breakout."""
    raw = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return (
        raw.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def _public_manifest(manifest: dict[str, Any], stats: dict[str, Any]) -> dict[str, Any]:
    plan = manifest.get("plan", {})
    requests = []
    task_by_request = {task.get("request_id"): task for task in manifest.get("tasks", [])}
    for request in plan.get("requests", []):
        items = request.get("payload", {}).get("asins", [])
        first = items[0] if items else {}
        task = task_by_request.get(request.get("id"), {})
        requests.append(
            {
                "id": request.get("id"),
                "label": request.get("label"),
                "purpose": request.get("purpose"),
                "requested_pages": request.get("requested_pages"),
                "actual_pages": sum(int(item.get("actual_pages") or 0) for item in task.get("items_summary", [])),
                "filter_star": first.get("filter_star"),
                "filter_sort_by": first.get("filter_sort_by"),
                "filter_reviewer_type": first.get("filter_reviewer_type"),
                "filter_media_type": first.get("filter_media_type"),
                "filter_variant": first.get("filter_variant"),
            }
        )
    return {
        "scenario": plan.get("scenario"),
        "scenario_label": plan.get("scenario_label"),
        "scenario_description": plan.get("scenario_description"),
        "asins": plan.get("asins", []),
        "marketplace": plan.get("marketplace"),
        "created_at": manifest.get("created_at"),
        "finished_at": max(
            (str(task.get("finished_at") or "") for task in manifest.get("tasks", [])),
            default="",
        ),
        "requested_pages": stats.get("requested_pages"),
        "actual_pages": stats.get("actual_pages"),
        "pre_deduct": stats.get("pre_deduct"),
        "actual_deduct": stats.get("actual_deduct"),
        "points_per_page_at_plan": plan.get("points_per_page_at_plan"),
        "sampling_notice": plan.get("sampling_notice"),
        "requests": requests,
    }


def _public_review(review: dict[str, Any], *, include_media_links: bool) -> dict[str, Any]:
    value = {
        "asin": review.get("asin"),
        "marketplace": review.get("marketplace"),
        "review_id": review.get("review_id"),
        "rating": review.get("rating"),
        "title": review.get("title"),
        "review_date": review.get("review_date"),
        "review_content": review.get("review_content"),
        "verified_purchase": review.get("verified_purchase"),
        "helpful_votes": review.get("helpful_votes"),
        "product_variant": review.get("product_variant"),
        "image_count": len(review.get("images", [])),
        "video_count": len(review.get("videos", [])),
        "sources": [
            {
                "request_id": source.get("request_id"),
                "label": source.get("label"),
                "filter_star": source.get("filter_star"),
                "filter_sort_by": source.get("filter_sort_by"),
                "filter_media_type": source.get("filter_media_type"),
                "page": source.get("page"),
            }
            for source in review.get("sources", [])
        ],
    }
    if include_media_links:
        value["images"] = review.get("images", [])
        value["videos"] = review.get("videos", [])
    return value


def render_report(
    *,
    run_dir: Path,
    analysis: dict[str, Any],
    output: Path,
    title_override: str | None = None,
    include_media_links: bool = False,
) -> None:
    manifest = _read_json(run_dir / "manifest.json")
    stats = _read_json(run_dir / "statistics.json")
    reviews = _read_reviews(run_dir / "reviews.jsonl")
    title = title_override or analysis.get("report_title") or "Amazon 评论分析报告"
    report_data = {
        "schema_version": 1,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "title": title,
        "manifest": _public_manifest(manifest, stats),
        "statistics": stats,
        "analysis": analysis,
        "reviews": [_public_review(review, include_media_links=include_media_links) for review in reviews],
    }
    template_path = Path(__file__).resolve().parent.parent / "assets" / "report-template.html"
    if not template_path.is_file():
        raise FileNotFoundError(f"缺少报告模板: {template_path}")
    document = template_path.read_text(encoding="utf-8")
    document = document.replace("__REPORT_TITLE__", html.escape(str(title), quote=True))
    document = document.replace("/*__REPORT_DATA__*/", _safe_json(report_data))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")

