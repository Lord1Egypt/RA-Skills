#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL_TEMPLATE = "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
DEFAULT_TEXT2IMG_MODEL = "@cf/stabilityai/stable-diffusion-xl-base-1.0"
DEFAULT_IMG2IMG_MODEL = "@cf/runwayml/stable-diffusion-v1-5-img2img"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(
            f"Missing required environment variable: {name}. "
            f"Pass it via docker compose environment:."
        )
    return value


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def timestamp_name(prefix: str, suffix: str) -> str:
    return f"{prefix}-{time.strftime('%Y%m%d-%H%M%S')}{suffix}"


def choose_output_path(output: str | None, prefix: str) -> Path | None:
    if not output:
        return None

    path = Path(output)
    if path.exists() and path.is_dir():
        path.mkdir(parents=True, exist_ok=True)
        return path / timestamp_name(prefix, ".png")

    if str(output).endswith(os.sep):
        path.mkdir(parents=True, exist_ok=True)
        return path / timestamp_name(prefix, ".png")

    if path.suffix:
        ensure_parent(path)
        return path

    path.mkdir(parents=True, exist_ok=True)
    return path / timestamp_name(prefix, ".png")


def detect_mime(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    return mime or "image/png"


def file_to_base64(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"Input file not found: {path}")
    encoded = base64.b64encode(p.read_bytes()).decode("ascii")
    return encoded


def build_payload(args: argparse.Namespace) -> tuple[str, dict]:
    if args.mode == "text2img":
        model = args.model or DEFAULT_TEXT2IMG_MODEL
        payload = {
            "prompt": args.prompt,
        }
        if args.negative_prompt:
            payload["negative_prompt"] = args.negative_prompt
        if args.num_steps is not None:
            payload["num_steps"] = args.num_steps
        if args.guidance is not None:
            payload["guidance"] = args.guidance
        if args.strength is not None:
            payload["strength"] = args.strength
        if args.width is not None:
            payload["width"] = args.width
        if args.height is not None:
            payload["height"] = args.height
        if args.seed is not None:
            payload["seed"] = args.seed
        return model, payload

    if args.mode == "img2img":
        model = args.model or DEFAULT_IMG2IMG_MODEL
        if not args.image:
            raise SystemExit("--image is required for img2img mode")
        payload = {
            "prompt": args.prompt,
            "image_b64": file_to_base64(args.image),
        }
        if args.negative_prompt:
            payload["negative_prompt"] = args.negative_prompt
        if args.num_steps is not None:
            payload["num_steps"] = args.num_steps
        if args.guidance is not None:
            payload["guidance"] = args.guidance
        if args.strength is not None:
            payload["strength"] = args.strength
        if args.seed is not None:
            payload["seed"] = args.seed
        return model, payload

    raise SystemExit(f"Unsupported mode: {args.mode}")


def call_api(model: str, payload: dict, timeout: int) -> bytes:
    account_id = require_env("CF_ACCOUNT_ID")
    api_token = require_env("CF_API_TOKEN")
    url = BASE_URL_TEMPLATE.format(account_id=account_id, model=model)

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Accept": "image/png",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            body = resp.read()
            if "application/json" in content_type:
                raise SystemExit(
                    "Workers AI returned JSON instead of image:\n" + body.decode("utf-8", errors="replace")
                )
            return body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {e.code} from Cloudflare Workers AI for model {model}:\n{body}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error calling Cloudflare Workers AI: {e}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate images through Cloudflare Workers AI (text2img, img2img)."
    )
    parser.add_argument("mode", choices=["text2img", "img2img"])
    parser.add_argument("prompt", help="Prompt text")
    parser.add_argument("--image", help="Source image path for img2img or inpainting")
    parser.add_argument("--output", required=True, help="Temporary or final output file path or directory. The script prints the saved file path to stdout.")
    parser.add_argument("--model", help="Override Workers AI model name")
    parser.add_argument("--negative-prompt", help="Negative prompt")
    parser.add_argument("--num-steps", type=int, help="Sampling steps")
    parser.add_argument("--guidance", type=float, help="Guidance scale")
    parser.add_argument("--strength", type=float, help="Transformation strength")
    parser.add_argument("--width", type=int, help="Output width (text2img when supported)")
    parser.add_argument("--height", type=int, help="Output height (text2img when supported)")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--timeout", type=int, default=180, help="HTTP timeout in seconds")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    model, payload = build_payload(args)
    output_path = choose_output_path(args.output, f"cf-workers-ai-{args.mode}")
    image_bytes = call_api(model, payload, args.timeout)

    ensure_parent(output_path)
    output_path.write_bytes(image_bytes)
    print(str(output_path.resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
