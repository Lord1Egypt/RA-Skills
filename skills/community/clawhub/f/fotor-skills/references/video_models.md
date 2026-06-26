# Video Models

Capability columns: **T2V** = Text-to-Video, **I2V** = Single-Image-to-Video,
**SE** = Start/End Frame Interpolation, **MI** = Multi-Image Reference Video.

| Model | model_id | T2V | I2V | SE | MI | Duration | Resolution |
|-------|----------|-----|-----|----|----|----------|------------|
| Seedance 1.0 Lite | T2V: `doubao-seedance-1-0-lite-t2v-250428` / I2V,SE,MI: `doubao-seedance-1-0-lite-i2v-250428` | Y | Y | Y | Y | 5s, 10s, 12s | 480p, 720p, 1080p |
| Seedance 1.0 Pro Fast | `doubao-seedance-1-0-pro-fast-251015` | Y | Y | - | - | 5s, 10s, 12s | 480p, 720p, 1080p |
| Seedance 1.0 Pro | `doubao-seedance-1-0-pro-250528` | Y | Y | - | - | 5s, 10s, 12s | 480p, 720p, 1080p |
| Seedance 1.5 Pro | `seedance-1-5-pro-251215` | Y | Y | Y | - | 4-12s | 480p, 720p |
| Seedance 2.0 | `doubao-seedance-2-0-260128` | Y | Y | Y | Y | 4-15s | 480p, 720p, 1080p |
| Kling 2.1 Master | `kling-v2-1-master` | Y | Y | Y | - | 5s, 10s | 1080p |
| Kling 2.1 | `kling-v2-1` | - | Y | Y | - | 5s, 10s | 720p, 1080p |
| Kling 2.5 Turbo | `kling-v2-5-turbo` | Y | Y | Y | - | 5s, 10s | 1080p |
| Kling 3.0 Omni | `kling-v3-omni` | Y | Y | Y | Y | 3-15s | 720p, 1080p |
| Kling 3.0 | `kling-v3` | Y | Y | Y | - | 3-15s | 720p, 1080p |
| Kling O1 | `kling-video-o1` | Y | Y | Y | Y | 5s, 10s | 1080p |
| Kling 2.6 | `kling-v2-6` | Y | Y | - | - | 5s, 10s | 1080p |
| Hailuo 02 | `MiniMax-Hailuo-02` | Y | Y | Y | - | 6s | 768p |
| Hailuo 2.3 Fast | `MiniMax-Hailuo-2.3-Fast` | - | Y | - | - | 6s, 10s | 768p, 1080p |
| Hailuo 2.3 | `MiniMax-Hailuo-2.3` | Y | Y | - | - | 6s, 10s | 768p, 1080p |
| Pixverse v4.5 | `pixverse-v4.5` | Y | Y | Y | - | 5s, 8s | 540p, 720p, 1080p |
| Veo 3 Fast | `veo-3.0-fast-generate-001` | Y | Y | - | - | 8s | 720p, 1080p |
| Veo 3 | `veo-3.0-generate-001` | Y | Y | - | - | 8s | 720p, 1080p |
| Veo 3.1 Fast | `veo-3.1-fast-generate-001` | Y | Y | Y | - | 4s, 6s, 8s | 720p, 1080p |
| Veo 3.1 | `veo-3.1-generate-001` | Y | Y | Y | Y | 4s, 6s, 8s | 720p, 1080p |
| Vidu 2.0 | `vidu-abroad-v2-m2-0` | Y | Y | Y | Y | 4s, 8s | 360p, 720p, 1080p |
| Vidu 1.5 | `vidu-abroad-v2-m1-5` | Y | Y | Y | Y | 4s, 8s | 360p, 720p, 1080p |
| Vidu Q2 Turbo | `viduq2-turbo` | - | Y | Y | - | 2-8s | 720p, 1080p |
| Vidu Q2 | `viduq2` | Y | - | - | Y | 2-8s | 540p, 720p, 1080p |
| Wan 2.5 | T2V: `wan2.5-t2v-preview` / I2V: `wan2.5-i2v-preview` | Y | Y | - | - | 5s, 10s | 480p, 720p, 1080p |
| Wan 2.6 | T2V: `wan2.6-t2v` / I2V: `wan2.6-i2v` | Y | Y | - | - | 5s, 10s, 15s | 720p, 1080p |

---

## Per-Model Parameter Specs

### Seedance 1.0 Lite

