#!/usr/bin/env python3
"""v4 rubric scorer: map v4 engine artifacts to the shared 6-dim rubric.

The v4 engine emits ``compile-result.json`` (qa/coverage/degradations),
``render-plan.json`` (slide geometry), and ``ir.json`` (Presentation IR v4).
This module maps those to the automatic-evidence inputs that the v3 scorer
(``scripts/score_deck.build_rubric_score``) already consumes, so the SAME
six-dimension rubric is scored for v4 producers:

  - title_role_and_message_quality
  - content_fidelity
  - expression_architecture
  - page_composition
  - component_craft
  - editability_hygiene

Golden anchoring uses the exact same mechanism as v3: add a
``reference-rubric.json`` (human/model-authored and evidence-bound) to a case
and pass ``use_reference_rubric=True``. Without it, the score is provisional
automatic evidence only and ``manual_review_required`` stays true — this is
intentional, not a failure.

This module never calls the renderer and never fabricates a trusted score:
metrics that need real-render readback (color drift, rasterized table/chart,
whole-slide raster, render success) are simply left absent, which the scorer
treats as zero (no penalty) and the evidence map reports honestly.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from score_deck import build_rubric_score, load_json, write_json  # noqa: E402

# v4 plan-level QA error code -> the rubric issue code the v3 scorer counts.
V4_TO_ISSUE_CODE = {
    "SLIDE_EMPTY": "PPTX_BLANK_SLIDE",
    "ELEMENT_OUT_OF_BOUNDS": "PPTX_TEXT_OUT_OF_BOUNDS",
    "TEXT_OVERFLOW_RISK": "TEXT_OVERFLOW_RISK",
}

_GENERIC_TITLES = {
    "overview", "summary", "introduction", "background", "next steps",
    "key points", "conclusion", "agenda", "appendix", "thank you",
    "概述", "概览", "背景", "介绍", "简介", "总结", "结论", "目录",
    "前言", "附录", "结束语", "致谢",
}


def _section_ratio(coverage: dict[str, Any]) -> Optional[float]:
    sources = coverage.get("sources")
    if not isinstance(sources, list) or not sources:
        return None
    ratios = [
        s.get("section_ratio")
        for s in sources
        if isinstance(s, dict) and isinstance(s.get("section_ratio"), (int, float))
    ]
    return min(ratios) if ratios else None


def qa_report_from_v4(
    compile_result: dict[str, Any],
    render_plan: Optional[dict[str, Any]],
    ir: Optional[dict[str, Any]],
) -> dict[str, Any]:
    """Build a score_deck-compatible qa_report from v4 artifacts."""
    qa = compile_result.get("qa", {}) if isinstance(compile_result.get("qa"), dict) else {}
    errors = qa.get("errors", []) if isinstance(qa.get("errors"), list) else []
    issues: list[dict[str, Any]] = []
    for err in errors:
        if not isinstance(err, dict):
            continue
        issue_code = V4_TO_ISSUE_CODE.get(str(err.get("code") or ""))
        if issue_code:
            issues.append({
                "issue_code": issue_code,
                "severity": "error",
                "detail": f"{err.get('slide_id')}:{err.get('element_id')}",
            })

    metrics: dict[str, Any] = {
        "source_coverage_ratio": _section_ratio(compile_result.get("coverage", {})),
        "qa_error_count": int(qa.get("error_count", 0)),
        "qa_fatal_count": 0,
    }

    if isinstance(render_plan, dict):
        slides = render_plan.get("slides")
        if isinstance(slides, list):
            counts = [
                len(s.get("elements", [])) if isinstance(s, dict) else 0
                for s in slides
            ]
            metrics["average_object_count"] = (sum(counts) / len(counts)) if counts else 0
            all_elements = [
                e for s in slides if isinstance(s, dict)
                for e in s.get("elements", []) if isinstance(e, dict)
            ]
            total_el = len(all_elements)
            # Native = anything not a rasterized image. v4 renders message
            # content as editable shapes/text/tables/charts, so a shape card
            # (fact/metric/list) is editable, not rasterized.
            image_el = sum(1 for e in all_elements if e.get("type") == "image")
            metrics["native_text_ratio"] = ((total_el - image_el) / total_el) if total_el else 1.0
            metrics["rasterized_table_count"] = sum(
                1 for e in all_elements
                if e.get("type") == "image" and e.get("semantic_role") == "table")
            metrics["rasterized_chart_count"] = sum(
                1 for e in all_elements
                if e.get("type") == "image" and e.get("semantic_role") == "chart")
            metrics["whole_slide_raster_count"] = sum(
                1 for s in slides if isinstance(s, dict) and s.get("elements")
                and all(isinstance(e, dict) and e.get("type") in ("image", "connector")
                        for e in s["elements"]))

    if isinstance(ir, dict):
        slides = ir.get("slides", [])
        if isinstance(slides, list):
            generic = 0
            unsupported = 0
            for slide in slides:
                if not isinstance(slide, dict):
                    continue
                title = str(slide.get("title") or "").strip()
                if title and title.lower() in _GENERIC_TITLES:
                    generic += 1
                has_message = bool(str(slide.get("message") or "").strip())
                blocks = slide.get("blocks", []) if isinstance(slide.get("blocks"), list) else []
                has_synthesis = any(
                    isinstance(b, dict) and b.get("role") in
                    ("insight", "risk", "recommendation", "context")
                    for b in blocks
                )
                if not has_message and not has_synthesis:
                    unsupported += 1
            metrics["generic_judgment_title_count"] = generic
            metrics["unsupported_judgment_count"] = unsupported

    status = "fail" if qa.get("error_count") else ("warning" if qa.get("warnings") else "pass")
    return {"status": status, "metrics": metrics, "issues": issues}


def score_v4(
    *,
    case_id: str,
    compile_result: dict[str, Any],
    render_plan: Optional[dict[str, Any]] = None,
    ir: Optional[dict[str, Any]] = None,
    case_path: Optional[Path] = None,
    use_reference_rubric: bool = False,
    reference_rubric: Optional[str] = None,
    pptx_path: Optional[Path] = None,
    render_report: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    case: dict[str, Any] = {"case_id": case_id, "expected_metrics": {}}
    if reference_rubric:
        case["reference_rubric"] = reference_rubric
    qa_report = qa_report_from_v4(compile_result, render_plan, ir)
    if render_report is not None:
        qa_report["evidence"] = {"render_report": render_report}
    return build_rubric_score(
        case=case,
        case_path=case_path or ROOT,
        ppt_ir=None,
        qa_report=qa_report,
        build_manifest=None,
        use_reference_rubric=use_reference_rubric,
        pptx_path=pptx_path,
    )


def provisional_summary(score: dict[str, Any]) -> dict[str, Any]:
    prov = {
        str(item.get("dimension")): item.get("provisional_score")
        for item in score.get("dimensions", []) if isinstance(item, dict)
    }
    trusted = {
        str(item.get("dimension")): item.get("score")
        for item in score.get("dimensions", []) if isinstance(item, dict)
    }
    is_trusted = not bool(score.get("manual_review_required"))
    return {
        "case_id": score.get("case_id"),
        "rubric_quality_status": score.get("rubric_quality_status"),
        "hard_gate_status": score.get("hard_gate_status"),
        "manual_review_required": score.get("manual_review_required"),
        "scores_source": "reference_rubric" if is_trusted else "automatic_provisional",
        "total": sum(v for v in (trusted if is_trusted else prov).values() if isinstance(v, int)),
        "dimensions": trusted if is_trusted else prov,
        "provisional_total": sum(v for v in prov.values() if isinstance(v, int)),
        "provisional_dimensions": prov,
    }


def _main(argv: Optional[list[str]] = None) -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--compile-result", required=True)
    parser.add_argument("--render-plan")
    parser.add_argument("--ir")
    parser.add_argument("--reference-rubric")
    parser.add_argument("--pptx")
    parser.add_argument("--render-report")
    parser.add_argument("--json-out")
    args = parser.parse_args(argv)

    def read(path: Optional[str]) -> Optional[dict[str, Any]]:
        if not path:
            return None
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    score = score_v4(
        case_id=args.case_id,
        compile_result=read(args.compile_result) or {},
        render_plan=read(args.render_plan),
        ir=read(args.ir),
        reference_rubric=args.reference_rubric,
        use_reference_rubric=bool(args.reference_rubric),
        pptx_path=Path(args.pptx) if args.pptx else None,
        render_report=read(args.render_report),
    )
    if args.json_out:
        write_json(score, Path(args.json_out))
    print(json.dumps(provisional_summary(score), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
