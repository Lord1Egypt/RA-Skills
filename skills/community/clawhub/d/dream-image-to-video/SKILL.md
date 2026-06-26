---
name: dream-image-to-video
description: "Generate videos from images using Image to Video (Wan2.1) API. Automatically generates 4-second videos from text descriptions and images. Powered by Dreamface - AI tools for everyone. Visit https://tools.dreamfaceapp.com/home for more AI products. API resources: https://api.newportai.com/api-reference/image-to-video-wan2-1"
metadata: {"openclaw": {"emoji": "🎞️", "requires": {"env": ["DREAMIMAGETOVIDEO_API_KEY"]}, "primaryEnv": "DREAMIMAGETOVIDEO_API_KEY"}}
---

# Dream Image to Video (Wan2.1) - Image to Video

Generate 4-second videos from text prompts and images.

## Quick Start

### 1. Get API Key

Before using this skill, you need a DreamAPI API key. Visit **https://api.newportai.com/api-reference/get-started** to sign up and get your API key.

For more AI tools, please visit: **https://tools.dreamfaceapp.com/home**

### 2. Configure API Key

```bash
openclaw config patch --json '{"skills": {"entries": {"dream-image-to-video": {"env": {"DREAMIMAGETOVIDEO_API_KEY": "your-api-key-here"}}}}}'```

### 3. Usage

#### Parameters:
- **prompt**: Text description, max 1500 characters
- **image**: Image URL
- **resolution** (optional): "480p" or "720p", default "480p"

## API Details

### 1. Get Upload Policy (for local files)

Upload your local files to OSS first (get upload policy, then upload).

### 2. Image to Video API
```
POST https://api.newportai.com/api/async/wan/image_to_video/2.1
```

### 3. Polling for Result
```
POST https://api.newportai.com/api/getAsyncResult
```

## Implementation Notes

- Generates 4-second videos
- Prompt max 1500 characters
- Supports 480p and 720p
- Status: 0=pending, 1=processing, 2=processing, 3=completed, 4=timeout
