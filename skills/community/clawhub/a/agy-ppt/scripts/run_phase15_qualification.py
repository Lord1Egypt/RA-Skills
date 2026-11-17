#!/usr/bin/env python3
"""Run Phase 15.6 contract qualification and optional live Tesseract checks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from ocr_qualification import run_contract_qualification, run_live_tesseract_qualification


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 15 OCR qualification")
    parser.add_argument("--baseline-sha", required=True, help="exact 40-character git commit under qualification")
    parser.add_argument("--live-tesseract", action="store_true", help="run opt-in real Tesseract qualification")
    parser.add_argument("--tessdata-dir", type=Path, help="trusted installed tessdata directory")
    parser.add_argument("--language", default="eng", help="installed Tesseract language id")
    args = parser.parse_args()
    if len(args.baseline_sha) != 40 or any(char not in "0123456789abcdef" for char in args.baseline_sha):
        parser.error("--baseline-sha must be 40 lowercase hexadecimal characters")
    report: dict[str, object] = {"contract": run_contract_qualification(baseline_sha=args.baseline_sha).to_dict()}
    if args.live_tesseract:
        if args.tessdata_dir is None:
            parser.error("--tessdata-dir is required with --live-tesseract")
        report["live_tesseract"] = run_live_tesseract_qualification(args.tessdata_dir, language=args.language, baseline_sha=args.baseline_sha)
    else:
        report["live_tesseract"] = {"status": "NOT QUALIFIED IN CURRENT ENVIRONMENT"}
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
