# FLUX (fal.ai)

## Models

| Model | Endpoint | Speed | Description |
|-------|----------|-------|-------------|
| FLUX.2 Pro | `fal-ai/flux-2-pro` | Medium | Latest, zero-config, best quality |
| FLUX Pro v1.1 | `fal-ai/flux-pro/v1.1` | Medium | 10x accelerated, commercial use |
| FLUX.1 Dev | `fal-ai/flux/dev` | Medium | 12B params, fine-tuning friendly |
| FLUX.1 Schnell | `fal-ai/flux/schnell` | ⚡ Fast | 1–4 steps, personal+commercial |

## FLUX.2 Pro — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Text prompt |
| `image_size` | ImageSize/enum | | `"landscape_4_3"` | `square_hd`, `square`, `portrait_4_3`, `portrait_16_9`, `landscape_4_3`, `landscape_16_9` or `{"width": W, "height": H}` |
| `seed` | integer | | random | |
| `safety_tolerance` | enum | | `"2"` | `1`–`5`. API only |
| `enable_safety_checker` | boolean | | `true` | |
| `output_format` | enum | | `"jpeg"` | `jpeg`, `png` |

## FLUX Pro v1.1 — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Text prompt |
| `image_size` | ImageSize/enum | | `"landscape_4_3"` | Same options as FLUX.2 |
| `seed` | integer | | random | |
| `num_images` | integer | | `1` | |
| `output_format` | enum | | `"jpeg"` | `jpeg`, `png` |
| `safety_tolerance` | enum | | `"2"` | `1`–`6`. API only |
| `enhance_prompt` | boolean | | `false` | Auto-enhance prompt |

## FLUX.1 Dev — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Text prompt |
| `image_size` | ImageSize/enum | | `"landscape_4_3"` | Same options |
| `num_inference_steps` | integer | | `28` | More steps = better quality |
| `seed` | integer | | random | |
| `guidance_scale` | float | | `3.5` | CFG scale |
| `num_images` | integer | | `1` | |
| `enable_safety_checker` | boolean | | `true` | |
| `output_format` | enum | | `"jpeg"` | `jpeg`, `png` |
| `acceleration` | enum | | `"none"` | `none`, `regular`, `high` |

## FLUX.1 Schnell — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Text prompt |
| `image_size` | ImageSize/enum | | `"landscape_4_3"` | Same options |
| `num_inference_steps` | integer | | `4` | 1–4 steps typical |
| `seed` | integer | | random | |
| `guidance_scale` | float | | `3.5` | CFG scale |
| `num_images` | integer | | `1` | |
| `enable_safety_checker` | boolean | | `true` | |
| `output_format` | enum | | `"jpeg"` | `jpeg`, `png` |
| `acceleration` | enum | | `"none"` | `none`, `regular`, `high` |

## Output Schema (all FLUX models)

```json
{
  "images": [
    {"url": "https://...", "width": 1024, "height": 768, "content_type": "image/jpeg"}
  ],
  "seed": 12345,
  "has_nsfw_concepts": [false],
  "prompt": "..."
}
```

## Python Example

```python
import fal_client
# Fast preview
result = fal_client.subscribe("fal-ai/flux/schnell", arguments={
    "prompt": "a cat astronaut, studio photo",
    "image_size": "square_hd",
    "num_inference_steps": 4,
    "output_format": "png",
})
# Pro quality
result = fal_client.subscribe("fal-ai/flux-2-pro", arguments={
    "prompt": "a cat astronaut, studio photo",
    "image_size": {"width": 1920, "height": 1080},
})
```
