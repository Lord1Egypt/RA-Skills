#!/usr/bin/env python3
from __future__ import annotations

import argparse
import logging
import sys
import traceback
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ppt_qa.render_report import build_render_report, iso_now, write_render_report
from ppt_qa.renderers.base import RenderResult, RendererUnavailable, select_renderer


class HarnessFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z")
        stage = getattr(record, "stage", "-")
        slide_id = getattr(record, "slide_id", "-")
        object_id = getattr(record, "object_id", "-")
        issue_code = getattr(record, "issue_code", "-")
        return f"{timestamp} {record.levelname} {stage} {slide_id} {object_id} {issue_code} {record.getMessage()}"


def configure_logging(level: str, log_file: Optional[Path]) -> logging.Logger:
    logger = logging.getLogger("render_pptx")
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
    parser = argparse.ArgumentParser(description="Render PPTX to PDF and slide PNGs using a real Office-compatible renderer.")
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--engine", choices=["auto", "libreoffice", "powerpoint_macos", "powerpoint_windows"], default="auto")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--expected-slides", type=int)
    parser.add_argument("--expected-aspect", type=float, default=16 / 9)
    parser.add_argument("--dpi", type=int, default=144)
    parser.add_argument("--log-level", default="INFO")
    parser.add_argument("--log-file", type=Path)
    return parser.parse_args(argv)


def _unavailable_result() -> RenderResult:
    return RenderResult(
        status="unavailable",
        engine=None,
        engine_version=None,
        pdf_path=None,
        errors=["RENDER_ENGINE_UNAVAILABLE"],
        duration_seconds=0.0,
        slide_count_rendered=0,
    )


def _write_report(args: argparse.Namespace, result: RenderResult, started_at: str) -> dict[str, object]:
    report = build_render_report(
        args.pptx,
        result,
        started_at=started_at,
        expected_slides=args.expected_slides,
        expected_aspect=args.expected_aspect,
    )
    write_render_report(report, args.output / "render-report.json")
    return report


def _exit_code(report: dict[str, object]) -> int:
    status = report["status"]
    if status == "passed":
        return 0
    if status == "unavailable":
        return 2
    if status == "partial":
        return 3
    return 1


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return 4 if isinstance(exc.code, int) and exc.code != 0 else 0
    logger = configure_logging(args.log_level, args.log_file)
    started_at = iso_now()
    try:
        if not args.pptx.exists():
            logger.error("PPTX file does not exist.", extra={"stage": "args", "slide_id": "-", "object_id": "-", "issue_code": "BAD_ARGS"})
            return 4
        if args.timeout <= 0 or args.dpi <= 0:
            logger.error("Timeout and DPI must be positive.", extra={"stage": "args", "slide_id": "-", "object_id": "-", "issue_code": "BAD_ARGS"})
            return 4
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "slides").mkdir(parents=True, exist_ok=True)
        (args.output / "logs").mkdir(parents=True, exist_ok=True)
        renderer = select_renderer(args.engine)
        if renderer is None:
            logger.error("No requested renderer is available.", extra={"stage": "render", "slide_id": "-", "object_id": "-", "issue_code": "RENDER_ENGINE_UNAVAILABLE"})
            report = _write_report(args, _unavailable_result(), started_at)
            return _exit_code(report)
        logger.info(f"Rendering with {renderer.name}.", extra={"stage": "render", "slide_id": "-", "object_id": "-", "issue_code": "-"})
        result = renderer.render(args.pptx, args.output, timeout_seconds=args.timeout, dpi=args.dpi)
        report = _write_report(args, result, started_at)
        for warning in report["warnings"]:  # type: ignore[index]
            logger.warning(warning["message"], extra={"stage": "render", "slide_id": warning.get("slide_index", "-"), "object_id": "-", "issue_code": warning["code"]})
        for error in report["errors"]:  # type: ignore[index]
            logger.error(error["message"], extra={"stage": "render", "slide_id": error.get("slide_index", "-"), "object_id": "-", "issue_code": error["code"]})
        return _exit_code(report)
    except RendererUnavailable as exc:
        logger.error(str(exc), extra={"stage": "args", "slide_id": "-", "object_id": "-", "issue_code": "BAD_ARGS"})
        return 4
    except Exception as exc:
        logger.error(f"Internal error: {exc}", extra={"stage": "internal", "slide_id": "-", "object_id": "-", "issue_code": "INTERNAL_ERROR"})
        logger.debug(traceback.format_exc(), extra={"stage": "internal", "slide_id": "-", "object_id": "-", "issue_code": "INTERNAL_ERROR"})
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
