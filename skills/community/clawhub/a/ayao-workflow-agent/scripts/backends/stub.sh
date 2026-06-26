#!/bin/bash
# stub.sh — Offline placeholder image backend

set -euo pipefail

PROMPT="${1:-}"
OUTPUT="${2:-}"
STYLE="${3:-}"

if [[ -z "$PROMPT" || -z "$OUTPUT" ]]; then
  echo "Usage: stub.sh <prompt> <output> [style]" >&2
  exit 1
fi

STUB_PROMPT="$PROMPT" STUB_OUTPUT="$OUTPUT" STUB_STYLE="$STYLE" python3 - <<'PYEOF'
import base64
import os
import textwrap

prompt = os.environ["STUB_PROMPT"]
output = os.environ["STUB_OUTPUT"]
style = os.environ.get("STUB_STYLE", "")

try:
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (800, 400), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)

    draw.rectangle([10, 10, 789, 389], outline=(180, 180, 180), width=2)
    draw.text((20, 20), "[DIAGRAM PLACEHOLDER]", fill=(100, 100, 100))

    lines = [prompt]
    if style:
        lines.append(f"Style: {style}")
    wrapped = textwrap.fill("\n".join(lines), width=80)
    draw.text((20, 60), wrapped, fill=(60, 60, 60))

    img.save(output)
    print("stub image saved")
except ImportError:
    minimal_png = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    with open(output, "wb") as f:
        f.write(minimal_png)
    print("minimal stub image saved")
PYEOF
