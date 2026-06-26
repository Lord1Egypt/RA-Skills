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

## Install

```bash
clawhub install fal-api
```

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

### Python Module

```python
from fal_api import FalAPI

api = FalAPI()

# Generate and wait
urls = api.generate_and_wait(
    prompt="A serene Japanese garden",
    model="flux-dev",
    guidance_scale=5.0,
    num_inference_steps=20
)
print(urls)
```

## Available Models

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

## Parameters

| Parameter | Type | Default | Description |
| ---------- | ---- | ------- | ----------- |
| prompt | str | required | Image/video description |
| model | str | "flux-dev" | Model name from table above |
| image_size | str | "landscape_16_9" | Preset: square, portrait_4_3, landscape_16_9, etc. |
| num_images | int | 1 | Number of images to generate |
| seed | int | None | Random seed for reproducibility |
| guidance_scale | float | None | CFG scale (how closely to follow prompt) |
| num_inference_steps | int | None | Inference steps (higher = more detail, slower) |

## Requirements

- Python 3.7+
- No external dependencies (uses stdlib only)

## License

MIT