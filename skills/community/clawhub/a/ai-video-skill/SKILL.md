---
name: aituber-api
description: >
  AITuber API skill for AI video creation. Generate videos with AI narration, visuals, and
  captions for YouTube Shorts, TikTok, Instagram Reels, and long-form content. Supports
  AI-generated images, video clips, stock footage, and viral templates like skeleton and
  character styles. Handles the full pipeline: pick a voice, generate a video, poll for
  completion, export to MP4, and download.

  TRIGGER when the user wants to: create an AI video, generate a video from a script or
  idea, list or browse AI voices, export a video to MP4, download a rendered video, check
  their AITuber subscription or credit balance, or automate video creation.

  DO NOT TRIGGER for: editing existing video files, uploading user-provided video footage,
  live streaming, video transcription or captioning of external files, image generation
  without video context, or anything unrelated to the AITuber platform.
license: MIT
compatibility:
  - claude-code
allowed-tools: Bash(curl:*) WebFetch Read Write
metadata:
  openclaw:
    emoji: "\U0001F3AC"
    homepage: https://aituber.app
    primaryEnv: AITUBER_API_KEY
    requires:
      env:
        - AITUBER_API_KEY
      bins:
        - curl
---

# AITuber API

Create AI videos from a script or idea. From 15-second Shorts to 7-minute long-form content. The API handles voice narration (1,300+ voices, any language), AI-generated visuals, word-synced captions, MP4 export, and publishing to YouTube, TikTok, and Instagram.

**Base URL:** `https://app.aituber.app/api/v1`
**OpenAPI spec:** `https://app.aituber.app/api/v1/openapi.json`
**API docs:** `https://app.aituber.app/api-docs`

> **Tip:** For the most up-to-date parameter details, examples, and response schemas, refer to the interactive API docs at https://app.aituber.app/api-docs when possible. The reference below covers everything you need to get started, but the docs always reflect the latest API.

## Authentication

All endpoints except `GET /voices` require a Bearer token. Create an API key in the AITuber dashboard at https://app.aituber.app/dashboard/api-keys.

```
Authorization: Bearer <AITUBER_API_KEY>
```

Store the key in the `AITUBER_API_KEY` environment variable.

## Complete Workflow

The typical flow is: **pick voice, generate video, poll status, export, download**.

### Step 1: Pick a voice

```bash
curl "https://app.aituber.app/api/v1/voices?gender=male&accent=American"
```

No auth required. Returns an array of voice objects. Use the `id` field as `voiceId` when generating.

### Step 2: Generate a video

From a script (you write the narration):

```bash
curl -X POST "https://app.aituber.app/api/v1/videos/generate" \
  -H "Authorization: Bearer $AITUBER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "script": "The human brain contains roughly 86 billion neurons. Every thought, memory, and emotion is the result of electrical signals racing through this incredible network.",
    "voiceId": "nPczCjzI2devNBz1zQrb",
    "imageStyleId": "cinematic",
    "aspectRatio": "9:16"
  }'
```

From an idea (AI writes the script):

```bash
curl -X POST "https://app.aituber.app/api/v1/videos/generate" \
  -H "Authorization: Bearer $AITUBER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "script": "5 mind-blowing facts about black holes",
    "inputType": "idea",
    "expectedDurationSeconds": 60
  }'
```

Returns `{ "videoId": "uuid", "status": "pending" }`.

### Step 3: Poll for completion

```bash
curl "https://app.aituber.app/api/v1/videos/VIDEO_ID" \
  -H "Authorization: Bearer $AITUBER_API_KEY"
```

Poll every 5-10 seconds. Generation typically takes 1-3 minutes. Wait until `status` is `completed` (or `failed`).

### Step 4: Export to MP4

```bash
curl -X POST "https://app.aituber.app/api/v1/exports" \
  -H "Authorization: Bearer $AITUBER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "videoId": "VIDEO_ID", "resolution": "1080p" }'
```

