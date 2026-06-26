---
name: echoflow-image-gen
description: Generate or edit images via EchoFlow API using Nano Banana Pro (Gemini 3 Pro Image). Supports image generation, image editing, and multi-image composition (up to 14 images). Use when user asks to generate images, create images, edit images, or combine images. Keywords: 图像生成, 图片生成, 生成图片, AI绘画, Nano Banana Pro, Gemini, Gemini 3 Pro Image.
homepage: https://api.echoflow.cn/
metadata:
  openclaw:
    emoji: "🍌"
    requires:
      bins: ["uv"]
      env: ["ECHOFLOW_API_KEY"]
    primaryEnv: "ECHOFLOW_API_KEY"
---

# EchoFlow Image Generation (Nano Banana Pro)

Generate or edit images using EchoFlow API with Nano Banana Pro (Gemini 3 Pro Image). EchoFlow provides OpenAI-compatible access to Gemini's powerful image generation model.

## Setup

1. Get your API key from EchoFlow: https://api.echoflow.cn/
2. Set environment variable: `ECHOFLOW_API_KEY`
3. Alternatively, set in OpenClaw config: `skills."echoflow-image-gen".apiKey`

## Quick Start

### Generate Image

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "a serene mountain landscape at sunset" --filename "mountain.png"
```

### Edit Image (Single)

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "add a rainbow in the sky" --filename "edited.png" -i "/path/to/input.png"
```

### Multi-Image Composition (up to 14 images)

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "combine these into one scene" --filename "combined.png" -i img1.png -i img2.png -i img3.png
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--prompt`, `-p` | Image description (required) | - |
| `--filename`, `-f` | Output filename (required) | - |
| `--input-image`, `-i` | Input image for editing (can repeat, max 14) | - |
| `--resolution`, `-r` | Output resolution: `1K`, `2K`, `4K` | `1K` |
| `--model`, `-m` | Model name | `gemini-3.1-flash-image-preview` |
| `--api-key`, `-k` | Override API key | - |
| `--api-base` | Override API base URL | `https://api.echoflow.cn/v1` |

## Available Models

- **gemini-3.1-flash-image-preview** (default) - Faster, more available
- **gemini-3-pro-image-preview** - Higher quality, may have availability issues

## Resolutions

- **1K** (default) - Standard quality
- **2K** - High quality
- **4K** - Ultra high quality

**Auto-detection**: When editing images, the script auto-detects resolution from the largest input dimension:
- Input ≥3000px → 4K
- Input ≥1500px → 2K
- Input <1500px → 1K

## Output

The script outputs:
- `Image saved: <full-path>` - Location of saved image
- `MEDIA: <full-path>` - Token for OpenClaw to auto-attach the image on supported chat providers

## Examples

```bash
# Simple generation
uv run {baseDir}/scripts/generate_image.py -p "a cute cat wearing a hat" -f "cat.png"

# High resolution
uv run {baseDir}/scripts/generate_image.py -p "futuristic city" -f "city.png" -r 4K

# Edit single image
uv run {baseDir}/scripts/generate_image.py -p "add snow to the scene" -f "snowy.png" -i summer.png

# Compose multiple images
uv run {baseDir}/scripts/generate_image.py -p "create a collage of these photos" -f "collage.png" -i photo1.png -i photo2.png -i photo3.png -i photo4.png

# Use gemini-3-pro-image-preview model
uv run {baseDir}/scripts/generate_image.py -p "abstract art" -f "art.png" -m "gemini-3-pro-image-preview"
```

## API Reference

For detailed API documentation, see [echoflow_api.md](references/echoflow_api.md).

## Notes

- Use timestamp-based filenames for organization: `2024-03-28-18-30-landscape.png`
- The script outputs a `MEDIA:` line for OpenClaw to auto-attach the image on supported providers
- Do not read the image back; report the saved path only
- For editing, ensure input images are in supported formats (PNG, JPEG, WebP)
- Nano Banana Pro supports up to 14 input images for composition
- If you get 429 errors, the upstream is saturated - wait a moment and retry
- EchoFlow API is OpenAI-compatible, so this skill works with any OpenAI-compatible endpoint by changing `--api-base`
