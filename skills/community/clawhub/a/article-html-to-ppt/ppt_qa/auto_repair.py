from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any, Callable, Optional

from .verifier import build_verification_report, write_json


RepairHandler = Callable[[Path, dict[str, Any]], dict[str, Any]]


SAFE_REPAIR_HANDLERS: dict[str, RepairHandler] = {}
VISUAL_RENDER_CODES = {
    "RENDER_BLANK_SLIDE",
    "RENDER_NEAR_BLANK_SLIDE",
    "RENDER_ASPECT_RATIO_MISMATCH",
    "RENDER_SIZE_MISMATCH",
    "TEXT_OVERFLOW_RISK",
    "OBJECT_OVERLAP",
}


def repair_deck(
    source_pptx: Path,
    output_pptx: Path,
    *,
    initial_report: dict[str, Any],
    max_iterations: int = 1,
    verifier_kwargs: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    if max_iterations < 1:
        raise ValueError("max_iterations must be >= 1")
    output_pptx.parent.mkdir(parents=True, exist_ok=True)
    if source_pptx.resolve() != output_pptx.resolve():
        shutil.copy2(str(source_pptx), str(output_pptx))
    verifier_kwargs = dict(verifier_kwargs or {})
    iterations: list[dict[str, Any]] = []
    current_report = initial_report
    for iteration in range(1, max_iterations + 1):
        attempts = _attempt_registered_repairs(output_pptx, current_report)
        iterations.append(
            {
                "iteration": iteration,
                "attempted_repairs": attempts,
                "remaining_issue_count_before_recheck": len(current_report.get("issues", []) or []),
            }
        )
        if not attempts:
            break
        current_report = build_verification_report(output_pptx, **verifier_kwargs)
    remaining_issues = current_report.get("issues", []) or []
    report = {
        "schema_version": "1.0",
        "source_pptx": str(source_pptx),
        "output_pptx": str(output_pptx),
        "max_iterations": max_iterations,
        "safe_repair_codes": sorted(SAFE_REPAIR_HANDLERS),
        "iterations": iterations,
        "remaining_issues": remaining_issues,
        "status": "repaired" if not remaining_issues and any(item["attempted_repairs"] for item in iterations) else "no_safe_repairs_available",
        "notes": [
            "No visual or render issue is marked repaired without a real renderer and a recheck.",
            "Unregistered issue codes are reported for manual repair instead of being mutated heuristically.",
        ],
    }
    if any(issue.get("issue_code") == "RENDER_ENGINE_UNAVAILABLE" for issue in remaining_issues if isinstance(issue, dict)):
        report["status"] = "renderer_unavailable"
    return report


def write_repair_report(report: dict[str, Any], output_path: Path) -> None:
    write_json(report, output_path)


def _attempt_registered_repairs(pptx_path: Path, report: dict[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for issue in report.get("issues", []) or []:
        if not isinstance(issue, dict):
            continue
        code = str(issue.get("issue_code", ""))
        handler = SAFE_REPAIR_HANDLERS.get(code)
        if handler is None:
            attempts.append(_skipped_attempt(code, issue))
            continue
        try:
            result = handler(pptx_path, issue)
            attempts.append(
                {
                    "issue_code": code,
                    "issue_id": issue.get("issue_id"),
                    "status": "attempted",
                    "result": result,
                }
            )
        except Exception as exc:
            attempts.append(
                {
                    "issue_code": code,
                    "issue_id": issue.get("issue_id"),
                    "status": "failed",
                    "message": str(exc),
                }
            )
    return [attempt for attempt in attempts if attempt["status"] != "skipped_unregistered" or attempt.get("manual_reason")]


def _skipped_attempt(code: str, issue: dict[str, Any]) -> dict[str, Any]:
    reason = "No safe deterministic repair is registered for this issue code."
    if code == "RENDER_ENGINE_UNAVAILABLE":
        reason = "Renderer availability is an environment capability, not a deck mutation."
    elif code in VISUAL_RENDER_CODES or str(issue.get("category")) == "render":
        reason = "Visual/render issues require rendered evidence and authoring review; no blind repair was attempted."
    return {
        "issue_code": code,
        "issue_id": issue.get("issue_id"),
        "slide_id": issue.get("slide_id"),
        "object_id": issue.get("object_id"),
        "status": "skipped_unregistered",
        "manual_reason": reason,
    }