Exporting is free. Requires an active paid subscription. Poll `GET /videos/VIDEO_ID` and check `exportStatus` until it is `completed` (typically 30 seconds to 5 minutes).

### Step 5: Download the MP4

```bash
curl "https://app.aituber.app/api/v1/exports/download?videoId=VIDEO_ID" \
  -H "Authorization: Bearer $AITUBER_API_KEY"
```

Returns `{ "url": "https://...", "videoId": "..." }`. The URL is a signed temporary link that expires in 2 minutes. Download immediately.

## Endpoints Reference

### GET /voices

List available AI voices. **No auth required.**

| Param | Type | Description |
|-------|------|-------------|
| gender | string | Filter: `male`, `female` |
| accent | string | Filter: `American`, `British`, `Australian`, `Indian` |
| useCase | string | Filter: `narration`, `conversational`, `characters`, `social_media` |
| search | string | Search by name or description |

Response: array of `{ id, name, description, previewUrl, gender, age, accent, useCase, optimizedFor }`.

### POST /videos/generate

Create a new video. Returns `{ videoId, status }`.

**Video types (all use this same endpoint):**

1. **Faceless narration (images)** - Default. AI images with Ken Burns animation. Just send a script or idea.
2. **Faceless narration (video clips)** - AI video clips. Set `mediaType: "video"`.
3. **Stock footage** - Real stock footage matched to narration. Set `mediaType: "stock"`.
4. **Skeleton template** - Viral "what happens if..." X-ray style. Set `templateId: "skeleton"`. Template handles mediaType/style.
5. **Character template** - Character-driven stories. Set `templateId: "character"`, `inputType: "idea"`. Only idea mode (AI writes the script for character consistency).

**Examples:**
```json
// Idea to Video (faceless images, AI writes the script)
{ "script": "5 facts about black holes", "inputType": "idea", "expectedDurationSeconds": 60 }

// Script to Video (video clips, you write the script)
{ "script": "The ocean covers over 70 percent of Earth...", "mediaType": "video" }

// Skeleton template
{ "script": "What happens if you eat 100 bananas", "templateId": "skeleton" }

// Character template
{ "script": "A detective solves a mystery in Tokyo", "templateId": "character", "inputType": "idea", "expectedDurationSeconds": 90 }

// Script with visual control (brackets tell AI what to show)
{ "script": "[A dark forest at night] The wind howled through the trees. [Glowing eyes in the shadows] Something was watching.", "imageStyleId": "cinematic" }
```

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| script | string | Yes | Narration text (script mode) or topic (idea mode). The AI generates visuals automatically. For more control, optionally add visual instructions in brackets: `[A dark forest] The wind howled.` Each `[bracket]` tells the AI what to show for that scene. |
| inputType | string | No | `script` (default) or `idea`. Character template requires `idea`. |
| voiceId | string | No | Voice ID from GET /voices. Default: "Adam" |
| voiceSpeed | number | No | 0.7 to 1.2. Default: 1.0 |
| mediaType | string | No | `images` (default), `video`, or `stock`. Ignored when using templates. |
| aspectRatio | string | No | `9:16` (default), `16:9`, or `1:1` |
| imageQuality | string | No | For images mediaType: `basic` (1 credit/image), `good` (3), `premium` (9), `max` (45). Ignored when using templates. |
| imageStyleId | string | No | Visual style: `photorealistic` (default), `cinematic`, `anime`, `3d-pixar`, `watercolor`, `comic-book`, etc. Ignored when using templates. |
| captionStyleId | string | No | `wrap-1` (default), `hormozi`, `classic`, `karaoke`, `box`, `minimal`, `handwritten`, `neon`. Create custom styles in the dashboard. |
| captionsEnabled | boolean | No | Default: true |
| captionPosition | string | No | `bottom` (default), `center`, `top` |
| expectedDurationSeconds | number | No | Target length in seconds (15-420). Required for idea mode. Max 420 (7 minutes). |
| templateId | string | No | `skeleton` or `character`. When using a template, do NOT send mediaType, imageStyleId, or imageQuality. The template handles these automatically. |
| videoQuality | string | No | For video mediaType: `basic`, `good` (default), `premium` |

