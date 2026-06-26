# Image Models

| Model | model_id | T2I | I2I / Multi-Ref | Resolution | Max Refs |
|-------|----------|-----|-----------------|------------|----------|
| Flux.1 Kontext Pro | `flux-1-kontext-pro` | Y | Y | 1K, 2K | 4 |
| Flux 2 Pro | `flux-2-pro` | Y | Y | 1K, 2K | 4 |
| Kontextdev | `kontextdev` | Y | Y | 1K, 2K | 4 |
| Nano Banana (Gemini 2.5 Flash) | `gemini-2.5-flash-image` | Y | Y | 1K, 2K | 4 |
| Nano Banana Pro (Gemini 3 Pro) | `gemini-3-pro-image-preview` | Y | Y | 1K, 2K, 4K | 4 |
| Nano Banana 2 (Gemini 3.1 Flash) | `gemini-3.1-flash-image-preview` | Y | Y | 1K, 2K, 4K | 4 |
| GPT Image 1 Low | `gpt-image-1-low` | Y | Y | 1K, 2K | 4 |
| GPT Image 1 Medium | `gpt-image-1-medium` | Y | Y | 1K, 2K | 4 |
| GPT Image 1 Mini | `gpt-image-1-mini` | Y | - | 1K, 2K | - |
| GPT Image 2 | `gpt-image-2` | Y | Y | 1K, 2K | 4 |
| Kling O1 | `kling-image-o1` | Y | Y | 1K, 2K | 4 |
| Midjourney v7 | `midjourney-v7` | Y | Y | 1K, 2K | 5 |
| Seedream 4.0 | `seedream-4-0-250828` | Y | Y | 1K, 2K, 4K | 4 |
| Seedream 4.5 | `seedream-4-5-251128` | Y | Y | 2K, 4K | 4 |
| Seedream 5.0 Lite | `seedream-5-0-260128` | Y | Y | 2K, 3K | 4 |
| Wan 2.5 | T2I: `wan2.5-t2i-preview` / I2I: `wan2.5-i2i-preview` | Y | Y | 1K, 2K | - |

---

## Per-Model Parameter Specs

### `flux-1-kontext-pro`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 64px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 3:7 ~ 7:3 |
| Max Multi-Image Inputs | 4 |
| Output Formats | JPG, PNG |
| Supported Resolution | 1K, 2K |
| Frames per Request | 1 |
| Supported Output Ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9, 9:21 |

---

### `flux-2-pro`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 64px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:3 ~ 3:1 |
| Max Multi-Image Inputs | 4 |
| Output Formats | JPG, PNG |
| Supported Resolution | 1K, 2K |
| Frames per Request | 1 |
| Supported Output Ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9, 9:21 |

---

### `kontextdev`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 3:7 ~ 7:3 |
| Max Multi-Image Inputs | 4 |
| Output Formats | JPG, PNG |
| Supported Resolution | 1K, 2K |
| Frames per Request | 1 |
| Supported Output Ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9, 9:21 |

---

### `gemini-2.5-flash-image`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 64px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 9:16 ~ 16:9 |
| Max Multi-Image Inputs | 4 |
| Output Formats | PNG, JPG |
| Supported Resolution | 1K, 2K |
| Frames per Request | 4 |
| Supported Output Ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |

---

### `gemini-3-pro-image-preview`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 64px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 9:16 ~ 16:9 |
| Max Multi-Image Inputs | 4 |
| Output Formats | PNG, JPG |
| Supported Resolution | 1K, 2K, 4K |
| Frames per Request | 4 |
| Supported Output Ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |

---

### `gemini-3.1-flash-image-preview`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 64px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 9:16 ~ 16:9 |
| Max Multi-Image Inputs | 4 |
| Output Formats | PNG, JPG |
| Supported Resolution | 1K, 2K, 4K |
| Frames per Request | 4 |
| Supported Output Ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |

---

### `gpt-image-1-low`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 64px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 9:16 ~ 16:9 |
| Max Multi-Image Inputs | 4 |
| Output Formats | PNG, JPG, WEBP |
| Supported Resolution | 1K, 2K |
| Frames per Request | 1 |
| Supported Output Ratios | 1:1, 2:3, 3:2 |

---

### `gpt-image-1-medium`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 64px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 9:16 ~ 16:9 |
| Max Multi-Image Inputs | 4 |
| Output Formats | PNG, JPG, WEBP |
| Supported Resolution | 1K, 2K |
| Frames per Request | 1 |
| Supported Output Ratios | 1:1, 2:3, 3:2 |

---

### `gpt-image-1-mini`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 64px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 9:16 ~ 16:9 |
| Output Formats | PNG, JPG, WEBP |
| Supported Resolution | 1K, 2K |
| Frames per Request | 1 |
| Supported Output Ratios | 1:1, 2:3, 3:2 |

---

### `gpt-image-2`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 64px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 9:16 ~ 16:9 |
| Max Multi-Image Inputs | 4 |
| Output Formats | PNG, JPG, WEBP |
| Supported Resolution | 1K, 2K |
| Frames per Request | 1 |
| Supported Output Ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9, 9:21 |

---

### `kling-image-o1`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 300px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2 ~ 2:1 |
| Max Multi-Image Inputs | 4 |
| Output Formats | PNG, JPG |
| Supported Resolution | 1K, 2K |
| Frames per Request | 4 |
| Supported Output Ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |

---

### `midjourney-v7`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 4096px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:3 ~ 3:1 |
| Max Multi-Image Inputs | 5 |
| Output Formats | PNG, WEBP |
| Supported Resolution | 1K, 2K |
| Frames per Request | 4 |
| Supported Output Ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 5:6, 6:5, 9:16, 16:9 |

---

### `seedream-4-0-250828`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 2048px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2 ~ 2:1 |
| Max Multi-Image Inputs | 4 |
| Output Formats | PNG, JPG |
| Supported Resolution | 1K, 2K, 4K |
| Frames per Request | 4 |
| Supported Output Ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |

---

### `seedream-4-5-251128`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 2048px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2 ~ 2:1 |
| Max Multi-Image Inputs | 4 |
| Output Formats | PNG, JPG |
| Supported Resolution | 2K, 4K |
| Frames per Request | 4 |
| Supported Output Ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |

---

### `seedream-5-0-260128`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 2048px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2 ~ 2:1 |
| Max Multi-Image Inputs | 4 |
| Output Formats | PNG, JPG |
| Supported Resolution | 2K, 3K |
| Frames per Request | 4 |
| Supported Output Ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 |

---

### Wan 2.5

**model_id by task**: T2I → `wan2.5-t2i-preview`, I2I → `wan2.5-i2i-preview`

| Constraint | Value |
|-----------|-------|
| Image Size Range | 512px - 2048px |
| Max Image File Size | 10 MB |
| Input Aspect Ratio Limit | 1:2 ~ 2:1 |
| Max Multi-Image Inputs | - |
| Output Formats | PNG, JPG |
| Supported Resolution | 1K, 2K |
| Frames per Request | 1 |
| Supported Output Ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9, 21:9 |
