---
name: comfyui-flux
description: "Generate images locally using ComfyUI + Flux.1 Dev model. Zero API cost, strong text rendering. Use when: generating images locally, creating slides/PPT graphics, or when user says 'local image', '本地生图', 'flux', 'comfyui'. Requires ComfyUI running at localhost:8188. For face-consistent selfies, prefer wanx-image-generation skill instead."
---

# ComfyUI Flux.1 Dev — Local Image Generation

Generate images locally via ComfyUI API + Flux.1 Dev. No API cost, excellent text rendering.

## Prerequisites

ComfyUI must be running (default port 8200):
```bash
# 启动
bash /Users/chrisliu/ComfyUI/start.sh
# 关闭
bash /Users/chrisliu/ComfyUI/stop.sh
```

Override URL via env: `COMFYUI_URL=http://127.0.0.1:8200`

Models (already installed):
- `flux1-dev.safetensors` (diffusion model)
- `t5xxl_fp8_e4m3fn.safetensors` + `clip_l.safetensors` (text encoders)
- `ae.safetensors` (VAE)

## Usage

```bash
python3 {baseDir}/scripts/flux_generate.py --prompt "PROMPT" [OPTIONS]
```

### Basic

```bash
python3 {baseDir}/scripts/flux_generate.py \
  --prompt "A professional presentation slide with title 'AI Revolution' in bold white text on dark gradient background"
```

### Custom Size (e.g. 16:9 for PPT slides)

```bash
python3 {baseDir}/scripts/flux_generate.py \
  --prompt "..." \
  --width 1344 --height 768
```

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `--prompt` | (required) | Image description |
| `--negative` | "" | Negative prompt |
| `--width` | 1024 | Image width |
| `--height` | 1024 | Image height |
| `--steps` | 20 | Sampling steps (more = better but slower) |
| `--cfg` | 1.0 | CFG scale (Flux works best at 1.0) |
| `--seed` | random | Reproducibility seed |
| `--output` | auto | Output path (default: generated-images/flux-{ts}.png) |
| `--timeout` | 600 | Max wait seconds |

## Common Sizes

| Use Case | Size | Flag |
|---|---|---|
| Square | 1024×1024 | (default) |
| PPT 16:9 | 1344×768 | `--width 1344 --height 768` |
| Portrait | 768×1344 | `--width 768 --height 1344` |
| Landscape | 1344×768 | `--width 1344 --height 768` |

## PuLID Face-Consistent Generation

Generate images with a reference face using PuLID-Flux (zero API cost, zero censorship):

```bash
python3 {baseDir}/scripts/pulid_generate.py \
  --prompt "PROMPT" \
  --ref-image path/to/face.jpg [OPTIONS]
```

### Basic (face-consistent portrait)

```bash
python3 {baseDir}/scripts/pulid_generate.py \
  --prompt "a girl sitting in a cafe, warm afternoon light, casual outfit" \
  --ref-image avatars/kimi.jpg
```

### Custom size + weight

```bash
python3 {baseDir}/scripts/pulid_generate.py \
  --prompt "a girl on the beach at sunset, wearing a sundress" \
  --ref-image avatars/kimi.jpg \
  --width 1024 --height 1024 \
  --weight 1.2
```

### PuLID Parameters

| Parameter | Default | Description |
|---|---|---|
| `--prompt` | (required) | Image description |
| `--ref-image` | (required) | Reference face image path |
| `--negative` | "" | Negative prompt |
| `--width` | 768 | Image width |
| `--height` | 1024 | Image height (portrait default) |
| `--steps` | 10 | Sampling steps (PuLID works well with fewer) |
| `--cfg` | 3.5 | Guidance scale |
| `--seed` | random | Reproducibility seed |
| `--weight` | 1.0 | Face similarity weight (0.0-5.0, higher = more similar) |
| `--start-at` | 0.0 | PuLID start timestep |
| `--end-at` | 1.0 | PuLID end timestep |
| `--output` | auto | Output path (default: generated-images/pulid-{ts}.png) |
| `--timeout` | 600 | Max wait seconds |

### PuLID Notes

- Default portrait orientation (768×1024) — good for face shots
- `--weight 1.0` is balanced; increase to 1.2-1.5 for stronger likeness
- `--steps 10` is enough for PuLID; increase to 20 for more detail
- First run is slower (loads PuLID + InsightFace + EVA-CLIP models)
- No content censorship — can generate anything locally

## Strengths vs API (qwen-image)

- ✅ Free — no API cost
- ✅ Excellent text/typography rendering (great for slides!)
- ✅ High detail and consistency
- ⚠️ Slower on Mac (~1-3 min per image)
- ❌ No native face-consistency (use PuLID/IPAdapter for that)

## Output

Prints `MEDIA:<path>` — auto-attached to chat reply. Default saves to `generated-images/`.

## Troubleshooting

If ComfyUI is not running, the script exits with an error and prints startup instructions.
