#!/usr/bin/env python3

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


def log(level, message, **context):
    payload = {"level": level, "message": message}
    if context:
        payload["context"] = context
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)


def main():
    if len(sys.argv) < 3:
      raise SystemExit("Usage: circle-avatar.py <input> <output> [size]")

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    size = int(sys.argv[3]) if len(sys.argv) > 3 else 96

    log("info", "Starting avatar circle crop", input=str(input_path), output=str(output_path), size=size)

    image = Image.open(input_path).convert("RGBA")
    square = ImageOps.fit(image, (size, size), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size - 1, size - 1), fill=255)

    square.putalpha(mask)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    square.save(output_path, format="PNG")

    log("info", "Avatar circle crop completed", output=str(output_path), size=size)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        log("error", "Avatar circle crop failed", error=str(exc))
        raise
