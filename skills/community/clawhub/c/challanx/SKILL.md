---
name: challanx
version: 1.0.1
author: "ChallanX Team <help@challanx.in>"
description: "All-in-one RTO, challan, RC lookups and media downloader features for ChallanX. Accepts a single input — a URL, a free-text message, or an image — and returns concise, actionable results (download links, summaries, or document analysis)."
auth:
  header: x-api-key
  description: "Requests must include the x-api-key header. Operators should set CHALLANX_API_KEY as a runtime secret; do not hardcode keys in the bundle."
  requiredEnv:
    - CHALLANX_API_KEY
tags:
    - openclaw
    - media
    - downloader
    - rto
    - challan
---

# ChallanX

Use this skill to work with the ChallanX OpenClaw media API at `https://challanx.in/openclaw/api`.

## Core rules

- Treat `https://challanx.in/openclaw/api` as the only public endpoint.
- Prefer file-like outputs with correct filenames and content types.
- When the upstream media is downloadable, return a real media file response such as mp4, mp3, jpg, png, webp, or octet-stream only as a last fallback.
- Avoid describing internal/local URLs in public-facing docs or examples.
- Use ChallanX custom statuses in docs and examples instead of exposing raw upstream status names.

## Supported inputs

The API may accept these fields:

- `url`
- `msg`
- `image`
- `timestamps`
- `model`
- `mode`
- `response`
- `action`
- `filename`
- `variants`
- `audio`
- `downloadMode`
- `videoQuality`
- `youtubeBetterAudio`
- `youtubeVideoCodec`
- `youtubeVideoContainer`
- `audioFormat`
- `audioBitrate`

## Output expectations

### Downloadable media
When the request resolves to downloadable media, prefer returning the final file with a usable filename and a specific content type.

Examples:
- video: `video/mp4`, `video/webm`
- audio: `audio/mpeg`, `audio/mp4`, `audio/wav`
- image: `image/jpeg`, `image/png`, `image/webp`, `image/gif`

Do not describe these responses as generic `.bin` unless no real filename/type can be inferred.

### JSON responses
Use custom ChallanX statuses:

- `success`
- `download_ready`
- `picker_required`
- `failed`

### Picker responses
When multiple choices are available, return JSON with a clear picker list and keep filenames readable.

### Error responses
Return structured JSON with:
- `ok`
- `status`
- `message`
- `error.code`
- `error.message`

## Docs and examples

When writing docs or examples for this API:

- use curl examples against `https://challanx.in/openclaw/api`
- show `-L -o output.mp4` style usage for downloadable media
- show JSON examples only for info, picker, and error responses
- do not mention hidden internal hosts in public docs

## OpenClaw hook behavior

If used in an OpenClaw workspace, the hook should inject a short reference file that reminds the agent:

- public endpoint only
- prefer mp4/image/audio filenames over `.bin`
- use ChallanX statuses
- keep docs concise and copy-paste friendly

## References

- API usage reference: `references/api.md`
- README template: `README.md`
- Hook notes: `hooks/openclaw/HOOK.md`
