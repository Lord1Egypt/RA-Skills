#!/usr/bin/env python3
"""Generate an internal audit report from orchestrator JSON outputs.

Usage:
    python3 scripts/generate_internal_report.py geo_orchestrator_v2 --output-dir geo_orchestrator_v2
    python3 scripts/generate_internal_report.py workflow_state.json --output internal_audit_report.md
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


KNOWN_FILES = {
    "workflow_state": "workflow_state.json",
    "brand_profile": "brand_profile.json",
    "geo_audit_report": "geo_audit_report.json",
    "content_gap_report": "content_gap_report.json",
    "content_tasks": "content_tasks.json",
    "platform_drafts": "platform_drafts.json",
    "publish_plan": "publish_plan.json",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def load_bundle(input_path: Path) -> dict[str, Any]:
    bundle: dict[str, Any] = {
        "workflow_state": {},
        "brand_profile": {},
        "geo_audit_report": [],
        "content_gap_report": {},
        "content_tasks": [],
        "platform_drafts": [],
        "publish_plan": {},
    }

    if input_path.is_dir():
        for key, filename in KNOWN_FILES.items():
            file_path = input_path / filename
            if file_path.exists():
                bundle[key] = load_json(file_path)
    else:
        payload = load_json(input_path)
        if isinstance(payload, dict):
            bundle["workflow_state"] = payload
            for key in bundle:
                if key in payload:
                    bundle[key] = payload[key]
        elif isinstance(payload, list):
            bundle["platform_drafts"] = payload

    workflow_state = bundle.get("workflow_state") or {}
    if isinstance(workflow_state, dict):
        for key in ("brand_profile", "geo_audit_report", "content_gap_report", "content_tasks", "platform_drafts", "publish_plan"):
            if not bundle.get(key) and workflow_state.get(key):
                bundle[key] = workflow_state[key]

    return bundle


def json_block(value: Any) -> str:
    return "```json\n" + json.dumps(value, ensure_ascii=False, indent=2) + "\n```"


def brand_name(bundle: dict[str, Any]) -> str:
    profile = bundle.get("brand_profile") or {}
    if isinstance(profile, dict):
        return as_text(profile.get("brand_name")) or "unknown"
    return "unknown"


def evidence_summary(geo_items: list[Any]) -> list[str]:
    if not geo_items:
        return ["No geo_audit_report items found."]
    lines: list[str] = []
    for index, item in enumerate(geo_items, start=1):
        if not isinstance(item, dict):
            lines.append(f"- geo_audit_report[{index}] is not an object.")
            continue
        lines.append(
            "- "
            + f"model={as_text(item.get('target_model') or 'unknown')}; "
            + f"keyword={as_text(item.get('keyword') or 'unknown')}; "
            + f"evidence_level={as_text(item.get('evidence_level') or 'missing')}; "
            + f"data_source={as_text(item.get('data_source') or 'missing')}; "
            + f"ranking_claim_allowed={as_text(item.get('ranking_claim_allowed'))}; "
            + f"score_claim_allowed={as_text(item.get('score_claim_allowed'))}"
        )
    return lines


def fact_dependency_summary(bundle: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for task in as_list(bundle.get("content_tasks")):
        if not isinstance(task, dict):
            continue
        task_id = as_text(task.get("task_id") or task.get("title") or "unknown_task")
        dependencies = task.get("fact_dependencies", [])
        gate = task.get("publish_gate", {})
        lines.append(
            "- "
            + f"{task_id}: fact_dependencies={as_text(dependencies) or '[]'}; "
            + f"publish_gate={as_text(gate) or '{}'}"
        )

    for draft in as_list(bundle.get("platform_drafts")):
        if not isinstance(draft, dict):
            continue
        draft_id = as_text(draft.get("draft_id") or draft.get("title") or "unknown_draft")
        lines.append(
            "- "
            + f"{draft_id}: publish_readiness={as_text(draft.get('publish_readiness') or 'missing')}; "
            + f"fact_check_items={as_text(draft.get('fact_check_items', []))}; "
            + f"blocking_items={as_text(draft.get('blocking_items', []))}"
        )
    return lines or ["No fact dependencies or draft readiness data found."]


def forbidden_claims_summary(bundle: dict[str, Any]) -> list[str]:
    profile = bundle.get("brand_profile") or {}
    forbidden = profile.get("forbidden_claims", []) if isinstance(profile, dict) else []
    lines = [f"- forbidden_claims={as_text(forbidden) or '[]'}"]
    draft_text = "\n".join(as_text(draft) for draft in as_list(bundle.get("platform_drafts")))
    for claim in forbidden:
        if isinstance(claim, str) and claim and claim in draft_text:
            lines.append(f"- FOUND forbidden claim in platform drafts: {claim}")
    if len(lines) == 1:
        lines.append("- No forbidden claim hits detected by simple text scan.")
    return lines


def publish_plan_summary(bundle: dict[str, Any]) -> list[str]:
    plan = bundle.get("publish_plan") or {}
    if not isinstance(plan, dict):
        return ["publish_plan is not an object."]
    lines = [
        f"- overall_publish_readiness={as_text(plan.get('overall_publish_readiness') or 'missing')}",
        f"- blocking_items={as_text(plan.get('blocking_items', []))}",
    ]
    for index, item in enumerate(as_list(plan.get("items")), start=1):
        if isinstance(item, dict):
            lines.append(
                "- "
                + f"item[{index}] draft_id={as_text(item.get('draft_id') or index)}; "
                + f"publish_readiness={as_text(item.get('publish_readiness') or 'missing')}; "
                + f"manual_review_required={as_text(item.get('manual_review_required'))}; "
                + f"suggested_publish_time={as_text(item.get('suggested_publish_time'))}; "
                + f"blocking_items={as_text(item.get('blocking_items', []))}"
            )
    return lines


def validation_note(input_path: Path) -> str:
    if input_path.is_dir() and not (input_path / "workflow_state.json").exists():
        return "No workflow_state.json found for full validation. Validate assembled workflow_state before final handoff."
    return "Run scripts/validate_workflow_state.py against workflow_state.json before final handoff."


def internal_report_markdown(bundle: dict[str, Any], input_path: Path) -> str:
    workflow_state = bundle.get("workflow_state") or {}
    api_status = workflow_state.get("api_status", {}) if isinstance(workflow_state, dict) else {}
    errors = workflow_state.get("errors", []) if isinstance(workflow_state, dict) else []
    version_notes = workflow_state.get("version_notes", []) if isinstance(workflow_state, dict) else []

    lines: list[str] = [
        "# PowerMatrix GEO Growth Internal Audit Report",
        "",
        "> 此报告仅供 PowerMatrix / WorkBuddy 内部交付、审计与质量控制使用，不建议直接发送给客户。",
        "",
        f"Generated at: {datetime.utcnow().isoformat(timespec='seconds')}Z",
        f"Input: {input_path}",
        f"Brand: {brand_name(bundle)}",
        "",
        "## 1. Workflow State",
        "",
        json_block(workflow_state or {"note": "workflow_state not provided"}),
        "",
        "## 2. Evidence and Source Quality",
        "",
    ]
    lines.extend(evidence_summary(as_list(bundle.get("geo_audit_report"))))
    lines.extend(["", "## 3. API and Tool Status", "", json_block(api_status or {"status": "not_provided"}), ""])
    lines.extend(["## 4. Schema and Validation Result", "", f"- {validation_note(input_path)}", f"- errors={as_text(errors) or '[]'}", ""])
    lines.extend(["## 5. Fact Dependencies and Publishing Prerequisites", ""])
    lines.extend(fact_dependency_summary(bundle))
    lines.extend(["", "## 6. Compliance and Forbidden Claims Check", ""])
    lines.extend(forbidden_claims_summary(bundle))
    lines.extend(["", "## 7. Platform Draft QA", "", f"- platform_drafts_count={len(as_list(bundle.get('platform_drafts')))}", json_block(bundle.get("platform_drafts") or []), ""])
    lines.extend(["## 8. Publish Plan QA", ""])
    lines.extend(publish_plan_summary(bundle))
    lines.extend(["", "## 9. Risks, Blockers, and Owner Actions", "", f"- content_gap_report={as_text(bundle.get('content_gap_report') or {})}", ""])
    lines.extend(["## 10. Version and File Notes", "", f"- version_notes={as_text(version_notes) or '[]'}", f"- source_files={as_text(list(KNOWN_FILES.values()))}", ""])
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an internal GEO audit report.")
    parser.add_argument("input", help="Input workflow_state JSON file or directory containing orchestrator JSON outputs.")
    parser.add_argument("--output", default=None, help="Output path for internal_audit_report.md.")
    parser.add_argument("--output-dir", default=None, help="Directory for internal_audit_report.md.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input not found: {input_path}")
        return 2

    bundle = load_bundle(input_path)
    report = internal_report_markdown(bundle, input_path)

    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "internal_audit_report.md"
    else:
        output_path = Path(args.output or "internal_audit_report.md")

    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

