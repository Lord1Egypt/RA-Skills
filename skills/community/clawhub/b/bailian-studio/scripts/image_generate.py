#!/usr/bin/env python3
"""Generate images with Bailian DashScope and save them locally."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from env import DEFAULT_ENV_PATH, get_dashscope_key, get_region_base_url
from oss_upload import upload_image

try:
    import dashscope
except Exception:  # pragma: no cover
    print("Error: dashscope not installed. pip install -r requirements.txt", file=sys.stderr)
    raise SystemExit(1)

try:
    import requests
except Exception:  # pragma: no cover
    print("Error: requests not installed. pip install -r requirements.txt", file=sys.stderr)
    raise SystemExit(1)

DEFAULT_MODEL = "qwen-image-2.0-pro"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[1] / "tmp" / "bailian-studio"
DEFAULT_TIMEOUT = 120
DEFAULT_NEGATIVE_PROMPT = (
    "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，"
    "画面具有AI感，构图混乱，文字模糊，扭曲"
)
VERSION = "0.1.0"


def is_url(value: str) -> bool:
    """Return True when the input is an HTTP(S) URL."""
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def slugify_prompt(prompt: str, limit: int = 32) -> str:
    """Create a filesystem-friendly prompt slug."""
    normalized = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", prompt.strip().lower())
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    return (normalized or "image")[:limit]


def build_size(width: int, height: int) -> str:
    """Build DashScope size string."""
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive integers")
    return f"{width}*{height}"


def ensure_parent(path: Path) -> None:
    """Ensure the parent directory exists."""
    path.parent.mkdir(parents=True, exist_ok=True)


def dedupe_path(path: Path) -> Path:
    """Auto-rename a path if it already exists."""
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix or ".png"
    counter = 1
    while True:
        candidate = path.with_name(f"{stem}-{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def resolve_output_path(base_dir: Path, output: Optional[str], prompt: str) -> Path:
    """Resolve the final output path."""
    if output:
        requested = Path(output).expanduser()
        if requested.is_dir() or str(output).endswith(("/", "\\")):
            requested = requested / f"{slugify_prompt(prompt)}.png"
        elif requested.suffix.lower() != ".png":
            requested = requested.with_suffix(".png")
        final_path = requested
    else:
        final_path = base_dir / f"{slugify_prompt(prompt)}.png"

    ensure_parent(final_path)
    return dedupe_path(final_path)


def prepare_reference_image(image: str) -> str:
    """Return a remote image URL for img2img."""
    if is_url(image):
        return image
    return upload_image(Path(image).expanduser())


def extract_image_url(response: Any) -> str:
    """Extract the first result image URL from DashScope response."""
    output = response.get("output") if isinstance(response, dict) else getattr(response, "output", None)
    if isinstance(output, dict):
        for key in ("results", "images"):
            items = output.get(key)
            if isinstance(items, list) and items:
                first = items[0]
                if isinstance(first, dict) and first.get("url"):
                    return first["url"]
        choices = output.get("choices")
        if isinstance(choices, list) and choices:
            message = choices[0].get("message") if isinstance(choices[0], dict) else None
            content = message.get("content") if isinstance(message, dict) else None
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("image"):
                        return item["image"]
        if output.get("url"):
            return output["url"]
    raise RuntimeError(f"Unexpected image generation response format: {response}")


def generate_image(
    prompt: str,
    model: str,
    width: int,
    height: int,
    reference_image: Optional[str] = None,
    env_path: Optional[Path] = None,
    negative_prompt: Optional[str] = None,
) -> str:
    """Call DashScope multimodal generation and return the result URL."""
    content: list[dict[str, str]] = []
    if reference_image:
        content.append({"image": reference_image})
    content.append({"text": prompt})

    messages = [{"role": "user", "content": content}]
    response = dashscope.MultiModalConversation.call(
        api_key=get_dashscope_key(env_path=env_path),
        model=model,
        messages=messages,
        result_format="message",
        stream=False,
        watermark=False,
        prompt_extend=True,
        negative_prompt=negative_prompt or DEFAULT_NEGATIVE_PROMPT,
        size=build_size(width, height),
    )
    return extract_image_url(response)


def download_image(url: str, output_path: Path, timeout: int) -> Path:
    """Download an image URL to disk."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    ensure_parent(output_path)
    output_path.write_bytes(response.content)
    return output_path


def read_prompt(prompt: Optional[str]) -> str:
    """Read prompt from argument or stdin."""
    if prompt and prompt.strip():
        return prompt.strip()
    if not sys.stdin.isatty():
        stdin_prompt = sys.stdin.read().strip()
        if stdin_prompt:
            return stdin_prompt
    raise ValueError("Prompt is required. Use --prompt or pipe text via stdin.")


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
    parser = argparse.ArgumentParser(description="Bailian image generation")
    parser.add_argument("--prompt", help="Prompt text. If omitted, read from stdin.")
    parser.add_argument("--image", help="Reference image path or URL for img2img")
    parser.add_argument("--width", type=int, default=1024, help="Output width")
    parser.add_argument("--height", type=int, default=1024, help="Output height")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="DashScope image model")
    parser.add_argument("--output", help="Output PNG path or directory")
    parser.add_argument("--config", type=Path, default=DEFAULT_ENV_PATH, help="Path to bailian env file")
    parser.add_argument("--base-url", default=None, help="Override DashScope base URL")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Download timeout in seconds")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return parser


def main() -> None:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        prompt = read_prompt(args.prompt)
        dashscope.base_http_api_url = args.base_url or get_region_base_url(env_path=args.config)
        reference_image = prepare_reference_image(args.image) if args.image else None
        output_path = resolve_output_path(DEFAULT_OUTPUT_DIR, args.output, prompt)
        image_url = generate_image(
            prompt=prompt,
            model=args.model,
            width=args.width,
            height=args.height,
            reference_image=reference_image,
            env_path=args.config,
        )
        saved_path = download_image(image_url, output_path, timeout=args.timeout)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(saved_path)


if __name__ == "__main__":
    main()
