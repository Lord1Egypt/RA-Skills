#!/usr/bin/env python3
"""Merge platform draft JSON files into a publish-plan input file.

Usage:
    python3 merge_platform_drafts.py draft1.json draft2.json --output merged_platform_drafts.json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


PRIORITY_ORDER = {
    "urgent": 0,
    "p0": 0,
    "high": 1,
    "p1": 1,
    "medium": 2,
    "normal": 2,
    "p2": 2,
    "low": 3,
    "p3": 3,
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def discover_json_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_dir():
            files.extend(sorted(path.glob("*.json")))
        else:
            files.append(path)
    return files


def normalize_drafts(payload: Any, source: Path) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        drafts = payload
    elif isinstance(payload, dict) and isinstance(payload.get("platform_drafts"), list):
        drafts = payload["platform_drafts"]
    elif isinstance(payload, dict) and ("draft_id" in payload or "platform" in payload or "body" in payload):
        drafts = [payload]
    else:
        raise ValueError(f"{source} does not look like a platform draft JSON file")

    normalized: list[dict[str, Any]] = []
    for index, draft in enumerate(drafts, start=1):
        if not isinstance(draft, dict):
            raise ValueError(f"{source} draft #{index} must be an object")
        item = dict(draft)
        item.setdefault("draft_id", f"{source.stem}-{index}")
        item.setdefault("priority", "medium")
        item.setdefault("manual_review_required", True)
        item.setdefault("publish_readiness", "needs_review")
        item.setdefault("fact_check_items", [])
        item.setdefault("blocking_items", [])
        item["_source_file"] = str(source)
        normalized.append(item)
    return normalized


def priority_rank(draft: dict[str, Any]) -> int:
    value = str(draft.get("priority", "medium")).lower()
    return PRIORITY_ORDER.get(value, 2)


def build_plan_input(drafts: list[dict[str, Any]]) -> dict[str, Any]:
    sorted_drafts = sorted(drafts, key=lambda draft: (priority_rank(draft), draft.get("platform", ""), draft.get("title", "")))
    priorities = {str(draft.get("priority", "medium")).lower() for draft in sorted_drafts}
    overall_priority = priorities.pop() if len(priorities) == 1 else "mixed"

    items = []
    for draft in sorted_drafts:
        items.append(
            {
                "draft_id": draft.get("draft_id", ""),
                "platform": draft.get("platform", ""),
                "title": draft.get("title", ""),
                "priority": draft.get("priority", "medium"),
                "suggested_publish_time": draft.get("suggested_publish_time", ""),
                "publish_readiness": draft.get("publish_readiness", "needs_review"),
                "blocking_items": draft.get("blocking_items", []),
                "preconditions": draft.get("preconditions", draft.get("fact_check_items", [])),
                "review_notes": draft.get("review_notes", draft.get("compliance_check", {}).get("notes", [])),
                "cta": draft.get("cta", ""),
                "manual_review_required": draft.get("manual_review_required") is True,
                "source_file": draft.get("_source_file", ""),
            }
        )

    return {
        "plan_id": f"merged-drafts-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "campaign_goal": "",
        "items": items,
        "priority": overall_priority,
        "overall_publish_readiness": "blocked" if any(item.get("publish_readiness") == "blocked" for item in items) else "needs_review",
        "blocking_items": [
            {
                "item": blocking_item,
                "reason": "Merged from platform draft blocking_items",
                "required_before": "publishing",
                "affected_draft_ids": [item.get("draft_id", "")]
            }
            for item in items
            for blocking_item in item.get("blocking_items", [])
        ],
        "suggested_schedule": [],
        "review_checklist": [
            "所有平台发布前必须人工审核",
            "确认草稿没有禁用表达、虚假案例或未经证实的数据",
            "确认 CTA 克制且符合平台规则",
            "最终发布动作由用户本人完成"
        ],
        "platform_drafts": sorted_drafts,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge platform draft JSON files into publish-plan input format.")
    parser.add_argument("inputs", nargs="+", help="Platform draft JSON files or directories containing JSON files.")
    parser.add_argument("--output", default="merged_platform_drafts.json", help="Output JSON file path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    files = discover_json_files(args.inputs)
    if not files:
        print("ERROR: No JSON files found.")
        return 2

    drafts: list[dict[str, Any]] = []
    for file_path in files:
        if not file_path.exists():
            print(f"ERROR: File not found: {file_path}")
            return 2
        try:
            drafts.extend(normalize_drafts(load_json(file_path), file_path))
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"ERROR: {exc}")
            return 2

    plan_input = build_plan_input(drafts)
    output_path = Path(args.output)
    output_path.write_text(json.dumps(plan_input, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Merged {len(drafts)} draft(s) into {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
