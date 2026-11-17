# AIVideoMaker API Reference (Aligned with `ApiV1Docs.tsx`)

## Base URL

- `https://aivideomaker.ai`

## Authentication

All requests require header:

- `key: <AIVIDEO_API_KEY>`

For direct REST calls, keep the key in `AIVIDEO_API_KEY`. The installed skill also supports the private credentials file created by `scripts/connect.mjs`; the client loads it automatically. Never put real keys in examples, URLs, analytics, or logs. API credits are distinct from consumer website subscriptions; a website plan does not provide unlimited API usage. The first API key created by an account receives 50 introductory API credits.

## MiniMax H3 pricing

One API credit is USD $0.01. MiniMax H3 costs $0.03/second at 720p Turbo, $0.04/second at 720p Base or 1080p Turbo, and $0.05/second at 1080p Base. A 5-second 720p Turbo clip costs 15 credits ($0.15); a 10-second clip costs 30 credits ($0.30). A request that includes `referenceVideoUrl` adds a flat 2 API credits. The quote endpoint is authoritative for a specific request.

## Endpoints

### 1) Check setup and balance

- `GET /api/v1/account`
- Non-billable. Returns the current balance, key limits, credit warning, API version, skill version, and supported models.

### 2) Quote a generation

- `POST /api/v1/quote/{model}`
- Send the same JSON payload as generation.
- Non-billable. Returns `credits`, `listPriceUsd`, `currentBalance`, `affordable`, and `billable: false`.

### 3) Create generation task

- `POST /api/v1/generate/{model}`
- Models: MiniMax H3 (`minimax`), Seedance 2.0 (`seedance20`), Wan 3.0 (`wan30`), HappyHorse 1.1 (`happyhorse`)
- Legacy identifiers: `t2v`/`i2v` use MiniMax H3 720p Turbo; `t2v_v3`/`i2v_v3` use MiniMax H3 1080p Turbo. Use `minimax` for new H3 requests. Legacy fields and duration restrictions remain unchanged.
- Send a stable `Idempotency-Key` header (8–128 characters) for every logical generation.
- Send `X-Max-Credits` with the caller-approved maximum. The server rejects a higher quote before billing.
- Retrying the same request with the same idempotency key returns the original task without charging again. Different inputs with the same key return HTTP 409.

#### Model parameters

##### `t2v` (MiniMax H3 · 720p Turbo · legacy text)

- `prompt`: string, required
- `aspectRatio`: `16:9` | `9:16` | `1:1`, required
- `duration`: `5` | `8`, required
- Credits: `duration * 3`

##### `i2v` (MiniMax H3 · 720p Turbo · legacy image)

- `image`: string (public image URL or `data:image/...;base64,...`), required
- `prompt`: string | null, optional
- `duration`: `5` | `8`, required
- Credits: `duration * 3`

##### `minimax` (MiniMax H3)

- `content`: string, required
- `imageUrl`: string or null, optional (first-frame image URL or image data URI)
- `lastFrameUrl`: string or null, optional (last-frame image URL or image data URI)
- `referenceImageUrls`: string[], optional, max 4 image URLs or image data URIs
- `referenceVideoUrl`: string or null, optional, public video URL (adds a flat 2 credits)
- `referenceAudioUrls`: string[], optional, max 2 public audio URLs
- `aspectRatio`: `auto` | `21:9` | `16:9` | `4:3` | `1:1` | `3:4` | `9:16`, optional, default `16:9`
- `duration`: number, optional, 5–20 seconds, default `5`
- `resolution`: `720p` | `1080p`, optional, default `720p` (480p is not supported)
- `tier`: `turbo` | `base`, optional, default `turbo`
- Frame inputs and reference assets are mutually exclusive.
- Credits: `duration * (3 for 720p or 4 for 1080p)`, plus `duration * 1` when `tier=base`, plus a flat `2` when `referenceVideoUrl` is set

##### `t2v_v3` (MiniMax H3 · 1080p Turbo · legacy text)

- `prompt`: string, required
- `aspectRatio`: `16:9` | `9:16` | `1:1`, required
- `duration`: `5` | `10` | `15` | `20`, required
- Credits: `duration * 4`

##### `i2v_v3` (MiniMax H3 · 1080p Turbo · legacy image)

- `image`: string (public image URL or `data:image/...;base64,...`), required
- `prompt`: string | null, optional
- `duration`: `5` | `10` | `15` | `20`, required
- Credits: `duration * 4`

##### `seedance20` (Seedance 2.0)

- `prompt`: string | null, optional\*
- `image`: string | null, optional\* (reference image URL)
- `video`: string | null, optional\* (reference video URL)
- `audio`: string | null, optional\* (reference audio URL, cannot be used alone)
- `duration`: 4–15 (number), required
- `resolution`: `480` | `720` (number), required
- `ratio`: `16:9` | `9:16` | `1:1`, required
- \*At least one of prompt, image, or video is required. Audio only alongside prompt/image/video.
- Credits: calculated dynamically from resolution, aspect ratio, and output duration. Use the quote endpoint for the authoritative charge.

