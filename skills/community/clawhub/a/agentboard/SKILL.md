---
name: agentboard
description: Build multi-panel storyboards programmatically — create projects, upload images/audio to boards, composite annotations, export PDFs, share via public URL. Invoke when the user wants a storyboard, pre-visualization, shot breakdown, animatic, or any ordered sequence of visual panels with text. Hosted at https://agentboard.fly.dev. Works over REST from any agent; MCP tools (mcp__agentboard__*) available in compatible runtimes. If you have your own image/audio generator, use it and UPLOAD the bytes — optional server-side generation endpoints exist as a fallback only for agents without built-in generation.
---

# AgentBoard

Base URL: `https://agentboard.fly.dev`. All examples below use REST. MCP tools accept the same argument shapes — same field names, same JSON structure. No client credentials are required to call the hosted endpoints.

## Data model

- **Project** — UUID, `aspectRatio` (default 1.7777), ordered list of **boards**.
- **Board** — 5-char `uid`, `dialogue`, `action`, `notes`, `duration` (ms), up to 6 layers (`fill` is primary; others: `tone`, `pencil`, `ink`, `reference`, `notes`).
- **Layer asset** — one image per `(board, layer)`. Re-upload replaces.
- **Audio asset** — one audio per `(board, kind)`. Kinds: `narration`, `sfx`, `music`, `ambient`, `reference`. Multiple kinds per board allowed.

## Workflow

```
1. create project + boards (one call)
2. populate: upload OR generate images/audio
3. (optional) annotate via draw_shapes
4. (optional) export PDF and/or get share URL
```

## 1. Create project

```json
POST /api/agent/create-project
{
  "title": "The Lighthouse Keeper",
  "aspectRatio": 1.7777,
  "boards": [
    { "dialogue": "...", "action": "...", "duration": 4000 },
    { "dialogue": "...", "action": "...", "duration": 3500 }
  ]
}
→ { id, project: { boards: [{ uid, number, ... }] }, viewUrl }
```
Save `id` and every board's `uid` from the response. Rate-limited: 50 creates/hour per IP+token.

## 2. Populate boards — upload your own bytes (PREFERRED)

Use this path if your runtime has image/audio generation (fal, Sora, Veo, Midjourney, Gemini, etc.). Generate with your tool, then upload. Skip to the **Fallback generation** section only if you can't generate.

### Batch upload (3+ panels)

```json
POST /api/agent/upload-batch
{
  "projectId": "...",
  "uploads": [
    { "boardUid": "ABC", "kind": "image", "imageBase64": "..." },
    { "boardUid": "DEF", "kind": "image", "imageBase64": "..." },
    { "boardUid": "ABC", "kind": "audio", "audioKind": "narration", "audioBase64": "..." }
  ]
}
→ 201 (all ok) or 207 Multi-Status { succeeded: [...], failed: [{ index, error }] }
```

Up to 100 items per call, mixing images and audio freely. Partial failures don't abort the batch.

**MCP `upload_assets_batch`** supports three input modes per item. **Always prefer path/url over base64** — they cost zero agent context:

| Field | What | Use for |
|---|---|---|
| `imagePath` / `audioPath` | Local file path | Preferred when the user has explicitly produced or pointed at a file. MCP subprocess reads and uploads the bytes. Never reference paths the user didn't authorize. |
| `imageUrl` / `audioUrl` | http/https URL | Remote CDN links (the MCP subprocess fetches them). Zero agent context cost. |
| `imageBase64` / `audioBase64` | Inline base64 | Only for tiny images (<10 KB). Burns agent context at 1.33× file size. |

### Single upload

```json
POST /api/agent/draw
{ "projectId":"...", "boardUid":"...", "layer":"fill", "imageBase64":"...", "mime":"image/png" }

POST /api/agent/upload-audio
{ "projectId":"...", "boardUid":"...", "kind":"narration", "audioBase64":"...", "mime":"audio/mpeg" }
```

Caps: images ≤ 256 MB, audio ≤ 512 MB. Mime is sniffed from magic bytes (client-declared mime is ignored). Accepted: `image/png`, `image/jpeg`, `image/gif`, `image/webp`, `audio/mpeg`, `audio/wav`, `audio/ogg`.

## 3. Draw annotations

Composite shapes or brush strokes onto any board layer. **Unique to AgentBoard — your image generator can't do this.** Use it to annotate AI panels (circle a character, add an arrow, label a shot).

```json
POST /api/agent/draw-shapes
{
  "projectId": "...",
  "boardUid": "...",
  "layer": "fill",
  "mode": "overlay",
  "shapes": [
    { "type":"circle", "center":[0.5,0.5], "radius":0.08, "stroke":"#cc0000", "strokeWidth":6 },
    { "type":"arrow",  "from":[0.7,0.3], "to":[0.5,0.5], "stroke":"#cc0000", "strokeWidth":6 },
    { "type":"text",   "position":[0.05,0.05], "text":"HERO", "fontSize":0.04, "fill":"#cc0000" }
  ]
}
```

