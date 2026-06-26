#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse


API_URL = "https://aistudio.baidu.com/llm/lmapi/v3/images/generations"
KEY_URL = "https://aistudio.baidu.com/account/accessToken"
ENV_NAME = "BAIDU_AISTUDIO_API_KEY"
SIZES = (
    "1024x1024",
    "1376x768",
    "1264x848",
    "1200x896",
    "896x1200",
    "848x1264",
    "768x1376",
)
MODELS = ("ERNIE-Image-Turbo", "ERNIE-Image")
PRESETS = (
    "auto",
    "text-poster",
    "infographic",
    "comic",
    "product",
    "ui",
    "photo",
    "concept",
    "abstract",
)
PRESET_SETTINGS = {
    "text-poster": {
        "size": "896x1200",
        "use_pe": False,
        "steps": 8,
        "guidance_scale": 1.0,
    },
    "infographic": {
        "size": "1376x768",
        "use_pe": False,
        "steps": 8,
        "guidance_scale": 1.0,
    },
    "comic": {
        "size": "1024x1024",
        "use_pe": False,
        "steps": 8,
        "guidance_scale": 1.0,
    },
    "product": {
        "size": "1024x1024",
        "use_pe": False,
        "steps": 8,
        "guidance_scale": 1.0,
    },
    "ui": {
        "size": "768x1376",
        "use_pe": False,
        "steps": 8,
        "guidance_scale": 1.0,
    },
    "photo": {
        "size": "1024x1024",
        "use_pe": True,
        "steps": 8,
        "guidance_scale": 1.0,
    },
    "concept": {
        "size": "1376x768",
        "use_pe": True,
        "steps": 8,
        "guidance_scale": 1.0,
    },
    "abstract": {
        "size": "896x1200",
        "use_pe": True,
        "steps": 8,
        "guidance_scale": 1.0,
    },
}
FALLBACK_SETTINGS = {
    "size": "1024x1024",
    "use_pe": True,
    "steps": 8,
    "guidance_scale": 1.0,
}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate images with ERNIE-Image through Baidu AI Studio."
    )
    parser.add_argument("--prompt", required=True, help="Text-to-image prompt.")
    parser.add_argument("--model", default="ERNIE-Image-Turbo", choices=MODELS)
    parser.add_argument(
        "--preset",
        default="auto",
        choices=PRESETS,
        help="Scene preset that chooses size, use_pe, steps, and guidance defaults.",
    )
    parser.add_argument("--n", type=int, default=1, choices=(1, 2, 3, 4))
    parser.add_argument(
        "--response-format", default="url", choices=("url", "b64_json")
    )
    parser.add_argument("--size", default=None, choices=SIZES)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--guidance-scale", type=float, default=None)
    pe_group = parser.add_mutually_exclusive_group()
    pe_group.add_argument("--use-pe", dest="use_pe", action="store_true", default=None)
    pe_group.add_argument("--no-use-pe", dest="use_pe", action="store_false")
    parser.add_argument("--out-dir", default=".", help="Directory for saved images.")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print request JSON and exit."
    )
    return parser.parse_args(argv)


def infer_preset(prompt: str) -> str:
    text = prompt.lower()
    checks = (
        (
            "infographic",
            (
                "infographic",
                "flowchart",
                "diagram",
                "timeline",
                "process",
                "chart",
                "流程图",
                "信息图",
                "步骤",
            ),
        ),
        (
            "comic",
            (
                "comic",
                "manga",
                "storyboard",
                "panel",
                "four-panel",
                "四格",
                "漫画",
                "分镜",
            ),
        ),
        (
            "ui",
            (
                "ui",
                "screenshot",
                "app screen",
                "dashboard",
                "interface",
                "启动页",
                "界面",
                "截图",
            ),
        ),
        (
            "product",
            (
                "product",
                "ecommerce",
                "hero image",
                "commercial shot",
                "产品",
                "电商",
                "主图",
            ),
        ),
        (
            "text-poster",
            (
                "exact text",
                "heading",
                "title",
                "poster",
                "banner",
                "label",
                "sign",
                "typography",
                "文字",
                "标题",
                "海报",
                "横幅",
                "说明牌",
            ),
        ),
        (
            "abstract",
            (
                "abstract",
                "bauhaus",
                "geometric",
                "surreal",
                "artistic",
                "抽象",
                "艺术",
            ),
        ),
        (
            "concept",
            (
                "concept art",
                "sci-fi",
                "fantasy",
                "worldbuilding",
                "environment design",
                "概念图",
                "科幻",
                "奇幻",
            ),
        ),
        (
            "photo",
            (
                "photorealistic",
                "photo",
                "photograph",
                "portrait",
                "camera",
                "lens",
                "摄影",
                "照片",
                "写实",
            ),
        ),
    )
    for preset, keywords in checks:
        if any(keyword in text for keyword in keywords):
            return preset
    return "photo"


