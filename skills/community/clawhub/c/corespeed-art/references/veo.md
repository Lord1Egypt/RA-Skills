# Veo 3.1 (fal.ai)

## Models

| Model | Endpoint | Mode |
|-------|----------|------|
| Veo 3.1 T2V | `fal-ai/veo3.1` | Text→Video, with audio |
| Veo 3.1 Fast T2V | `fal-ai/veo3.1/fast` | Faster variant |
| Veo 3.1 I2V | `fal-ai/veo3.1/image-to-video` | Image→Video |
| Veo 3.1 Fast I2V | `fal-ai/veo3.1/fast/image-to-video` | Fast Image→Video |
| Veo 3.1 Ref-to-Video | `fal-ai/veo3.1/reference-to-video` | Reference-based |

## Text-to-Video — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Video description. Include: subject, context, action, style, camera motion, composition, ambiance |
| `aspect_ratio` | enum | | `"16:9"` | `16:9`, `9:16` |
| `duration` | enum | | `"8s"` | `4s`, `6s`, `8s` |
| `negative_prompt` | string | | — | What to avoid |
| `resolution` | enum | | `"720p"` | `720p`, `1080p`, `4k` |
| `generate_audio` | boolean | | `true` | Generate native audio |
| `seed` | integer | | random | |
| `auto_fix` | boolean | | `true` | Auto-fix prompts that fail policy |
| `safety_tolerance` | enum | | `"4"` | `1`–`6`. API only |

## Image-to-Video — Input Schema

Same as T2V plus:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image_url` | string | ✅ | — | Input image URL (720p+, 16:9 or 9:16) |
| `aspect_ratio` | enum | | `"auto"` | `auto`, `16:9`, `9:16` |

## Prompting Guide

Best results when prompt includes:
- **Subject**: What you want (object, person, animal, scenery)
- **Context**: Background/setting
- **Action**: What the subject is doing
- **Style**: Film style keywords (horror, noir, cartoon, etc.)
- **Camera motion** (optional): aerial view, tracking shot, etc.
- **Composition** (optional): wide shot, close-up, etc.
- **Ambiance** (optional): color and lighting details

For dialogue, use format:
```
Sample Dialogue:
Host: "Did you hear the news?"
Person: "Yes! This is amazing."
```

## Output Schema

```json
{
  "video": {
    "url": "https://...",
    "content_type": "video/mp4",
    "file_size": 12345678
  }
}
```

## Key Features

- **Native audio generation** — voice, music, sound effects generated with video
- **720p–4K resolution**
- **5–8 second clips at 24 FPS**
- **Safety filters** on both input and output

## Python Example

```python
import fal_client

# Text-to-video with audio
result = fal_client.subscribe("fal-ai/veo3.1", arguments={
    "prompt": "Two friends chatting at a café. One says: 'Have you tried the new menu?' The other replies: 'Yes, it's amazing!' Warm lighting, close-up shots.",
    "aspect_ratio": "16:9",
    "duration": "8s",
    "resolution": "1080p",
    "generate_audio": True,
})

# Image-to-video
result = fal_client.subscribe("fal-ai/veo3.1/image-to-video", arguments={
    "prompt": "The flowers gently sway in the breeze, petals falling slowly",
    "image_url": "https://example.com/garden.jpg",
    "duration": "6s",
    "generate_audio": True,
})

video_url = result["video"]["url"]
```
