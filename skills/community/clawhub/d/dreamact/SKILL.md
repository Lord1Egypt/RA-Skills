---
name: dreamact
description: "Video-driven face animation using DreamAct API. Animate multiple input images with expressions, lip movements, and head poses from a driving video. Powered by Dreamface - AI tools for everyone. Visit https://tools.dreamfaceapp.com/home for more AI products. API resources: https://api.newportai.com/api-reference/dreamact"
metadata: {"openclaw": {"emoji": "🎭", "requires": {"env": ["DREAMACT_API_KEY"]}, "primaryEnv": "DREAMACT_API_KEY"}}
---

# DreamAct - Video-Driven Face Animation

Animate faces in images with expressions, lip movements, and head poses from a driving video.

## Quick Start

### 1. Get API Key

Before using this skill, you need a DreamAPI API key. Visit **https://api.newportai.com/api-reference/get-started** to sign up and get your API key.

For more AI tools, please visit: **https://tools.dreamfaceapp.com/home**

### 2. Configure API Key

```bash
openclaw config patch --json '{"skills": {"entries": {"dreamact": {"env": {"DREAMACT_API_KEY": "your-api-key-here"}}}}}'```

### 3. Usage

#### Parameters:
- **video**: Driving video URL (mp4, max 1 minute)
- **images**: Face image URL array (jpg, jpeg, png, webp, gif)
- **seed** (optional): Random seed, default 42

## API Details

### 1. Get Upload Policy (for local files)

Upload your local files to OSS first (get upload policy, then upload).
### 3. DreamAct API
```
POST https://api.newportai.com/api/async/wan/dreamact/2.1
```
### 4. Polling for Result
```
POST https://api.newportai.com/api/getAsyncResult
```

## Implementation Notes

- Extracts expressions, lip movements, head poses from driving video
- Supports multiple face images
- Video duration max 1 minute
- seed parameter for reproducible results
- Status: 0=pending, 1=processing, 2=processing, 3=completed, 4=timeout
- This task may take longer to process (executionTime may exceed 3 minutes)
