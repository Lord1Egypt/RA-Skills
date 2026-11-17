#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


PROFILES = {"fast", "standard", "premium"}

ARTIFACTS_BY_PROFILE: dict[str, list[str]] = {
    "fast": [
        ".ppt-work/analysis/content-lock.md",
        ".ppt-work/contracts/ppt-ir.json",
        ".ppt-work/contracts/style-contract.json",
        ".ppt-work/contracts/delivery-plan.json",
        ".ppt-work/contracts/build-manifest.json",
        "deck.pptx",
        "delivery-manifest.json",
    ],
    "standard": [
        ".ppt-work/analysis/content-lock.md",
        ".ppt-work/analysis/storyboard.md",
        ".ppt-work/contracts/ppt-ir.json",
        ".ppt-work/contracts/style-contract.json",
        ".ppt-work/contracts/asset-manifest.json",
        ".ppt-work/contracts/delivery-plan.json",
        ".ppt-work/contracts/build-manifest.json",
        ".ppt-work/qa/qa-report.json",
        ".ppt-work/renders/representative-renders/",
        "deck.pptx",
        "deck-preview.pdf",
        "verification-report.md",
        "delivery-manifest.json",
    ],
    "premium": [
        ".ppt-work/analysis/content-lock.md",
        ".ppt-work/analysis/storyboard.md",
        ".ppt-work/contracts/ppt-ir.json",
        ".ppt-work/contracts/style-contract.json",
        ".ppt-work/contracts/asset-manifest.json",
        ".ppt-work/contracts/delivery-plan.json",
        ".ppt-work/contracts/build-manifest.json",
        ".ppt-work/qa/qa-report.json",
        ".ppt-work/references/visual-references/",
        ".ppt-work/renders/full-renders/",
        ".ppt-work/renders/contact-sheet.png",
        ".ppt-work/qa/repair-cycles/",
        ".ppt-work/qa/benchmark-score.json",
        "deck.pptx",
        "deck-preview.pdf",
        "verification-report.md",
        "delivery-manifest.json",
    ],
}

GATES_BY_PROFILE: dict[str, list[str]] = {
    "fast": [
        "contracts_valid",
        "pptx_package_readable",
        "no_whole_slide_raster",
        "no_missing_media",
    ],
    "standard": [
        "contracts_valid",
        "pptx_package_readable",
        "structural_inspection",
        "editability_check",
        "color_contract_check",
        "representative_render_when_available",
        "qa_error_count_zero",
    ],
    "premium": [
        "contracts_valid",
        "pptx_package_readable",
        "full_render",
        "read_back",
        "complete_qa",
        "auto_repair_attempted",
        "rubric_score_at_least_14",
        "qa_error_count_zero",
        "all_fallbacks_disclosed",
    ],
}

