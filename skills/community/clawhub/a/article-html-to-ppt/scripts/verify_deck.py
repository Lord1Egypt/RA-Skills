#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import logging
import sys
import traceback
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ppt_qa.verifier import (
    VerificationInputError,
    build_verification_report,
    load_json,
    run_render_report,
    run_structural_inspection,
    verification_exit_code,
    write_json,
)

try:
    from .package_delivery import calculate_delivery_status
except ImportError:
    from package_delivery import calculate_delivery_status


class HarnessFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z")
        stage = getattr(record, "stage", "-")
        slide_id = getattr(record, "slide_id", "-")
        object_id = getattr(record, "object_id", "-")
        issue_code = getattr(record, "issue_code", "-")
        return f"{timestamp} {record.levelname} {stage} {slide_id} {object_id} {issue_code} {record.getMessage()}"


def configure_logging(level: str, log_file: Optional[Path]) -> logging.Logger:
    logger = logging.getLogger("verify_deck")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.handlers.clear()
    handler: logging.Handler
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_file, encoding="utf-8")
    else:
        handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(HarnessFormatter())
    logger.addHandler(handler)
    return logger


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify a PPTX deck with structural inspection and optional real render evidence.")
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--ppt-ir", type=Path)
    parser.add_argument("--style", type=Path)
    parser.add_argument("--delivery", type=Path)
    parser.add_argument("--build", type=Path)
    parser.add_argument("--schema-dir", type=Path, default=ROOT / "schemas")
    parser.add_argument("--inspection-report", type=Path)
    parser.add_argument("--render-report", type=Path)
    parser.add_argument("--render", action="store_true", help="Attempt rendering with a real local renderer and embed the render report.")
    parser.add_argument("--render-output", type=Path, default=Path(".ppt-work/renders"))
    parser.add_argument("--render-engine", choices=["auto", "libreoffice", "powerpoint_macos", "powerpoint_windows"], default="auto")
    parser.add_argument("--render-required", action="store_true")
    parser.add_argument("--capabilities", type=Path, help="Capability report used to decide whether Premium can claim final visual QA.")
    parser.add_argument("--expected-aspect", type=float, default=16 / 9)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--dpi", type=int, default=144)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--profile", choices=["fast", "standard", "premium"], help="Override profile embedded in PPT IR or Build Manifest.")
    parser.add_argument("--benchmark-score", type=Path, help="Optional benchmark score JSON for trusted delivery status calculation.")
    parser.add_argument("--benchmark-case-id", help="Optional benchmark case ID to embed in the QA report for traceability.")
    parser.add_argument("--write-inspection-report", type=Path)
    parser.add_argument("--write-render-report", type=Path)
    parser.add_argument("--json-output", action="store_true")
    parser.add_argument("--log-level", default="INFO")
    parser.add_argument("--log-file", type=Path)
    return parser.parse_args(argv)


def _capability_path(args: argparse.Namespace, build_manifest: dict | None) -> Path | None:
    if args.capabilities:
        return args.capabilities
    if not build_manifest:
        return None
    raw = None
    environment = build_manifest.get("environment") if isinstance(build_manifest.get("environment"), dict) else {}
    contract_refs = build_manifest.get("contract_refs") if isinstance(build_manifest.get("contract_refs"), dict) else {}
    raw = environment.get("capability_report") or contract_refs.get("capability_report")
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute() and args.build:
        path = args.build.parent / path
    return path


