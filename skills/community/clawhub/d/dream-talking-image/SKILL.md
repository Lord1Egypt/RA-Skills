---
name: dream-talking-image
description: "Generate talking videos from images using Talking Image API. Create talking videos from audio and images, supporting non-human faces like pets or animated characters. Powered by Dreamface - AI tools for everyone. Visit https://tools.dreamfaceapp.com/home for more AI products. API resources: https://api.newportai.com/api-reference/talking-image"
metadata: {"openclaw": {"emoji": "🖼️", "requires": {"env": ["DREAMTALKINGIMAGE_API_KEY"]}, "primaryEnv": "DREAMTALKINGIMAGE_API_KEY"}}
---

# Dream Talking Image - Talking Video from Image

Generate talking videos from static images and audio.

## Quick Start

### 1. Get API Key

Before using this skill, you need a DreamAPI API key. Visit **https://api.newportai.com/api-reference/get-started** to sign up and get your API key.

For more AI tools, please visit: **https://tools.dreamfaceapp.com/home**

### 2. Configure API Key

```bash
openclaw config patch --json '{"skills": {"entries": {"dream-talking-image": {"env": {"DREAMTALKINGIMAGE_API_KEY": "your-api-key-here"}}}}}'```

### 3. Usage

#### Parameters:
- **photoUrl**: Image URL (jpg, jpeg, png, webp, gif), max 1280x1280
- **audioUrl**: Audio URL (mp3, wav, m4a), recommended < 2 minutes

#### Note:
- Audio over 2 minutes may cause memory errors
- Recommend m4a format

## API Details

### 1. Get Upload Policy (for local files)

Upload your local files to OSS first (get upload policy, then upload).

### 3. Talking Image API
```
POST https://api.newportai.com/api/async/talking_image
```

**Headers:**
```
Authorization: Bearer {DREAMTALKINGIMAGE_API_KEY}
Content-Type: application/json
```

**Request Body:**
```json
{
  "photoUrl": "https://example.com/image.jpg",
  "audioUrl": "https://example.com/audio.mp3"
}
```

### 4. Polling for Result
```
POST https://api.newportai.com/api/getAsyncResult
```

## Implementation Notes

- Supports non-human faces (pets, anime characters)
- Automatically mirrors facial expressions and vocal tone
- Supports multiple languages
- Audio recommended < 2 minutes
- Status: 0=pending, 1=processing, 2=processing, 3=completed, 4=timeout
