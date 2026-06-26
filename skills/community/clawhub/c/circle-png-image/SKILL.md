---
name: circle-png-image
description: Convert PNG images into circular PNG avatars with transparent corners. Use when the user asks to crop, mask, cut out, or convert a PNG image into a circle.
version: 1.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python
        - python3
    install:
      - kind: uv
        package: pillow
    emoji: "⭕"
---

# Circle PNG Image

## What This Skill Does

Use this skill to turn any PNG image into a circular PNG with transparency outside the circle. It is intended for avatars, profile photos, icons, and other round image assets.

The default behavior is:

1. Open the input PNG.
2. Convert it to RGBA so transparency is preserved.
3. Center-crop the image to a square using the shorter side.
4. Apply a circular alpha mask.
5. Save the result as a PNG.

## Quick Start

Run the helper script:

```bash
python scripts/circle_png.py input.png output.png
```

If the system uses `python3`:

```bash
python3 scripts/circle_png.py input.png output.png
```

## Options

Set an exact output size:

```bash
python scripts/circle_png.py input.png output.png --size 512
```

Preserve the entire image by padding it to a square before applying the circular mask:

```bash
python scripts/circle_png.py input.png output.png --fit contain
```

Overwrite an existing output file:

```bash
python scripts/circle_png.py input.png output.png --force
```

## Dependency

The script requires Pillow. If it is missing, install it in the active Python environment:

```bash
python -m pip install pillow
```

Prefer a virtual environment when modifying a project:

```bash
python -m venv .venv
.venv/Scripts/python -m pip install pillow
.venv/Scripts/python scripts/circle_png.py input.png output.png
```

On macOS or Linux, use `.venv/bin/python` instead of `.venv/Scripts/python`.

## Agent Instructions

When the user asks to make a PNG circular:

1. Confirm the input image path and desired output path. If no output is specified, use the input name with `-circle.png` appended before the extension.
2. Use `scripts/circle_png.py` to generate the output.
3. Use `--fit cover` by default for avatar-style results.
4. Use `--fit contain` when the user says to preserve the full image.
5. Use `--size` only when the user asks for a specific output dimension.
6. Never overwrite an existing output unless the user explicitly asks or `--force` is appropriate.

## Notes

- Output is always PNG with an alpha channel.
- Non-square inputs are centered automatically.
- The circle touches the output square's edges.
