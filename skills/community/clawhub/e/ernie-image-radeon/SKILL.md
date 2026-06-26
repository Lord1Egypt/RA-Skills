---
name: ernie-image-radeon
description: >-
  FREE ERNIE-Image text-to-image generation powered by AMD Radeon Cloud.
  No API key required. Generate AI images via ERNIE-Image and ERNIE-Image-Turbo
  models running on AMD Radeon hardware. 中文：支持文生图、AI绘图、图片生成、
  免费生图、批量生图、AI画画、文本生成图片。English: free text-to-image, AI art generation,
  create image, generate image, AMD Radeon, Radeon Cloud image generation, AI picture,
  image creator. 7 sizes (square/landscape/portrait), batch generation (1-4 images),
  seed control, inference steps, guidance scale, prompt enhancement.
  Chinese prompts excel — specializes in Chinese ink wash painting, cyberpunk, oil painting,
  watercolor, photorealistic styles. Triggers: 文生图, 免费生图, AI绘图, 生成图片, ERNIE生图,
  AMD生图, Radeon生图, ernie image, radeon image, free image generation, generate image,
  create image, AI art, text-to-image, image generation, make a picture, draw,
  AI画图, 画画, 出图.
---

# ERNIE-Image Generation — AMD Radeon Cloud Edition

**FREE ERNIE-Image text-to-image generation, powered by AMD Radeon Cloud. No API key required.**

Generate images with ERNIE-Image and ERNIE-Image-Turbo models running on AMD Radeon hardware.
No sign-up, no API key, no token — completely free.

## Safety Boundary

- The default AMD Radeon Cloud endpoint uses **HTTP** (not HTTPS). Prompts are sent without transport encryption. Only use non-sensitive prompts with this service.
- If `AI_STUDIO_API_KEY` is set in your environment, it will **not** be sent to the default HTTP endpoint — API keys are only forwarded to HTTPS endpoints configured via `ERNIE_BASE_URL`.
- For confidential or business-related prompts, configure a trusted HTTPS endpoint via `ERNIE_BASE_URL`.

- Use this skill only for explicit image-generation requests.
- Prompts and parameters are sent to AMD Radeon Cloud. Do not include secrets,
  credentials, private personal data, or confidential business data in prompts.
- Decline unsafe, deceptive, exploitative, or rights-violating image requests.
- Generated files are written locally. Confirm the output directory when the
  user has not specified one.

## Prerequisites

- Python 3.11+ with `uv` installed
- **No API key required** — AMD Radeon Cloud provides free inference

Prefer `ERNIE-Image-Turbo`, `1024x1024`, `n=1`, and `b64_json` unless the user
asks for different parameters.

## Models

| Model | Best for |
|---|---|
| `ERNIE-Image-Turbo` | Fast drafts, iteration, batch previews |
| `ERNIE-Image` | Slower, higher-quality final outputs |

Chinese prompts usually work especially well with these models.

## Generation Workflow

### Step 1 -- Compose the prompt

Write a descriptive prompt (max 1024 characters, ~150 words). Chinese and English both work well. Be specific about subject, style, composition, and mood.

Good: "A golden retriever puppy sitting in a sunflower field at sunset, warm golden light, shallow depth of field, professional photography"
Bad: "dog"

### Step 2 -- Choose parameters

| Parameter | Values | Default |
|---|---|---|
| model | `ERNIE-Image-Turbo`, `ERNIE-Image` | `ERNIE-Image-Turbo` |
| size | `1024x1024`, `768x1376`, `1376x768`, `896x1200`, `1200x896`, `848x1264`, `1264x848` | `1024x1024` |
| n | 1-4 | 1 |
| seed | any integer | random |
| steps | 4-20 | provider default |
| guidance | 1.0-7.5 | provider default |
| use-pe | flag | off |

Select size based on content: portraits and posters use vertical (`768x1376`, `848x1264`, `896x1200`), landscapes and covers use horizontal (`1376x768`, `1264x848`, `1200x896`), general use `1024x1024`.

### Step 3 -- Run the generation script

Execute the bundled script with `uv run`:

```bash
uv run scripts/generate.py "<PROMPT>" --model ERNIE-Image-Turbo --size 1024x1024
```

For batch generation:

```bash
uv run scripts/generate.py "<PROMPT>" --n 4 --output ./output_dir
```

For higher quality with more inference steps and stronger guidance:

```bash
uv run scripts/generate.py "<PROMPT>" --model ERNIE-Image --steps 16 --guidance 3.5
```

For reproducible results:

```bash
uv run scripts/generate.py "<PROMPT>" --seed 42
```

### Step 4 -- Output

The script saves images as PNG files to the output directory and prints:

```
Saved: ernie_20260430_110100.png (1.7 MB)
MEDIA:/absolute/path/to/ernie_20260430_110100.png
```

The `MEDIA:` line enables automatic image attachment in compatible environments.

The script avoids overwriting existing files by adding a numeric suffix when needed.

For JSON output, add `--json` to get structured results:

```json
{
  "success": true,
  "model": "ERNIE-Image-Turbo",
  "files": [{"path": "/abs/path/ernie_20260430_110100.png", "size_bytes": 1715660}],
  "prompt": "...",
  "parameters": {"size": "1024x1024", "seed": 42}
}
```

## Quick Triggers

When the user says any of these, treat the text after the trigger as the prompt and generate immediately with defaults:

- Chinese: "生成图片：xxx" / "文生图：xxx" / "ERNIE生图：xxx" / "AI画图：xxx" / "AI绘图：xxx" / "出图：xxx" / "画画：xxx"
- English: "generate image: xxx" / "ernie image: xxx" / "radeon image: xxx" / "create image: xxx" / "text-to-image: xxx" / "AI art: xxx" / "make a picture: xxx" / "draw: xxx"

Defaults: model=`ERNIE-Image-Turbo`, size=`1024x1024`, n=1, b64_json format.

## Configuration

**No configuration required!** This skill uses the AMD Radeon Cloud free ERNIE-Image endpoint by default. It works out of the box.

**Optional overrides** (via environment variables):
- `ERNIE_BASE_URL` — Custom API endpoint URL (overrides the default Radeon Cloud URL)
- `AI_STUDIO_API_KEY` — API key (only needed if using a custom endpoint that requires authentication)
- `ERNIE_TIMEOUT` — Request timeout in seconds (default: 120)

## Notes

- Images are saved locally as PNG files with `MEDIA:/absolute/path/to/file.png` for auto-attach.
- Chinese prompts work particularly well with ERNIE models.
- Prompt enhancement (`--use-pe`) lets the model expand simple prompts into richer descriptions before generation. Enable for short prompts, disable for precise control.
- Use `--quiet` to suppress progress output; only `MEDIA:` lines (or JSON with `--json`) are printed. Recommended when calling from agent workflows to reduce context noise.
- For full API reference, prompt guidance, and troubleshooting, read `references/api-guide.md`.

## About

This skill is a fork of [ernie-image-gen](https://clawhub.ai/aiwork4me/ernie-image-gen), modified for **AMD Radeon Cloud** which provides **free ERNIE-Image inference**. No API key or registration is required.