**Coordinates are normalized `[0, 1]`** — `(0,0)` top-left, `(1,1)` bottom-right. `radius`, `size`, `fontSize` are also normalized (`0.05` = 5% of canvas).

**Modes:** `"overlay"` (composite on existing layer — for annotating) or `"replace"` (blank canvas — for sketching).

**Shape types:**

| Type | Required fields |
|---|---|
| `line` | `from`, `to` |
| `circle` | `center`, `radius` |
| `rect` | `topLeft`, `size: [w,h]` |
| `arrow` | `from`, `to` |
| `text` | `position`, `text` |
| `polyline` | `points: [[x,y], ...]` |
| `polygon` | `points: [[x,y], ...]` |
| `bezier` | `from`, `cp1`, `cp2`, `to` |

All shapes accept `stroke`, `fill`, `strokeWidth`, `opacity`. Colors are any CSS color string.

**Freeform strokes** — `POST /api/agent/draw-strokes` with `{ brush, color, size, points: [[x,y]...] }` per stroke. Brushes: `pencil` | `pen` | `ink` | `marker` | `eraser`. Eraser removes pixels — pair with `mode:"overlay"`. Sparse point arrays get Catmull-Rom smoothed; no need to pass dense polylines.

## 4. Share + export

```
GET  /api/agent/share/{projectId}             → { viewUrl }  — public read-only HTML viewer
POST /api/agent/export/pdf { projectId }       → PDF bytes    — one page per board
POST /api/agent/share/{projectId}              → scoped share token
     body: { permission: "view|comment|edit", ttlMs: 86400000 }
```

## Editing an existing project

```json
POST /api/agent/set-metadata
{ "projectId":"...", "updates":[
  { "boardUid":"ABC", "dialogue":"new line", "expectedVersion":4 }
]}
```

Optimistic concurrency via `expectedVersion`. On 409 `VERSION_MISMATCH`: `GET /api/agent/project/{id}`, merge, retry. Asset uploads are last-write-wins and don't need `expectedVersion`.

Append boards later with `POST /api/agent/add-scene` (batch, body: `{ projectId, boards: [...] }`) or `POST /api/agent/add-board` (single).

## Optional server-side generation (skip if you can generate)

Only for agents without built-in image/audio generation. Uploading your own bytes via the primary workflow is faster and more reliable; these endpoints exist as a fallback. Any required provider configuration is handled server-side — the agent supplies only the request payload below.

| Endpoint | Purpose | Key fields |
|---|---|---|
| `POST /api/agent/generate-image` | AI image | `prompt`, `style?`, `quality?`, `model?` |
| `POST /api/agent/generate-speech` | Text-to-speech | `text`, `voice?` |
| `POST /api/agent/generate-sfx` | Sound effect | `prompt`, `durationSeconds?` (0.5–22) |
| `POST /api/agent/generate-music` | Music | `prompt`, `musicLengthMs?` (3000–600000) |

**Style presets** (pass `style`): `storyboard-sketch`, `cinematic-color`, `comic-panel`. Enumerate via `GET /api/agent/image-styles`.

**Quality tiers** (pass `quality`): `low` (draft) | `medium` (balanced default) | `high` (final render). Project-level default settable on `create-project`.

**Voice lookup** — call `GET /api/agent/voices` **before** `generate-speech` to see which voices the server is configured to use.

## Errors

Shape: `{ "error": { "code": "...", "message": "..." } }`. Retry rules:

| Code(s) | HTTP | Action |
|---|---|---|
| `BAD_REQUEST`, `BAD_BASE64`, `BAD_MIME`, `BAD_DRAW` | 400 | Fix request shape |
| `UPLOAD_TOO_LARGE` | 413 | Resize/compress (images > 256 MB, audio > 512 MB) |
| `WRONG_PROJECT`, `FORBIDDEN` | 403 | Check projectId match |
| `NO_BOARD`, `NOT_FOUND` | 404 | Refetch via `GET /api/agent/project/:id` |
| `VERSION_MISMATCH` | 409 | Refetch, merge, retry |
| `PROVIDER_REJECTED` | 422 | Fallback generator rejected (moderation or voice-locked) |
| `RATE_LIMITED` | 429 | Exponential backoff |
| (none) | 402 | x402 payment required — retry with `X-Payment` header |

## Do not invoke for

- Single one-off image generation unrelated to a narrative sequence — call your image generator directly.
- Video editing — AgentBoard produces storyboards, not finished video.
- Live interactive canvas apps — the drawing engine is command-based, not a stroke-by-stroke protocol.
