---
name: comfyui
version: 1.0.0
description: "Generate images and videos via ComfyUI on local GPU. Supports Flux text-to-image, Wan2.1 text-to-video, and image-to-video."
metadata: { "openclaw": { "emoji": "🎨", "requires": { "bins": ["python3"] } } }
tags: ["image-generation", "video-generation", "flux", "wan2.1", "comfyui", "local-gpu"]
---

# ComfyUI — Image & Video Generation

Use to generate **images** (Flux schnell) and **videos** (Wan2.1 T2V/I2V) on the local RTX 5080 GPU.

## Environment

- ComfyUI: `~/ComfyUI` (systemd user service: `comfyui.service`)
- Python venv: `~/comfyui-venv`
- API: `http://127.0.0.1:8188`
- Output: `~/ComfyUI/output/`

## Script

```
{baseDir}/scripts/generate.py <mode> [options]
```

### Mode: `image` — Text-to-Image (Flux schnell)

```bash
{baseDir}/scripts/generate.py image \
  --prompt "A cat on the moon" \
  --output /tmp/output.png
```

| Option | Default | Description |
|--------|---------|-------------|
| `--prompt` | (required) | Text prompt |
| `--negative` | "" | Negative prompt |
| `--width` | 1024 | Image width |
| `--height` | 1024 | Image height |
| `--steps` | 4 | Sampling steps (schnell optimized) |
| `--seed` | random | Reproducible seed |
| `--output` | ComfyUI output dir | Copy output here |
| `--model` | flux1-schnell.safetensors | UNET filename |
| `--weight-dtype` | fp8_e4m3fn | Weight quantization |
| `--wait` | 120 | Max wait seconds |

**Recommended Flux schnell params:** steps=4, cfg=1.0, sampler=euler, scheduler=simple

### Mode: `t2v` — Text-to-Video (Wan2.1 T2V-1.3B)

```bash
{baseDir}/scripts/generate.py t2v \
  --prompt "A red sports car driving on a mountain road at sunset" \
  --length 49 \
  --output /tmp/video_frames/
```

| Option | Default | Description |
|--------|---------|-------------|
| `--prompt` | (required) | Text prompt |
| `--negative` | "" | Negative prompt |
| `--width` | 832 | Frame width |
| `--height` | 480 | Frame height |
| `--length` | 49 | Number of frames (≈3s at 16fps) |
| `--steps` | 20 | Sampling steps |
| `--seed` | random | Reproducible seed |
| `--output` | ComfyUI output dir | Copy frames here |
| `--wait` | 300 | Max wait seconds |

**Recommended Wan2.1 T2V params:** steps=20, cfg=5.0, sampler=uni_pc_bh2, scheduler=simple

### Mode: `i2v` — Image-to-Video (Wan2.1 I2V using T2V-1.3B)

```bash
{baseDir}/scripts/generate.py i2v \
  --prompt "gentle wave motion, water flowing" \
  --image /path/to/input.png \
  --output /tmp/video_frames/
```

| Option | Default | Description |
|--------|---------|-------------|
| `--prompt` | (required) | Motion description |
| `--image` | (required) | Path to input image |
| `--length` | 49 | Number of frames |
| `--steps` | 20 | Sampling steps |
| `--seed` | random | Reproducible seed |
| `--output` | ComfyUI output dir | Copy frames here |
| `--wait` | 300 | Max wait seconds |

## Server Management

```bash
# Start (systemd user service)
systemctl --user start comfyui.service

# Check status
systemctl --user status comfyui.service

# Check API
curl -s http://127.0.0.1:8188/system_stats | python3 -m json.tool

# Manual start (if systemd not available)
cd ~/ComfyUI && LD_LIBRARY_PATH=~/comfyui-venv/lib/python3.12/site-packages/nvidia/cuda_runtime/lib:$LD_LIBRARY_PATH ~/comfyui-venv/bin/python main.py --listen 127.0.0.1 --port 8188
```

## Installed Models

### Image (Flux)
| File | Location | Size |
|------|----------|------|
| flux1-schnell.safetensors | models/unet/ | 23.8GB |
| ae.safetensors | models/vae/ | 335MB |
| clip_l.safetensors | models/clip/ | 250MB |
| t5xxl_fp16.safetensors | models/clip/ | 9.8GB |

### Video (Wan2.1)
| File | Location | Size |
|------|----------|------|
| wan2.1_t2v_1.3B_bf16.safetensors | models/diffusion_models/ | 5.3GB |
| wan2.1_vae.pth | models/vae/ | 485MB |
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | models/text_encoders/ | 6.1GB |
| open_clip_xlm_roberta_large_vit_huge_14.pth | models/clip/ | 4.5GB (for I2V) |

## Workflow

1. Check ComfyUI status (`curl http://127.0.0.1:8188/system_stats`).
2. Start if needed (`systemctl --user start comfyui.service`).
3. Call `generate.py` with appropriate mode and options.
4. Return output image/frames to user; offer `xdg-open` to view.
5. For video: frames are individual PNGs; optionally combine into MP4 with `imageio`.

## Troubleshooting

- `libcudart.so` not found: set `LD_LIBRARY_PATH` with nvidia/cuda_runtime/lib.
- OOM on 16GB VRAM: reduce resolution or use lower `--length` for video.
- Video generation slow: T2V-1.3B 49 frames ≈ 2-3 minutes on RTX 5080.
- Server won't start: `pkill -f "main.py"` for stale processes.
- All models downloaded from ModelScope (domestic) — HuggingFace inaccessible.
