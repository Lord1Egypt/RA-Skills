"""The single compile entry (D2): sources [+ optional LLM IR] -> deck.pptx.

Stage order (all deterministic, no LLM anywhere):
  parse -> [validate + provenance + coverage] -> policy -> layout ->
  render-plan self-check -> QA (fail-closed) -> build -> artifacts

Degradation ladder (D5): an invalid or unverifiable LLM IR falls back to
the extractive IR — the pipeline never exits empty-handed; every fallback
and bound is recorded in the decision trace outcomes.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from . import __version__
from .coverage import coverage_report
from .extractive_ir import build_extractive_ir
from .layout import layout_deck
from .policy import decide_deck, decisions_to_trace, select_style_pack
from .pptx_builder import build_pptx
from .pptxgenjs_builder import build_pptx as build_pptx_js, available as pptxgenjs_available
from .provenance import verify_ir
from .qa_plan import check_plan
from .structural_parser import parse_source
from .style_pack import load_style_pack

_SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"


def _canonical_sha(document: dict) -> str:
    return hashlib.sha256(
        json.dumps(document, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def _subset_validate(document: dict, schema_file: str) -> list[dict]:
    """Reuse the skill's stdlib schema-subset validator."""
    scripts_dir = str(_SCHEMA_DIR.parent / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import validate_contracts  # noqa: PLC0415

    schema = json.loads((_SCHEMA_DIR / schema_file).read_text(encoding="utf-8"))
    return validate_contracts.validate_schema_subset(
        document, schema, Path(schema_file), True)


def compile_deck(*, sources: list[tuple[str, str, str]], ir_path: str | None = None,
                 style_path: str | None = None, output_dir: str,
                 degrade_on_error: bool = True,
                 allow_content_truncation: bool = True,
                 refine_spec_path: str | None = None,
                 final_delivery: bool = False) -> dict:
    """sources: [(source_id, type, path)]. Returns the compile report."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    docs, meta = {}, {}
    for source_id, source_type, path in sources:
        text = Path(path).read_text(encoding="utf-8")
        docs[source_id] = parse_source(text, source_type, source_id)
        meta[source_id] = {"type": source_type, "path": path}

    report: dict = {"stages": [], "degradations": [], "ir_origin": None}
    if final_delivery and not ir_path:
        report.update(
            ok=False,
            stage="model_authoring",
            errors=[{
                "code": "MODEL_AUTHORING_REQUIRED",
                "message": "Final delivery requires a model-authored, source-backed IR.",
            }],
        )
        (out / "compile-result.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return report

    # ---- IR acquisition with degradation ladder --------------------------
    ir = None
    ir_findings: list = []
    if ir_path:
        candidate = json.loads(Path(ir_path).read_text(encoding="utf-8"))
        schema_errors = _subset_validate(candidate, "v4/presentation-ir.schema.json")
        provenance_errors = [] if schema_errors else verify_ir(candidate, docs)
        ir_findings = [
            {"stage": "schema", **e} for e in schema_errors
        ] + [{"stage": "provenance", **e} for e in provenance_errors]
        if not ir_findings:
            ir, report["ir_origin"] = candidate, "provided"
        elif not degrade_on_error or final_delivery:
            report.update(ok=False, stage="ir_validation", errors=ir_findings)
            (out / "compile-result.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            return report
    if ir is None:
        first_id = sources[0][0]
        extraction = build_extractive_ir(docs[first_id], source_meta=meta[first_id])
        ir = extraction["ir"]
        report["ir_origin"] = "extractive_fallback" if ir_path else "extractive"
        if ir_path:
            report["degradations"].append(
                {"kind": "extractive_ir_fallback", "detail_code": "ir_rejected"})
            report["ir_rejection_errors"] = ir_findings
        report["extraction_warnings"] = extraction["warnings"]
        if any(warning.startswith("deck truncated from ") for warning in extraction["warnings"]):
            report.update(
                ok=False,
                stage="source_capacity",
                errors=[{
                    "code": "STRUCTURED_IR_REQUIRED",
                    "message": "The source exceeds extractive fallback page capacity; provide a structured, source-anchored IR.",
                }],
            )
            (out / "ir.json").write_text(
                json.dumps(ir, ensure_ascii=False, indent=2), encoding="utf-8")
            (out / "compile-result.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            return report
    report["stages"].append("ir")

    from .speaker_notes import validate_speaker_notes  # noqa: PLC0415
    notes_contract = validate_speaker_notes(
        ir, require_body_notes=final_delivery,
    )
    report["speaker_notes"] = {"contract": notes_contract}
    if final_delivery and notes_contract["status"] != "pass":
        report.update(
            ok=False,
            stage="speaker_notes",
            errors=notes_contract["issues"],
        )
        (out / "compile-result.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return report
    from .model_authored_quality import evaluate_model_authored_quality  # noqa: PLC0415
    authored_quality = evaluate_model_authored_quality(
        ir, require_assertions=final_delivery,
    )
    report["model_authored_quality"] = authored_quality
    if final_delivery and authored_quality["status"] != "pass":
        report.update(
            ok=False,
            stage="model_authored_quality",
            errors=authored_quality["issues"],
        )
        (out / "compile-result.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return report

    # P12-refine: apply a compile-time refine spec (user chose refinement at
    # generation time). Applied BEFORE chart inference so refine intent wins.
    if refine_spec_path:
        from .refine_spec import apply_refine_spec, load_refine_spec  # noqa: PLC0415
        spec = load_refine_spec(refine_spec_path)
        refine_report = apply_refine_spec(ir, spec)
        report["refine_spec"] = refine_report
        report["stages"].append("refine_spec")

    # P10: chart auto-inference — when the model didn't write chart/diagram_ir,
    # infer one from metric blocks + relations. Never overrides what the model
    # deliberately provided.
    from .chart_inference import infer_charts  # noqa: PLC0415
    infer_charts(ir, docs)
    report["stages"].append("chart_inference")

    coverage = coverage_report(ir, docs)
    report["coverage"] = coverage
    report["stages"].append("coverage")

    # ---- policy / layout / plan ------------------------------------------
    if style_path is None:
        style_path = str(Path(__file__).resolve().parents[1] / "styles"
                         / f"{select_style_pack(ir)}.json")
    style = load_style_pack(style_path)
    decisions = decide_deck(ir)
    # P11: apply L1/L2 autonomy proposals (engine-validated, QA-gated,
    # fall back to the rule archetype when rejected).
    from .proposal_apply import apply_proposals  # noqa: PLC0415
    autonomy_report = apply_proposals(ir, decisions)
    report["autonomy"] = autonomy_report
    report["stages"].append("autonomy")
    laid = layout_deck(ir, decisions, style, docs)
    report["degradations"].extend(laid["degradations"])
    report["stages"].append("layout")

    truncations = [
        item for item in report["degradations"]
        if item.get("kind") == "content_truncation"
    ]
    if truncations and (not allow_content_truncation or final_delivery):
        report.update(
            ok=False,
            stage="content_capacity",
            errors=[{
                "code": "CONTENT_TRUNCATION_FORBIDDEN",
                "count": len(truncations),
                "slide_ids": sorted({item.get("slide_id") for item in truncations if item.get("slide_id")}),
            }],
        )
        (out / "ir.json").write_text(
            json.dumps(ir, ensure_ascii=False, indent=2), encoding="utf-8")
        (out / "compile-result.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return report

    ir_sha = _canonical_sha(ir)
    run_id = f"run-{ir_sha[:12]}"
    plan = {
        "schema_version": "4.0.0",
        "plan": {"plan_id": f"plan-{ir_sha[:12]}", "engine_version": __version__,
                 "ir_sha256": ir_sha, "trace_run_id": run_id,
                 "style_pack": {"pack_id": style.pack_id, "version": style.schema_version}},
        "canvas": laid["canvas"],
        "fonts_used": laid["fonts_used"],
        "slides": laid["slides"],
    }
    plan_errors = _subset_validate(plan, "v4/render-plan.schema.json")
    if plan_errors:
        report.update(ok=False, stage="render_plan_selfcheck",
                      errors=[dict(e) for e in plan_errors[:20]])
        (out / "render-plan.json").write_text(
            json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        (out / "compile-result.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return report
    report["stages"].append("plan_selfcheck")

    qa = check_plan(plan)
    report["qa"] = qa
    report["stages"].append("qa")

    trace = decisions_to_trace(
        decisions, run_id=run_id, engine_version=__version__, ir_sha256=ir_sha,
        style_pack={"pack_id": style.pack_id, "version": style.schema_version})
    trace["outcomes"] = {
        "qa_error_count": qa["error_count"],
        "repair_rounds": 0,
        "autonomy": autonomy_report,
        "degradations": [
            {k: v for k, v in d.items() if k in ("kind", "slide_id", "detail_code")}
            for d in report["degradations"]],
    }
    trace_errors = _subset_validate(trace, "v4/decision-trace.schema.json")
    if trace_errors:  # engine bug, not user error — surface loudly
        report.setdefault("internal_warnings", []).extend(
            dict(e) for e in trace_errors[:5])

    (out / "render-plan.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "decision-trace.json").write_text(
        json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "ir.json").write_text(
        json.dumps(ir, ensure_ascii=False, indent=2), encoding="utf-8")

    if qa["status"] != "pass":
        report.update(ok=False, stage="qa")
        (out / "compile-result.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return report

    # Builder decision: PptxGenJS is the primary renderer (v3 visual parity);
    # python-pptx is the fallback when the Node runtime is unavailable.
    if pptxgenjs_available():
        pptx_path = build_pptx_js(plan, out / "deck.pptx")
        report["builder"] = "pptxgenjs"
    else:
        pptx_path = build_pptx(plan, out / "deck.pptx")
        report["builder"] = "python_pptx"
        report.setdefault("degradations", []).append(
            {"kind": "builder_fallback", "detail_code": "pptxgenjs_unavailable"})
    report["stages"].append("build")
    from .speaker_notes import inspect_speaker_notes  # noqa: PLC0415
    notes_inspection = inspect_speaker_notes(
        pptx_path,
        required_slide_indices=(
            list(range(2, len(plan["slides"]) + 1)) if final_delivery else []
        ),
    )
    report["speaker_notes"]["inspection"] = notes_inspection
    if final_delivery and notes_inspection["status"] != "pass":
        report.update(ok=False, stage="speaker_notes_readback", errors=[{
            "code": "SPEAKER_NOTES_READBACK_FAILED",
            "missing_slide_indices": notes_inspection["missing_slide_indices"],
        }])
        (out / "compile-result.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return report
    report.update(ok=True, pptx=str(pptx_path),
                  slide_count=len(plan["slides"]),
                  render_plan=str(out / "render-plan.json"),
                  decision_trace=str(out / "decision-trace.json"))
    (out / "compile-result.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
