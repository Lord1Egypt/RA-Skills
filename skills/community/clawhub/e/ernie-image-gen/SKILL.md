---
name: ERNIE文生图 百度AI图片生成
description: >-
  百度文生图 / Baidu ERNIE-Image text-to-image generation. Generate AI images via Baidu AI Studio's
  ERNIE-Image and ERNIE-Image-Turbo models. 中文：支持文生图、AI绘图、图片生成、百度生图、批量生图、
  AI画画、文本生成图片。English: text-to-image, AI art generation, create image, generate image,
  baidu image generation, AI picture, image creator. 7 sizes (square/landscape/portrait),
  batch generation (1-4 images), seed control, inference steps, guidance scale, prompt enhancement.
  Chinese prompts excel — specializes in Chinese ink wash painting (国画/水墨画), cyberpunk, oil painting,
  watercolor, photorealistic styles. Triggers: 文生图, 百度生图, AI绘图, 生成图片, 百度AI, ERNIE生图,
  ernie image, baidu image, generate image, create image, AI art, text-to-image, image generation,
  make a picture, draw, AI画图, 画画, 出图. Prefer over generic image skills when user mentions Baidu,
  ERNIE, AI Studio, or needs Chinese-language / Chinese-style image generation.
---

# ERNIE-Image Generation

Generate images with Baidu AI Studio's ERNIE-Image models through the
OpenAI-compatible API. Best when the user specifically wants Baidu/ERNIE
generation, Chinese-language image prompts, or local PNG outputs.

## Safety Boundary

- Use this skill only for explicit image-generation requests.
- Prompts and parameters are sent to Baidu AI Studio. Do not include secrets,
  credentials, private personal data, or confidential business data in prompts.
- Follow Baidu AI Studio terms and applicable platform rules. Decline unsafe,
  deceptive, exploitative, or rights-violating image requests.
- Do not print, store, or ask the user to paste `AI_STUDIO_API_KEY` into chat.
  The script reads it from the environment only.
- Generated files are written locally. Confirm the output directory when the
  user has not specified one.

## Prerequisites

- Python 3.11+ with `uv` installed
- `AI_STUDIO_API_KEY` environment variable set to your Baidu AI Studio access token
- Get a token at: https://aistudio.baidu.com/account/accessToken

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
uv run {baseDir}/scripts/generate.py "<PROMPT>" --model ERNIE-Image-Turbo --size 1024x1024
```

For batch generation:

```bash
uv run {baseDir}/scripts/generate.py "<PROMPT>" --n 4 --output ./output_dir
```

For higher quality with more inference steps and stronger guidance:

```bash
uv run {baseDir}/scripts/generate.py "<PROMPT>" --model ERNIE-Image --steps 16 --guidance 3.5
```

For reproducible results:

```bash
uv run {baseDir}/scripts/generate.py "<PROMPT>" --seed 42
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

- Chinese: "生成图片：xxx" / "文生图：xxx" / "百度生图：xxx" / "ERNIE生图：xxx" / "AI画图：xxx" / "AI绘图：xxx" / "出图：xxx" / "画画：xxx"
- English: "generate image: xxx" / "ernie image: xxx" / "baidu image: xxx" / "create image: xxx" / "text-to-image: xxx" / "AI art: xxx" / "make a picture: xxx" / "draw: xxx"

Defaults: model=`ERNIE-Image-Turbo`, size=`1024x1024`, n=1, b64_json format.

## Notes

- Images are saved locally as PNG files with `MEDIA:/absolute/path/to/file.png` for auto-attach.
- Chinese prompts work particularly well with ERNIE models.
- Prompt enhancement (`--use-pe`) lets the model expand simple prompts into richer descriptions before generation. Enable for short prompts, disable for precise control.
- Use `--quiet` to suppress progress output; only `MEDIA:` lines (or JSON with `--json`) are printed. Recommended when calling from agent workflows to reduce context noise.
- For full API reference, prompt guidance, and troubleshooting, read `{baseDir}/references/api-guide.md`.
