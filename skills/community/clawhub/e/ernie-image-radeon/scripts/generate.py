#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai==1.82.0"]
# ///
"""Generate images with ERNIE-Image models via AMD Radeon Cloud.

The AMD Radeon Cloud provides FREE PaddleOCR-VL and ERNIE-Image inference.
No API key is required. Images are saved as local PNG files with MEDIA lines
that compatible clients can attach automatically.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlparse

from openai import OpenAI


RADEON_BASE_URL = "http://134.199.132.159/ocr/v1"
VALID_SIZES = [
    "1024x1024",
    "1376x768",
    "1264x848",
    "1200x896",
    "896x1200",
    "848x1264",
    "768x1376",
]
VALID_MODELS = ["ERNIE-Image", "ERNIE-Image-Turbo"]
MAX_PROMPT_LENGTH = 1024
SAFE_PREFIX_RE = re.compile(r"[^A-Za-z0-9._-]+")
DOWNLOAD_TIMEOUT_SECONDS = 120
OPENAI_TIMEOUT_SECONDS = 120.0


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate images using ERNIE-Image models via AMD Radeon Cloud (FREE)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s "一只可爱的橘猫坐在窗台上，柔和晨光，摄影风格"
  %(prog)s "a sunset over the ocean" --model ERNIE-Image --size 1376x768
  %(prog)s "mountain landscape" --n 2 --seed 42 --steps 12 --guidance 3.0
  %(prog)s "city skyline" --output ./images --prefix skyline --json
  %(prog)s "quick draft" --quiet

Configuration:
  Default: AMD Radeon Cloud endpoint (no configuration needed)
  Optional: ERNIE_BASE_URL, ERNIE_TIMEOUT
""",
    )
    parser.add_argument("prompt", help="Image generation prompt (max 1024 chars)")
    parser.add_argument(
        "--model",
        default="ERNIE-Image-Turbo",
        choices=VALID_MODELS,
        help="Model to use (default: ERNIE-Image-Turbo)",
    )
    parser.add_argument(
        "--size",
        default="1024x1024",
        choices=VALID_SIZES,
        help="Image dimensions (default: 1024x1024)",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        choices=range(1, 5),
        metavar="1-4",
        help="Number of images to generate (default: 1)",
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Output directory (default: current directory)",
    )
    parser.add_argument(
        "--format",
        dest="response_format",
        default="b64_json",
        choices=["b64_json", "url"],
        help="Response format (default: b64_json)",
    )
    parser.add_argument("--seed", type=int, default=None, help="Seed for reproducibility")
    parser.add_argument(
        "--steps",
        type=int,
        default=None,
        metavar="4-20",
        help="Number of inference steps (default: provider default)",
    )
    parser.add_argument(
        "--guidance",
        type=float,
        default=None,
        help="Guidance scale 1.0-7.5 (default: provider default)",
    )
    parser.add_argument(
        "--use-pe",
        action="store_true",
        default=False,
        help="Enable prompt enhancement",
    )
    parser.add_argument(
        "--prefix",
        default="ernie",
        help="Safe output filename prefix (default: ernie)",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=False,
        help="Output result as JSON to stdout",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        default=False,
        help="Suppress progress output; only print MEDIA: lines or JSON",
    )
    return parser


def sanitize_prefix(prefix: str) -> str:
    """Reject path-like prefixes and normalize unsafe characters."""
    if "/" in prefix or "\\" in prefix:
        raise ValueError("--prefix must be a filename prefix, not a path")
    sanitized = SAFE_PREFIX_RE.sub("_", prefix.strip()).strip("._-")
    if not sanitized:
        raise ValueError("--prefix must contain at least one letter or number")
    return sanitized[:80]


def unique_path(path: Path) -> Path:
    """Return *path* unchanged if it does not exist, otherwise append a numeric suffix."""
    if not path.exists():
        return path
    for index in range(1, 10000):
        candidate = path.with_name(f"{path.stem}-{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not find an unused filename for {path}")


def validate_args(args: argparse.Namespace) -> None:
    if len(args.prompt) > MAX_PROMPT_LENGTH:
        print(
            f"Error: Prompt is {len(args.prompt)} characters, "
            f"exceeding the {MAX_PROMPT_LENGTH} character limit.",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.guidance is not None and (args.guidance < 1.0 or args.guidance > 7.5):
        print("Error: --guidance must be between 1.0 and 7.5", file=sys.stderr)
        sys.exit(1)

    if args.steps is not None and (args.steps < 4 or args.steps > 20):
        print("Error: --steps must be between 4 and 20", file=sys.stderr)
        sys.exit(1)

    try:
        args.prefix = sanitize_prefix(args.prefix)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output)
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    if not output_dir.is_dir():
        print(f"Error: {args.output} is not a directory", file=sys.stderr)
        sys.exit(1)


