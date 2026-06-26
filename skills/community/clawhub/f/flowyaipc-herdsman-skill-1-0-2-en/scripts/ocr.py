#!/usr/bin/env python3
"""
Herdsman OCR recognition script

Calls the POST /v1/ocr endpoint to recognize text in images, returning full page text,
per-line results, confidence scores, and bounding box coordinates.

Usage:
  uv run python ocr.py ./invoice.jpg --model paddleocr-ppocrv5-server [--output result.json] [--json]

Examples:
  uv run python ocr.py ./test.png --model paddleocr-ppocrv5-server
  uv run python ocr.py ./test.png --model paddleocr-ppocrv5-server --json
  uv run python ocr.py ./test.png --model paddleocr-ppocrv5-server --output "D:/ocr_result.json"
"""

from __future__ import annotations

import json
import sys
import os
from pathlib import Path
from argparse import ArgumentParser, Namespace

# ── Add parent directory to sys.path to reuse herdsman_client.py ──
_THIS_DIR = Path(__file__).resolve().parent
_SKILL_DIR = _THIS_DIR.parent
sys.path.insert(0, str(_SKILL_DIR))

from scripts.herdsman_client import HerdsmanClient, file_to_data_url


def build_parser() -> ArgumentParser:
    p = ArgumentParser(description="Herdsman OCR Image Text Recognition")
    p.add_argument("image_path", help="Image file path to recognize (PNG/JPG etc.)")
    p.add_argument("--model", default="paddleocr-ppocrv5-server", help="OCR model ID (default paddleocr-ppocrv5-server)")
    p.add_argument("--output", "-o", help="Output file path (optional, writes JSON file)")
    p.add_argument("--json", action="store_true", help="Output full results as JSON (includes line details)")
    p.add_argument("--timeout", type=int, default=120, help="Timeout in seconds (default 120)")
    return p


def main() -> None:
    args = build_parser().parse_args()

    image_path = args.image_path
    if not os.path.isfile(image_path):
        print(f"Error: file not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    client = HerdsmanClient(timeout=args.timeout)

    # Convert local image to data URL
    image_base64 = file_to_data_url(image_path, default_mime_type="image/png")

    print(f"Recognizing: {image_path}", file=sys.stderr)
    print(f"Model: {args.model}", file=sys.stderr)

    try:
        result = client.ocr(model=args.model, image_base64=image_base64)
    except Exception as e:
        print(f"OCR recognition failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.output:
        output_path = os.path.abspath(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Result saved: {output_path}", file=sys.stderr)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Default: print full page text only
        print(result.get("text", ""))


if __name__ == "__main__":
    main()