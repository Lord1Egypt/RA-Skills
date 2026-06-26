---
name: 赛博鲁班日记
description: AI diary service - push diary entries, query diaries, get AI analysis and cover images via HTTP API.
metadata: {"openclaw":{"emoji":"📔","requires":{"bins":["curl","jq"],"env":["AI_DIARY_TOKEN"]},"primaryEnv":"AI_DIARY_TOKEN"}}
---

# 赛博鲁班日记

An AI-powered diary service. Push diary entries, retrieve them by date, get AI-generated analysis (feedback + keywords), and fetch cover images.

## Setup

1. Click the link below to authorize with Feishu and get your API token (long-lived, no expiration):

   https://image.yezishop.vip/api/openclaw/auth-redirect

2. After Feishu login, copy the token displayed on the page.

3. Set the token as an environment variable:

```bash
export AI_DIARY_TOKEN="your_token_here"
```

## Usage

### Push a diary entry

When the user wants to save or push a diary entry for a specific date:

```bash
curl -s -X POST "https://image.yezishop.vip/api/diary-hook/$AI_DIARY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"date\": \"$DATE\", \"content\": \"$CONTENT\"}" | jq .
```

- `date` must be in `YYYY-MM-DD` format
- `content` is the diary text

### Get diary by date

When the user asks about a specific date's diary:

```bash
curl -s "https://image.yezishop.vip/api/diary-hook/$AI_DIARY_TOKEN/diaries?date=$DATE" | jq .
```

### List recent diaries

When the user wants to see recent diary entries:

```bash
curl -s "https://image.yezishop.vip/api/diary-hook/$AI_DIARY_TOKEN/diaries?limit=$LIMIT&offset=$OFFSET" | jq .
```

- `limit` defaults to 20, `offset` defaults to 0

### Get a single diary by ID

```bash
curl -s "https://image.yezishop.vip/api/diary-hook/$AI_DIARY_TOKEN/diaries/$DIARY_ID" | jq .
```

### Analyze a diary (AI feedback + keywords)

When the user wants AI analysis of a diary entry. Returns cached result if analysis already exists:

```bash
curl -s -X POST "https://image.yezishop.vip/api/diary-hook/$AI_DIARY_TOKEN/diaries/$DIARY_ID/analyze" \
  -H "Content-Type: application/json" | jq .
```

Response includes `feedback` (text review) and `keywords` (3 key terms).

### Get diary cover image

```bash
curl -s "https://image.yezishop.vip/api/diary-hook/$AI_DIARY_TOKEN/diaries/$DIARY_ID/image" | jq .
```

Returns `image` field with the image URL, or `null` if no image exists.

## Response Format

All endpoints return JSON with `success: true/false`. Diary objects contain:

- `id` - Diary ID
- `diary_date` - Date in YYYY-MM-DD format
- `content` - Diary text content
- `feedback` - AI analysis feedback (after analyze)
- `keywords` - Array of 3 keywords (after analyze)
- `cover_image` - Cover image URL (if generated)
- `hook_content` - Content pushed via webhook
- `status` - Processing status

## Important Notes

- The API token is tied to your Feishu account. Keep it secure.
- To reset your token, log in to the web app and regenerate it in diary settings.
- The analyze endpoint may take a few seconds on first call as it invokes an AI model. Subsequent calls return cached results instantly.
