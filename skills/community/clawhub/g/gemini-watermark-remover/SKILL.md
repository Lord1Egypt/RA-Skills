---
name: gemini-watermark-remover
description: Remove visible Gemini AI watermarks from images via reverse alpha blending. Use for cleaning Gemini-generated images, removing the star/sparkle logo watermark.
metadata:
  author: star-master
  version: "1.0.0"
---

# Gemini Watermark Remover

Remove visible Gemini AI watermarks (star/sparkle logo) from generated images using mathematically accurate reverse alpha blending.

**Fully offline — pure Python, local processing only, images are not uploaded.**

## When to Use

- Remove watermark from Gemini AI generated images
- Clean images before publishing or sharing
- Batch process multiple images

## Quick Start

### Install Dependencies (one-time)

```bash
pip install Pillow numpy
```

### Usage

```bash
# Single image (auto-detect watermark)
python3 scripts/remove_watermark.py photo.jpg

# Specify output path
python3 scripts/remove_watermark.py photo.jpg -o clean_photo.jpg

# Force removal without detection
python3 scripts/remove_watermark.py photo.jpg -o clean.jpg --force
```

## How It Works

Gemini adds watermark using alpha blending:

```
watermarked = alpha * 255 + (1 - alpha) * original
```

Reverse the equation:

```
original = (watermarked - alpha * 255) / (1 - alpha)
```

### Detection Rules

| Image Size | Watermark Size | Right Margin | Bottom Margin |
|------------|---------------|--------------|---------------|
| Width > 1024 AND Height > 1024 | 96×96 | 64px | 64px |
| Otherwise | 48×48 | 32px | 32px |

## Key Points

- Uses built-in watermark templates (`assets/bg_48.png` / `assets/bg_96.png`)
- Alpha map = max RGB channel value (not alpha channel)
- Includes noise filtering (ALPHA_NOISE_FLOOR)
- Pure mathematical method, pixel-level accuracy

## Limitations

- Removes only visible watermark (bottom-right semi-transparent logo)
- Cannot remove invisible watermarks (e.g., SynthID)
- Designed for current Gemini watermark pattern

## Dependencies

- Python 3
- Pillow (PIL)
- NumPy
