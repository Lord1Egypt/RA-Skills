---
name: cutout-visual-api
description: Call Cutout.Pro visual processing APIs to perform background removal, face cutout, and photo enhancement. Supports both file upload and image URL input, returning binary stream or Base64-encoded results.
risk: safe
source: community
date_added: '2026-03-13'
author: cutout-pro
tags:
- image-processing
- background-removal
- face-cutout
- photo-enhance
- api
tools:
- claude-code
- cursor
- codex-cli
---

# Cutout.Pro Visual API — Image Processing Toolkit

## Overview

Access three core image processing capabilities via the Cutout.Pro REST API:

1. **Background Remover** — Automatically detects the foreground, removes the background, and returns a transparent PNG
2. **Face Cutout** — Precisely segments the face and hair region, with support for 68-point facial landmark detection
3. **Photo Enhancer** — AI super-resolution enhancement that transforms blurry, low-quality photos into high-definition images

## When to Use This Skill

- When the user needs to remove an image background
- When the user needs to extract a face or avatar region
- When the user needs to improve photo clarity or resolution
- When the user mentions "background removal", "cutout", "portrait segmentation", or related topics
- When the user mentions "image enhancement", "super resolution", "photo restoration", or related topics

## Do Not Use This Skill When

- The task is unrelated to image processing
- The user needs to generate a new image (not process an existing one)
- The user needs video processing (use another tool)

## How It Works

Images are processed by the Cutout.Pro API using AI. Each call consumes credits (standard: 1 credit/image; preview mode: 0.25 credits/image).

## API Comparison

| Use Case | Recommended API |
|----------|----------------|
| Remove background from products, people, or animals | **Background Remover** |
| Extract face/hair region for avatars | **Face Cutout** |
| Turn a blurry photo into HD | **Photo Enhancer** |
| Super-resolution for anime/cartoon images | **Photo Enhancer** (faceModel=anime) |
| Get facial landmark coordinates | **Face Cutout** (faceAnalysis=true) |

## Quick Start

1. Go to https://www.cutout.pro/user/secret-key to get your API Key
2. Add it to your `.env` file: `CUTOUT_API_KEY=your_key_here`
3. Install dependencies: `pip install -r scripts/requirements.txt`
4. Run the script: `python scripts/cutout.py --api bg-remover --image photo.jpg`

See `references/setup-guide.md` for full setup instructions.

## 1. Operation Modes

| CLI Argument | Function | Endpoint |
|-------------|----------|----------|
| `--api bg-remover` | Background removal (file upload, binary response) | `/api/v1/matting?mattingType=6` |
| `--api bg-remover --base64` | Background removal (file upload, Base64 response) | `/api/v1/matting2?mattingType=6` |
| `--api bg-remover --url` | Background removal (image URL, Base64 response) | `/api/v1/mattingByUrl?mattingType=6` |
| `--api face-cutout` | Face cutout (file upload, binary response) | `/api/v1/matting?mattingType=3` |
| `--api face-cutout --base64` | Face cutout (file upload, Base64 response) | `/api/v1/matting2?mattingType=3` |
| `--api face-cutout --url` | Face cutout (image URL, Base64 response) | `/api/v1/mattingByUrl?mattingType=3` |
| `--api photo-enhancer` | Photo enhancement (file upload, binary response) | `/api/v1/photoEnhance` |
| `--api photo-enhancer --base64` | Photo enhancement (file upload, Base64 response) | `/api/v1/photoEnhance2` |
| `--api photo-enhancer --url` | Photo enhancement (image URL, Base64 response) | `/api/v1/photoEnhanceByUrl` |

## 2. Usage Examples

```bash
# Background removal — upload file, save as PNG
python scripts/cutout.py --api bg-remover --image product.jpg --output out.png

# Background removal — pass image URL, get Base64
python scripts/cutout.py --api bg-remover --url "https://example.com/photo.jpg"

# Background removal — crop whitespace, add white background
python scripts/cutout.py --api bg-remover --image photo.jpg --crop --bgcolor FFFFFF

# Face cutout — upload file, save as PNG
python scripts/cutout.py --api face-cutout --image portrait.jpg --output face.png

# Face cutout — get Base64 + 68 facial landmarks
python scripts/cutout.py --api face-cutout --image portrait.jpg --base64 --face-analysis

# Photo enhancement — upload file, save HD image
python scripts/cutout.py --api photo-enhancer --image blurry.jpg --output hd.png

# Photo enhancement — anime/cartoon super-resolution
python scripts/cutout.py --api photo-enhancer --image anime.jpg --face-model anime

# Preview mode (0.25 credits, max 500×500)
python scripts/cutout.py --api bg-remover --image photo.jpg --preview
```

## 3. Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--api` | Select API: `bg-remover`, `face-cutout`, `photo-enhancer` | Required |
| `--image` | Local image file path | — |
| `--url` | Image URL (replaces --image in URL mode) | — |
| `--output` | Output file path | `data/outputs/` |
| `--base64` | Return Base64 JSON instead of binary stream | false |
| `--crop` | Crop whitespace (bg-remover/face-cutout only) | false |
| `--bgcolor` | Background color, hex (e.g. FFFFFF) or blur | — |
| `--preview` | Preview mode, max 500×500, costs 0.25 credits | false |
| `--output-format` | Output format: png, webp, jpg_75, etc. | png |
| `--face-analysis` | Return facial landmarks (face-cutout --base64 only) | false |
| `--face-model` | Enhancement model: quality or anime (photo-enhancer only) | quality |

## 4. Output

Images are saved to `data/outputs/` with the naming pattern: `{api}_{timestamp}.png`

Metadata is saved in a `.meta.json` file containing: API type, parameters, processing time, and file size.

## Integration with Other Tools

- **Image editing**: Use background removal first, then composite a new background
- **Avatar generation**: Face cutout → crop → generate avatar
- **Photo restoration**: Photo enhancement → background removal → composite

## Limits & Quotas

- Supported formats: PNG, JPG, JPEG, BMP, WEBP
- Maximum resolution: 4096×4096 pixels
- Maximum file size: 15 MB
- QPS limit: up to 5 concurrent requests per second
- Credit cost: 1 credit/image (standard), 0.25 credits/image (preview mode)

## File Reference

| File | Purpose |
|------|---------|
| `references/setup-guide.md` | Initial setup, API Key retrieval, troubleshooting |
| `references/api-reference.md` | Full API docs, parameters, response formats, error codes |
| `scripts/cutout.py` | Main script |
| `scripts/config.py` | Configuration management (API Key, endpoints, limits) |
| `scripts/requirements.txt` | Python dependencies |
