# LTX 2.3 (fal.ai)

Open-source video model by Lightricks. Supports audio generation, up to 2160p (4K), 6–20s.

## Models

| Model | Endpoint | Mode | Speed |
|-------|----------|------|-------|
| LTX 2.3 T2V | `fal-ai/ltx-2.3/text-to-video` | Text→Video | Medium |
| LTX 2.3 T2V Fast | `fal-ai/ltx-2.3/text-to-video/fast` | Text→Video | ⚡ Fast |
| LTX 2.3 I2V | `fal-ai/ltx-2.3/image-to-video` | Image→Video | Medium |
| LTX 2.3 I2V Fast | `fal-ai/ltx-2.3/image-to-video/fast` | Image→Video | ⚡ Fast |
| LTX 2.3 Extend | `fal-ai/ltx-2.3/extend-video` | Video extension | Medium |
| LTX 2.3 Retake | `fal-ai/ltx-2.3/retake-video` | Video retake | Medium |

## Text-to-Video (Fast) — Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Video description |
| `duration` | integer | | `6` | `6`, `8`, `10`, `12`, `14`, `16`, `18`, `20`. Must be integer, not string. Durations >10 require 25fps + 1080p |
| `resolution` | string | | `"1080p"` | `1080p`, `1440p`, `2160p` |
| `aspect_ratio` | string | | `"16:9"` | `16:9`, `9:16` |
| `fps` | integer | | `25` | `24`, `25`, `48`, `50`. Must be integer |
| `generate_audio` | boolean | | `true` | Generate audio |

## Image-to-Video — Input Schema

Same as T2V plus:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image_url` | string | ✅ | — | Start frame image |
| `end_image_url` | string | | — | End frame (transition between start→end) |
| `duration` | integer | | `6` | `6`, `8`, `10` (I2V has shorter max). Must be integer |

## Output Schema

```json
{
  "video": {
    "url": "https://...",
    "content_type": "video/mp4"
  }
}
```

## Key Features

- **Up to 2160p (4K)** resolution
- **Up to 20 seconds** at 25fps 1080p
- **Native audio generation**
- **Open source** (Lightricks)
- **Fast variant** available for quick iteration

## Python Example

```python
import fal_client
# Fast text-to-video
result = fal_client.subscribe("fal-ai/ltx-2.3/text-to-video/fast", arguments={
    "prompt": "A drone flies over a tropical forest at sunrise",
    "duration": 8,
    "resolution": "1080p",
    "aspect_ratio": "16:9",
    "generate_audio": True,
})
# Image-to-video
result = fal_client.subscribe("fal-ai/ltx-2.3/image-to-video", arguments={
    "prompt": "The scene comes alive, waves crashing on the shore",
    "image_url": "https://example.com/beach.jpg",
    "duration": 6,
    "resolution": "1080p",
})
video_url = result["video"]["url"]
```
