# Sora 2 (fal.ai)

## Models

| Model | Endpoint | Mode |
|-------|----------|------|
| Sora 2 T2V | `fal-ai/sora-2/text-to-video` | Text→Video |
| Sora 2 I2V | `fal-ai/sora-2/image-to-video` | Image→Video |
| Sora 2 Pro T2V | `fal-ai/sora-2/text-to-video/pro` | Text→Video (Pro) |
| Sora 2 Pro I2V | `fal-ai/sora-2/image-to-video/pro` | Image→Video (Pro) |
| Sora 2 Remix | `fal-ai/sora-2/video-to-video/remix` | Video remix |
| Sora 2 Characters | `fal-ai/sora-2/characters` | Character consistency |

## Text-to-Video — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Text describing the video |
| `resolution` | string | | `"720p"` | |
| `aspect_ratio` | enum | | `"16:9"` | `9:16`, `16:9` |
| `duration` | enum | | `"4"` | `4`, `8`, `12`, `16`, `20` seconds |
| `delete_video` | boolean | | `true` | Delete after gen for privacy (can't remix if true) |
| `model` | enum | | `"sora-2"` | `sora-2`, `sora-2-2025-12-08`, `sora-2-2025-10-06` |
| `detect_and_block_ip` | boolean | | — | Block known IP references |
| `character_ids` | list[string] | | — | Up to 2 character IDs. Refer by name in prompt |

## Image-to-Video — Input Schema

Same as T2V plus:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image_url` | string | ✅ | — | First frame image URL |
| `resolution` | enum | | `"auto"` | `auto`, `720p` |
| `aspect_ratio` | enum | | `"auto"` | `auto`, `9:16`, `16:9` |

## Output Schema

```json
{
  "video": {
    "url": "https://...",
    "content_type": "video/mp4"
  },
  "video_id": "video_123",
  "thumbnail": {"url": "https://..."},
  "spritesheet": {"url": "https://..."}
}
```

## Python Example

```python
import fal_client

# Text-to-video
result = fal_client.subscribe("fal-ai/sora-2/text-to-video", arguments={
    "prompt": "A dramatic sunset over the ocean with a sailboat, cinematic 4K",
    "duration": "8",
    "aspect_ratio": "16:9",
})

# Image-to-video
result = fal_client.subscribe("fal-ai/sora-2/image-to-video", arguments={
    "prompt": "The person starts speaking and gesturing naturally",
    "image_url": "https://example.com/person.png",
    "duration": "8",
})

video_url = result["video"]["url"]
```
