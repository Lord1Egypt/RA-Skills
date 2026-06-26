# Nano Banana (fal.ai)

## Models

| Model | Endpoint | Description |
|-------|----------|-------------|
| Nano Banana Pro | `fal-ai/nano-banana-pro` | Gemini-based image generation (generate) |
| Nano Banana Pro Edit | `fal-ai/nano-banana-pro/edit` | Gemini-based image editing |
| Nano Banana 2 | `fal-ai/nano-banana-2` | Latest Nano Banana with web search + thinking |

## Nano Banana 2 — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Text prompt to generate image from |
| `num_images` | integer | | `1` | Number of images to generate |
| `seed` | integer | | random | Seed for reproducibility |
| `aspect_ratio` | enum | | `"auto"` | `auto`, `21:9`, `16:9`, `3:2`, `4:3`, `5:4`, `1:1`, `4:5`, `3:4`, `2:3`, `9:16`, `4:1`, `1:4`, `8:1`, `1:8` |
| `output_format` | enum | | `"png"` | `jpeg`, `png`, `webp` |
| `safety_tolerance` | enum | | `"4"` | `1` (strictest) to `6` (most permissive). API only |
| `resolution` | enum | | `"1K"` | `0.5K`, `1K`, `2K`, `4K` |
| `limit_generations` | boolean | | `true` | Limit to 1 image per round; ignore prompt instructions about count |
| `enable_web_search` | boolean | | `false` | Let model use latest web info |
| `thinking_level` | enum | | — | `minimal` or `high` — enables model reasoning |

## Nano Banana Pro — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Text prompt |
| `image_size` | ImageSize/enum | | `"landscape_4_3"` | `square_hd`, `square`, `portrait_4_3`, `portrait_16_9`, `landscape_4_3`, `landscape_16_9` or `{"width": W, "height": H}` |
| `num_images` | integer | | `1` | |
| `seed` | integer | | random | |
| `output_format` | enum | | `"png"` | `jpeg`, `png` |
| `safety_tolerance` | enum | | `"4"` | `1`–`6` |

## Nano Banana Pro Edit — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Edit instructions |
| `image_url` | string | ✅ | — | Source image URL |
| `image_size` | ImageSize/enum | | `"landscape_4_3"` | Same as generate |
| `num_images` | integer | | `1` | |
| `output_format` | enum | | `"png"` | `jpeg`, `png` |
| `safety_tolerance` | enum | | `"4"` | `1`–`6` |

## Output Schema (all variants)

```json
{
  "images": [
    {
      "url": "https://...",
      "content_type": "image/png",
      "file_name": "...",
      "width": 1024,
      "height": 1024
    }
  ],
  "description": "..." // Nano Banana 2 only
}
```

## Python Example

```python
import fal_client
result = fal_client.subscribe("fal-ai/nano-banana-2", arguments={
    "prompt": "A futuristic city at sunset",
    "resolution": "2K",
    "aspect_ratio": "16:9",
    "output_format": "png",
})
image_url = result["images"][0]["url"]
```
