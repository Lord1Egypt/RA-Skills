---
name: comfyui-imagegen
description: Generate images via ComfyUI API (localhost:8188) using Flux2 workflow. Supports prompt/seed/steps customization. Use when user requests AI image generation with ComfyUI (e.g., 'generate image of X using ComfyUI').
---

# ComfyUI ImageGen

## Changelog
- **[2026-02-10 23:05]**: **v1.0.2** - Workflow v3: "Image Save with Prompt/Info (WLSH)" (node 85) for improved metadata embedding. Script updated to poll node 85.
- **[2026-02-10 23:00]**: Added explicit instruction to **always send generated image** to user post-generation via `message` tool.
- **[2026-02-10]**: Updated to new workflow: JPG output with embedded prompt/metadata via "Image Save with Prompt File (WLSH)". Model changed to `darkBeastFeb0826Latest_dbkBlitzV15.safetensors`. Script now polls node 84.

## Usage

1. Verify ComfyUI runs on `localhost:8188` (or override `--host`).
2. exec: `python skills/comfyui-imagegen/scripts/generate.py "your prompt here" --output ./my-image.png`
3. **Always send** generated JPG to user **immediately** via `message` tool's `media`/`path` (e.g., `message action=send channel=telegram media=./output.jpg replyTo=<message_id>`; infer channel/current replyTo as needed).
4. Customize:
   | Arg | Default | Notes |
   |-----|---------|-------|
   | `--seed` | random | Fix for repro
   | `--steps` | 5 | Up to 20-50 for quality
   | `--host` | localhost:8188 | Remote if needed
   | `--output` | gen-{seed}.jpg | Full path

## Workflow Details

- Model: darkBeastFeb0826Latest_dbkBlitzV15.safetensors (Flux2 variant)
- CLIP: qwen_3_8b_fp8mixed.safetensors
- VAE: flux2-vae.safetensors
- Sampler: dpmpp_2m (CFG=1.0)
- Size: 1024x1024
- Template: workflows/flux2.json (edit for advanced changes)

Script handles POST `/prompt`, polls `/history`, downloads via `/view`.

## Examples

```bash
python skills/comfyui-imagegen/scripts/generate.py "A butler in a library" --steps 10 --output ./butler.jpg
```

For batch/variants: Loop in bash or spawn sub-agent.