#!/usr/bin/env python3
"""
claw-text-and-pics — Extract text and images from documents via Mistral OCR API.

Supports: JPEG, PNG, PDF (local file or URL)

Usage:
  python3 ocr.py --input scan.jpg
  python3 ocr.py --input document.pdf --pages 3
  python3 ocr.py --input scan.jpg --extract-images --output-dir ./images/
  python3 ocr.py --input scan.jpg --extract-images --send --target 123456789
  python3 ocr.py --input https://example.com/doc.pdf
  python3 ocr.py --input scan.jpg --debug

Environment variables:
  MISTRAL_API_KEY      Required: your Mistral API key
  TELEGRAM_CHAT_ID     Default Telegram chat ID for --send (can be overridden with --target)
  TELEGRAM_BOT_TOKEN   Required when using --send
"""

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_KEY = os.environ.get("MISTRAL_API_KEY", "")
API_URL = "https://api.mistral.ai/v1/ocr"


def encode_file(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")


def send_telegram(image_path: str, target: str, bot_token: str) -> bool:
    """Send image as Telegram photo via Bot API (stdlib only)."""
    import json as _json

    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    boundary = "----ClawDocScanBoundary"

    ogg_path = Path(image_path)
    data = ogg_path.read_bytes()

    parts: list[bytes] = [
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
            f"{target}\r\n"
        ).encode("utf-8"),
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="photo"; filename="{ogg_path.name}"\r\n'
            f"Content-Type: image/jpeg\r\n\r\n"
        ).encode("utf-8") + data + b"\r\n",
        f"--{boundary}--\r\n".encode("utf-8"),
    ]

    body = b"".join(parts)
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = _json.loads(resp.read())
        if result.get("ok"):
            print(f"Sent: {image_path}")
            return True
        else:
            print(f"Telegram error: {result}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"Telegram send failed: {e}", file=sys.stderr)
        return False


def crop_from_original(input_path: str, bbox: dict, page_dims: dict, out_path: str) -> str:
    """
    Crop an image from the original scan using the bounding box returned by the OCR API.

    bbox: absolute pixel coordinates in the OCR-processed image space
    page_dims: {"width": N, "height": N} — OCR image dimensions
    Coordinates are scaled to match the original image size.

    Requires: Pillow (pip install pillow)
    """
    try:
        from PIL import Image
    except ImportError:
        print(
            "ERROR: Pillow not installed. Install with: pip install pillow",
            file=sys.stderr,
        )
        sys.exit(1)

    img = Image.open(input_path)
    orig_w, orig_h = img.size

    ocr_w = page_dims.get("width", orig_w)
    ocr_h = page_dims.get("height", orig_h)

    scale_x = orig_w / ocr_w
    scale_y = orig_h / ocr_h

    x1 = int(bbox.get("top_left_x", 0) * scale_x)
    y1 = int(bbox.get("top_left_y", 0) * scale_y)
    x2 = int(bbox.get("bottom_right_x", orig_w) * scale_x)
    y2 = int(bbox.get("bottom_right_y", orig_h) * scale_y)

    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(orig_w, x2), min(orig_h, y2)

    cropped = img.crop((x1, y1, x2, y2)).convert("RGB")
    cropped.save(out_path, "JPEG", quality=92)
    print(f"Saved: {out_path} ({cropped.size[0]}x{cropped.size[1]}px)", file=sys.stderr)
    return out_path


def ocr(
    input_path: str,
    pages: int | None = None,
    extract_images: bool = False,
    output_dir: str | None = None,
    send: bool = False,
    target: str | None = None,
    bot_token: str | None = None,
    debug: bool = False,
) -> list[str]:
    if not API_KEY:
        print("ERROR: MISTRAL_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Build document payload
    if is_url(input_path):
        doc = (
            {"type": "document_url", "document_url": input_path}
            if input_path.lower().endswith(".pdf")
            else {"type": "image_url", "image_url": input_path}
        )
    else:
        ext = input_path.lower().split(".")[-1]
        data = encode_file(input_path)
        if ext == "pdf":
            doc = {"type": "document_url", "document_url": f"data:application/pdf;base64,{data}"}
        else:
            mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
            doc = {"type": "image_url", "image_url": f"data:{mime};base64,{data}"}

    payload: dict = {
        "model": "mistral-ocr-latest",
        "document": doc,
        "include_image_base64": False,
    }
    if pages:
        payload["pages"] = list(range(pages))

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"API error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

    if debug:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return []

    # Print extracted text (Markdown)
    for page in result.get("pages", []):
        print(page.get("markdown", ""))

    # Extract embedded images via bounding-box crop
    if extract_images:
        out_dir = Path(output_dir) if output_dir else Path("./extracted-images")
        out_dir.mkdir(parents=True, exist_ok=True)
        extracted: list[str] = []

        for page_idx, page in enumerate(result.get("pages", [])):
            images = page.get("images", [])
            if not images:
                print(f"Page {page_idx}: no embedded images.", file=sys.stderr)
                continue

            for img_meta in images:
                img_id = img_meta.get("id", f"img_{page_idx}")
                safe_name = img_id.replace("/", "_").replace(":", "_")
                if not safe_name.lower().endswith((".jpg", ".jpeg", ".png")):
                    safe_name += ".jpg"
                out_path = str(out_dir / safe_name)

                bbox = {
                    "top_left_x":     img_meta.get("top_left_x", 0),
                    "top_left_y":     img_meta.get("top_left_y", 0),
                    "bottom_right_x": img_meta.get("bottom_right_x", 9999),
                    "bottom_right_y": img_meta.get("bottom_right_y", 9999),
                }
                page_dims = page.get("dimensions", {})

                if not is_url(input_path):
                    crop_from_original(input_path, bbox, page_dims, out_path)
                    extracted.append(out_path)
                    if send and target and bot_token:
                        send_telegram(out_path, target, bot_token)
                else:
                    print("WARNING: Image crop from URL not supported — use a local file.", file=sys.stderr)

        if not extracted:
            print("No images extracted.", file=sys.stderr)
        return extracted

    return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract text and images from documents via Mistral OCR API"
    )
    parser.add_argument("--input", required=True, help="Path or URL to image/PDF")
    parser.add_argument("--pages", type=int, help="Number of pages (PDFs)")
    parser.add_argument("--extract-images", action="store_true",
                        help="Crop and save embedded images using bounding boxes")
    parser.add_argument("--output-dir", help="Output directory for extracted images (default: ./extracted-images)")
    parser.add_argument("--send", action="store_true",
                        help="Send extracted images via Telegram")
    parser.add_argument("--target", default=None,
                        help="Telegram chat ID (or set TELEGRAM_CHAT_ID env var)")
    parser.add_argument("--debug", action="store_true",
                        help="Print raw API response")
    args = parser.parse_args()

    # Resolve Telegram config from environment variables
    target = args.target or os.environ.get("TELEGRAM_CHAT_ID")
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")

    if args.send:
        if not target:
            print("ERROR: Provide --target or set TELEGRAM_CHAT_ID env var", file=sys.stderr)
            sys.exit(1)
        if not bot_token:
            print("ERROR: TELEGRAM_BOT_TOKEN not set", file=sys.stderr)
            sys.exit(1)

    ocr(
        args.input,
        pages=args.pages,
        extract_images=args.extract_images,
        output_dir=args.output_dir,
        send=args.send,
        target=target,
        bot_token=bot_token,
        debug=args.debug,
    )