**model_id by task**: T2V → `doubao-seedance-1-0-lite-t2v-250428`, I2V/SE/MI → `doubao-seedance-1-0-lite-i2v-250428`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2.5 ~ 2.5:1 |
| Max Multi-Image Inputs | 4 |
| Duration | 5s, 10s, 12s |
| Resolution | 480p, 720p, 1080p |
| T2V Ratios | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 |
| I2V Ratios | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 |
| MI Ratios | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `doubao-seedance-1-0-pro-fast-251015`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2.5 ~ 2.5:1 |
| Duration | 5s, 10s, 12s |
| Resolution | 480p, 720p, 1080p |
| T2V Ratios | 16:9, 1:1, 9:16, 3:4, 4:3, 21:9 |
| I2V Ratios | 16:9, 1:1, 9:16, 3:4, 4:3, 21:9 |

---

### `doubao-seedance-1-0-pro-250528`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2.5 ~ 2.5:1 |
| Duration | 5s, 10s, 12s |
| Resolution | 480p, 720p, 1080p |
| T2V Ratios | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 |
| I2V Ratios | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 |

---

### `seedance-1-5-pro-251215`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 300px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2.5 ~ 2.5:1 |
| Duration | 4s, 5s, 6s, 7s, 8s, 9s, 10s, 11s, 12s |
| Resolution | 480p, 720p |
| T2V Ratios | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 |
| I2V Ratios | 16:9, 4:3, 1:1, 3:4, 9:16, 21:9 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `doubao-seedance-2-0-260128`

| Constraint | Value |
|-----------|-------|
| Max Multi-Image Inputs | 9 |
| Max Video Reference Inputs | 3 |
| Max Audio Reference Inputs | 3 |
| Duration | 4s, 5s, 6s, 7s, 8s, 9s, 10s, 11s, 12s, 13s, 14s, 15s |
| Resolution | 480p, 720p, 1080p |
| Output FPS | 24 |
| T2V Support | Text-to-video |
| I2V Support | First-frame image-to-video |
| MI Support | Multimodal reference video (image / video / audio references) |
| SE Support | First-and-last-frame image-to-video |
| Notes | Supports text/video generation, multimodal reference, and editing workflows. |

---

### `kling-v2-1-master`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 300px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2 ~ 2:1 |
| Duration | 5s, 10s |
| Resolution | 1080p |
| T2V Ratios | 16:9, 1:1, 9:16 |
| I2V Ratios | 16:9, 1:1, 9:16 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `kling-v2-1`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 300px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2 ~ 2:1 |
| Duration | 5s, 10s |
| Resolution | 720p, 1080p |
| I2V Ratios | 16:9, 1:1, 9:16 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `kling-v2-5-turbo`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 300px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2 ~ 2:1 |
| Duration | 5s, 10s |
| Resolution | 1080p |
| T2V Ratios | 16:9, 1:1, 9:16 |
| I2V Ratios | 16:9, 1:1, 9:16 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `kling-v3-omni`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 300px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 2:5 ~ 5:2 |
| Max Multi-Image Inputs | 7 |
| Duration | 3s, 4s, 5s, 6s, 7s, 8s, 9s, 10s, 11s, 12s, 13s, 14s, 15s |
| Resolution | 720p, 1080p |
| T2V Ratios | 16:9, 1:1, 9:16 |
| I2V Ratios | 16:9, 1:1, 9:16 |
| MI Ratios | 16:9, 1:1, 9:16 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `kling-v3`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 300px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 2:5 ~ 5:2 |
| Duration | 3s, 4s, 5s, 6s, 7s, 8s, 9s, 10s, 11s, 12s, 13s, 14s, 15s |
| Resolution | 720p, 1080p |
| T2V Ratios | 16:9, 1:1, 9:16 |
| I2V Ratios | 16:9, 1:1, 9:16 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `kling-video-o1`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 300px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 2:5 ~ 5:2 |
| Max Multi-Image Inputs | 10 |
| Duration | 5s, 10s |
| Resolution | 1080p |
| T2V Ratios | 16:9, 1:1, 9:16 |
| I2V Ratios | 16:9, 1:1, 9:16 |
| MI Ratios | 16:9, 1:1, 9:16 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `kling-v2-6`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 300px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 2:5 ~ 5:2 |
| Duration | 5s, 10s |
| Resolution | 1080p |
| T2V Ratios | 16:9, 1:1, 9:16 |
| I2V Ratios | 16:9, 1:1, 9:16 |

---

### `MiniMax-Hailuo-02`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 300px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 2:5 ~ 5:2 |
| Duration | 6s |
| Resolution | 768p |
| T2V Ratios | 16:9 |
| I2V Ratios | 16:9 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `MiniMax-Hailuo-2.3-Fast`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 300px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 2:5 ~ 5:2 |
| Duration | 6s, 10s |
| Resolution | 768p, 1080p |
| I2V Ratios | 16:9, 1:1, 9:16, 3:4, 4:3, 21:9 |

---

### `MiniMax-Hailuo-2.3`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 300px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 2:5 ~ 5:2 |
| Duration | 6s, 10s |
| Resolution | 768p, 1080p |
| T2V Ratios | 16:9 |
| I2V Ratios | 16:9 |

