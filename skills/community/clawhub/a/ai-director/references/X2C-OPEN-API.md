# X2C Open API Documentation

## Overview

The X2C Open API provides a unified interface for third-party developers to integrate AI video generation capabilities into their applications.

**Base URL:** `$X2C_API_BASE_URL`

**Method:** All requests use `POST`

**Content-Type:** `application/json`

---

## Authentication

### Step 1: Send Verification Code

```json
POST /functions/v1/open-api
{
  "action": "auth/send-code",
  "email": "user@example.com"
}
```

**Response:**

```json
{ "success": true, "message": "Verification code sent to email" }
```

### Step 2: Verify Code & Get API Key

```json
POST /functions/v1/open-api
{
  "action": "auth/verify",
  "email": "user@example.com",
  "code": "123456"
}
```

**Response:**

```json
{
  "success": true,
  "api_key": "x2c_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "user_id": "uuid"
}
```

> ⚠️ Save your API key securely. All subsequent requests require the `X-API-Key` header.

---

## Common Headers (for protected endpoints)

| Header       | Value            | Required             |
| ------------ | ---------------- | -------------------- |
| Content-Type | application/json | Yes                  |
| X-API-Key    | x2c_sk_xxxx      | Yes (except auth/\*) |

---

## API Endpoints

### 1. Get Configuration Options

Get available styles, categories, pricing tiers and other configuration parameters.

```json
POST /functions/v1/open-api
Headers: { "X-API-Key": "x2c_sk_xxxx" }
{
  "action": "config/get-options"
}
```

**Response:**

```json
{
  "success": true,
  "modes": ["short_video", "short_drama"],
  "ratios": ["9:16", "16:9"],
  "durations": [
    { "value": "60", "label": "60s", "credits": 299, "usd": 2.99 },
    { "value": "120", "label": "120s", "credits": 599, "usd": 5.99 },
    { "value": "180", "label": "180s", "credits": 799, "usd": 7.99 },
    { "value": "300", "label": "300s", "credits": 999, "usd": 9.99 }
  ],
  "script_pricing": [
    { "mode": "short_video", "credits": 6, "usd": 0.06 },
    { "mode": "short_drama", "credits": 60, "usd": 0.6 }
  ],
  "styles": [{ "id": 101, "name": "3D古风", "thumbnail_url": "..." }],
  "categories": [{ "id": "uuid", "name": "都市情感", "target_language": "zh-CN" }]
}
```

---

### 2. Generate Script

Generate a script with automatic credit deduction.

```json
POST /functions/v1/open-api
Headers: { "X-API-Key": "x2c_sk_xxxx" }
{
  "action": "script/generate",
  "prompt": "A story about a time traveler in ancient China",
  "mode": "short_drama",
  "duration": "120",
  "style": "3D古风",
  "ratio": "9:16",
  "total_episodes": 10,
  "category_id": "optional-category-uuid",
  "language": "zh"
}
```

| Parameter      | Type   | Required | Description                                                         |
| -------------- | ------ | -------- | ------------------------------------------------------------------- |
| prompt         | string | Yes      | Story idea/description                                              |
| mode           | string | No       | "short_video" (default) or "short_drama"                            |
| duration       | string | No       | "60", "120" (default), "180", or "300"                              |
| style          | string | No       | Style name from config/get-options                                  |
| ratio          | string | No       | "9:16" (default) or "16:9"                                          |
| total_episodes | number | No       | Number of episodes (default: 1 for short_video, 10 for short_drama) |
| category_id    | string | No       | Category UUID from config/get-options                               |
| language       | string | No       | "zh" (default) or "en"                                              |

**Response:**

```json
{
  "success": true,
  "project_id": "workspace-uuid",
  "status": "generating",
  "mode": "short_drama",
  "total_episodes": 10,
  "credits_charged": 60
}
```

---

### 3. Query Script Status

Poll the script generation status and retrieve completed scripts.

```json
POST /functions/v1/open-api
Headers: { "X-API-Key": "x2c_sk_xxxx" }
{
  "action": "script/query",
  "project_id": "workspace-uuid"
}
```

**Response:**

```json
{
  "success": true,
  "project_id": "workspace-uuid",
  "title": "穿越秦朝当宰相",
  "status": "completed",
  "total_episodes": 10,
  "completed_episodes": 10,
  "mode": "short_drama",
  "duration": "120",
  "style": "3D古风",
  "episodes": [
    {
      "episode_number": 1,
      "title": "第1集：穿越之日",
      "content": "### 🎬 第1集...",
      "thumbnail_url": "https://...",
      "has_video": false,
      "is_published": false
    }
  ]
}
```

| Status     | Description                |
| ---------- | -------------------------- |
| generating | Script is being generated  |
| partial    | Some episodes are complete |
| completed  | All episodes are complete  |

---

### 4. Produce Video (Single Episode)

Submit a single episode for video production with automatic credit deduction.

```json
POST /functions/v1/open-api
Headers: { "X-API-Key": "x2c_sk_xxxx" }
{
  "action": "video/produce",
  "project_id": "workspace-uuid",
  "episode_number": 1
}
```

**Response:**

```json
{
  "success": true,
  "task_id": "director-project-uuid",
  "status": "processing",
  "credits_charged": 599,
  "episode_number": 1
}
```