def _has_available_renderer(capabilities: dict | None) -> bool:
    if not isinstance(capabilities, dict):
        return False
    return any(
        isinstance(renderer, dict) and renderer.get("available") is True
        for renderer in (capabilities.get("renderers", {}) or {}).values()
    )


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return 3 if isinstance(exc.code, int) and exc.code != 0 else 0
    logger = configure_logging(args.log_level, args.log_file)
    try:
        if not args.pptx.exists():
            logger.error("PPTX file does not exist.", extra={"stage": "args", "slide_id": "-", "object_id": "-", "issue_code": "BAD_INPUT"})
            return 3
        if args.timeout <= 0 or args.dpi <= 0:
            logger.error("Timeout and DPI must be positive.", extra={"stage": "args", "slide_id": "-", "object_id": "-", "issue_code": "BAD_INPUT"})
            return 3
        ppt_ir = load_json(args.ppt_ir)
        style = load_json(args.style)
        delivery = load_json(args.delivery)
        build_manifest = load_json(args.build)
        capability_report = load_json(_capability_path(args, build_manifest))
        inspection_report = load_json(args.inspection_report)
        if inspection_report is None:
            inspection_report = run_structural_inspection(
                args.pptx,
                ppt_ir=ppt_ir,
                style=style,
                delivery=delivery,
                build_manifest=build_manifest,
            )
        render_report = load_json(args.render_report)
        if render_report is None and args.render:
            if capability_report is not None and not _has_available_renderer(capability_report):
                render_report = {
                    "schema_version": "1.0",
                    "pptx": str(args.pptx),
                    "engine": None,
                    "engine_version": None,
                    "duration_seconds": 0.0,
                    "status": "unavailable",
                    "slide_count_expected": int(inspection_report.get("slide_count") or 0),
                    "slide_count_rendered": 0,
                    "pdf": None,
                    "slides": [],
                    "warnings": [],
                    "errors": [{"code": "RENDER_ENGINE_UNAVAILABLE", "message": "Capability report declares no renderer available."}],
                }
            else:
                render_report = run_render_report(
                    args.pptx,
                    args.render_output,
                    engine=args.render_engine,
                    expected_slides=int(inspection_report.get("slide_count") or 0),
                    expected_aspect=args.expected_aspect,
                    timeout=args.timeout,
                    dpi=args.dpi,
                )
        effective_profile = args.profile or str((build_manifest or {}).get("profile") or "standard")
        render_required = args.render_required
        if effective_profile == "premium" and capability_report is not None and not _has_available_renderer(capability_report):
            render_required = True
        report = build_verification_report(
            args.pptx,
            ppt_ir=ppt_ir,
            style=style,
            delivery=delivery,
            build_manifest=build_manifest,
            inspection_report=inspection_report,
            render_report=render_report,
            ppt_ir_ref=str(args.ppt_ir) if args.ppt_ir else None,
            style_ref=str(args.style) if args.style else None,
            delivery_ref=str(args.delivery) if args.delivery else None,
            build_ref=str(args.build) if args.build else None,
            render_required=render_required,
            profile=args.profile,
        )
        benchmark_score = load_json(args.benchmark_score)
        if build_manifest is not None:
            report["trusted_delivery_status"] = calculate_delivery_status(
                profile=args.profile or str(build_manifest.get("profile") or report.get("profile") or "standard"),
                build_manifest=build_manifest,
                qa_report=report,
                benchmark_score=benchmark_score,
            )
        if args.benchmark_case_id:
            report["benchmark_case_id"] = args.benchmark_case_id
        write_json(report, args.output)
        if args.write_inspection_report:
            write_json(inspection_report, args.write_inspection_report)
        if args.write_render_report and render_report is not None:
            write_json(render_report, args.write_render_report)
        if args.json_output:
            print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
        for issue in report["issues"]:
            level = logging.ERROR if issue["severity"] in {"error", "fatal"} else logging.WARNING
            logger.log(
                level,
                issue["message"],
                extra={
                    "stage": issue["category"],
                    "slide_id": issue["slide_id"] or "-",
                    "object_id": issue["object_id"] or "-",
                    "issue_code": issue["issue_code"],
                },
            )
        return verification_exit_code(report)
    except VerificationInputError as exc:
        logger.error(str(exc), extra={"stage": "args", "slide_id": "-", "object_id": "-", "issue_code": "BAD_INPUT"})
        return 3
    except Exception as exc:
        logger.error(f"Internal error: {exc}", extra={"stage": "internal", "slide_id": "-", "object_id": "-", "issue_code": "INTERNAL_ERROR"})
        logger.debug(traceback.format_exc(), extra={"stage": "internal", "slide_id": "-", "object_id": "-", "issue_code": "INTERNAL_ERROR"})
        return 4


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
