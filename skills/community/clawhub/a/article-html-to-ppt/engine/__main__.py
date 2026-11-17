"""Engine CLI.

Usage:
  python3 -m engine compile    --source id:type:path [--ir IR.json]
                               [--style PACK.json] --output-dir DIR
                               [--no-degrade]
  python3 -m engine parse      --source id:type:path [--json-out FILE]
  python3 -m engine extract-ir --source id:type:path [--json-out FILE]
  python3 -m engine verify     --ir IR.json --source id:type:path [...]
  python3 -m engine coverage   --ir IR.json --source id:type:path [...]
  python3 -m engine plan-bespoke --request REQUEST.json --ir IR.json
                                  --content-assessment ASSESSMENT.json
                                  [--template-pptx REFERENCE.pptx]
  python3 -m engine author-bespoke --script AUTHOR.py --manifest MANIFEST.json
                                    --ir IR.json --output-dir DIR
                                    [--template-pptx REFERENCE.pptx]
                                    [--source ID:TYPE:PATH]
                                    [--render-engine ENGINE]
  python3 -m engine review-bespoke --authoring-report REPORT.json --review REVIEW.json
  python3 -m engine review-template --strict-report REPORT.json --review REVIEW.json
  python3 -m engine strict-template --request REQUEST.json --template-pptx TEMPLATE.pptx
                                    --plan STRICT-PLAN.json --ir IR.json
                                    [--component-atlas ATLAS.json]
                                    --source ID:TYPE:PATH --output-pptx OUTPUT.pptx
  python3 -m engine component-atlas --template-pptx TEMPLATE.pptx
                                     --review REVIEW.json [--json-out ATLAS.json]
  python3 -m engine component-inventory --template-pptx TEMPLATE.pptx
                                         --component-atlas ATLAS.json
                                         [--json-out INVENTORY.json]
  python3 -m engine compose-components --component-atlas ATLAS.json
                                        --composition COMPOSITION.json
                                        [--json-out STRICT-PLAN.json]
  python3 -m engine plan-manuscript-components --component-atlas ATLAS.json
                                                 --content-bindings BINDINGS.json
                                                 --storyboard STORYBOARD.json
                                                 [--json-out COMPOSITION.json]
  python3 -m engine plan-model-template-components --ir IR.json
                                                    --component-atlas ATLAS.json
                                                    --model-plan MODEL-PLAN.json
                                                    [--json-out COMPOSITION.json]

`compile` is the single entry (D2): parse -> validate/provenance ->
policy -> layout -> QA -> deck.pptx + render-plan + decision-trace.
The other subcommands expose individual stages for debugging and repair
loops. `--source` takes `source_id:type:path` (type markdown|html|text)
and may repeat. Exit codes: 0 ok, 1 findings/failure, 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .coverage import coverage_report
from .evidence_outline import build_evidence_outline
from .extractive_ir import build_extractive_ir
from .provenance import verify_ir
from .structural_parser import parse_source


def _load_sources(specs: list[str]) -> tuple[dict, dict]:
    docs, meta = {}, {}
    for spec in specs:
        parts = spec.split(":", 2)
        if len(parts) != 3:
            raise SystemExit(f"--source expects source_id:type:path, got '{spec}'")
        source_id, source_type, path = parts
        text = Path(path).read_text(encoding="utf-8")
        docs[source_id] = parse_source(text, source_type, source_id)
        meta[source_id] = {"type": source_type, "path": path}
    return docs, meta


def _emit(payload: dict, json_out: str | None) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if json_out:
        Path(json_out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "template":
        from .native_template.cli import main as template_main
        return template_main(argv[1:])
    if argv and argv[0] == "design":
        from .design_scene.cli import main as design_main
        return design_main(argv[1:])
    parser = argparse.ArgumentParser(prog="engine", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("parse", "extract-ir", "evidence-outline", "verify", "coverage"):
        p = sub.add_parser(name)
        p.add_argument("--source", action="append", required=True,
                       metavar="ID:TYPE:PATH")
        p.add_argument("--json-out")
        if name in ("verify", "coverage"):
            p.add_argument("--ir", required=True)

    sv = sub.add_parser("style-validate")
    sv.add_argument("--style", required=True)
    sv.add_argument("--json-out")

    c = sub.add_parser("compile")
    c.add_argument("--source", action="append", required=True, metavar="ID:TYPE:PATH")
    c.add_argument("--ir")
    c.add_argument("--style")
    c.add_argument("--output-dir", required=True)
    c.add_argument("--refine", dest="refine_spec_path",
                   help="JSON refine spec applied at generation time "
                        "(page-level composition intent per slide)")
    c.add_argument("--no-degrade", action="store_true",
                   help="fail on invalid IR instead of falling back to extraction")
    c.add_argument("--allow-content-truncation", action="store_true",
                   help="allow truncated diagnostic output; delivery CLI fails closed by default")
    c.add_argument(
        "--final-delivery",
        action="store_true",
        help="require model-authored IR, complete speaker notes, and no truncation",
    )

    rc = sub.add_parser("refine-code",
                        help="P12 Level 2: run a python-pptx refine script with QA safety net")
    rc.add_argument("--script", required=True)
    rc.add_argument("--source", action="append", required=True, metavar="ID:TYPE:PATH")
    rc.add_argument("--ir", required=True)
    rc.add_argument("--output-dir", required=True)
    rc.add_argument("--deck", help="refine an existing deck.pptx instead of building from IR")
    rc.add_argument("--high-fidelity", action="store_true",
                    help="apply content lock + real-render gate to model-authored page code")
    rc.add_argument("--render-engine", choices=["auto", "libreoffice", "powerpoint_macos", "powerpoint_windows"],
                    default="auto")

    bespoke = sub.add_parser(
        "plan-bespoke",
        help="build an independent high-capability-model authoring manifest",
    )
    bespoke.add_argument("--request", required=True)
    bespoke.add_argument("--ir", required=True)
    bespoke.add_argument("--content-assessment", required=True)
    bespoke.add_argument("--narrative-contract")
    bespoke.add_argument("--template-pptx")
    bespoke.add_argument("--json-out")

    author_bespoke = sub.add_parser(
        "author-bespoke",
        help="run an independent Bespoke author script and its non-visual delivery gates",
    )
    author_bespoke.add_argument("--script", required=True)
    author_bespoke.add_argument("--manifest", required=True)
    author_bespoke.add_argument("--ir", required=True)
    author_bespoke.add_argument("--output-dir", required=True)
    author_bespoke.add_argument("--template-pptx")
    author_bespoke.add_argument("--source", action="append", metavar="ID:TYPE:PATH")
    author_bespoke.add_argument(
        "--render-engine",
        choices=["auto", "libreoffice", "powerpoint_macos", "powerpoint_windows"],
        default="auto",
    )
    author_bespoke.add_argument("--json-out")

    review_bespoke = sub.add_parser("review-bespoke", help="validate a hash-bound external visual review")
    review_bespoke.add_argument("--authoring-report", required=True)
    review_bespoke.add_argument("--review", required=True)
    review_bespoke.add_argument("--json-out")

    review_template = sub.add_parser(
        "review-template",
        help="validate a hash-bound visual review for a strict Template candidate",
    )
    review_template.add_argument("--strict-report", required=True)
    review_template.add_argument("--review", required=True)
    review_template.add_argument("--json-out")

    strict_template = sub.add_parser(
        "strict-template",
        help="apply only declared native template operations to a hash-bound strict template",
    )
    strict_template.add_argument("--request", required=True)
    strict_template.add_argument("--template-pptx", required=True)
    strict_template.add_argument("--plan", required=True)
    strict_template.add_argument("--ir", required=True)
    strict_template.add_argument("--evidence-ledger", required=True)
    strict_template.add_argument("--content-bindings", required=True)
    strict_template.add_argument("--component-atlas")
    strict_template.add_argument("--source", action="append", required=True, metavar="ID:TYPE:PATH")
    strict_template.add_argument("--output-pptx", required=True)
    strict_template.add_argument(
        "--render-engine",
        choices=["auto", "libreoffice", "powerpoint_macos", "powerpoint_windows"],
        default="auto",
    )
    strict_template.add_argument("--json-out")
    strict_template.add_argument(
        "--final-delivery",
        action="store_true",
        help="require complete speaker notes and all final-delivery gates",
    )

    component_atlas = sub.add_parser(
        "component-atlas",
        help="resolve a reviewed native component declaration against a template",
    )
    component_atlas.add_argument("--template-pptx", required=True)
    component_atlas.add_argument("--review", required=True)
    component_atlas.add_argument("--json-out")

    component_inventory = sub.add_parser(
        "component-inventory",
        help="inventory full-template native content coverage by reviewed components",
    )
    component_inventory.add_argument("--template-pptx", required=True)
    component_inventory.add_argument("--component-atlas", required=True)
    component_inventory.add_argument("--json-out")

    component_atlas_report = sub.add_parser(
        "component-atlas-report",
        help="write human-readable suitability tables for a reviewed component atlas",
    )
    component_atlas_report.add_argument("--component-atlas", required=True)
    component_atlas_report.add_argument("--json-out")
    component_atlas_report.add_argument("--markdown-out")

    compose_components = sub.add_parser(
        "compose-components",
        help="build strict component_clone operations from semantic page slots",
    )
    compose_components.add_argument("--component-atlas", required=True)
    compose_components.add_argument("--composition", required=True)
    compose_components.add_argument("--json-out")

    plan_manuscript_components = sub.add_parser(
        "plan-manuscript-components",
        help="derive reviewed component slots and placements for a complete manuscript",
    )
    plan_manuscript_components.add_argument("--component-atlas", required=True)
    plan_manuscript_components.add_argument("--content-bindings", required=True)
    plan_manuscript_components.add_argument("--storyboard", required=True)
    plan_manuscript_components.add_argument("--evidence-ledger")
    plan_manuscript_components.add_argument("--delivery-candidate", action="store_true")
    plan_manuscript_components.add_argument("--json-out")

    plan_model_template_components = sub.add_parser(
        "plan-model-template-components",
        help="compile an explicit model-authored Template component composition",
    )
    plan_model_template_components.add_argument("--ir", required=True)
    plan_model_template_components.add_argument("--component-atlas", required=True)
    plan_model_template_components.add_argument("--model-plan", required=True)
    plan_model_template_components.add_argument("--no-intent-audit", action="store_true")
    plan_model_template_components.add_argument("--json-out")

    args = parser.parse_args(argv)

    if args.command == "plan-model-template-components":
        from .model_template_composer import build_model_template_composition

        try:
            composition = build_model_template_composition(
                json.loads(Path(args.ir).read_text(encoding="utf-8")),
                json.loads(Path(args.component_atlas).read_text(encoding="utf-8")),
                json.loads(Path(args.model_plan).read_text(encoding="utf-8")),
                enforce_intent_audit=not args.no_intent_audit,
            )
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        _emit(composition, args.json_out)
        return 0

    if args.command == "component-inventory":
        from .component_inventory import build_template_component_inventory

        try:
            atlas = json.loads(Path(args.component_atlas).read_text(encoding="utf-8"))
            inventory = build_template_component_inventory(args.template_pptx, atlas)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        _emit(inventory, args.json_out)
        return 0

    if args.command == "component-atlas-report":
        from .component_atlas_report import (
            build_component_suitability_table,
            render_component_suitability_markdown,
        )

        try:
            atlas = json.loads(Path(args.component_atlas).read_text(encoding="utf-8"))
            report = build_component_suitability_table(atlas)
            if args.markdown_out:
                Path(args.markdown_out).write_text(
                    render_component_suitability_markdown(report), encoding="utf-8",
                )
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        _emit(report, args.json_out)
        return 0

    if args.command == "plan-manuscript-components":
        from .manuscript_component_planner import build_manuscript_component_composition

        try:
            atlas = json.loads(Path(args.component_atlas).read_text(encoding="utf-8"))
            content_bindings = json.loads(
                Path(args.content_bindings).read_text(encoding="utf-8")
            )
            storyboard = json.loads(Path(args.storyboard).read_text(encoding="utf-8"))
            evidence_ledger = (
                json.loads(Path(args.evidence_ledger).read_text(encoding="utf-8"))
                if args.evidence_ledger else None
            )
            composition = build_manuscript_component_composition(
                atlas, content_bindings, storyboard,
                evidence_ledger=evidence_ledger,
                enforce_content_integrity=args.delivery_candidate,
            )
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        _emit(composition, args.json_out)
        return 0

    if args.command == "compose-components":
        from .component_composer import build_component_plan

        try:
            atlas = json.loads(Path(args.component_atlas).read_text(encoding="utf-8"))
            composition = json.loads(Path(args.composition).read_text(encoding="utf-8"))
            plan = build_component_plan(atlas, composition)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        _emit(plan, args.json_out)
        return 0

    if args.command == "component-atlas":
        from .component_atlas import build_component_atlas

        try:
            review = json.loads(Path(args.review).read_text(encoding="utf-8"))
            atlas = build_component_atlas(args.template_pptx, review)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        _emit(atlas, args.json_out)
        return 0

    if args.command == "plan-bespoke":
        from .bespoke import build_authoring_manifest
        from .production_request import prepare_template_context

        request = json.loads(Path(args.request).read_text(encoding="utf-8"))
        ir = json.loads(Path(args.ir).read_text(encoding="utf-8"))
        assessment = json.loads(Path(args.content_assessment).read_text(encoding="utf-8"))
        narrative_contract = (
            json.loads(Path(args.narrative_contract).read_text(encoding="utf-8"))
            if args.narrative_contract else None
        )
        template_context = None
        if request.get("template"):
            template_context = prepare_template_context(request, args.template_pptx)
        manifest = build_authoring_manifest(
            request, ir, assessment, template_context,
            narrative_contract=narrative_contract,
        )
        _emit(manifest, args.json_out)
        return 0 if manifest.get("status") == "ready_for_authoring" else 1

    if args.command == "author-bespoke":
        from .bespoke_runtime import run_bespoke_author

        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        ir = json.loads(Path(args.ir).read_text(encoding="utf-8"))
        result = run_bespoke_author(
            args.script, manifest, ir, args.output_dir,
            template_pptx=args.template_pptx, source_specs=args.source,
            render_engine=args.render_engine,
        )
        _emit(result, args.json_out)
        return 0 if result.get("ok") else 1

    if args.command == "review-bespoke":
        from .visual_review import apply_visual_review

        review = json.loads(Path(args.review).read_text(encoding="utf-8"))
        result = apply_visual_review(args.authoring_report, review)
        _emit(result, args.json_out)
        return 0 if result.get("status") == "visual_approved" else 1

    if args.command == "review-template":
        from .visual_review import apply_template_visual_review

        review = json.loads(Path(args.review).read_text(encoding="utf-8"))
        result = apply_template_visual_review(args.strict_report, review)
        _emit(result, args.json_out)
        return 0 if result.get("status") == "final_delivery_ready" else 1

    if args.command == "strict-template":
        from .strict_template import execute_strict_template

        try:
            source_docs, _meta = _load_sources(args.source)
        except (OSError, ValueError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        result = execute_strict_template(
            request=json.loads(Path(args.request).read_text(encoding="utf-8")),
            template_pptx=args.template_pptx,
            strict_plan=json.loads(Path(args.plan).read_text(encoding="utf-8")),
            ir=json.loads(Path(args.ir).read_text(encoding="utf-8")),
            source_docs=source_docs,
            output_pptx=args.output_pptx,
            render_engine=args.render_engine,
            component_atlas=(
                json.loads(Path(args.component_atlas).read_text(encoding="utf-8"))
                if args.component_atlas else None
            ),
            evidence_ledger=json.loads(
                Path(args.evidence_ledger).read_text(encoding="utf-8")
            ),
            content_bindings=json.loads(
                Path(args.content_bindings).read_text(encoding="utf-8")
            ),
            final_delivery=args.final_delivery,
        )
        _emit(result, args.json_out)
        return 0 if result.get("ok") else 1

    if args.command == "refine-code":
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
        from refine_code import main as refine_main  # noqa: PLC0415
        return refine_main(["--script", args.script,
                            *(f"--source={s}" for s in args.source),
                            "--ir", args.ir,
                            "--output-dir", args.output_dir]
                           + (["--deck", args.deck] if args.deck else [])
                           + (["--high-fidelity"] if args.high_fidelity else [])
                           + (["--render-engine", args.render_engine] if args.high_fidelity else []))

    if args.command == "style-validate":
        from .style_validator import validate_style_pack
        pack = json.loads(Path(args.style).read_text(encoding="utf-8"))
        result = validate_style_pack(pack)
        _emit(result, args.json_out)
        return 0 if result["status"] != "fail" else 1

    if args.command == "compile":
        from .compile import compile_deck
        specs = []
        for spec in args.source:
            parts = spec.split(":", 2)
            if len(parts) != 3:
                print(f"error: --source expects source_id:type:path, got '{spec}'",
                      file=sys.stderr)
                return 2
            specs.append(tuple(parts))
        report = compile_deck(sources=specs, ir_path=args.ir, style_path=args.style,
                              output_dir=args.output_dir,
                              degrade_on_error=not args.no_degrade,
                              allow_content_truncation=args.allow_content_truncation,
                              refine_spec_path=args.refine_spec_path,
                              final_delivery=args.final_delivery)
        print(json.dumps({k: report[k] for k in
                          ("ok", "ir_origin", "slide_count", "pptx", "stage")
                          if k in report}, ensure_ascii=False, indent=2))
        return 0 if report.get("ok") else 1
    try:
        docs, meta = _load_sources(args.source)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.command == "parse":
        _emit({"documents": [doc.to_dict() for doc in docs.values()]}, args.json_out)
        return 0

    if args.command in {"extract-ir", "evidence-outline"}:
        if len(docs) != 1:
            print(f"error: {args.command} expects exactly one --source", file=sys.stderr)
            return 2
        (source_id, doc), = docs.items()
        result = (
            build_extractive_ir(doc, source_meta=meta[source_id])
            if args.command == "extract-ir"
            else build_evidence_outline(doc)
        )
        _emit(result, args.json_out)
        return 0

    ir = json.loads(Path(args.ir).read_text(encoding="utf-8"))
    if args.command == "verify":
        errors = verify_ir(ir, docs)
        _emit({"ok": not errors, "error_count": len(errors), "errors": errors},
              args.json_out)
        return 1 if errors else 0

    report = coverage_report(ir, docs)
    _emit(report, args.json_out)
    return 1 if report["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
