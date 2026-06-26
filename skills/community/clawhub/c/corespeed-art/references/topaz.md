# Topaz Upscale (fal.ai)

## Models

| Model | Endpoint | Description |
|-------|----------|-------------|
| Topaz Upscale Image | `fal-ai/topaz/upscale/image` | AI image upscaling (2x–4x) |
| Topaz Upscale Video | `fal-ai/topaz/upscale/video` | AI video upscaling |

## Image Upscale — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image_url` | string | ✅ | — | Image URL to upscale |
| `model` | enum | | `"Standard V2"` | `Low Resolution V2`, `Standard V2`, `CGI`, `High Fidelity V2`, `Text Refine`, `Recovery`, `Redefine`, `Recovery V2`, `Standard MAX`, `Wonder` |
| `upscale_factor` | float | | `2` | Scale factor (e.g., 2.0 doubles dimensions) |
| `crop_to_fill` | boolean | | — | |
| `output_format` | enum | | — | |

### Model Selection

| Model | Best For |
|-------|----------|
| Standard V2 | General purpose, balanced |
| Low Resolution V2 | Very low-res input (thumbnails, icons) |
| High Fidelity V2 | Preserve fine details |
| CGI | 3D renders, game assets |
| Text Refine | Images with text/typography |
| Recovery / Recovery V2 | Damaged, compressed, or noisy images |
| Standard MAX | Maximum quality |
| Wonder | Creative enhancement |

## Output Schema

```json
{"image": {"url": "https://..."}}
```

## Python Example

```python
import fal_client
result = fal_client.subscribe("fal-ai/topaz/upscale/image", arguments={
    "image_url": "https://example.com/low-res.jpg",
    "model": "Standard V2",
    "upscale_factor": 2,
})
image_url = result["image"]["url"]
```
