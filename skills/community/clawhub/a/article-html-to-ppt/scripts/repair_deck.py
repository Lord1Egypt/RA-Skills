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

from ppt_qa.auto_repair import repair_deck, write_repair_report
from ppt_qa.verifier import VerificationInputError, build_verification_report, load_json


class HarnessFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z")
        stage = getattr(record, "stage", "-")
        issue_code = getattr(record, "issue_code", "-")
        return f"{timestamp} {record.levelname} {stage} {issue_code} {record.getMessage()}"


def configure_logging(level: str, log_file: Optional[Path]) -> logging.Logger:
    logger = logging.getLogger("repair_deck")
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
    parser = argparse.ArgumentParser(description="Run safe deterministic PPTX auto-repair attempts and report remaining QA issues.")
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--ppt-ir", type=Path)
    parser.add_argument("--style", type=Path)
    parser.add_argument("--delivery", type=Path)
    parser.add_argument("--build", type=Path)
    parser.add_argument("--qa-report", type=Path)
    parser.add_argument("--output-pptx", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=1)
    parser.add_argument("--json-output", action="store_true")
    parser.add_argument("--log-level", default="INFO")
    parser.add_argument("--log-file", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return 3 if isinstance(exc.code, int) and exc.code != 0 else 0
    logger = configure_logging(args.log_level, args.log_file)
    try:
        if not args.pptx.exists():
            logger.error("PPTX file does not exist.", extra={"stage": "args", "issue_code": "BAD_INPUT"})
            return 3
        ppt_ir = load_json(args.ppt_ir)
        style = load_json(args.style)
        delivery = load_json(args.delivery)
        build_manifest = load_json(args.build)
        initial_report = load_json(args.qa_report)
        verifier_kwargs = {
            "ppt_ir": ppt_ir,
            "style": style,
            "delivery": delivery,
            "build_manifest": build_manifest,
            "ppt_ir_ref": str(args.ppt_ir) if args.ppt_ir else None,
            "style_ref": str(args.style) if args.style else None,
            "delivery_ref": str(args.delivery) if args.delivery else None,
            "build_ref": str(args.build) if args.build else None,
        }
        if initial_report is None:
            initial_report = build_verification_report(args.pptx, **verifier_kwargs)
        report = repair_deck(
            args.pptx,
            args.output_pptx,
            initial_report=initial_report,
            max_iterations=args.max_iterations,
            verifier_kwargs=verifier_kwargs,
        )
        write_repair_report(report, args.output_report)
        if args.json_output:
            print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
        for iteration in report["iterations"]:
            for attempt in iteration["attempted_repairs"]:
                logger.info(
                    attempt.get("manual_reason") or attempt.get("status"),
                    extra={"stage": f"iteration-{iteration['iteration']}", "issue_code": attempt.get("issue_code", "-")},
                )
        return 0 if report["status"] == "repaired" else 1
    except (VerificationInputError, ValueError) as exc:
        logger.error(str(exc), extra={"stage": "args", "issue_code": "BAD_INPUT"})
        return 3
    except Exception as exc:
        logger.error(f"Internal error: {exc}", extra={"stage": "internal", "issue_code": "INTERNAL_ERROR"})
        logger.debug(traceback.format_exc(), extra={"stage": "internal", "issue_code": "INTERNAL_ERROR"})
        return 4


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
