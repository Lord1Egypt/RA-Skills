---
name: chenyu-aigc
description: >
  Generate AI videos and images via Chenyu Studio AIGC API.
  Supports text-to-video, image-to-video, video extension, style transfer, and AI image generation.
  Trigger when: generate video, create AI video, text to video, image to video,
  AI image generation, video generation, 生成视频, AI视频, 文生视频, 图生视频, 生成图片.
version: 1.0.4
metadata:
  openclaw:
    requires:
      env:
        - CHENYU_API_KEY
        - CHENYU_BASE_URL
      bins:
        - curl
        - jq
        - uuidgen
        - base64
    primaryEnv: CHENYU_API_KEY
    emoji: "\U0001F3AC"
    os:
      - darwin
      - linux
---

# Chenyu AIGC - AI Video & Image Generation

Generate videos and images using AI models through the Chenyu Studio AIGC orchestration API.

## When to Use

- User wants to generate a video from text prompt
- User wants to generate a video from an image (first/last frame)
- User wants to extend or remix a video
- User wants to generate AI images
- User wants to check status of a generation task
- User wants to list available AI models

## When NOT to Use

- User wants to analyze or understand existing videos (use video-analysis skill)
- User wants to download videos from social platforms (use video-fetch skill)
- User wants to manage digital humans or clone voices (use chenyu-core skill)

## Authentication

```
Authorization: Bearer $CHENYU_API_KEY
```

Base URL: `$CHENYU_BASE_URL` (default: `https://chenyu.pro`)

## Workflow

1. **Discover recipes** — list available AI models (see below)
2. **Get recipe schema** — check what inputs/parameters the recipe accepts
3. **Execute** — submit a generation task → see [execute-recipe.md](execute-recipe.md)
4. **Poll & manage** — track status, get output, cancel → see [manage-tasks.md](manage-tasks.md)

## Step 1: List Available Recipes

```bash
curl -s "$CHENYU_BASE_URL/api/v1/aigc/recipes" \
  -H "Authorization: Bearer $CHENYU_API_KEY" | jq '.data[] | {recipe_id, name, slug, description, output_type}'
```

Each recipe represents an AI model capability. Key response fields:
- `recipe_id` — use this ID when executing
- `slug` — human-readable identifier (e.g. `volcengine-seedance-v1-pro`)
- `output_type` — what it produces: `video`, `image`, `audio`

## Step 2: Get Recipe Schema

```bash
curl -s "$CHENYU_BASE_URL/api/v1/aigc/recipes/{recipe_id}/schema" \
  -H "Authorization: Bearer $CHENYU_API_KEY" | jq '.data'
```

The schema tells you:
- `typed_inputs_schema.definitions` — accepted input types and their fields
- `parameters_schema` — available parameters with constraints (min/max/enum)
- `credit_cost` / `credit_cost_rules` — how many credits it costs

After getting the schema, read [execute-recipe.md](execute-recipe.md) for execution details.
