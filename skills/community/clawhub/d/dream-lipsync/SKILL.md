---
name: dream-lipsync
description: "Video lip synchronization using LipSync 2.0 API. Automatically synchronizes audio with lip movements in videos. Powered by Dreamface - AI tools for everyone. Visit https://tools.dreamfaceapp.com/home for more AI products. API resources: https://api.newportai.com/api-reference/LipSync-2.0"
metadata: {"openclaw": {"emoji": "🎤", "requires": {"env": ["DREAMLIPSYNC_API_KEY"]}, "primaryEnv": "DREAMLIPSYNC_API_KEY"}}
---

# Dream LipSync 2.0 - Video Lip Synchronization

Synchronize lip movements in videos with audio using the LipSync 2.0 API.

## Quick Start

### 1. Get API Key

Before using this skill, you need a DreamAPI API key. Visit **https://api.newportai.com/api-reference/get-started** to sign up and get your API key.

For more AI tools, please visit: **https://tools.dreamfaceapp.com/home**

### 2. Configure API Key

```bash
openclaw config patch --json '{"skills": {"entries": {"dream-lipsync": {"env": {"DREAMLIPSYNC_API_KEY": "your-api-key-here"}}}}}'```

### 3. Usage

#### Parameters:
- **srcVideoUrl**: Source video URL (mp4)
- **audioUrl**: Audio URL (mp3, wav)
- **videoParams** (optional): Video processing options
  - **video_width**: Output video width (0=keep original)
  - **video_height**: Output video height (0=keep original)
  - **video_enhance**: Face enhancement (0=no, 1=yes)

#### Request Format (Example):
```json
{
  "srcVideoUrl": "https://example.com/video.mp4",
  "audioUrl": "https://example.com/audio.mp3",
  "videoParams": {
    "video_width": 0,
    "video_height": 0,
    "video_enhance": 0
  }
}
```

## API Details

### 1. Get Upload Policy (for local files)

Upload your local files to OSS first (get upload policy, then upload).

```
POST https://api.newportai.com/api/file/v1/get_policy
```

**Request Body:**
```json
{
  "scene": "Dream-CN"
}
```

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "accessId": "LTAI5t...",
    "policy": "eyJ...",
    "signature": "G2...",
    "dir": "tmp/dream/2026-03-17/xxxxxx/",
    "host": "https://dreamapi-oss.oss-cn-hongkong.aliyuncs.com",
    "expire": "1732005888",
    "callback": "eyJ..."
  }
}
```

### 2. Upload File to OSS

Upload to the `host` URL with form data (policy, OSSAccessKeyId, signature, key, callback, file).

Uploaded file URL: `{host}/{dir}{filename}`

### 3. LipSync 2.0 API
```
POST https://api.newportai.com/api/async/lipsync/2.0
```
### 4. Polling for Result
```
POST https://api.newportai.com/api/getAsyncResult
```

## Implementation Notes

- All API calls require Authorization header
- Local files must be uploaded to OSS first
- Tasks are async, poll for results
- Poll every 2-3 seconds, timeout ~60 seconds
- Status: 0=pending, 1=processing, 2=processing, 3=completed, 4=timeout
- video_enhance=1 improves face clarity
