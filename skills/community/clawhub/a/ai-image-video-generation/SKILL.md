---
name: vibevideo-generate
description: Generate images and videos using the VibeVideo API. Use when the user
  asks to create AI images or videos, check generation status, list available models,
  or calculate credit costs.
homepage: https://vibevideo.app
metadata: {"clawdbot":{"requires":{"bins":["curl"],"env":["VIBEVIDEO_API_KEY"]},"primaryEnv":"VIBEVIDEO_API_KEY","env":[{"name":"VIBEVIDEO_API_KEY","description":"API key for the VibeVideo API.","required":true,"sensitive":true}]}}
---

# VibeVideo Generation Skill

## Prerequisites

- Environment variable `VIBEVIDEO_API_KEY` must be set with a valid API key
- Get your API key from: **Dashboard → Settings → API Keys**

## API Endpoint

This skill always uses the official VibeVideo API endpoint: `https://vibevideo.app`

## Generate Image

Create an image generation task:

```bash
curl -s -X POST https://vibevideo.app/api/ai/generate \
  -H "Authorization: Bearer $VIBEVIDEO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "mediaType": "image",
    "scene": "text-to-image",
    "model": "nano-banana-2",
    "prompt": "A cat sitting on a rainbow",
    "options": {
      "aspect_ratio": "1:1",
      "quality": "2K"
    }
  }'
```

For image-to-image, set `"scene": "image-to-image"` and add `"image_url": "..."` in options.

Response:
```json
{ "code": 0, "data": { "id": "task_id", "status": "pending", "taskId": "...", "costCredits": 5 } }
```

## Generate Video

Create a video generation task:

```bash
curl -s -X POST https://vibevideo.app/api/ai/generate \
  -H "Authorization: Bearer $VIBEVIDEO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "mediaType": "video",
    "scene": "text-to-video",
    "model": "seedance-2-0",
    "prompt": "A dog playing in a park",
    "options": {
      "resolution": "720p",
      "duration": "5s",
      "aspect_ratio": "16:9"
    }
  }'
```

For image-to-video, set `"scene": "image-to-video"` and add `"image_url": "..."` in options.
For frames-to-video, add `"start_image_url": "..."` and `"end_image_url": "..."` in options.

## Query Task Status

Tasks are asynchronous. Poll until status is `success`, `failed`, or `canceled`:

```bash
curl -s -X POST https://vibevideo.app/api/ai/query \
  -H "Authorization: Bearer $VIBEVIDEO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "taskId": "YOUR_TASK_ID" }'
```

Response includes `status`, `taskInfo`, `taskResult`, and `taskUrls` (JSON string of media URLs).

## Calculate Cost

Check credit cost before generating:

```bash
curl -s -X POST https://vibevideo.app/api/ai/cost \
  -H "Authorization: Bearer $VIBEVIDEO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedance-2-0",
    "mediaType": "video",
    "scene": "text-to-video",
    "options": { "resolution": "720p", "duration": "5s" }
  }'
```

## Cancel Task

```bash
curl -s -X DELETE https://vibevideo.app/api/ai/tasks/YOUR_TASK_ID \
  -H "Authorization: Bearer $VIBEVIDEO_API_KEY"
```

## Workflow

1. If the user doesn't specify a model, pick the default for the scene (see tables below)
2. Call the generate endpoint
3. Poll the query endpoint every 5 seconds until status is terminal (`success`/`failed`/`canceled`)
4. Parse `taskUrls` from the response and report the media URL(s) to the user
5. If `code` is not 0, handle the error (see Error Handling below)

## Image Models

| ID | Label | Vendor | Scenes | Qualities |
|----|-------|--------|--------|-----------|
| nano-banana-2 | Nano Banana 2 | Google | text-to-image, image-to-image | 1K, 2K, 4K |
| gpt-image-1-5 | GPT Image 1.5 | OpenAI | text-to-image, image-to-image | Medium, High |
| grok-imagine | Grok Imagine | Grok | text-to-image, image-to-image | — |
| seedream-5-0 | Seedream 5.0 | ByteDance | text-to-image, image-to-image | Basic, High |
| qwen-image | Qwen Image | Qwen | text-to-image, image-to-image | — |
| wan-2-7-image | Wan 2.7 Image | Qwen/Alibaba | text-to-image, image-to-image | 1K, 2K |
| wan-2-7-image-pro | Wan 2.7 Image Pro | Qwen/Alibaba | text-to-image, image-to-image | 1K, 2K, 4K |

Default for `text-to-image`: **nano-banana-2**

## Video Models

| ID | Label | Vendor | Scenes | Resolutions | Durations |
|----|-------|--------|--------|-------------|-----------|
| seedance-2-0 | Seedance 2.0 | ByteDance | text-to-video, image-to-video, frames-to-video, reference-to-video | 720p, 1080p | 5s, 10s, 15s |
| seedance-2-0-fast | Seedance 2.0 Fast | ByteDance | text-to-video, image-to-video, frames-to-video, reference-to-video | 720p, 1080p | 5s, 10s, 15s |
| seedance-1-5-pro | Seedance 1.5 Pro | ByteDance | text-to-video, image-to-video | 480p, 720p, 1080p | 4s, 8s, 12s |
| grok-imagine | Grok Imagine | Grok | text-to-video, image-to-video | 480p, 720p | 6s, 10s, 15s |
| kling-2-6 | Kling 2.6 | Kling | text-to-video, image-to-video | — | 5s, 10s |
| runway | Runway | Runway | text-to-video, image-to-video | 720p, 1080p | 5s, 10s |
| veo-3-1 | Veo 3.1 | Google | text-to-video, image-to-video, frames-to-video, reference-to-video | 720p, 1080p, 4k | — |
| veo-3-1-fast | Veo 3.1 Fast | Google | text-to-video, image-to-video, frames-to-video, reference-to-video | 720p, 1080p, 4k | — |
| seedence-1-0-pro | Seedence 1.0 Pro | ByteDance | text-to-video, image-to-video | 480p, 720p, 1080p | 5s, 10s |
| seedence-1-0-pro-fast | Seedence 1.0 Pro Fast | ByteDance | image-to-video | 720p, 1080p | 5s, 10s |
| seedence-1-0-lite | Seedence 1.0 Lite | ByteDance | text-to-video, image-to-video | 480p, 720p, 1080p | 5s, 10s |

Default for `text-to-video`: **seedance-2-0**

## Error Handling

- **`code: -1` with "no auth"**: User's API key is missing or invalid. Remind them to set `VIBEVIDEO_API_KEY`.
- **`code: -1002` with "insufficient credits"**: User needs to purchase credits at VibeVideo dashboard.
- **`code: -1` with "invalid"**: Wrong model ID, scene, or mediaType. Check against the model tables above.
- **Task stuck in "processing"**: Polling timeout. The task may still complete — suggest the user wait and query again later.

## API Response Envelope

All endpoints return:
```json
{ "code": 0, "message": "ok", "data": { ... } }
```

`code: 0` means success. Non-zero `code` means error (check `message`).
