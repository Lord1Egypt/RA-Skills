---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image on Replicate
user-invocable: true
metadata: {"openclaw": {"emoji": "🎨", "requires": {"env": ["REPLICATE_API_TOKEN"], "bins": ["uv"]}, "primaryEnv": "REPLICATE_API_TOKEN"}}
---

# Nano Banana Pro Image Generator

Generate and edit images using Google's Nano Banana Pro model via the Replicate API.

## Usage

Run the generation script:

    uv run --with replicate python {baseDir}/generate.py --prompt "<user prompt>" [--aspect-ratio 1:1] [--output image.png]

## Options

- `--prompt`: The image description (required)
- `--aspect-ratio`: Ratio like 1:1, 4:3, 16:9 (default: 1:1)
- `--output`: Output file path (default: generated_image.png)

## Rules

- Only use the `google/nano-banana-pro` model. Never fall back to other models like `google/nano-banana` or any alternative. If the model is unavailable or rate-limited, report the error to the user and stop.
- After generating an image, send the image file directly in the chat. Do not just save it to the workspace silently.

## Tips

- For text in images, be specific about fonts, size, and placement
- The model supports resolutions up to 2K
- Safety filtering is on by default
