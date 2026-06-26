# Qwen Image 2 Pro (fal.ai)

## Models

| Model | Endpoint | Description |
|-------|----------|-------------|
| Qwen Image 2 Pro T2I | `fal-ai/qwen-image-2/pro/text-to-image` | Native 2K, Chinese+English, typography |
| Qwen Image 2 Pro Edit | `fal-ai/qwen-image-2/pro/edit` | Style transfer, compositing |

## Text-to-Image — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Supports Chinese and English |
| `negative_prompt` | string | | `""` | Max 500 chars |
| `image_size` | ImageSize/enum | | `"square_hd"` | `square_hd`, `square`, `portrait_4_3`, `portrait_16_9`, `landscape_4_3`, `landscape_16_9` or `{"width": W, "height": H}`. Total pixels between 512×512 and 2048×2048 |
| `enable_prompt_expansion` | boolean | | `true` | LLM prompt optimization |
| `seed` | integer | | random | 0–2147483647 |
| `enable_safety_checker` | boolean | | `true` | |
| `num_images` | integer | | `1` | |
| `output_format` | enum | | — | |

## Edit — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Edit instructions |
| `image_urls` | list[string] | ✅ | — | Input images for editing |
| `image_size` | ImageSize/enum | | `"square_hd"` | Same as T2I |

## Output Schema

```json
{
  "images": [{"url": "https://...", "width": 2048, "height": 2048, "content_type": "image/png"}],
  "seed": 12345
}
```

## Python Example

```python
import fal_client
result = fal_client.subscribe("fal-ai/qwen-image-2/pro/text-to-image", arguments={
    "prompt": "A Chinese ink painting of mountains with calligraphy text '山高水长'",
    "image_size": {"width": 2048, "height": 1024},
    "enable_prompt_expansion": True,
})
```
