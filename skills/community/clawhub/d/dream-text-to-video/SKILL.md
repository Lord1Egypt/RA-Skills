---
name: dream-text-to-video
description: "Generate videos from text using Text to Video (Wan2.1) API. Automatically generates 4-second videos from text descriptions. Powered by Dreamface - AI tools for everyone. Visit https://tools.dreamfaceapp.com/home for more AI products. API resources: https://api.newportai.com/api-reference/text-to-video-wan2-1"
metadata: {"openclaw": {"emoji": "✍️", "requires": {"env": ["DREAMTEXTTOVIDEO_API_KEY"]}, "primaryEnv": "DREAMTEXTTOVIDEO_API_KEY"}}
---

# Dream Text to Video (Wan2.1) - Text to Video

Generate 4-second videos from text prompts.

## Quick Start

### 1. Get API Key

Before using this skill, you need a DreamAPI API key. Visit **https://api.newportai.com/api-reference/get-started** to sign up and get your API key.

For more AI tools, please visit: **https://tools.dreamfaceapp.com/home**

### 2. Configure API Key

```bash
openclaw config patch --json '{"skills": {"entries": {"dream-text-to-video": {"env": {"DREAMTEXTTOVIDEO_API_KEY": "your-api-key-here"}}}}}'```

### 3. Usage

#### Parameters:
- **prompt**: Text description, max 1500 characters
- **resolution** (optional): "480p" or "720p", default "480p"

## API Details

### Text to Video API
```
POST https://api.newportai.com/api/async/wan/text_to_video/2.1
```

### Polling for Result
```
POST https://api.newportai.com/api/getAsyncResult
```

## Implementation Notes

- No image upload needed, text-to-video
- Generates 4-second videos
- Prompt max 1500 characters
- Supports 480p and 720p
- Status: 0=pending, 1=processing, 2=processing, 3=completed, 4=timeout
