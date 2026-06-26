#!/usr/bin/env python3
"""Validate a PowerMatrix GEO Growth workflow_state JSON file.

Usage:
    python3 validate_workflow_state.py workflow_state.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "workflow_id",
    "current_stage",
    "delivery_status",
    "brand_profile",
    "geo_audit_report",
    "content_tasks",
    "platform_drafts",
    "publish_plan",
    "errors",
    "next_actions",
]

EVIDENCE_LEVELS = {
    "verified_live_check",
    "manual_check",
    "inferred_estimate",
    "unverified_assumption",
}

PUBLISH_READINESS = {"ready", "needs_review", "blocked"}

UNCERTAIN_EVIDENCE_LEVELS = {"inferred_estimate", "unverified_assumption"}

UNCERTAIN_RANK_OR_SCORE_PATTERNS = [
    "预计第",
    "预计前",
    "排名第",
    "排名前",
    "/100",
    "评分",
    "第1位",
    "第一位",
    "前3位",
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(as_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(as_text(item) for item in value.values())
    return str(value)


def collect_draft_text(draft: dict[str, Any]) -> str:
    parts = [
        draft.get("title"),
        draft.get("body"),
        draft.get("cta"),
        draft.get("tags"),
        draft.get("summary"),
    ]
    return as_text(parts).lower()


def has_unverified_rank_or_score_claim(value: Any) -> bool:
    text = as_text(value)
    return any(pattern in text for pattern in UNCERTAIN_RANK_OR_SCORE_PATTERNS)


def is_conditional_publish_time(value: Any) -> bool:
    text = as_text(value)
    if not text.strip():
        return True
    conditional_markers = ["补齐", "待确认", "确认后", "再排期", "暂不排期", "blocked"]
    return any(marker in text for marker in conditional_markers)


def validate_workflow_state(state: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in state:
            errors.append(f"Missing required field: {field}")

    delivery_status = state.get("delivery_status")
    if delivery_status not in PUBLISH_READINESS:
        errors.append("delivery_status must be one of ready, needs_review, blocked")

    brand_profile = state.get("brand_profile") or {}
    if not isinstance(brand_profile, dict):
        errors.append("brand_profile must be an object")
        brand_profile = {}

    forbidden_claims = brand_profile.get("forbidden_claims", [])
    if forbidden_claims is None:
        forbidden_claims = []
    if not isinstance(forbidden_claims, list):
        errors.append("brand_profile.forbidden_claims must be an array")
        forbidden_claims = []

    platform_drafts = state.get("platform_drafts", [])
    if not isinstance(platform_drafts, list):
        errors.append("platform_drafts must be an array")
        platform_drafts = []

    if not platform_drafts:
        warnings.append("platform_drafts is empty; publish plan may be incomplete")

    for index, draft in enumerate(platform_drafts, start=1):
        label = draft.get("draft_id", f"draft_at_index_{index}") if isinstance(draft, dict) else f"draft_at_index_{index}"
        if not isinstance(draft, dict):
            errors.append(f"{label} must be an object")
            continue

        if "manual_review_required" not in draft:
            errors.append(f"{label} missing manual_review_required")
        elif draft.get("manual_review_required") is not True:
            errors.append(f"{label} manual_review_required must be true")

        publish_readiness = draft.get("publish_readiness")
        if publish_readiness not in PUBLISH_READINESS:
            errors.append(f"{label} publish_readiness must be one of ready, needs_review, blocked")
        if publish_readiness == "blocked" and not draft.get("blocking_items"):
            errors.append(f"{label} is blocked but missing blocking_items")

        draft_text = collect_draft_text(draft)
        for claim in forbidden_claims:
            if not isinstance(claim, str) or not claim.strip():
                continue
            if claim.lower() in draft_text:
                errors.append(f"{label} contains forbidden claim: {claim}")

    geo_audit_report = state.get("geo_audit_report", [])
    if not isinstance(geo_audit_report, list):
        errors.append("geo_audit_report must be an array")
        geo_audit_report = []

    for index, item in enumerate(geo_audit_report, start=1):
        label = item.get("query", f"geo_audit_item_{index}") if isinstance(item, dict) else f"geo_audit_item_{index}"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        evidence_level = item.get("evidence_level")
        if evidence_level not in EVIDENCE_LEVELS:
            errors.append(f"{label} evidence_level must be one of {sorted(EVIDENCE_LEVELS)}")
        if not item.get("data_source"):
            errors.append(f"{label} missing data_source")
        if evidence_level in UNCERTAIN_EVIDENCE_LEVELS:
            if item.get("ranking_claim_allowed") is True:
                errors.append(f"{label} cannot allow ranking claims with {evidence_level}")
            if item.get("score_claim_allowed") is True:
                errors.append(f"{label} cannot allow score claims with {evidence_level}")
            if has_unverified_rank_or_score_claim(item):
                errors.append(f"{label} contains rank/score language without verified evidence")

    publish_plan = state.get("publish_plan") or {}
    if isinstance(publish_plan, dict):
        overall_readiness = publish_plan.get("overall_publish_readiness")
        if overall_readiness not in PUBLISH_READINESS:
            errors.append("publish_plan.overall_publish_readiness must be one of ready, needs_review, blocked")

        plan_blocking_items = publish_plan.get("blocking_items", [])
        if overall_readiness == "blocked" and not plan_blocking_items:
            errors.append("publish_plan is blocked but blocking_items is empty")
        if overall_readiness == "blocked" and delivery_status == "ready":
            errors.append("delivery_status cannot be ready when publish_plan is blocked")

        for index, item in enumerate(publish_plan.get("items", []), start=1):
            if not isinstance(item, dict):
                errors.append(f"publish_plan.items[{index}] must be an object")
                continue
            if item.get("manual_review_required") is not True:
                errors.append(f"publish_plan item {item.get('draft_id', index)} manual_review_required must be true")
            publish_readiness = item.get("publish_readiness")
            if publish_readiness not in PUBLISH_READINESS:
                errors.append(f"publish_plan item {item.get('draft_id', index)} publish_readiness must be one of ready, needs_review, blocked")
            if publish_readiness == "blocked":
                if not item.get("blocking_items"):
                    errors.append(f"publish_plan item {item.get('draft_id', index)} is blocked but missing blocking_items")
                if not is_conditional_publish_time(item.get("suggested_publish_time")):
                    errors.append(f"publish_plan item {item.get('draft_id', index)} is blocked but has a concrete publish time")
    elif "publish_plan" in state:
        errors.append("publish_plan must be an object")

    return errors, warnings


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("workflow_state.json")
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        return 2

    try:
        state = load_json(path)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}")
        return 2

    if not isinstance(state, dict):
        print("ERROR: workflow_state must be a JSON object")
        return 2

    errors, warnings = validate_workflow_state(state)

    result = {
        "file": str(path),
        "valid": not errors,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
