---
name: "dezgo-img-gen"
description: "Generate and edit images via freegen container: TXT2IMG, IMG2IMG, Inpainting, RemoveBG, Upscale. Flux, SDXL, SD1.5 models."
---

# Dezgo Image Generation

Generate images via the local freegen container at `http://freegen:3000`.

## POST /generate

Required fields: `prompt`, `category` (or `model` for flux/backwards compat)

| category | Description | Model param |
|---|---|---|
| `flux` | Fast everyone-model | none needed |
| `sdxl` | High-res SDXL | dreamshaperxl_1024px, juggernautxl_1024px, ponyxl_6 |
| `sd1` | SD 1.5 many models | realistic_vision_5_1, deliberate_2, juggernaut_reborn |
| `sdxl2` | Lightning fast | juggernautxl_10_hyper, dreamshaperxl_lightning |
| `i2i` | Image-to-image | realistic_vision_5_1, dreamshaper_8 |
| `inpaint` | Fill area (mask) | SD 1.5 inpainting |
| `inpaint_sdxl` | Fill area (SDXL) | SDXL inpainting |
| `textinpaint` | Fill by description | dreamshaper_8_inpaint |
| `controlnet` | Structure-guided | canny, hed, openpose, depth |
| `edit` | Edit image | SD 1.5 |
| `removebg` | Remove background | none |
| `upscale` | Upscale 2x-4x | none |

## Examples

**Flux** (fast, no model selection needed):
```json
{"prompt": "a cute cat", "model": "flux", "width": 1024, "height": 1024}
```

**SDXL** (with model selection):
```json
{"prompt": "portrait of a woman", "category": "sdxl", "model": "juggernautxl_1024px", "width": 1024, "height": 1024}
```

**IMG2IMG**:
```json
{"prompt": "red dress", "category": "i2i", "model": "realistic_vision_5_1", "init_image": "data:image/png;base64,..."}
```

## Image tools

- RemoveBG: `{"category": "removebg", "init_image": "data:image/png;base64,..."}`
- Upscale: `{"category": "upscale", "init_image": "data:image/png;base64,...", "scale": 2}`
- Inpainting: `{"category": "inpaint_sdxl", "prompt": "filling item", "init_image": "data:image/png;base64,...", "mask_image": "data:image/png;base64,..."}`
- Text Inpainting: `{"category": "textinpaint", "mask_prompt": "shirt", "prompt": "blue shirt", "init_image": "data:image/png;base64,..."}`

## General options

- `width`, `height` – image dimensions
- `steps` – quality vs speed (flux: 4, sdxl: 20-30, sd1: 20-30)
- `guidance` – prompt adherence (default 7, sdxl2 lightning: 2)
- `seed` – reproducible results
- `sampler` – auto, dpmpp_2m_karras, euler, etc.

## Response

Returns JSON: `{success, file, url, size, elapsed, cost, balance, model, sub_model}`

## GET /info

Lists available models for each category.

## GET /health

Container health check.
