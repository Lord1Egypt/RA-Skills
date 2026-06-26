# MCP Tools Reference

Filtrix MCP endpoint:

- URL: `https://mcp.filtrix.ai/mcp`
- Auth header: `Authorization: Bearer <FILTRIX_MCP_API_KEY>`

This page documents video-related MCP tools and typical outputs.

## Tools

### `get_account_credits`

Purpose: query current account credits and subscription status.

Input arguments:

- none

Typical output:

- `ok` boolean
- `credits` number
- `tier` string or null
- `status` string or null

Example `tools/call` arguments:

```json
{}
```

### `generate_video_text`

Purpose: start text-to-video generation task.

Input arguments:

- `prompt` required, string, `1..4000`
- `aspect_ratio` optional, string, default `16:9`
- `idempotency_key` required, string, `8..128`

Typical output:

- `ok` boolean
- downstream task payload from video backend
  - usually includes `request_id` and a status/state field

Example `tools/call` arguments:

```json
{
  "prompt": "a drone shot over neon city at night",
  "aspect_ratio": "16:9",
  "idempotency_key": "vid-001-demo"
}
```

### `generate_video_image`

Purpose: start image-to-video generation task.

Input arguments:

- `prompt` required, string, `1..4000`
- `mode` optional, enum, default `seedance-1-5-pro`
  - `grok-imagine`
  - `seedance-1-5-pro`
- `image_url` optional, string URL
- `image_base64` optional, string, raw base64 or `data:image/...;base64,...`
- `image_mime_type` optional, string
  - used when `image_base64` is raw base64; example `image/png`
- `aspect_ratio` optional, string, default `16:9`
- `duration_seconds` required in practice for deterministic behavior
  - Grok: `6` or `15`
  - Seedance: `5`, `8`, `10`, `12`
- `idempotency_key` required, string, `8..128`

Rules:

- Must provide exactly one of `image_url` or `image_base64`.
- Seedance audio is fixed `on` in MCP (no `generate_audio` argument).

Typical output:

- `ok` boolean
- downstream task payload from video backend
  - usually includes `request_id` and a status/state field
- echoed fields:
  - `model`
  - `duration_seconds`
  - `aspect_ratio`
  - `generate_audio` (for Seedance, always `true`)

Example `tools/call` arguments (Grok):

```json
{
  "prompt": "slow camera push in, cinematic lighting",
  "mode": "grok-imagine",
  "image_url": "https://example.com/input.png",
  "aspect_ratio": "16:9",
  "duration_seconds": 6,
  "idempotency_key": "vid-i2v-grok-001"
}
```

Example `tools/call` arguments (Seedance):

```json
{
  "prompt": "gentle motion and parallax, subject breathing naturally",
  "mode": "seedance-1-5-pro",
  "image_base64": "<raw-base64>",
  "image_mime_type": "image/png",
  "aspect_ratio": "16:9",
  "duration_seconds": 8,
  "idempotency_key": "vid-i2v-seedance-001"
}
```

### `get_video_status`

Purpose: query status for a previously created video request.

Input arguments:

- `request_id` required, string

Typical output:

- `ok` boolean
- downstream status payload from video backend
  - may include `status` and downloadable `video_url` when complete

Example `tools/call` arguments:

```json
{
  "request_id": "your-request-id"
}
```

## Idempotency Rules

- Reusing the same `idempotency_key` for the same user and same feature prevents duplicate billing.
- Duplicate replay normally returns an `already_deducted` style response (often mapped to HTTP `409` downstream).
- New generation intent should use a new `idempotency_key`.

## Common Error Patterns

- `401 Unauthorized`: invalid or revoked MCP API key
- `402`: insufficient credits
- `409`: duplicate `idempotency_key`
- `400`: invalid tool arguments
