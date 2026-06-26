---
name: fal-api
description: Fal.Ai Media Generation — Generate images, videos, and audio via fal.ai API (FLUX, SDXL, Whisper, etc.)
version: 1.0.1
metadata:
  {
    "openclaw": { "requires": { "env": ["FAL_KEY"] }, "primaryEnv": "FAL_KEY" },
  }
---

# Fal.Ai Media Generation

Generate images, videos, and transcripts using fal.ai's API with support for FLUX, Stable Diffusion, Whisper, and more.

## Features

- Queue-based async generation (submit → poll → result)
- Support for 600+ AI models
- Image generation (FLUX, SDXL, Recraft)
- Video generation (MiniMax, WAN)
- Speech-to-text (Whisper)
- Robust error handling with clear messages
- Stdlib-only dependencies (no external packages)

## Setup

1. Get your API key from https://fal.ai/dashboard/keys
2. Configure with:

```bash
export FAL_KEY="your-api-key"
```

Or via clawdbot config:

```bash
clawdbot config set skill.fal_api.key YOUR_API_KEY
```

## Usage

### Interactive Mode

```
You: Generate a cyberpunk cityscape with FLUX
clawd: Creates the image and returns the URL
```

### CLI

```bash
# Basic image generation
python3 fal_api.py --prompt "A cyberpunk cityscape" --model flux-schnell

# High-quality with custom settings
python3 fal_api.py --prompt "A sunset over mountains" --model flux-dev \
    --guidance-scale 5.0 --steps 20

# Reproducible (same seed = same image)
python3 fal_api.py --prompt "A robot" --seed 12345

# List available models
python3 fal_api.py --list-models
```

### Python Script

```python
from fal_api import FalAPI

api = FalAPI()

# Generate and wait
urls = api.generate_and_wait(
    prompt="A serene Japanese garden",
    model="flux-dev"
)
print(urls)
```

### Available Models

| Model         | Endpoint                              | Type         |
| ------------- | ------------------------------------- | ------------ |
| flux-schnell  | `fal-ai/flux/schnell`                 | Image (fast) |
| flux-dev      | `fal-ai/flux/dev`                     | Image        |
| flux-pro      | `fal-ai/flux-pro/v1.1-ultra`          | Image (2K)   |
| fast-sdxl     | `fal-ai/fast-sdxl`                    | Image        |
| recraft-v3    | `fal-ai/recraft-v3`                   | Image        |
| sd35-large    | `fal-ai/stable-diffusion-v35-large`   | Image        |
| minimax-video | `fal-ai/minimax-video/image-to-video` | Video        |
| wan-video     | `fal-ai/wan/v2.1/1.3b/text-to-video`  | Video        |
| whisper       | `fal-ai/whisper`                      | Audio        |

For the full list, run:

```bash
python3 fal_api.py --list-models
```

## Parameters

| Parameter  | Type | Default          | Description                                        |
| ---------- | ---- | ---------------- | -------------------------------------------------- |
| prompt     | str  | required         | Image/video description                            |
| model      | str  | "flux-dev"       | Model name from table above                        |
| image_size | str  | "landscape_16_9" | Preset: square, portrait_4_3, landscape_16_9, etc. |
| num_images | int  | 1                | Number of images to generate                       |
| seed       | int  | None             | Random seed for reproducibility                    |
| guidance_scale | float | None | CFG scale (how closely to follow prompt) |
| num_inference_steps | int | None | Inference steps (higher = more detail, slower) |
| steps      | int  | None             | CLI alias for num_inference_steps                  |

### CLI Examples

```bash
# Basic image
python fal_api.py --prompt "A sunset over mountains" --model flux-schnell

# High-quality with custom settings
python fal_api.py --prompt "A cyberpunk city" --model flux-dev \
    --guidance-scale 5.0 --steps 20

# Reproducible (same seed = same image)
python fal_api.py --prompt "A robot" --seed 12345
```

## Error Handling

The skill provides clear error messages for common issues:

- **401 Unauthorized** → Invalid API key
- **429 Rate Limit** → Wait and retry
- **402 Payment Required** → Insufficient credits

## Requirements

- Python 3.7+
- No external dependencies (uses stdlib only)