### GET /videos

List your videos. Returns array sorted newest first.

| Param | Type | Description |
|-------|------|-------------|
| limit | number | Max results, 1-100. Default: 50 |

### GET /videos/{id}

Get a single video by ID. Use for polling generation and export status.

### GET /subscription

Check your plan and credit balance. Returns `{ plan, status, credits, monthlyCredits }`.

### POST /exports

Export a completed video to MP4. Free, but requires an active paid subscription.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| videoId | string | Yes | Video ID (must have status: completed) |
| resolution | string | No | `1080p` (default) or `4k` |

### GET /exports/download

Get a temporary download URL for a rendered MP4.

| Param | Type | Description |
|-------|------|-------------|
| videoId | string | Finds the latest completed export for this video |

The returned URL expires in 2 minutes. Download immediately.

## Credit Costs

| Operation | Cost |
|-----------|------|
| Image (basic) | 1 credit/image |
| Image (good) | 3 credits/image |
| Image (premium) | 9 credits/image |
| Image (max) | 45 credits/image |
| Audio narration | ~50 credits/minute |
| Video clip (4s) | 75 credits |
| Video clip (8s) | 150 credits |
| Export to MP4 | Free |

A typical 60-second video with basic image quality costs approximately 75 credits.

## Error Handling

| HTTP Status | Meaning |
|-------------|---------|
| 401 | Missing or invalid API key |
| 402 | Not enough credits. Response includes `creditsRequired` and `creditsAvailable` |
| 403 | Feature requires an active paid subscription |
| 404 | Resource not found |
| 400 | Bad request (check error message for details) |

## Full Example (bash)

```bash
# 1. Check credits
curl -s "https://app.aituber.app/api/v1/subscription" \
  -H "Authorization: Bearer $AITUBER_API_KEY" | jq .

# 2. Browse voices
curl -s "https://app.aituber.app/api/v1/voices?gender=female&useCase=narration" | jq '.[0:3]'

# 3. Generate video
VIDEO_ID=$(curl -s -X POST "https://app.aituber.app/api/v1/videos/generate" \
  -H "Authorization: Bearer $AITUBER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "script": "Did you know that octopuses have three hearts and blue blood?",
    "voiceId": "EXAVITQu4vr4xnSDxMaL",
    "imageStyleId": "cinematic",
    "aspectRatio": "9:16"
  }' | jq -r '.videoId')

echo "Video ID: $VIDEO_ID"

# 4. Poll until completed
while true; do
  STATUS=$(curl -s "https://app.aituber.app/api/v1/videos/$VIDEO_ID" \
    -H "Authorization: Bearer $AITUBER_API_KEY" | jq -r '.status')
  echo "Status: $STATUS"
  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then break; fi
  sleep 10
done

# 5. Export to MP4
curl -s -X POST "https://app.aituber.app/api/v1/exports" \
  -H "Authorization: Bearer $AITUBER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"videoId\": \"$VIDEO_ID\"}"

# 6. Poll export status
while true; do
  EXPORT_STATUS=$(curl -s "https://app.aituber.app/api/v1/videos/$VIDEO_ID" \
    -H "Authorization: Bearer $AITUBER_API_KEY" | jq -r '.exportStatus')
  echo "Export: $EXPORT_STATUS"
  if [ "$EXPORT_STATUS" = "completed" ] || [ "$EXPORT_STATUS" = "failed" ]; then break; fi
  sleep 10
done

# 7. Download
DOWNLOAD_URL=$(curl -s "https://app.aituber.app/api/v1/exports/download?videoId=$VIDEO_ID" \
  -H "Authorization: Bearer $AITUBER_API_KEY" | jq -r '.url')

curl -L -o video.mp4 "$DOWNLOAD_URL"
echo "Downloaded: video.mp4"
```
