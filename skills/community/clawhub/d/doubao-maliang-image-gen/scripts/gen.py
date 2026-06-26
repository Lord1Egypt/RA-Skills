#!/usr/bin/env python3
import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html import escape as html_escape
from pathlib import Path
from typing import Optional


DEFAULT_MODEL = "doubao-seedream-5-0-260128"
DEFAULT_ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
DEFAULT_SIZE = "2K"


def resolve_api_key() -> str:
    for key in ("VOLCANO_ENGINE_API_KEY", "ARK_API_KEY", "SEEDREAM_API_KEY"):
        value = os.environ.get(key, "").strip()
        if value:
            return value
    raise RuntimeError(
        "Missing API key. Set VOLCANO_ENGINE_API_KEY, ARK_API_KEY, or SEEDREAM_API_KEY."
    )


def default_out_dir() -> Path:
    now = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    base = Path.home() / ".openclaw" / "workspace" / "tmp"
    base.mkdir(parents=True, exist_ok=True)
    return base / f"doubao-maliang-image-gen-{now}"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "image"


def request_images(
    *,
    api_key: str,
    prompt: str,
    model: str,
    endpoint: str,
    size: str,
    count: int,
) -> dict:
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "size": size,
            "n": count,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=body,
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        payload = err.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Seedream API failed ({err.code}): {payload}") from err
    except urllib.error.URLError as err:
        raise RuntimeError(f"Seedream API request failed: {err}") from err


def download_url(url: str, target: Path) -> None:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "doubao-maliang-image-gen/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        target.write_bytes(resp.read())


def infer_extension(item: dict, url: Optional[str]) -> str:
    mime = str(item.get("mime_type", "")).lower()
    if "png" in mime:
        return ".png"
    if "jpeg" in mime or "jpg" in mime:
        return ".jpg"
    if "webp" in mime:
        return ".webp"
    if url:
        path = urllib.parse.urlparse(url).path.lower()
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            if path.endswith(ext):
                return ext
    return ".png"


def write_gallery(out_dir: Path, items: list[dict]) -> None:
    figures = "\n".join(
        f"""
<figure>
  <a href="{html_escape(item['file'], quote=True)}"><img src="{html_escape(item['file'], quote=True)}" loading="lazy" /></a>
  <figcaption>{html_escape(item['prompt'])}</figcaption>
</figure>
""".strip()
        for item in items
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>doubao-maliang-image-gen</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 24px; background: #f7f2e8; color: #1f2a2e; }}
    h1 {{ margin-bottom: 8px; }}
    p {{ color: #4b5c61; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; }}
    figure {{ margin: 0; padding: 12px; border-radius: 16px; background: #fffaf0; box-shadow: 0 8px 24px rgba(30, 42, 46, 0.08); }}
    img {{ width: 100%; height: auto; display: block; border-radius: 12px; }}
    figcaption {{ margin-top: 10px; line-height: 1.45; white-space: pre-wrap; }}
    code {{ background: rgba(31, 42, 46, 0.08); padding: 2px 6px; border-radius: 8px; }}
  </style>
</head>
<body>
  <h1>doubao-maliang-image-gen</h1>
  <p>Local output in <code>{html_escape(str(out_dir))}</code></p>
  <div class="grid">
    {figures}
  </div>
</body>
</html>
"""
    (out_dir / "index.html").write_text(html, encoding="utf-8")


def save_outputs(out_dir: Path, prompt: str, response: dict) -> list[dict]:
    items = response.get("data")
    if not isinstance(items, list) or not items:
        raise RuntimeError(f"Seedream API returned no images: {json.dumps(response, ensure_ascii=False)}")

    saved: list[dict] = []
    prefix = slugify(prompt)[:48]
    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        image_url = item.get("url")
        b64_json = item.get("b64_json")
        if not image_url and not b64_json:
            continue
        ext = infer_extension(item, image_url if isinstance(image_url, str) else None)
        filename = f"{prefix}-{idx}{ext}"
        target = out_dir / filename
        if isinstance(image_url, str) and image_url:
            download_url(image_url, target)
        else:
            target.write_bytes(base64.b64decode(str(b64_json)))
        saved.append(
            {
                "file": filename,
                "path": str(target),
                "prompt": prompt,
                "source_url": image_url if isinstance(image_url, str) else "",
            }
        )

    if not saved:
        raise RuntimeError(f"Seedream API response could not be saved: {json.dumps(response, ensure_ascii=False)}")

    (out_dir / "manifest.json").write_text(
        json.dumps(
            {
                "model": response.get("model", DEFAULT_MODEL),
                "created_at": dt.datetime.now().isoformat(),
                "prompt": prompt,
                "count": len(saved),
                "items": saved,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    write_gallery(out_dir, saved)
    return saved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate images with Doubao Seedream via Volcano Engine ARK.")
    parser.add_argument("--prompt", required=True, help="Text prompt for image generation.")
    parser.add_argument("--count", type=int, default=1, help="How many images to request (1-4).")
    parser.add_argument("--size", default=DEFAULT_SIZE, help="Requested size: 1K (1024x1024) or 2K (2048x2048).")
    parser.add_argument("--model", default=os.environ.get("SEEDREAM_MODEL", DEFAULT_MODEL), help="Seedream model ID.")
    parser.add_argument("--endpoint", default=os.environ.get("SEEDREAM_API_ENDPOINT", DEFAULT_ENDPOINT), help="ARK images endpoint URL.")
    parser.add_argument("--out-dir", default="", help="Output directory. Default: ~/.openclaw/workspace/tmp/doubao-maliang-image-gen-<timestamp>")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prompt = args.prompt.strip()
    if not prompt:
        raise RuntimeError("Prompt must not be empty.")
    if args.count < 1 or args.count > 4:
        raise RuntimeError("Count must be between 1 and 4.")

    out_dir = Path(args.out_dir).expanduser() if args.out_dir else default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    response = request_images(
        api_key=resolve_api_key(),
        prompt=prompt,
        model=args.model,
        endpoint=args.endpoint,
        size=args.size,
        count=args.count,
    )
    saved = save_outputs(out_dir, prompt, response)

    print(f"Saved {len(saved)} image(s) to {out_dir}")
    for item in saved:
        print(item["path"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as err:
        print(f"Error: {err}", file=sys.stderr)
        raise SystemExit(1)