ALLOWED_SKIPS_BY_PROFILE: dict[str, list[str]] = {
    "fast": ["storyboard", "asset_manifest_when_unused", "render", "benchmark", "verification_report"],
    "standard": ["full_render", "benchmark"],
    "premium": [],
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return data


def explicit_profile(requirements: dict[str, Any]) -> str | None:
    for key in ("production_profile", "profile", "requested_profile", "profile_override"):
        value = requirements.get(key)
        if isinstance(value, str) and value.lower() in PROFILES:
            return value.lower()

    user_request = str(requirements.get("user_request", "")).lower()
    if re.search(r"\b(fast|quick|quickly|draft|rough)\b", user_request):
        return "fast"
    if re.search(r"\b(premium profile|profile premium|premium delivery|premium validation|premium qa|premium gate|premium gates|final|full validation|complete validation|production ready|public release)\b", user_request):
        return "premium"
    if re.search(r"\bstandard\b", user_request):
        return "standard"
    return None


def _norm(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip().lower()


def _intensity(value: Any) -> int:
    text = _norm(value)
    if text in {"very_high", "high", "strict", "strong", "complex", "public", "premium"}:
        return 2
    if text in {"medium", "moderate", "normal", "standard"}:
        return 1
    if text in {"low", "simple", "none", "false", ""}:
        return 0
    if isinstance(value, (int, float)):
        return 2 if value >= 0.75 else 1 if value >= 0.35 else 0
    return 0


def diagram_complexity(requirements: dict[str, Any], ppt_ir: dict[str, Any]) -> int:
    explicit = _intensity(requirements.get("diagram_complexity"))
    if explicit:
        return explicit
    max_score = 0
    for slide in ppt_ir.get("slides", []) or []:
        if not isinstance(slide, dict):
            continue
        for obj in slide.get("objects", []) or []:
            if not isinstance(obj, dict):
                continue
            complexity = obj.get("complexity") if isinstance(obj.get("complexity"), dict) else {}
            score = int(complexity.get("node_count", 0) or 0) + int(complexity.get("edge_count", 0) or 0)
            if obj.get("primary_expression") == "relationship_visual" or obj.get("component_type") in {"ecosystem_map", "architecture_diagram"}:
                score += 5
            max_score = max(max_score, score)
    if max_score >= 18:
        return 2
    if max_score >= 8:
        return 1
    return 0


def source_complexity(requirements: dict[str, Any], ppt_ir: dict[str, Any]) -> int:
    explicit = _intensity(requirements.get("source_complexity"))
    if explicit:
        return explicit
    slide_count = len([slide for slide in ppt_ir.get("slides", []) or [] if isinstance(slide, dict)])
    source_count = len([src for src in ppt_ir.get("sources", []) or [] if isinstance(src, dict)])
    if slide_count >= 14 or source_count >= 8:
        return 2
    if slide_count >= 6 or source_count >= 3:
        return 1
    return 0


def recommend_profile(requirements: dict[str, Any], ppt_ir: dict[str, Any]) -> dict[str, Any]:
    override = explicit_profile(requirements)
    reason_codes: list[str] = []
    if override:
        reason_codes.append({
            "fast": "USER_REQUESTED_FAST",
            "standard": "USER_REQUESTED_STANDARD",
            "premium": "USER_REQUESTED_PREMIUM",
        }[override])
        return profile_result(override, 0.99, reason_codes, override_applied=True)

    public_or_internal = _norm(requirements.get("public_or_internal") or requirements.get("audience"))
    delivery_value = _intensity(requirements.get("delivery_value"))
    editability = _intensity(requirements.get("editability_requirement"))
    brand = _intensity(requirements.get("brand_requirement"))
    deadline = _norm(requirements.get("deadline_mode"))
    source = source_complexity(requirements, ppt_ir)
    diagrams = diagram_complexity(requirements, ppt_ir)

    score = 0
    if any(word in public_or_internal for word in ("public", "external", "client", "customer", "conference")):
        score += 3
        reason_codes.append("PUBLIC_DELIVERY")
    if delivery_value >= 2:
        score += 2
    if source >= 2:
        score += 1
        reason_codes.append("COMPLEX_SOURCE")
    if diagrams >= 2:
        score += 2
        reason_codes.append("COMPLEX_DIAGRAMS")
    if editability >= 2:
        score += 1
        reason_codes.append("HIGH_EDITABILITY_REQUIREMENT")
    if brand >= 2:
        score += 2
        reason_codes.append("BRAND_ASSETS_REQUIRED")
    if deadline in {"fast", "urgent", "same_day", "quick"}:
        score -= 2
        reason_codes.append("USER_REQUESTED_FAST")

    internal = any(word in public_or_internal for word in ("internal", "team", "draft"))
    simple = source == 0 and diagrams == 0 and delivery_value == 0 and brand == 0
    if internal and simple:
        score -= 2
        reason_codes.append("INTERNAL_DRAFT")
    if simple:
        reason_codes.append("LOW_RISK_SIMPLE_CONTENT")

    if score >= 4:
        selected = "premium"
    elif score <= -1:
        selected = "fast"
    else:
        selected = "standard"
    confidence = min(0.95, 0.62 + abs(score) * 0.07)
    return profile_result(selected, confidence, reason_codes or ["LOW_RISK_SIMPLE_CONTENT"], override_applied=False)


def profile_result(profile: str, confidence: float, reason_codes: list[str], *, override_applied: bool) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "selected_profile": profile,
        "confidence": round(confidence, 2),
        "override_applied": override_applied,
        "reason_codes": reason_codes,
        "required_artifacts": ARTIFACTS_BY_PROFILE[profile],
        "required_gates": GATES_BY_PROFILE[profile],
        "allowed_skips": ALLOWED_SKIPS_BY_PROFILE[profile],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve fast/standard/premium production profile for article-html-to-ppt.")
    parser.add_argument("--requirements", type=Path, required=True)
    parser.add_argument("--ppt-ir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--json-output", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        result = recommend_profile(load_json(args.requirements), load_json(args.ppt_ir))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        if args.json_output:
            print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(f"resolve_production_profile: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