def resolve_settings(args: argparse.Namespace) -> dict:
    preset = infer_preset(args.prompt) if args.preset == "auto" else args.preset
    settings = dict(FALLBACK_SETTINGS)
    settings.update(PRESET_SETTINGS.get(preset, {}))

    if args.model == "ERNIE-Image" and args.steps is None:
        settings["steps"] = 50
        settings["guidance_scale"] = 4.0

    if args.size is not None:
        settings["size"] = args.size
    if args.steps is not None:
        settings["steps"] = args.steps
    if args.guidance_scale is not None:
        settings["guidance_scale"] = args.guidance_scale
    if args.use_pe is not None:
        settings["use_pe"] = args.use_pe

    settings["preset"] = preset
    return settings


def build_payload(args: argparse.Namespace) -> dict:
    settings = resolve_settings(args)
    return {
        "model": args.model,
        "prompt": args.prompt,
        "n": args.n,
        "response_format": args.response_format,
        "size": settings["size"],
        "seed": args.seed,
        "use_pe": settings["use_pe"],
        "num_inference_steps": settings["steps"],
        "guidance_scale": settings["guidance_scale"],
    }


def request_generation(api_key: str, payload: dict) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": f"bearer {api_key}",
        "Content-Type": "application/json",
        "X-Client-Platform": "aistudio",
        "Accept": "application/json",
    }
    req = urllib.request.Request(API_URL, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {exc.code} {exc.reason}: {error_body}") from None
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from None

    try:
        parsed = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        raise RuntimeError(f"Non-JSON response: {raw[:300]!r}") from None

    if "error" in parsed:
        raise RuntimeError(f"API error: {parsed['error']}")
    return parsed


def ensure_out_dir(path: str) -> Path:
    out_dir = Path(path).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def timestamp_name(index: int, suffix: str = ".png") -> str:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    return f"ernie-image-{stamp}-{index}{suffix}"


def extension_from_url(url: str) -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        return suffix
    return ".png"


def download_url(url: str, out_path: Path) -> None:
    req = urllib.request.Request(
        url, headers={"User-Agent": "OpenClaw ERNIE-Image Skill"}
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = resp.read()
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch generated image: {exc}") from None
    out_path.write_bytes(data)


def save_b64(data: str, out_path: Path) -> None:
    try:
        out_path.write_bytes(base64.b64decode(data))
    except Exception as exc:
        raise RuntimeError(f"Failed to decode b64_json image: {exc}") from None


def response_items(response: dict) -> list[dict]:
    data = response.get("data")
    if not isinstance(data, list) or not data:
        raise RuntimeError(f"Response did not include image data: {response}")
    items = []
    for item in data:
        if isinstance(item, dict):
            items.append(item)
        else:
            raise RuntimeError(f"Unexpected image item: {item!r}")
    return items


def save_outputs(response: dict, response_format: str, out_dir: Path) -> None:
    for index, item in enumerate(response_items(response), start=1):
        if response_format == "url":
            url = item.get("url")
            if not url:
                raise RuntimeError(f"Image item missing URL: {item}")
            print(f"IMAGE_URL:{url}")
            out_path = out_dir / timestamp_name(index, extension_from_url(url))
            download_url(url, out_path)
        else:
            b64 = item.get("b64_json")
            if not b64:
                raise RuntimeError(f"Image item missing b64_json: {item}")
            out_path = out_dir / timestamp_name(index, ".png")
            save_b64(b64, out_path)
        print(f"MEDIA:{out_path.resolve()}")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    payload = build_payload(args)

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    api_key = os.getenv(ENV_NAME, "").strip()
    if not api_key:
        print(
            f"Error: set {ENV_NAME} before generating. Get a key from {KEY_URL}.",
            file=sys.stderr,
        )
        return 2

    out_dir = ensure_out_dir(args.out_dir)
    response = request_generation(api_key, payload)
    save_outputs(response, args.response_format, out_dir)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