---

### `pixverse-v4.5`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 2048px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 16:9 ~ 16:9 |
| Duration | 5s, 8s |
| Resolution | 540p, 720p, 1080p |
| T2V Ratios | 16:9, 9:16, 1:1, 4:3, 3:4 |
| I2V Ratios | 16:9, 9:16, 1:1, 4:3, 3:4 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `veo-3.0-fast-generate-001`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 9:16 ~ 16:9 |
| Duration | 8s |
| Resolution | 720p, 1080p |
| T2V Ratios | 16:9, 9:16 |
| I2V Ratios | 16:9, 9:16 |

---

### `veo-3.0-generate-001`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 9:16 ~ 16:9 |
| Duration | 8s |
| Resolution | 720p, 1080p |
| T2V Ratios | 16:9, 9:16 |
| I2V Ratios | 16:9, 9:16 |

---

### `veo-3.1-fast-generate-001`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 9:16 ~ 16:9 |
| Duration | 4s, 6s, 8s |
| Resolution | 720p, 1080p |
| T2V Ratios | 16:9, 9:16 |
| I2V Ratios | 16:9, 9:16 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `veo-3.1-generate-001`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 9:16 ~ 16:9 |
| Duration | 4s, 6s, 8s |
| Resolution | 720p, 1080p |
| T2V Ratios | 16:9, 9:16 |
| I2V Ratios | 16:9, 9:16 |
| MI Ratios | 16:9, 9:16 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `vidu-abroad-v2-m2-0`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 128px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:4 ~ 4:1 |
| Max Multi-Image Inputs | 3 |
| Duration | 4s, 8s |
| Resolution | 360p, 720p, 1080p |
| T2V Ratios | 16:9, 1:1, 9:16 |
| I2V Ratios | 16:9, 1:1, 9:16 |
| MI Ratios | 16:9, 1:1, 9:16 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `vidu-abroad-v2-m1-5`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 128px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:4 ~ 4:1 |
| Max Multi-Image Inputs | 3 |
| Duration | 4s, 8s |
| Resolution | 360p, 720p, 1080p |
| T2V Ratios | 16:9, 1:1, 9:16 |
| I2V Ratios | 16:9, 1:1, 9:16 |
| MI Ratios | 16:9, 1:1, 9:16 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `viduq2-turbo`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 128px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:4 ~ 4:1 |
| Duration | 2s, 3s, 4s, 5s, 6s, 7s, 8s |
| Resolution | 720p, 1080p |
| I2V Ratios | 16:9, 1:1, 9:16, 3:4, 4:3 |
| SE Notes | Start/end frames must have identical dimensions; output ratio matches input image |

---

### `viduq2`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 128px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:4 ~ 4:1 |
| Max Multi-Image Inputs | 7 |
| Duration | 2s, 3s, 4s, 5s, 6s, 7s, 8s |
| Resolution | 540p, 720p, 1080p |
| T2V Ratios | 16:9, 1:1, 9:16, 3:4, 4:3 |
| MI Ratios | 16:9, 1:1, 9:16, 3:4, 4:3 |

---

### Wan 2.5

**model_id by task**: T2V → `wan2.5-t2v-preview`, I2V → `wan2.5-i2v-preview`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2 ~ 2:1 |
| Duration | 5s, 10s |
| Resolution | 480p, 720p, 1080p |
| T2V Ratios | 16:9, 1:1, 9:16, 3:4, 4:3 |
| I2V Ratios | 16:9, 1:1, 9:16, 3:4, 4:3 |

---

### Wan 2.6

**model_id by task**: T2V → `wan2.6-t2v`, I2V → `wan2.6-i2v`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2 ~ 2:1 |
| Duration | 5s, 10s, 15s |
| Resolution | 720p, 1080p |
| T2V Ratios | 16:9, 1:1, 9:16, 3:4, 4:3 |
| I2V Ratios | 16:9, 1:1, 9:16, 3:4, 4:3 |

---

## General Notes

### Audio

All video tasks support `audio_enable` (bool, default `False`).

When `audio_enable=True`, you can optionally provide `audio_prompt` (str) via `**extra` kwargs to describe the desired audio:

```python
result = await text2video(
    client,
    prompt="A jazz band performing",
    model_id="kling-v3",
    audio_enable=True,
    audio_prompt="Smooth jazz with saxophone",
)
```

If `audio_enable=False`, do **not** include `audio_prompt`.

### Default Aspect Ratio

- **Text-to-Video**: defaults to `16:9`
- **Image-conditioned tasks** (I2V / SE / MI): defaults to `16:9`

### Frame Interpolation (SE)

All models supporting SE require:
- Start and end frame images must have **identical dimensions**
- Output ratio is **fixed to original image aspect ratio**
