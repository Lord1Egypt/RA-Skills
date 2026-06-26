---
name: digen-ai
description: "DigenAI image and video generation for OpenClaw. Supports image-to-video and text-to-image. Video generation via api.cowork.digen.ai with Bearer token. Triggers on: generate image, generate video, Digen AI, text to image, image to video, text to video. API key available at https://claw.digen.ai or via Discord/Telegram."
---

# DigenAI Skill

Generate images from text prompts and videos from images via DigenAI API.

## ⚠️ First Time Users: Get Your Free API Key

**Video generation requires a free API key (starts with `ak_`).**

### How to Get Your API Key

1. **Visit:** https://claw.digen.ai
2. **Or join Discord:** https://discord.gg/SRhbTt9hwp
3. **Or contact Telegram:** @digen_skill_bot

Your API key is used as:
```
Authorization: Bearer YOUR_API_KEY
```

**Note:** The API uses `https://api.cowork.digen.ai` as the base URL.

---

## Quick Start

```python
from digen_ai_client import DigenAIClient

# Video generation — requires API Key (ak_xxx)
client = DigenAIClient(api_key="ak_xxxxxxxxxxxxxxxxxxxx")
```

---

## Image Generation (Old API)

**Uses `api.digen.ai` with DIGEN_TOKEN + DIGEN_SESSION_ID**

### Available Models
| Model | Description |
|-------|-------------|
| `default` | High quality model |

### Example

```python
from digen_ai_client import DigenAIClient

client = DigenAIClient(
    old_api_token="your_token",
    old_api_session="your_session"
)

result = client.generate_image_sync(
    prompt="futuristic cyberpunk city at night, neon lights, rainy streets, highly detailed, 8K",
    model="default",
    resolution="1:1"
)

if result["success"]:
    print(f"✅ Image: {result['images'][0]}")
else:
    print(f"❌ Error: {result.get('error')}")
```

---

## Video Generation (New API)

**Uses new API with Bearer API Key**

### ⚠️ Important: Use `model="turbo"`

The video generation API requires `model="turbo"` parameter (not `default`).

### Available Models
| Model | Description | Max Duration |
|-------|-------------|--------------|
| `turbo` | Fast and high quality generation | 10s |

### Video Types
- **Image-to-Video**: ✅ Works - requires `image_url` + `prompt`
- **Text-to-Video**: ⚠️ May not work with all API keys (depends on credits)

### Example: Image-to-Video (Recommended)

```python
from digen_ai_client import DigenAIClient

client = DigenAIClient(api_key="ak_xxxxxxxxxxxxxxxxxxxx")

result = client.generate_video_sync(
    image_url="https://your-image.jpg",
    prompt="gentle camera pan left, neon lights twinkling",
    model="turbo",  # IMPORTANT: use "turbo", not "default"
    duration=5
)

if result["success"]:
    print(f"✅ Video: {result['video_url']}")
    print(f"   Thumbnail: {result['thumbnail_url']}")
else:
    print(f"❌ Error: {result.get('error')}")
```

### Example: Text-to-Video (May Not Work)

```python
client = DigenAIClient(api_key="ak_xxxxxxxxxxxxxxxxxxxx")

result = client.generate_video_sync(
    prompt="A cute cat playing piano in a cozy room, soft lighting",
    model="turbo",
    duration=5
)

if result["success"]:
    print(f"✅ Video: {result['video_url']}")
else:
    print(f"❌ Error: {result.get('error')}")
    # Note: Text-to-Video may fail if your API key only has image-to-video credits
```

---

## API Key Management (New API)

### Check API Key Info

```python
client = DigenAIClient(api_key="ak_xxx")
info = client.get_api_key_info()
print(info)
# {'success': True, 'data': {'api_key': 'ak_xxx', 'status': 1, 'created_at': '...'}}
```

### Upload Image

```python
result = client.upload_image(file_path="/path/to/image.jpg")
if result["success"]:
    print(f"Image URL: {result['url']}")
```

---

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DIGEN_TOKEN` | Old API token for image generation |
| `DIGEN_SESSION_ID` | Old API session ID for image generation |
| `DIGEN_API_KEY` | New API key (ak_xxx) for video generation |

### Setup

```bash
# Image generation (old API)
export DIGEN_TOKEN="your_token"
export DIGEN_SESSION_ID="your_session"

# Video generation (new API)
export DIGEN_API_KEY="ak_xxxxxxxxxxxxxxxxxxxx"
```

---

## Error Handling

### No API Key Error (Video)

```
❌ API Key Not Found!

Get your free API key:
- Visit: https://claw.digen.ai
- Or join Discord: https://discord.gg/SRhbTt9hwp
```

### Error Codes (New API)

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 400 | invalid_request | Invalid or missing parameters |
| 401 | invalid_api_key | Invalid or missing API key |
| 402 | insufficient_credits | Not enough credits |
| 404 | not_found | Resource not found |
| 500 | internal_error | Internal server error |

---

## API Reference

### New API Endpoints (Video)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/b/v1/api-key` | Get API key info |
| `POST` | `/b/v1/upload` | Upload image file |
| `POST` | `/b/v1/video/generate` | Generate video |
| `GET` | `/b/v1/video/{id}` | Get video status |

Base URL: `https://api.cowork.digen.ai`

### Old API Endpoints (Image)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v2/tools/text_to_image` | Generate image |
| `POST` | `/v6/video/get_task_v2` | Get image status |

Base URL: `https://api.digen.ai`

---

## Scripts

- `scripts/digen_ai_client.py` - Python client with sync/async support
- `scripts/batch_generate.py` - Batch image generation utility
- `assets/telegram-bot.py` - Telegram bot for API key distribution
- `assets/discord-bot.py` - Discord bot for API key distribution

## Tips

- **Video model**: Always use `model="turbo"` (not `default` or `seedance-2.0`)
- **Image-to-Video**: Requires `image_url` parameter
- **Text-to-Video**: May not work with all API keys
- Video generation: poll every 5 seconds, timeout 300s
- Image generation: poll every 3 seconds, timeout 120s
