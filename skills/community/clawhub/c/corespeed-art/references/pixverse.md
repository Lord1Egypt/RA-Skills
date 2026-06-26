# Pixverse v5 (fal.ai)

## Model

| Model | Endpoint | Description |
|-------|----------|-------------|
| Pixverse v5 I2V | `fal-ai/pixverse/v5/image-to-video` | Stylized video (anime, 3D, cyberpunk, etc.) |

## Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Video description |
| `image_url` | string | ✅ | — | First frame image URL |
| `resolution` | enum | | `"720p"` | `360p`, `540p`, `720p`, `1080p` |
| `duration` | enum | | `"5"` | `5` or `8` seconds. 8s costs double. 1080p limited to 5s |
| `negative_prompt` | string | | `""` | |
| `style` | enum | | — | `anime`, `3d_animation`, `clay`, `comic`, `cyberpunk` |
| `seed` | integer | | random | |

## Output Schema

```json
{
  "video": {"url": "https://..."}
}
```

## Python Example

```python
import fal_client
result = fal_client.subscribe("fal-ai/pixverse/v5/image-to-video", arguments={
    "prompt": "A warrior walks through a futuristic city",
    "image_url": "https://example.com/warrior.png",
    "resolution": "720p",
    "duration": "5",
    "style": "cyberpunk",
})
```
