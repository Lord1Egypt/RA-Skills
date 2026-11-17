#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
import traceback
import zipfile
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ppt_qa.package_inspector import inspect_package
from ppt_qa.report import inspection_to_dict, write_inspection
from ppt_qa.slide_inspector import inspect_slides


class HarnessFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z")
        stage = getattr(record, "stage", "-")
        slide_id = getattr(record, "slide_id", "-")
        object_id = getattr(record, "object_id", "-")
        issue_code = getattr(record, "issue_code", "-")
        return f"{timestamp} {record.levelname} {stage} {slide_id} {object_id} {issue_code} {record.getMessage()}"


def configure_logging(level: str, log_file: Optional[Path]) -> logging.Logger:
    logger = logging.getLogger("inspect_pptx")
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


def load_json(path: Optional[Path]) -> Optional[dict[str, Any]]:
    if path is None:
        return None
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect PPTX package and structural editability.")
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--ppt-ir", type=Path)
    parser.add_argument("--style", type=Path)
    parser.add_argument("--delivery", type=Path)
    parser.add_argument("--build", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", action="store_true")
    parser.add_argument("--fail-on", default="")
    parser.add_argument("--warning-on", default="")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--include-raw-xml", action="store_true")
    parser.add_argument("--extract-media", type=Path, nargs="?", const=Path("media"))
    parser.add_argument("--extract-thumbnails", type=Path, nargs="?", const=Path("thumbnails"))
    parser.add_argument("--log-level", default="INFO")
    parser.add_argument("--log-file", type=Path)
    return parser.parse_args(argv)


def _copy_media(pptx: Path, output_dir: Path, logger: logging.Logger) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    with zipfile.ZipFile(pptx) as package:
        for name in package.namelist():
            if name.startswith("ppt/media/") and not name.endswith("/"):
                target = output_dir / Path(name).name
                target.write_bytes(package.read(name))
                count += 1
    logger.info("Extracted media files.", extra={"stage": "package", "slide_id": "-", "object_id": "-", "issue_code": f"count={count}"})


def _extract_thumbnails_notice(output_dir: Path, logger: logging.Logger) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    notice = output_dir / "README.txt"
    notice.write_text("Thumbnail extraction is unavailable in inspect_pptx without a renderer.\n", encoding="utf-8")
    logger.warning("Thumbnail extraction unavailable without renderer; wrote notice.", extra={"stage": "render", "slide_id": "-", "object_id": "-", "issue_code": "READBACK_UNAVAILABLE"})


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 3
    logger = configure_logging(args.log_level, args.log_file)

    try:
        if not args.pptx.exists():
            logger.error("PPTX file does not exist.", extra={"stage": "args", "slide_id": "-", "object_id": "-", "issue_code": "PPTX_PACKAGE_CORRUPT"})
            return 2
        ppt_ir = load_json(args.ppt_ir)
        style = load_json(args.style)
        delivery = load_json(args.delivery)
        build = load_json(args.build)
        inspection = inspect_package(args.pptx, ppt_ir=ppt_ir, build_manifest=build)
        if any(issue.severity == "fatal" for issue in inspection.issues):
            data = inspection_to_dict(inspection, include_raw_xml=args.include_raw_xml)
            if args.output:
                write_inspection(inspection, args.output, include_raw_xml=args.include_raw_xml)
            if args.json_output:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            for issue in data["issues"]:
                logger.error(issue["message"], extra={"stage": "package", "slide_id": issue["slide_id"] or "-", "object_id": issue["object_id"] or "-", "issue_code": issue["issue_code"]})
            unreadable_codes = {"PPTX_PACKAGE_CORRUPT", "PPTX_PRESENTATION_XML_MISSING"}
            return 2 if any(issue["issue_code"] in unreadable_codes for issue in data["issues"]) else 1
        inspection = inspect_slides(args.pptx, inspection, ppt_ir=ppt_ir, style=style, delivery=delivery, include_raw_xml=args.include_raw_xml)
        if args.extract_media:
            _copy_media(args.pptx, args.extract_media, logger)
        if args.extract_thumbnails:
            _extract_thumbnails_notice(args.extract_thumbnails, logger)
        data = write_inspection(inspection, args.output, include_raw_xml=args.include_raw_xml) if args.output else inspection_to_dict(inspection, include_raw_xml=args.include_raw_xml)
        if args.json_output:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        fail_codes = {item.strip() for item in args.fail_on.split(",") if item.strip()}
        warning_codes = {item.strip() for item in args.warning_on.split(",") if item.strip()}
        hard_fail = False
        for issue in data["issues"]:
            level = logging.ERROR if issue["severity"] in {"error", "fatal"} else logging.WARNING
            logger.log(level, issue["message"], extra={"stage": issue["category"], "slide_id": issue["slide_id"] or "-", "object_id": issue["object_id"] or "-", "issue_code": issue["issue_code"]})
            if issue["severity"] in {"error", "fatal"}:
                hard_fail = True
            if issue["issue_code"] in fail_codes or (issue["issue_code"] in warning_codes and issue["severity"] == "warning"):
                hard_fail = True
        if args.strict and any(issue["severity"] == "warning" for issue in data["issues"]):
            hard_fail = True
        return 1 if hard_fail else 0
    except (json.JSONDecodeError, ValueError) as exc:
        logger.error(str(exc), extra={"stage": "args", "slide_id": "-", "object_id": "-", "issue_code": "BAD_ARGS"})
        return 3
    except Exception as exc:
        logger.error(f"Internal error: {exc}", extra={"stage": "internal", "slide_id": "-", "object_id": "-", "issue_code": "INTERNAL_ERROR"})
        logger.debug(traceback.format_exc(), extra={"stage": "internal", "slide_id": "-", "object_id": "-", "issue_code": "INTERNAL_ERROR"})
        return 4


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
