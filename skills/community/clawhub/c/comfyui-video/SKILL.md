---
name: comfyui-video
description: Automate AI video generation with ComfyUI and LTX-2.3. Supports text-to-video (T2V), image-to-video (I2V), batch scene rendering for music videos, and multi-scene workflows. Includes progress monitoring, fault recovery, and performance tuning. Use when generating AI videos with ComfyUI, creating MV scenes in batch, troubleshooting video rendering, or optimizing generation speed.
---

# ComfyUI Video Generation

Automate AI video generation using ComfyUI + LTX-2.3 model. Ideal for music video (MV) production, multi-scene batch rendering, and AI video content creation.

## Requirements

| Item | Spec |
|------|------|
| GPU | ≥24GB VRAM (Turing/Ampere/Ada) |
| ComfyUI | 0.17+ |
| PyTorch | 2.6+cu124 |
| Access | SSH tunnel forwarding port 18188 |

## Model Setup

| Model | Size | Path |
|-------|------|------|
| LTX-2.3 dev (bf16) | 43GB | `models/checkpoints/ltx-2.3-22b-dev.safetensors` |
| Gemma 3 12B | 23GB | `models/text_encoders/comfy_gemma_3_12B_it.safetensors` |
| Distilled LoRA | 7.1GB | `models/loras/ltxv/ltx2/ltx-2.3-22b-distilled-lora-384.safetensors` |
| Video VAE (bf16) | - | `models/vae/LTX23_video_vae_bf16.safetensors` |

**Turing GPUs** (e.g., Quadro RTX 8000) do NOT support `fp8_e4m3fn`. Use bf16/fp16 models only.

## Performance Baseline

```
Per-step time: ~221s (constant, regardless of frame count!)
15 steps: ~57 min
25 steps: ~1h45m
Frames: 72=3s, 121=5s, 480=20s (24fps)
```

**Key insight**: Frame count does NOT affect total time. Bottleneck is model forward pass.

## Workflow Node Reference

| Node | ID | Purpose |
|------|-----|---------|
| LoadImage | 2004 | I2V reference input |
| CLIPTextEncode (positive) | 2483 | Positive prompt |
| CLIPTextEncode (negative) | 2612 | Negative prompt |
| EmptyLTXVLatentVideo | 3059 | Empty latent |
| LTXVScheduler | 4966 | Steps/length params |
| LoraLoaderModelOnly | 4922+ | LoRA loader |
| SaveVideo | 4823/4852 | Output mp4 |

## Quick Start

### Generate a Single Video (I2V)

1. Load workflow: `/workspace/ComfyUI/custom_nodes/ComfyUI-LTXVideo/example_workflows/2.3/LTX-2.3_T2V_I2V_Single_Stage_Distilled_Full.json`
2. Set params using `scripts/batch_scenes.js`
3. Click Run
4. Wait ~1 hour
5. Download from `/workspace/ComfyUI/output/`

### Batch Scene Generation

Use `scripts/batch_scenes.js` for automation:

```javascript
// Load script first, then configure each scene:
await comfyui_batch.configureScene({
  name: "scene_01",
  prompt: "A lonely girl running through rain at night, neon reflections",
  image: "unified_ref.png",
  steps: 15,
  frames: 72
});
// Click Run, repeat for next scene
```

## Step Count Guide

| Steps | Quality | Time/Scene | Use Case |
|-------|---------|------------|----------|
| 8 | Rough | ~30min | Quick preview |
| 15 | Good | ~57min | **Recommended sweet spot** |
| 25 | Best | ~1h45m | Final quality output |

I2V + LoRA at 15 steps achieves ~90% of 25-step quality with 40% less time.

## Troubleshooting

### VAEDecode Validation Failed

**Error**: `Exception when validating node: 'VAEDecode'`
**Cause**: VAE load timing or insufficient VRAM
**Fix**: Reload the entire workflow (fetch + loadGraphData), wait for models to fully load, then run. Never reload during execution.

### Browser Tab Lost

**Cause**: SSH tunnel disconnected
**Fix**:
1. Rebuild tunnel: `ssh -f -N -L 18188:localhost:18188 user@host -p port`
2. Navigate to ComfyUI
3. Reload workflow

### Inconsistent Characters Across Scenes

**Cause**: Different reference images per scene
**Fix**: Use the SAME reference image for all scenes. Extract a clear frame from an existing video if needed. The I2V input image dictates the visual baseline.

### Output Video Not Saved

**Check**: `ssh -p PORT root@HOST "ls -lht /workspace/ComfyUI/output/*.mp4"`
**Fix**: Check for VAEDecode errors in log, then re-run.

## Monitoring Progress

```bash
# Current sampling progress
ssh -p PORT root@HOST "grep 'it/s' /tmp/comfy.log | tail -1"

# Completion check
ssh -p PORT root@HOST "grep 'Prompt executed' /tmp/comfy.log | tail -1"

# Output files
ssh -p PORT root@HOST "ls -lht /workspace/ComfyUI/output/*.mp4"
```

## Best Practices

1. **15 steps is the sweet spot** — I2V converges at 15-20 steps, 25 has diminishing returns
2. **Unified reference image** — Same input image for all scenes ensures character consistency
3. **Reload workflow every time** — Avoids VAEDecode validation failures
4. **Never reload during execution** — Current run will fail
5. **Frame selection** — 72 frames (3s) for testing, 480 frames (20s) for final output
6. **VRAM management** — Wait for each generation to complete before starting next

## T2V vs I2V Comparison

| Mode | Steps | Quality | Notes |
|------|-------|---------|-------|
| T2V (no LoRA) | 15 | ❌ Very blurry | Not recommended |
| I2V + LoRA | 25 | ✅ Excellent | Major quality improvement |
| I2V + LoRA | 15 | ✅ Very good | Best time/quality ratio |

**Conclusion**: I2V + LoRA is the recommended combination.

## Resources

- `scripts/batch_scenes.js` — Batch scene automation
- `references/workflow_nodes.md` — Full node ID mapping
- `references/tips.md` — Prompt tips, VRAM management, optimization
