# GPT Image 1.5 (fal.ai)

## Model

| Model | Endpoint | Description |
|-------|----------|-------------|
| GPT Image 1.5 | `fal-ai/gpt-image-1.5` | OpenAI GPT Image via fal |
| GPT Image 1.5 Edit | `fal-ai/gpt-image-1.5/edit` | Edit existing images |

## Input Schema — Generate

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Prompt for image generation |
| `image_size` | enum | | `"1024x1024"` | `1024x1024`, `1536x1024`, `1024x1536` |
| `background` | enum | | `"auto"` | `auto`, `transparent`, `opaque` |
| `quality` | enum | | `"high"` | `low`, `medium`, `high` |
| `num_images` | integer | | `1` | |
| `output_format` | enum | | `"png"` | `jpeg`, `png`, `webp` |

## Input Schema — Edit

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Edit instructions |
| `image_urls` | list[string] | ✅ | — | Source image URLs |
| `image_size` | enum | | `"auto"` | `auto`, `1024x1024`, `1536x1024`, `1024x1536` |
| `background` | enum | | `"auto"` | Same |
| `quality` | enum | | `"high"` | Same |
| `output_format` | enum | | `"png"` | Same |

## Output Schema

```json
{
  "images": [
    {"url": "https://...", "width": 1024, "height": 1024, "content_type": "image/png", "file_name": "..."}
  ]
}
```

## Python Example

```python
import fal_client
result = fal_client.subscribe("fal-ai/gpt-image-1.5", arguments={
    "prompt": "A photorealistic product shot of a perfume bottle",
    "image_size": "1536x1024",
    "quality": "high",
    "background": "transparent",
    "output_format": "webp",
})
```
