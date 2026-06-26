from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from render_brat import render_image, resolve_font_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse !brat command and generate assets.")
    parser.add_argument("message", help="Raw message, e.g. '!brat hello world'")
    parser.add_argument("--out-dir", default=".", help="Optional subdirectory under the managed output directory")
    parser.add_argument("--size", type=int, default=1024)
    parser.add_argument("--sticker-size", type=int, default=512)
    parser.add_argument("--font-size", type=int, default=120)
    parser.add_argument("--blur", type=float, default=2.8)
    parser.add_argument("--padding-x", type=int, default=120)
    parser.add_argument("--shift-y", type=int, default=0)
    return parser.parse_args()


def sanitize_slug(text: str, max_len: int = 40) -> str:
    normalized = text.strip().lower().replace("/", "-").replace("\\", "-")
    normalized = normalized.replace("..", "-")
    normalized = re.sub(r"[^a-z0-9._-]+", "-", normalized)
    normalized = re.sub(r"-+", "-", normalized).strip("-._")
    return (normalized[:max_len] or "brat")


def resolve_safe_out_dir(requested: str) -> Path:
    base_out_dir = (Path(__file__).parent / "out").resolve()
    base_out_dir.mkdir(parents=True, exist_ok=True)

    requested_path = Path(requested or "")
    if not requested or str(requested_path) in {"", "."}:
        return base_out_dir

    if requested_path.is_absolute():
        try:
            resolved = requested_path.resolve()
            if resolved == base_out_dir or base_out_dir in resolved.parents:
                resolved.mkdir(parents=True, exist_ok=True)
                return resolved
        except OSError:
            pass
        return base_out_dir

    requested_str = str(requested_path).replace("\\", "/")
    safe_parts = []
    for part in requested_str.split("/"):
        part = part.strip()
        if not part or part in {".", ".."}:
            continue
        part = re.sub(r"[^A-Za-z0-9._-]+", "-", part).strip("-._")
        if part:
            safe_parts.append(part)

    safe_dir = base_out_dir.joinpath(*safe_parts) if safe_parts else base_out_dir
    safe_dir.mkdir(parents=True, exist_ok=True)
    return safe_dir


def main() -> int:
    args = parse_args()
    raw = (args.message or "").strip()
    if not raw.lower().startswith("!brat"):
        print(json.dumps({"ok": False, "error": "message must start with !brat"}))
        return 1

    text = raw[5:].strip()
    if not text:
        print(json.dumps({"ok": False, "error": "missing text after !brat"}))
        return 1

    slug = sanitize_slug(text)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = resolve_safe_out_dir(args.out_dir)
    font_path = str(resolve_font_path())

    png_path = out_dir / f"{stamp}-{slug}.png"
    webp_path = out_dir / f"{stamp}-{slug}.webp"

    image_png = render_image(
        text=text,
        size=args.size,
        font_size=args.font_size,
        blur=args.blur,
        padding_x=args.padding_x,
        shift_y=args.shift_y,
        background="#FFFFFF",
        color="#111111",
        min_font_size=16,
        font_path=font_path,
    )
    image_png.save(png_path, format="PNG")

    image_webp = render_image(
        text=text,
        size=args.sticker_size,
        font_size=args.font_size,
        blur=args.blur,
        padding_x=max(36, round(args.padding_x * (args.sticker_size / max(args.size, 1)))),
        shift_y=round(args.shift_y * (args.sticker_size / max(args.size, 1))),
        background="#FFFFFF",
        color="#111111",
        min_font_size=16,
        font_path=font_path,
    )
    image_webp.save(webp_path, format="WEBP", lossless=True, quality=95, method=6)

    print(json.dumps({
        "ok": True,
        "text": text,
        "png": str(png_path),
        "webp": str(webp_path),
        "stickerCandidate": str(webp_path)
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