> ⚠️ Credits are charged based on the duration setting when the script was created.

---

### 5. Query Video Production Progress

Poll the video production status, progress, and retrieve the final video URL.

```json
POST /functions/v1/open-api
Headers: { "X-API-Key": "x2c_sk_xxxx" }
{
  "action": "video/query",
  "project_id": "workspace-uuid",
  "episode_number": 1
}
```

**Response (in progress):**

```json
{
  "success": true,
  "task_id": "director-project-uuid",
  "status": "processing",
  "progress": 45,
  "current_step": "video_generation",
  "characters": [
    { "id": "char-1", "name": "李明", "imageUrl": "https://...", "status": "completed" }
  ],
  "storyboard_shots": [{ "id": "shot-1", "description": "...", "imageUrl": "https://..." }],
  "video_url": null,
  "is_complete": false,
  "is_failed": false,
  "is_published": false
}
```

**Response (completed):**

```json
{
  "success": true,
  "task_id": "director-project-uuid",
  "status": "completed",
  "progress": 100,
  "video_url": "https://...",
  "video_asset": {
    "signed_url": "https://...",
    "download_url": "https://...",
    "thumbnail_url": "https://..."
  },
  "is_complete": true,
  "is_failed": false
}
```

| Status      | Description                        |
| ----------- | ---------------------------------- |
| not_started | Video production not yet initiated |
| processing  | Video is being produced            |
| completed   | Video is ready                     |
| failed      | Production failed                  |

---

### 6. Publish Project

Publish a completed video to the platform.

```json
POST /functions/v1/open-api
Headers: { "X-API-Key": "x2c_sk_xxxx" }
{
  "action": "project/publish",
  "project_id": "workspace-uuid",
  "episode_number": 1
}
```

**Response:**

```json
{
  "success": true,
  "status": "published",
  "project_id": "published-project-uuid",
  "asset_name": "穿越秦朝当宰相",
  "category": "都市情感"
}
```

---

## Error Codes

| HTTP Status | Code | Description                      |
| ----------- | ---- | -------------------------------- |
| 200         | -    | Success                          |
| 400         | 400  | Bad request / Missing parameters |
| 401         | 401  | Invalid or missing API key       |
| 402         | 402  | Insufficient credits             |
| 403         | 403  | Unauthorized access to resource  |
| 404         | 404  | Resource not found               |
| 500         | 500  | Internal server error            |

**Error Response Format:**

```json
{
  "success": false,
  "error": "Error description",
  "code": 400,
  "details": "Optional additional information"
}
```

---

## Complete Workflow Example

```text
1. auth/send-code  →  Send verification email
2. auth/verify     →  Get API Key
3. config/get-options → Get styles, categories, pricing
4. script/generate →  Create script (auto-charges credits)
5. script/query    →  Poll until status = "completed"
6. video/produce   →  Submit episode for production (auto-charges credits)
7. video/query     →  Poll until status = "completed" and video_url is available
8. project/publish →  Publish to platform
```

### cURL Example

```bash
# Step 1: Send verification code
curl -X POST $X2C_API_BASE_URL \
  -H "Content-Type: application/json" \
  -d '{"action": "auth/send-code", "email": "dev@example.com"}'

# Step 2: Verify and get API key
curl -X POST $X2C_API_BASE_URL \
  -H "Content-Type: application/json" \
  -d '{"action": "auth/verify", "email": "dev@example.com", "code": "123456"}'

# Step 3: Generate script
curl -X POST $X2C_API_BASE_URL \
  -H "Content-Type: application/json" \
  -H "X-API-Key: x2c_sk_xxxx" \
  -d '{"action": "script/generate", "prompt": "A love story in ancient China", "mode": "short_video", "duration": "120"}'

# Step 4: Check script status
curl -X POST $X2C_API_BASE_URL \
  -H "Content-Type: application/json" \
  -H "X-API-Key: x2c_sk_xxxx" \
  -d '{"action": "script/query", "project_id": "workspace-uuid"}'

# Step 5: Start video production
curl -X POST $X2C_API_BASE_URL \
  -H "Content-Type: application/json" \
  -H "X-API-Key: x2c_sk_xxxx" \
  -d '{"action": "video/produce", "project_id": "workspace-uuid", "episode_number": 1}'

# Step 6: Check video progress
curl -X POST $X2C_API_BASE_URL \
  -H "Content-Type: application/json" \
  -H "X-API-Key: x2c_sk_xxxx" \
  -d '{"action": "video/query", "project_id": "workspace-uuid", "episode_number": 1}'

# Step 7: Publish
curl -X POST $X2C_API_BASE_URL \
  -H "Content-Type: application/json" \
  -H "X-API-Key: x2c_sk_xxxx" \
  -d '{"action": "project/publish", "project_id": "workspace-uuid", "episode_number": 1}'
```

---

## Rate Limits

- Authentication endpoints: 5 requests/minute per email
- Protected endpoints: 60 requests/minute per API key

## Credits System

- 100 credits = $1 USD
- Script credits are charged at generation time
- Video credits are charged at production time
- Credits cannot be refunded once video production starts

---

_Last Updated: 2026-02-10_
