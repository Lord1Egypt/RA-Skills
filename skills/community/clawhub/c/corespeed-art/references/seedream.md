# Seedream (fal.ai)

## Models

| Model | Endpoint | Description |
|-------|----------|-------------|
| Seedream 5.0 Lite Edit | `fal-ai/bytedance/seedream/v5/lite/edit` | AI image editor with reasoning & web search |
| Seedream 4.5 Edit | `fal-ai/bytedance/seedream/v4.5/edit` | Image editing |
| Seedream 4 Edit | `fal-ai/bytedance/seedream/v4/edit` | Image editing |

## Seedream 5.0 Lite — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Edit instructions |
| `image_urls` | list[string] | ✅ | — | Input image URLs for editing (up to 10) |
| `image_size` | ImageSize/enum | | `"auto_2K"` | `square_hd`, `square`, `portrait_4_3`, `portrait_16_9`, `landscape_4_3`, `landscape_16_9`, `auto_2K`, `auto_3K` or `{"width": W, "height": H}` |
| `num_images` | integer | | `1` | Number of generations to run |
| `max_images` | integer | | `1` | Max images per generation (total up to `num_images × max_images`) |
| `enable_safety_checker` | boolean | | `true` | |

Note: Total pixels must be between 2560×1440 and 3072×3072. Images outside range are auto-scaled.

## Output Schema

```json
{
  "images": [
    {"url": "https://...", "width": 2048, "height": 1152}
  ],
  "seed": 42
}
```

## Python Example

```python
import fal_client
result = fal_client.subscribe("fal-ai/bytedance/seedream/v5/lite/edit", arguments={
    "prompt": "Replace the product in Figure 1 with that in Figure 2. Add frosted glass texture.",
    "image_urls": [
        "https://example.com/product.png",
        "https://example.com/replacement.png",
    ],
    "image_size": "auto_2K",
    "num_images": 1,
})
```
