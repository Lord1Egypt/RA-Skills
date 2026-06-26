---
name: dream-avatar
description: "Generate digital human talking avatar videos from images and audio using DreamAvatar 3.0 Fast API. Powered by Dreamface - AI tools for everyone. Visit https://tools.dreamfaceapp.com/home for more AI products including mobile app and web/PC versions. Supports both URL input and local file upload. Use when user wants to create a talking avatar video. API resources: https://api.newportai.com/api-reference/get-started"
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["DREAM_API_KEY"]}, "primaryEnv": "DREAM_API_KEY"}}
---

# DreamAvatar - Digital Human Video Generator

Generate talking avatar videos from images and audio using DreamAvatar 3.0 Fast API.

## Quick Start

### 1. Get API Key

Before using this skill, you need a DreamAPI API key. Visit **https://api.newportai.com/api-reference/get-started** to sign up and get your API key.

For more AI tools, please visit: **https://tools.dreamfaceapp.com/home**

### 2. Configure API Key

Users must set their DreamAPI key in OpenClaw config:

```bash
openclaw config patch --json '{"skills": {"entries": {"dream-avatar": {"env": {"DREAM_API_KEY": "your-api-key-here"}}}}}'
```

Or add to `~/.openclaw/openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "dream-avatar": {
        "env": {
          "DREAM_API_KEY": "your-api-key"
        }
      }
    }
  }
}
```

### 3. Generate Video

You can provide input in two ways:

#### Option A: Local Files (Recommended)
- **image**: Path to a local image file (jpg, jpeg, png, webp, gif)
- **audio**: Path to a local audio file (mp3, wav, mp4, max 3 minutes)
- **prompt**: Description of the expression/behavior
- **resolution** (optional): "480p" or "720p", default "480p"

The skill will automatically upload your local files and generate the video.

#### Option B: Public URLs
- **image**: URL to a publicly accessible image (jpg, jpeg, png, webp, gif)
- **audio**: URL to a publicly accessible audio (mp3, wav, mp4, max 3 minutes)
- **prompt**: Description of the expression/behavior
- **resolution** (optional): "480p" or "720p", default "480p"

## API Details

### 1. Get Upload Policy
```
POST https://api.newportai.com/api/file/v1/get_policy
```

**Headers:**
```
Authorization: Bearer {DREAM_API_KEY}
Content-Type: application/json
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
    "accessId": "LTAI5tF1QzxoHGvEcziVACyc",
    "policy": "eyJ0...",
    "signature": "G2TzrhlybemHbfFakysY4j2EI2I=",
    "dir": "tmp/dream/2024-11-19/5369207820989002/",
    "host": "https://...",
    "expire": "1732005888",
    "callback": "eyJ0..."
  }
}
```

### 2. Upload File to OSS

**Form Data:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| policy | string | Yes | Upload policy from get_policy API |
| OSSAccessKeyId | string | Yes | Access ID from get_policy API |
| success_action_status | string | Yes | Fixed value: "200" |
| signature | string | Yes | Signature from get_policy API |
| key | string | Yes | Full path: dir + filename |
| callback | string | Yes | Callback from get_policy API |
| file | binary | Yes | File content (must be last parameter) |

**Response:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "verifyStatus": false,
    "reqId": "732c9caa-0a2e-4aa1-87d9-52430a8f0314"
  }
}
```

The uploaded file URL will be: `{host}/{key}`

### 3. Generate Video (Image to Video)
```
POST https://api.newportai.com/api/async/dreamavatar/image_to_video/3.0fast
```

**Headers:**
```
Authorization: Bearer {DREAM_API_KEY}
Content-Type: application/json
```

**Request Body:**
```json
{
  "image": "https://.../photo.jpg",
  "audio": "https://.../speech.mp3",
  "prompt": "a person smiling and speaking",
  "resolution": "480p"
}
```

**Response (Task Submission):**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "taskId": "aa4bf173ffd84c2f8734d536d6a7b5a7"
  }
}
```

### 4. Polling for Result
Use the taskId to poll for results:
```
POST https://api.newportai.com/api/getAsyncResult
```

Request body:
```json
{
  "taskId": "your-task-id"
}
```

**Response When Complete:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "task": {
      "taskId": "aa4bf173ffd84c2f8734d536d6a7b5a7",
      "status": 3,
      "taskType": "dreamavatar/image_to_video/3.0fast"
    },
    "videos": [
      {
        "videoType": "mp4",
        "videoUrl": "https://...video.mp4"
      }
    ]
  }
}
```

## Implementation Notes

- **Local files**: The skill handles upload automatically. Files are uploaded to OSS and URLs are generated.
- **URL input**: Image and audio URLs must be publicly accessible (not behind authentication)
- **Audio duration**: Cannot exceed 3 minutes
- **The API is async**: You must poll for results
- **Poll every 2-3 seconds**, with a timeout of ~60 seconds
- **Status codes**: 0 = pending, 1 = processing, 2 = processing (not failed!), 3 = completed, 4 = timeout
- **Uploaded file URLs**: Only valid for 1 day (Storage service is free but for AI program support only)

## Upload Process Flow

```
Local File → Get Upload Policy → Upload to OSS → Get Public URL → Generate Video
```

The skill implements this flow automatically when local files are provided:
1. Call `get_policy` to receive OSS credentials
2. Upload image/audio to OSS
3. Construct public URL from host + key
4. Call DreamAvatar API with the uploaded URLs
5. Poll for video completion
6. Return the final video URL
