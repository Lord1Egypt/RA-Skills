#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_DRAFT_FIELDS = [
    "document_title",
    "source_authority",
    "target_structure",
    "document_purpose",
    "audience",
    "output_mode",
]

REQUIRED_FINAL_FIELDS = [
    "delivery_stage",
    "completeness_scope",
    "review_mode",
    "format_authority",
    "file_naming_and_version",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve Word-job readiness and package composition from a delivery brief and format profile."
    )
    parser.add_argument("--delivery-brief", required=True, help="Path to delivery brief JSON")
    parser.add_argument("--format-profile", required=True, help="Path to format profile JSON")
    parser.add_argument(
        "--stage",
        choices=("draft", "final"),
        default="final",
        help="Target assembly stage",
    )
    parser.add_argument("--out", help="Optional output file")
    parser.add_argument(
        "--format",
        choices=("md", "json"),
        default="md",
        help="Output format",
    )
    return parser.parse_args()


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def missing_fields(payload: dict, fields: list[str]) -> list[str]:
    missing: list[str] = []
    for field in fields:
        value = payload.get(field)
        if value is None:
            missing.append(field)
            continue
        if isinstance(value, str) and not value.strip():
            missing.append(field)
    return missing


def derive_components(scope: str, stage: str) -> list[str]:
    normalized = scope.lower()
    components = ["body"]
    if stage == "draft" and "body-only draft" in normalized:
        return components
    if "full-deliverable" in normalized or stage == "final":
        for item in ("cover", "table-of-contents"):
            if item not in components:
                components.append(item)
    keyword_map = {
        "append": "appendices",
        "glossary": "glossary",
        "figure list": "figure-list",
        "table list": "table-list",
        "attachment": "attachments-manifest",
    }
    for needle, component in keyword_map.items():
        if needle in normalized and component not in components:
            components.append(component)
    return components


def resolve_job(brief: dict, profile: dict, stage: str) -> dict:
    blockers: list[str] = []
    warnings: list[str] = []
    assumptions: list[str] = []

    draft_missing = missing_fields(brief, REQUIRED_DRAFT_FIELDS)
    if draft_missing:
        blockers.extend(f"missing draft field: {field}" for field in draft_missing)

    if stage == "final":
        final_missing = missing_fields(brief, REQUIRED_FINAL_FIELDS)
        if final_missing:
            blockers.extend(f"missing final field: {field}" for field in final_missing)
        if brief.get("delivery_stage", "").strip().lower() != "final":
            blockers.append("delivery_stage is not set to final")
        if profile.get("needs_confirmation") is True:
            blockers.append("format profile still requires confirmation")

    scope = brief.get("completeness_scope", "body-only draft")
    components = derive_components(scope, stage)

    review_mode = brief.get("review_mode", "clean-copy")
    if review_mode == "clean-copy" and brief.get("output_mode") == "edit-existing-docx":
        warnings.append("editing an existing docx as clean-copy may hide review history")

    if scope == "body-only draft" and stage == "final":
        warnings.append("final stage with body-only draft scope will generate a minimal package")

    if not brief.get("cleanup_rule"):
        assumptions.append("default cleanup rule should remove working notes from final body")

    return {
        "target_stage": stage,
        "ready": not blockers,
        "blockers": blockers,
        "warnings": warnings,
        "assumptions": assumptions,
        "package_components": components,
        "review_artifact_mode": review_mode,
        "cleanup_rule": brief.get("cleanup_rule", ""),
        "format_authority": brief.get("format_authority", profile.get("format_authority", "")),
        "file_naming_and_version": brief.get("file_naming_and_version", ""),
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Word Job Resolution",
        "",
        f"- Target stage: {report['target_stage']}",
        f"- Ready: {'yes' if report['ready'] else 'no'}",
        f"- Review artifact mode: {report['review_artifact_mode']}",
        f"- Format authority: {report['format_authority'] or '[unknown]'}",
        f"- File naming and version: {report['file_naming_and_version'] or '[to confirm]'}",
        f"- Cleanup rule: {report['cleanup_rule'] or '[to confirm]'}",
        "",
        "## Package components",
        "",
    ]
    for component in report["package_components"]:
        lines.append(f"- {component}")
    lines.extend(["", "## Blockers", ""])
    if report["blockers"]:
        for blocker in report["blockers"]:
            lines.append(f"- {blocker}")
    else:
        lines.append("- None")
    lines.extend(["", "## Warnings", ""])
    if report["warnings"]:
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    else:
        lines.append("- None")
    lines.extend(["", "## Assumptions", ""])
    if report["assumptions"]:
        for assumption in report["assumptions"]:
            lines.append(f"- {assumption}")
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def emit(text: str, out: str | None) -> None:
    if out:
        Path(out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def main() -> int:
    args = parse_args()
    brief = load_json(args.delivery_brief)
    profile = load_json(args.format_profile)
    report = resolve_job(brief, profile, args.stage)
    if args.format == "json":
        text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    else:
        text = render_markdown(report)
    emit(text, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
