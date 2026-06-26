---
name: postmoore
description: Post to Instagram, TikTok, YouTube Shorts, LinkedIn, Facebook, Threads, and Bluesky via the Postmoore API. Schedule posts, upload media, save drafts, and manage content autonomously.
version: 1.1.0
emoji: 🚀
homepage: https://postmoo.re
metadata: {"openclaw": {"requires": {"env": ["POSTMOORE_API_KEY"]}, "primaryEnv": "POSTMOORE_API_KEY", "requires": {"bins": ["ffmpeg"], "env": ["POSTMOORE_API_KEY"]}}}
---

# Postmoore — Social Media Assistant

Autonomously manage social media posting via the Postmoore API.

## Setup

1. Create a Postmoore account at postmoo.re
2. Connect your social accounts (Instagram, TikTok, YouTube Shorts, LinkedIn, Facebook, Threads, Bluesky)
3. Go to Profile → API Keys and generate an API key (Creator or Premium plan required)
4. Store your key in your workspace `.env`:

```
POSTMOORE_API_KEY=pm_live_xxxxx
```

## Auth

All requests use a Bearer token:

```
Authorization: Bearer <POSTMOORE_API_KEY>
```

Base URL: `https://postmoo.re/api/v1`

## Core Workflow

### 1. Get Social Accounts

```
GET /accounts
```

Optional filter by platform:

```
GET /accounts?platform=tiktok
```

Supported platform values: `instagram` · `tiktok` · `ytshorts` · `linkedin` · `facebook` · `threads` · `bluesky`

Returns an array of connected accounts. Each account has:
- `id` — use this in every post request
- `platform` — the platform name
- `displayName` — the account display name
- `platformUsername` — username on the platform
- `status` — always `active`

**Always fetch account IDs before posting — never guess them.**

### 2. Upload Media

```
POST /media
Content-Type: multipart/form-data

file: <binary>
```

Supported formats: `image/jpeg` · `image/png` · `image/gif` · `image/webp` · `video/mp4` · `video/quicktime` · `video/webm`

Max file size: 100 MB. Storage quota: 5 GB (Creator plan) · 20 GB (Premium plan).

Returns:
```json
{
  "data": {
    "id": "uploads/user123/filename.mp4",
    "type": "video",
    "url": "https://storage.postmoo.re/...",
    "mimeType": "video/mp4",
    "size": 10485760,
    "filename": "video.mp4"
  }
}
```

Save both `id` and `url` — you need both when creating a media post.

### 3. Create a Post

```
POST /posts
Content-Type: application/json
```

**Text post (post now):**
```json
{
  "contentType": "text",
  "text": "Your caption here #hashtags",
  "accounts": ["<account_id_1>", "<account_id_2>"],
  "schedule": { "type": "now" }
}
```

**Text post (scheduled):**
```json
{
  "contentType": "text",
  "text": "Scheduled caption #hashtags",
  "accounts": ["<account_id_1>"],
  "schedule": { "type": "scheduled", "at": "2026-06-01T14:00:00Z" }
}
```

**Media post (image or video):**
```json
{
  "contentType": "media",
  "text": "Caption for the post #hashtags",
  "media": [{ "id": "<id_from_upload>", "url": "<url_from_upload>" }],
  "accounts": ["<account_id_1>", "<account_id_2>"],
  "schedule": { "type": "now" }
}
```

**Draft (save without publishing):**
```json
{
  "contentType": "text",
  "text": "Draft caption to review",
  "accounts": ["<account_id_1>"],
  "schedule": { "type": "draft" }
}
```

**schedule** options:
- `{ "type": "now" }` — publish immediately
- `{ "type": "scheduled", "at": "<ISO 8601 datetime>" }` — schedule for future
- `{ "type": "draft" }` — save as draft, no publishing

Returns post object with:
- `id` — post ID
- `status` — `pending` · `scheduled` · `published` · `failed` · `draft`
- `accounts` — array of `{ id, platform }`
- `results` — per-platform result with `success`, `postId`, `url`, `error`

### 4. List Posts

```
GET /posts
GET /posts?status=scheduled
GET /posts?status=draft&page=1&limit=20
```

Status filters: `pending` · `scheduled` · `published` · `failed` · `draft`

Pagination params: `page` (default 1) · `limit` (default 20, max 100)

Returns paginated array with `data` and `pagination` object containing `page`, `limit`, `total`, `totalPages`, `hasMore`.

### 5. Get a Single Post

```
GET /posts/<post_id>
```

Returns full post object including per-platform results.

### 6. Delete a Post

```
DELETE /posts/<post_id>
```

Only works on posts with status `pending` or `draft`. Scheduled and published posts cannot be deleted.

Returns `{ "data": { "id": "<post_id>", "deleted": true } }`.

## Recommended Workflow for Video Content

1. Ask the user for the video file path
2. Extract a frame to understand the content:
   ```
   ffmpeg -i video.mp4 -ss 00:00:03 -frames:v 1 frame.jpg -y
   ```
3. Read the frame and write a caption with 4–5 relevant hashtags
4. Upload the video: `POST /media`
5. Get account IDs: `GET /accounts`
6. Create the post with the media `id` and `url` from the upload
7. Confirm status: `GET /posts/<post_id>`

## Tips

- Post to multiple platforms in one request by including multiple account IDs
- Use `"type": "draft"` when the user wants to review content before it goes live
- Stagger scheduled posts throughout the day for better reach
- Keep hashtags to 4–5 per post
- Always confirm account IDs from `GET /accounts` before every session
- Check the `results` array after posting for per-platform success or failure details
- If a post fails on one platform but succeeds on others, the overall status will be `failed` — check individual results