def build_extra_body(args: argparse.Namespace) -> dict:
    extra = {}
    if args.seed is not None:
        extra["seed"] = args.seed
    if args.use_pe:
        extra["use_pe"] = True
    if args.steps is not None:
        extra["num_inference_steps"] = args.steps
    if args.guidance is not None:
        extra["guidance_scale"] = args.guidance
    return extra


def generate_image(args: argparse.Namespace) -> object:
    base_url = os.environ.get("ERNIE_BASE_URL", "").strip() or RADEON_BASE_URL
    api_key = os.environ.get("AI_STUDIO_API_KEY", "").strip()

    # Suppress API key for plaintext HTTP endpoints to avoid credential leakage.
    # Key is only forwarded when the endpoint uses HTTPS (a trusted endpoint).
    if api_key and base_url.startswith("http://"):
        print(
            "Warning: AI_STUDIO_API_KEY is set but the endpoint uses HTTP. "
            "Key will NOT be sent over plaintext. Use an HTTPS endpoint "
            "(ERNIE_BASE_URL) to enable authentication.",
            file=sys.stderr,
        )
        api_key = ""
    if not api_key:
        api_key = "radeon-cloud"

    timeout = OPENAI_TIMEOUT_SECONDS
    timeout_str = os.environ.get("ERNIE_TIMEOUT", "").strip()
    if timeout_str:
        try:
            timeout = float(timeout_str)
        except ValueError:
            pass

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=timeout,
    )

    extra_body = build_extra_body(args)

    try:
        return client.images.generate(
            model=args.model,
            prompt=args.prompt,
            n=args.n,
            size=args.size,
            response_format=args.response_format,
            extra_body=extra_body if extra_body else None,
        )
    except Exception as exc:
        error_msg = str(exc)
        print(f"Error: API call failed: {error_msg}", file=sys.stderr)
        if "502" in error_msg:
            print(
                "Hint: AMD Radeon Cloud endpoint is temporarily unavailable (502 Bad Gateway). "
                "Please try again later.",
                file=sys.stderr,
            )
        elif "401" in error_msg or "403" in error_msg:
            print(
                "Hint: Authentication failed. The default Radeon Cloud endpoint "
                "requires no API key.",
                file=sys.stderr,
            )
        sys.exit(1)


def write_image_from_url(url: str, filepath: Path) -> None:
    """Download an image from *url* to *filepath* with timeout checks."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Image URL must use http or https, got {parsed.scheme}")
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ernie-image-radeon/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=DOWNLOAD_TIMEOUT_SECONDS) as response:
            filepath.write_bytes(response.read())
    except URLError as exc:
        raise RuntimeError(f"Could not download image URL: {exc}") from exc


def save_images(response, args: argparse.Namespace) -> list[dict]:
    output_dir = Path(args.output).resolve()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    files = []

    for index, img_data in enumerate(response.data):
        suffix = f"_{index + 1}" if args.n > 1 else ""
        filename = f"{args.prefix}_{timestamp}{suffix}.png"
        filepath = unique_path(output_dir / filename)

        if args.response_format == "b64_json":
            try:
                img_bytes = base64.b64decode(img_data.b64_json, validate=True)
            except (binascii.Error, TypeError) as exc:
                raise RuntimeError("API returned invalid base64 image data") from exc
            filepath.write_bytes(img_bytes)
        else:
            write_image_from_url(img_data.url, filepath)

        size_bytes = filepath.stat().st_size
        files.append(
            {
                "path": str(filepath),
                "size_bytes": size_bytes,
                "size_mb": round(size_bytes / (1024 * 1024), 2),
            }
        )

    return files


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)
    validate_args(args)

    if not args.json_output and not args.quiet:
        print(f"Generating image with {args.model} via AMD Radeon Cloud...")
        print(f'Prompt: "{args.prompt}"')
        details = f"Size: {args.size}"
        if args.seed is not None:
            details += f", Seed: {args.seed}"
        if args.steps is not None:
            details += f", Steps: {args.steps}"
        if args.guidance is not None:
            details += f", Guidance: {args.guidance}"
        print(details)

    response = generate_image(args)
    try:
        files = save_images(response, args)
    except Exception as exc:
        print(f"Error: failed to save generated image: {exc}", file=sys.stderr)
        return 1

    if args.json_output:
        result = {
            "success": True,
            "model": args.model,
            "prompt": args.prompt,
            "parameters": {
                "size": args.size,
                "n": args.n,
                "seed": args.seed,
                "steps": args.steps,
                "guidance": args.guidance,
                "use_pe": args.use_pe,
            },
            "files": files,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for file_info in files:
            print(f"\nSaved: {Path(file_info['path']).name} ({file_info['size_mb']} MB)")
            print(f"MEDIA:{file_info['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
