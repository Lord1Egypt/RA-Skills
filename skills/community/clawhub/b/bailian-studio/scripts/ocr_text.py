#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
import os

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from env import get_dashscope_key, get_region_base_url
from oss_upload import upload_image

try:
    import dashscope
except Exception as e:  # pragma: no cover
    print("Error: dashscope not installed. pip install dashscope", file=sys.stderr)
    raise


def _extract_text(resp) -> str:
    try:
        content = resp["output"]["choices"][0]["message"]["content"][0]
    except Exception:
        content = None
    if isinstance(content, dict):
        if "text" in content:
            return content["text"]
        if "ocr_result" in content:
            return content["ocr_result"]
    raise RuntimeError("Unexpected OCR response format")


def run_ocr(image_url: str, model: str, min_pixels: int, max_pixels: int, enable_rotate: bool) -> str:
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "image": image_url,
                    "min_pixels": min_pixels,
                    "max_pixels": max_pixels,
                    "enable_rotate": enable_rotate,
                }
            ],
        }
    ]

    resp = dashscope.MultiModalConversation.call(
        api_key=get_dashscope_key(),
        model=model,
        messages=messages,
        ocr_options={"task": "text_recognition"},
    )
    return _extract_text(resp)


def main():
    parser = argparse.ArgumentParser(description="Bailian OCR text extraction")
    parser.add_argument("--url", help="Image URL")
    parser.add_argument("--image", help="Local image path")
    parser.add_argument("--model", default="qwen-vl-ocr-2025-11-20")
    parser.add_argument("--min-pixels", type=int, default=32 * 32 * 3)
    parser.add_argument("--max-pixels", type=int, default=32 * 32 * 8192)
    parser.add_argument("--enable-rotate", action="store_true")
    parser.add_argument("--base-url", default=None)

    args = parser.parse_args()
    if not args.url and not args.image:
        parser.error("Provide --url or --image")

    if args.base_url:
        dashscope.base_http_api_url = args.base_url
    else:
        dashscope.base_http_api_url = get_region_base_url()

    if args.url:
        image_url = args.url
    else:
        image_url = upload_image(Path(args.image))

    text = run_ocr(image_url, args.model, args.min_pixels, args.max_pixels, args.enable_rotate)
    print(text)


if __name__ == "__main__":
    main()
