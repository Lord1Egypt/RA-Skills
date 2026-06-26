# Kling Video (fal.ai)

## Models

| Model | Endpoint | Mode | Description |
|-------|----------|------|-------------|
| Kling v3 Pro I2V | `fal-ai/kling-video/v3/pro/image-to-video` | Image→Video | Latest, multi-shot, audio gen, up to 15s |
| Kling v2.6 Pro I2V | `fal-ai/kling-video/v2.6/pro/image-to-video` | Image→Video | |
| Kling v2.5 Turbo T2V | `fal-ai/kling-video/v2.5-turbo/pro/text-to-video` | Text→Video | Fast, 5-10s |
| Kling v2.5 Turbo I2V | `fal-ai/kling-video/v2.5-turbo/pro/image-to-video` | Image→Video | Fast |
| Kling v2.1 Pro I2V | `fal-ai/kling-video/v2.1/pro/image-to-video` | Image→Video | |

## Kling v3 Pro (Image-to-Video) — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | | — | Text prompt (either `prompt` or `multi_prompt`, not both) |
| `multi_prompt` | list | | — | Multi-shot prompts for multi-shot video |
| `start_image_url` | string | ✅ | — | First frame image URL |
| `duration` | enum | | `"5"` | `3`–`15` seconds |
| `generate_audio` | boolean | | `true` | Generate native audio (Chinese/English) |
| `end_image_url` | string | | — | Last frame image URL |
| `voice_ids` | list[string] | | — | Voice IDs (max 2). Ref in prompt: `<<<voice_1>>>`, `<<<voice_2>>>` |
| `elements` | list | | — | Characters/objects. Ref in prompt: `@Element1`, `@Element2` |
| `shot_type` | string | | `"customize"` | Multi-shot type |
| `negative_prompt` | string | | `"blur, distort, and low quality"` | |
| `cfg_scale` | float | | `0.5` | Guidance scale |

## Kling v2.5 Turbo (Text-to-Video) — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | |
| `duration` | enum | | `"5"` | `5` or `10` seconds |
| `aspect_ratio` | enum | | `"16:9"` | `16:9`, `9:16`, `1:1` |
| `negative_prompt` | string | | `"blur, distort, and low quality"` | |
| `cfg_scale` | float | | `0.5` | |

## Output Schema

```json
{
  "video": {
    "url": "https://...",
    "content_type": "video/mp4",
    "file_size": 8431922
  }
}
```

## Python Example

```python
import fal_client

# Text-to-video
result = fal_client.subscribe("fal-ai/kling-video/v2.5-turbo/pro/text-to-video", arguments={
    "prompt": "A cat walking on the moon, cinematic lighting",
    "duration": "5",
    "aspect_ratio": "16:9",
})

# Image-to-video (v3)
result = fal_client.subscribe("fal-ai/kling-video/v3/pro/image-to-video", arguments={
    "prompt": "The character starts dancing gracefully",
    "start_image_url": "https://example.com/photo.jpg",
    "duration": "10",
    "generate_audio": True,
})

video_url = result["video"]["url"]
```
