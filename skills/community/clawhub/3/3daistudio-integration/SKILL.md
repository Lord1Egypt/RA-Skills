---
name: 3daistudio
description: Convert images and text prompts to 3D models (.glb) using the 3D AI Studio API. Supports TRELLIS.2, Hunyuan Rapid, and Hunyuan Pro models.
homepage: https://www.3daistudio.com
owner: Whale Professor
repository: https://github.com/whale-professor/3daistudio-skill
credentials:
  primary: THREE_D_AI_STUDIO_API_KEY
  type: api_key
  help: "Get your API key from https://www.3daistudio.com/Platform/API"
required_env:
  - THREE_D_AI_STUDIO_API_KEY
tags:
  - 3d
  - ai
  - image-to-3d
  - text-to-3d
  - model-generation
  - 3d-printing
---

# 3D AI Studio Skill

Convert images (or text prompts) to 3D models using the 3D AI Studio API.

## Credentials

- **API Key:** Set via `THREE_D_AI_STUDIO_API_KEY` environment variable
- **Base URL:** `https://api.3daistudio.com`
- **Get API Key:** https://www.3daistudio.com/Platform/API
- **Documentation:** https://www.3daistudio.com/Platform/API/Documentation

## Setup

```bash
# Set your API key
export THREE_D_AI_STUDIO_API_KEY="your-api-key-here"

# Run the skill
python 3daistudio.py balance
```

## Available Models

| Model | Endpoint | Input | Credits | Speed |
|-------|----------|-------|---------|-------|
| Hunyuan Rapid | `/v1/3d-models/tencent/generate/rapid/` | Text or image | 35-55 | 2-3 min |
| Hunyuan Pro | `/v1/3d-models/tencent/generate/pro/` | Text, image, multi-view | 60-100 | 3-6 min |
| TRELLIS.2 | `/v1/3d-models/trellis2/generate/` | Image only | 15-55 | 25s-4min |

## Workflow (ALL models are async)

1. **Submit** - POST to generation endpoint - get `task_id`
2. **Poll** - GET `/v1/generation-request/{task_id}/status/` every 10-15s
3. **Download** - When `status == "FINISHED"`, use `results[].asset` URL

The script auto-polls and downloads when you use `--output`.

## How to Use

```bash
# Check credit balance
python 3daistudio.py balance

# Image to 3D (TRELLIS.2 - fastest, image-only)
python 3daistudio.py trellis --image photo.png --textures -o model.glb

# Image to 3D (Hunyuan Rapid - text or image)
python 3daistudio.py rapid --image photo.png --pbr -o model.glb
python 3daistudio.py rapid --prompt "a red sports car" -o model.glb

# Image to 3D (Hunyuan Pro - highest quality)
python 3daistudio.py pro --image photo.png --pbr --model 3.1 -o model.glb
python 3daistudio.py pro --prompt "a cute blue hedgehog" -o model.glb

# Check status
python 3daistudio.py status <task_id>

# Download result
python 3daistudio.py download <task_id> -o model.glb
```

## Options

### TRELLIS.2
- `--image` - Path to local image (PNG/JPG/WebP)
- `--resolution` - 512, 1024 (default), or 1536
- `--textures` - Enable PBR textures
- `--texture-size` - 1024, 2048 (default), or 4096

### Hunyuan Rapid
- `--image` - Path to local image
- `--prompt` - Text description
- `--pbr` - Enable PBR textures (+20 credits)

### Hunyuan Pro
- `--image` - Path to local image
- `--prompt` - Text description
- `--model` - 3.0 or 3.1 (default: 3.1)
- `--pbr` - Enable PBR textures (+20 credits)
- `--generate-type` - Normal, LowPoly, Geometry, or Sketch

## Credit Costs

### TRELLIS.2
| Resolution | Geometry Only | Textured 2048 | Textured 4096 |
|-----------|---------------|---------------|---------------|
| 512 | 15 | 25 | 30 |
| 1024 (default) | 20 | 30 | 40 |
| 1536 | 25 | 40 | 55 |
| +thumbnail | +2 | +2 | +2 |

### Hunyuan
| Edition | Base | +PBR | +Multi-View | Max |
|---------|------|------|-------------|-----|
| Rapid | 35 | +20 | N/A | 55 |
| Pro | 60 | +20 | +20 | 100 |

## Tips

- **TRELLIS.2** = best for image-to-3D; fast, cheap, great quality
- **Hunyuan Rapid** = good balance, supports text-to-3D
- **Hunyuan Pro** = highest quality, supports multi-view input
- Rate limit: **3 requests/minute**
- Results expire after **24 hours**
- Failed jobs are **automatically refunded**
- For best TRELLIS results: clean background or transparent PNG
