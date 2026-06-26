---
name: filtrix-video-gen
description: Generate videos through Filtrix Remote MCP. Use when users ask for text-to-video, image-to-video, video task polling, or downloading completed videos with generate_video_text, generate_video_image, and get_video_status.
---

# Filtrix Video Gen (MCP)

This skill is MCP-only.

- Endpoint: `https://mcp.filtrix.ai/mcp`
- Auth: `Authorization: Bearer <FILTRIX_MCP_API_KEY>`
- Primary tools:
  - `generate_video_text`
  - `generate_video_image`
  - `get_video_status`

## Setup

Required:
- `FILTRIX_MCP_API_KEY`

Optional:
- `FILTRIX_MCP_URL` (default: `https://mcp.filtrix.ai/mcp`)

## Generate Video (Text)

```bash
python scripts/generate.py \
  --mode text-to-video \
  --prompt "a cinematic drone shot over a neon city at night" \
  [--aspect-ratio 16:9] \
  [--idempotency-key KEY] \
  [--wait] \
  [--poll-interval 8] \
  [--timeout 600] \
  [--output /tmp/video.mp4]
```

Default behavior submits a request and prints `request_id`.
Add `--wait` to poll until completion and download the final video.

## Generate Video (Image-to-Video)

Grok Imagine:

```bash
python scripts/generate.py \
  --mode grok-imagine \
  --prompt "camera slowly pushes in, fog drifting" \
  --image-path /path/to/input.png \
  --duration-seconds 6 \
  [--aspect-ratio 16:9] \
  [--wait]
```

Seedance 1.5 Pro:

```bash
python scripts/generate.py \
  --mode seedance-1-5-pro \
  --prompt "soft cinematic motion, subject turns to camera" \
  --image-url https://... \
  --duration-seconds 8 \
  [--aspect-ratio 16:9] \
  [--wait]
```

Notes:
- Grok duration: `6` or `15`
- Seedance duration: `5`, `8`, `10`, `12`
- Seedance in MCP has audio fixed to `on`

## Check Status

```bash
python scripts/status.py \
  --request-id YOUR_REQUEST_ID \
  [--download] \
  [--output /tmp/video.mp4]
```

## Idempotency

`idempotency_key` prevents duplicate billing on retries.
If omitted, scripts auto-generate one UUID-based key.

## References

- [MCP Tools Reference](references/mcp-tools.md)
- [Video Prompt Guide](references/prompts.md)
