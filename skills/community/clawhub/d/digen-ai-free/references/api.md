# DigenAI API Reference

> **Last updated: 2026-04-15** - New API (video) and Old API (image) separated

---

## 📺 New API — Video Generation ([New API])

**Auth: `Authorization: Bearer <API_KEY>`**

### Base URL
```
[NEW_API_BASE]
```

---

### Get API Key Info

```
GET /b/v1/api-key
```

Response:
```json
{
  "api_key": "ak_xxxxxxxxxxxxxxxx",
  "api_secret": "as_xxxxx...",
  "callback_url": "https://your-domain.com/webhook",
  "status": 1,
  "created_at": "2026-04-09T10:30:00Z"
}
```

---

### Upload Image

```
POST /b/v1/upload
```

Content-Type: `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file | ✅ | Image file (jpg, png, gif, webp) |

Response:
```json
{
  "url": "https://s3.us-west-1.wasabisys.com/...",
  "width": 1920,
  "height": 1080
}
```

---

### Generate Video

```
POST /b/v1/video/generate
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | string | ❌ | `wan` (default), `turbo`, `2.6` |
| `prompt` | string | ⚠️ | Text prompt (* Either prompt or image_url required) |
| `image_url` | string | ⚠️ | Input image URL (* Either prompt or image_url required) |
| `image_end_url` | string | ❌ | End frame image URL |
| `aspect_ratio` | string | ❌ | `16:9`, `9:16`, `1:1` (default: `16:9`) |
| `duration` | integer | ❌ | `5` or `10` seconds (default: `5`) |
| `resolution` | string | ❌ | `720p` or `1080p` |
| `webhook_url` | string | ❌ | Completion callback URL |

Response:
```json
{
  "id": "12345",
  "status": "pending",
  "created_at": "2026-04-09T10:30:00Z"
}
```

---

### Get Video Status

```
GET /b/v1/video/{id}
```

**Status values:** `pending` → `processing` → `completed` / `failed`

Processing:
```json
{
  "id": "12345",
  "status": "processing",
  "progress": 50,
  "created_at": "2026-04-09T10:30:00Z"
}
```

Completed:
```json
{
  "id": "12345",
  "status": "completed",
  "progress": 100,
  "output": {
    "video_url": "https://cdn.example.com/video.mp4",
    "thumbnail_url": "https://cdn.example.com/thumb.jpg"
  },
  "created_at": "2026-04-09T10:30:00Z",
  "completed_at": "2026-04-09T10:35:00Z"
}
```

Failed:
```json
{
  "id": "12345",
  "status": "failed",
  "error": "Content policy violation",
  "completed_at": "2026-04-09T10:35:00Z"
}
```

---

### Webhook Events

When a video completes, POST to your `webhook_url`:

```json
// Completed
{
  "id": "12345",
  "status": "completed",
  "output": {
    "video_url": "https://cdn.example.com/video.mp4",
    "thumbnail_url": "https://cdn.example.com/thumb.jpg"
  },
  "completed_at": "2026-04-09T10:35:00Z"
}

// Failed
{
  "id": "12345",
  "status": "failed",
  "error": "Content policy violation",
  "completed_at": "2026-04-09T10:35:00Z"
}
```

---

### Error Codes (New API)

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 400 | invalid_request | Invalid or missing parameters |
| 401 | invalid_api_key | Invalid or missing API key |
| 402 | insufficient_credits | Not enough credits |
| 404 | not_found | Resource not found |
| 500 | internal_error | Internal server error |

Error format:
```json
{
  "error": {
    "message": "Invalid API Key",
    "code": "invalid_api_key"
  }
}
```

---

## 🖼️ Old API — Image Generation (api.digen.ai)

**Auth: `DIGEN-Token` + `DIGEN-SessionID` headers**

### Base URL
```
https://api.digen.ai
```

### Image Generation (Text-to-Image)

```
POST /v2/tools/text_to_image
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | ✅ | Positive prompt |
| `mode` | string | ✅ | Always `"text_to_image"` |
| `aspect_ratio` | string | ✅ | Resolution ratio |
| `image_size` | string | ✅ | Calculated size |
| `model` | string | ✅ | `flux2-klein`, `image_motion`, `zimage` |
| `batch_size` | int | ❌ | Number of images (default 1) |
| `negative_prompt` | string | ❌ | Things to avoid |

### Image Size Mapping

| aspect_ratio | image_size |
|--------------|------------|
| `1:1` | `1024x1024` |
| `16:9` | `1024x576` |
| `9:16` | `576x1024` |
| `4:3` | `1024x768` |
| `3:4` | `768x1024` |
| `3:2` | `1024x683` |
| `2:3` | `683x1024` |
| `5:4` | `1024x819` |
| `4:5` | `819x1024` |
| `21:9` | `1280x512` |

### Poll Image Status

```
POST /v6/video/get_task_v2
```

Request: `{"jobID": "<job_id>"}`

Response:
```json
{
  "errCode": 0,
  "data": {
    "status": 4,
    "resource_urls": ["https://..."]
  }
}
```

**Status:** 1=new, 2=running, 4=completed, 5=failed

---

### Error Codes (Old API)

| errCode | Meaning |
|---------|---------|
| `0` | Success |
| `-1` | Network error |

Error format:
```json
{
  "errCode": -1,
  "errMsg": "error description"
}
```

---

## Quick Test Commands

```bash
# New API - Check key info
curl "[NEW_API_BASE]/b/v1/api-key" \
  -H "Authorization: Bearer YOUR_KEY"

# New API - Generate video
curl -X POST "[NEW_API_BASE]/b/v1/video/generate" \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A cat playing piano","model":"wan","duration":5}'

# New API - Check video status
curl "[NEW_API_BASE]/b/v1/video/12345" \
  -H "Authorization: Bearer YOUR_KEY"

# Old API - Generate image
curl -X POST "https://api.digen.ai/v2/tools/text_to_image" \
  -H "DIGEN-Token: YOUR_TOKEN" \
  -H "DIGEN-SessionID: YOUR_SESSION" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"a cat","mode":"text_to_image","aspect_ratio":"1:1","image_size":"1024x1024","model":"flux2-klein"}'
```