##### `wan30` (Wan 3.0)

- `prompt`: string, required
- `image`: string | null, optional (i2v if provided, t2v otherwise)
- `duration`: `5` | `10` | `15` (string), required
- `resolution`: `480P` | `720P` | `1080P`, required
- `ratio`: `16:9` | `9:16` | `1:1` | `4:3` | `3:4`, required
- `promptExtend`: boolean, optional (default: false)
- Credits: `duration * 8` (480P) / `duration * 15` (720P) / `duration * 30` (1080P)

##### `happyhorse` (HappyHorse 1.1)

- `prompt`: string, required
- `image`: string | string[] | null, optional (single image=i2v, multiple=r2v, null=t2v)
- `duration`: 3–15 (number), required
- `resolution`: `720P` | `1080P`, required
- `ratio`: `16:9` | `9:16` | `3:4` | `4:3` | `1:1` | null, optional (default: `16:9`, not used in i2v)
- Credits: `duration * 25` (720P) / `duration * 50` (1080P)

## Image input note

- Skill contract accepts both public image URLs and `data:image/...;base64,...` for image inputs.
- Prefer `data:image/...;base64,...` in OpenClaw to avoid unreachable URL issues.
- Backend uploads base64 image to R2 first.
- Task input stored in `/api/v1/tasks/{taskId}` keeps the R2 URL instead of the full base64 string.

#### Raw API success response (from docs)

```json
{
  "status": "SUBMITTED",
  "taskId": "ckxxxxxxxx",
  "creditsCharged": 15,
  "idempotentReplay": false,
  "responseUrl": "https://aivideomaker.ai/api/v1/tasks/ckxxxxxxxx",
  "statusUrl": "https://aivideomaker.ai/api/v1/tasks/ckxxxxxxxx/status",
  "cancelUrl": "https://aivideomaker.ai/api/v1/tasks/ckxxxxxxxx/cancel"
}
```

#### Raw API error response (from docs)

```json
{
  "status": "FAILED",
  "errorCode": "INSUFFICIENT_CREDITS",
  "message": "Insufficient credits"
}
```

### 4) List tasks

- `GET /api/v1/tasks`
- Returns all tasks for current API key, newest first

#### Raw API response example (from docs)

```json
{
  "tasks": [
    {
      "id": "ckxxxxxxxx",
      "createdAt": "2026-03-19T08:00:00.000Z",
      "model": "t2v",
      "input": { "prompt": "...", "aspectRatio": "16:9" },
      "output": null,
      "status": "PROGRESS",
      "completedAt": null
    }
  ]
}
```

### 5) Get task details

- `GET /api/v1/tasks/{taskId}`
- Returns full task data: input, output, status, completion time

Completed task example:

```json
{
  "id": "ckxxxxxxxx",
  "model": "minimax",
  "input": {
    "content": "A cinematic close-up of a candle on a wooden table.",
    "duration": 5,
    "resolution": "720p",
    "tier": "turbo",
    "aspectRatio": "16:9"
  },
  "output": {
    "url": "https://example.com/generated-video.mp4",
    "msg": "The file will only be saved for 24 hours, please download it promptly."
  },
  "status": "COMPLETED",
  "completedAt": "2026-09-05T12:00:00.000Z"
}
```

### 6) Get task status

- `GET /api/v1/tasks/{taskId}/status`
- Returns only current status; suitable for polling

#### Raw API response example (from docs)

```json
{
  "status": "COMPLETED"
}
```

### 7) Cancel task

- `PUT /api/v1/tasks/{taskId}/cancel`
- Only works when task status is still `SUBMITTED`

## Task status values

- `SUBMITTED`
- `PROGRESS`
- `COMPLETED`
- `FAILED`
- `CANCEL`

## Rate limiting

- Task query endpoints are limited to `60 requests/minute/IP`
- Exceeded limit returns HTTP `429` with `Retry-After` header
- Generation also enforces the API key's configured requests-per-minute and daily-credit limits.
- Configure daily credits, generation RPM, and the low-credit warning from **Account → API Keys → Limits**. Use `-1` for unlimited.

## Note on Skill runtime output

The scripts in this skill wrap raw API responses into a normalized shape for automation (`ok`, `errorCode`, `httpStatus`, etc.), but the raw endpoint contract above is copied from `ApiV1Docs.tsx`.

- Exit `0`: requested operation succeeded
- Exit `1`: validation, API, terminal job, or output-retrieval failure
- Exit `2`: polling timed out; use the returned `taskId` to resume without creating a duplicate
- Debug diagnostics are written to stderr. Structured JSON is written to stdout.
