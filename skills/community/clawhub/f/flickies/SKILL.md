---
name: flickies
description: Self-hosted video REST + MCP API. POST JSON, get a video back. Lipsync (LatentSync 1.5 + Wav2Lip/Wav2Lip-GAN) at /v1/video/lipsync, GFPGAN face restore at /v1/video/restore, pure-ffmpeg ops (trim, concat, transcode incl. gif + fps + codec, scale, mux_audio, extract_audio, thumbnail_grid) under /v1/video/*, and ffprobe metadata at /v1/video/info. file_path (staged) xor file_url in; output_path xor output_url out. Fire-and-forget async jobs (async_job=true → 202 → poll /v1/jobs/{id}) with HMAC-signed webhooks. 11 MCP tools at /v1/mcp. Bearer-token auth. CPU + CUDA images. Use when the user wants to lipsync a face to audio, restore faces in footage, trim/concat/transcode/scale/mux/extract/thumbnail video, probe a video's metadata, or drive any of that from an LLM over MCP.
homepage: https://github.com/psyb0t/docker-flickies
user-invocable: true
permissions:
  - network: outbound HTTP to the configured FLICKIES_URL, plus server-side fetch of file_url, delivery to output_url, and HMAC-signed webhook callbacks
  - shell: the documented examples invoke local curl / docker
  - filesystem: manages server-side staged files (upload, fetch, remove) and engine lifecycle (load, evict) on the configured instance
metadata:
  { "openclaw": { "emoji": "🎬", "primaryEnv": "FLICKIES_URL", "requires": { "bins": ["docker", "curl"] } } }
---

# flickies

Self-hosted video toolkit — lipsync, face restore, and ffmpeg ops in one container. POST a JSON body, get a video back. Every video endpoint takes the same input/output contract; drive it from curl, the generated Go/Python clients, or point a function-calling LLM at the MCP endpoint.

Lipsync (`POST /v1/video/lipsync`): drive a face video/image from an audio track. Engines: `latentsync-1.5` (ByteDance, Apache-2.0, commercial-safe default, CUDA-only) and `wav2lip` / `wav2lip-gan` (Rudrabha, fast/low-VRAM, LRS2 non-commercial, refused unless `FLICKIES_ENABLE_NONCOMMERCIAL=1` is set in the **server** env). To clean up the mouth, run restore on the result; the MCP `lipsync` tool can chain GFPGAN with `restore_face=true` (the REST route ignores that field).

Face restore (`POST /v1/video/restore`): GFPGAN v1.4 (`gfpgan`, Apache-2.0) — clean up a Wav2Lip mouth crop or old footage, standalone.

ffmpeg ops (pure CPU, no engine): `POST /v1/video/trim`, `/concat`, `/transcode` (mp4/webm/mov/mkv + gif + fps + codec change), `/scale`, `/mux_audio`, `/extract_audio`, `/thumbnail_grid`. Metadata: `POST /v1/video/info` (ffprobe).

Extras: async jobs (`async_job=true` → 202 + `job_id` → poll `GET /v1/jobs/{job_id}`), HMAC-signed webhooks on async completion, server-side file staging, engine load/evict control, an MCP endpoint at `/v1/mcp` with 11 tools, optional bearer-token auth.

For installation, configuration, and container setup, see [references/setup.md](references/setup.md).

## Security & safety

- **Auth is off by default** — `FLICKIES_AUTH_TOKEN` is unset out of the box, so the whole API is open to anyone who can reach the port. Set it for any deployment beyond localhost, pass `Authorization: Bearer <token>` once it's set, and bind to loopback / behind an authenticating proxy. Never expose an unauthenticated instance on a network.
- **File and engine management** — the staging and engine endpoints include remove and evict operations. Like any state change, only run them against a resource the current task created, only when the user asked, and not against a shared instance others depend on.

## When To Use

- Lipsync a face (video or still image) to a driving audio track — `latentsync-1.5` (commercial-safe, CUDA) or `wav2lip` / `wav2lip-gan` (non-commercial gate).
- Restore / sharpen faces in a video with GFPGAN, standalone or as a second call after a Wav2Lip pass.
- Trim a clip, concatenate several clips, or transcode to another container/codec (incl. animated GIF).
- Change frame rate, re-encode with a specific codec/CRF/preset, scale dimensions, mux an audio track in, extract the audio out, or generate a thumbnail sprite-sheet.
- Probe a video for duration, codec, fps, dimensions, bitrate (`/v1/video/info`).
- Run any long operation fire-and-forget: submit with `async_job=true`, poll `/v1/jobs/{id}`, or receive an HMAC-signed webhook on completion.
- Drive the whole pipeline from a function-calling LLM (Claude, LibreChat, Cursor) via MCP at `/v1/mcp`.

## When NOT To Use

- Real-time / streaming video output — every endpoint is request/response; long jobs go async + poll, not stream.
- `latentsync-1.5` on the CPU image. It's CUDA-only (`cuda_only: true`) and its libraries are not in the CPU image, so the request fails with a plain-text 500. Use the `:latest-cuda` image for it. GFPGAN runs on both images (slowly on the CPU).
- `wav2lip` / `wav2lip-gan` anywhere unless the **server** was started with `FLICKIES_ENABLE_NONCOMMERCIAL=1` — otherwise the request returns 403 `NONCOMMERCIAL_GATE_REFUSED`. This is a server-side env flag; you cannot flip it per-request.
- Two engines resident at once — one model is resident at a time. A different engine request triggers hot-swap eviction of the current one. If you need two simultaneously, run two containers.
- `output_url` via the MCP tools — MCP tools only accept `output_path` (they write under FILES_DIR). Use the REST endpoint if you need presigned-PUT `output_url` delivery.
- Multipart upload on the video endpoints — only `PUT /v1/files/{path}` accepts a raw-body upload. Video endpoints take JSON with `file_path` or `file_url`.

## Setup

The container should already be running. Set the base URL:

```bash
export FLICKIES_URL=http://localhost:8000
```

If the server has `FLICKIES_AUTH_TOKEN` set, export it too:

```bash
export FLICKIES_AUTH_TOKEN=<your-token>
# every request below then needs: -H "Authorization: Bearer $FLICKIES_AUTH_TOKEN"
```

**Verify:** `curl $FLICKIES_URL/healthz` returns `{"status": "ok"}` (unversioned, always auth-exempt). For the richer discovery payload (device, ffmpeg version, available/enabled/loaded engines, non-commercial flag), hit `GET /v1/health`, which needs the token when auth is on:

```bash
curl -s $FLICKIES_URL/v1/health | jq
# { "status": "ok", "version": "...", "device": "cuda", "ffmpeg": "...",
#   "available_engines": [...], "enabled_engines": [...],
#   "loaded_engine": null, "noncommercial_enabled": false }
```

For install / configuration / env vars / CPU vs CUDA images / engine weights, see [references/setup.md](references/setup.md).

## Quick Start

The input/output contract is uniform across every video endpoint:

- **Input**: exactly one of `file_path` (FILES_DIR-relative, staged via `/v1/files`) or `file_url` (any HTTP/HTTPS URL the server fetches).
- **Output**: exactly one of `output_path` (server writes to FILES_DIR/<path>, response `{path, size, ...}`; download via `GET /v1/files/<path>`) or `output_url` (server PUTs to a presigned/PUT-accepting URL, response `{url, size, ...}`). In async mode both are ignored: the result always goes to `jobs/<uuid>.<ext>` under FILES_DIR, and the job's `result.path` says where.

```bash
# Probe a video (stage it first, then reference by path).
curl -s -X PUT --data-binary @clip.mp4 \
  -H "Authorization: Bearer $FLICKIES_AUTH_TOKEN" \
  "$FLICKIES_URL/v1/files/uploads/clip.mp4"

curl -s -X POST "$FLICKIES_URL/v1/video/info" \
  -H "Content-Type: application/json" \
  -d '{"file_path": "uploads/clip.mp4"}' | jq

# Trim seconds 5–12, write the result under FILES_DIR, download it.
curl -s -X POST "$FLICKIES_URL/v1/video/trim" \
  -H "Content-Type: application/json" \
  -d '{
        "file_path": "uploads/clip.mp4",
        "start_sec": 5, "end_sec": 12, "precise": true,
        "output_path": "out/clip-trimmed.mp4"
      }' | jq
curl -s "$FLICKIES_URL/v1/files/out/clip-trimmed.mp4" --output clip-trimmed.mp4

# Lipsync a face to an audio track (LatentSync, commercial-safe default, CUDA).
curl -s -X POST "$FLICKIES_URL/v1/video/lipsync" \
  -H "Content-Type: application/json" \
  -d '{
        "face_url": "https://example.com/face.mp4",
        "audio_url": "https://example.com/voice.wav",
        "engine": "latentsync-1.5",
        "output_path": "out/lipsynced.mp4"
      }' | jq
```

Add `-H "Authorization: Bearer $FLICKIES_AUTH_TOKEN"` to every call if the server has a token set. `/healthz` is the only always-exempt route.

## API — `POST /v1/video/lipsync`

Drive a face from an audio track. JSON body.

### Request Fields

| Field | Required | Default | Notes |
|---|---|---|---|
| `face_path` / `face_url` | exactly one | — | Driving face — a video OR a still image. `face_path` is FILES_DIR-relative; `face_url` is an HTTP(S) URL the server fetches. |
| `audio_path` / `audio_url` | exactly one | — | Driving audio (wav/mp3/m4a). `audio_path` FILES_DIR-relative; `audio_url` an HTTP(S) URL. |
| `engine` | no | `latentsync-1.5` | `latentsync-1.5` (Apache-2.0, CUDA-only, commercial-safe) / `wav2lip` / `wav2lip-gan`. The two `wav2lip*` slugs require `FLICKIES_ENABLE_NONCOMMERCIAL=1` on the server → else 403. |
| `restore_face` | no | `false` | Ignored by this REST route; only the MCP `lipsync` tool honours it. To fix the soft 96×96 Wav2Lip mouth crop over REST, call `/v1/video/restore` on the result. |
| `output_path` / `output_url` | one (sync) | | Sync mode requires exactly one. Async mode ignores both and stages to `jobs/`. |
| `output_format` | no | `mp4` | Ignored here; lipsync always writes MP4. |
| `async_job` | no | `false` | `true` → 202 + `job_id`; poll `/v1/jobs/{id}`. |
| `webhook_url` | no | — | Async only. HMAC-signed POST on completion — see [Async Job Lifecycle](#async-job-lifecycle). |

### Response

`200` (sync) — one of:

```json
{ "path": "out/lipsynced.mp4", "size": 4823110 }
```
```json
{ "url": "https://bucket.example.com/out.mp4?...", "size": 4823110 }
```

The server returns only `path` (or `url`) and `size`. `202` (async): `{ "job_id": "<uuid>", "status": "accepted" }`.

### Error Contract

| Status | `code` | When |
|---|---|---|
| 400 | `BAD_REQUEST` | not exactly one of `face_*`, not exactly one of `audio_*`, `output_path`+`output_url` both set, or neither in sync mode |
| 401 | `UNAUTHORIZED` | `FLICKIES_AUTH_TOKEN` set, missing/wrong bearer |
| 403 | `NONCOMMERCIAL_GATE_REFUSED` | `wav2lip` / `wav2lip-gan` requested but server has no `FLICKIES_ENABLE_NONCOMMERCIAL=1` |
| 404 | `ENGINE_NOT_REGISTERED` | engine slug not in the registry |
| 422 | `VALIDATION_FAILED` | body is not valid JSON or not a JSON object |
| 500 | `INTERNAL_SERVER_ERROR` | inference failed; a plain-text 500 means a missing `Content-Type: application/json` header or LatentSync on the CPU image |

Error body is always `{ "code": "UPPER_SNAKE", "message": "...", "details"?: {...} }`.

## API — `POST /v1/video/restore`

GFPGAN face restoration on a video. Input via `file_path` / `file_url`, output via `output_path` / `output_url` (same contract).

### Request Fields

| Field | Required | Default | Notes |
|---|---|---|---|
| `file_path` / `file_url` | exactly one | — | Source video. |
| `engine` | no | `gfpgan` | Only `gfpgan`. |
| `output_path` / `output_url` | one (sync) | — | Standard output contract. |
| `async_job` / `webhook_url` | no | `false` / none | As above. Output is always MP4. |

### Response

`200` → `StagedOutputResponse` or `UrlOutputResponse` (as lipsync). `202` → `JobAcceptedResponse`.

### Error Contract

`400` `BAD_REQUEST`, `401` `UNAUTHORIZED`, `422` `VALIDATION_FAILED`. GFPGAN has no non-commercial gate and runs on both images.

## API — ffmpeg ops (`POST /v1/video/{trim,concat,transcode,scale,mux_audio,extract_audio,thumbnail_grid}`)

Pure ffmpeg, CPU. Each takes the standard input/output contract plus op-specific fields. All return `StagedOutputResponse` xor `UrlOutputResponse` on `200`. All of them accept `async_job` / `webhook_url`, including `extract_audio` and `thumbnail_grid`. The server does not validate bodies against the spec: a missing required field ends in a plain-text 500.

### `trim` — cut `[start_sec, end_sec]`

| Field | Required | Default | Notes |
|---|---|---|---|
| `file_path` / `file_url` | exactly one | — | Source. |
| `start_sec` | yes | — | ≥ 0. |
| `end_sec` | yes | — | ≥ 0. |
| `precise` | no | `false` | `false`: `-c copy`, fast, but `start_sec` snaps to the nearest keyframe (can eat up to one GOP of leading content). `true`: re-encode H.264 + AAC for frame-accurate boundaries (slower, visually transparent). |

### `concat` — join ≥2 videos in order

| Field | Required | Default | Notes |
|---|---|---|---|
| `inputs_paths` / `inputs_urls` | exactly one | — | Array, `minItems: 2`. FILES_DIR paths or HTTP(S) URLs. |
| `precise` | no | `false` | `false`: concat demuxer + `-c copy` — requires identical codec/timebase/SAR across inputs. `true`: re-encode to uniform H.264 + AAC so mixed inputs join cleanly (slower). |

### `transcode` — universal re-encode

`output_format` (`mp4`/`webm`/`mov`/`mkv`/`gif`, default `mp4`) picks the container and the file extension; `gif` uses a palette filter graph. Additional:

| Field | Required | Default | Notes |
|---|---|---|---|
| `file_path` / `file_url` | exactly one | — | Source. |
| `video_codec` | no | — | e.g. `libx264`, `libx265`, `libvpx-vp9`, `libaom-av1`. |
| `audio_codec` | no | — | e.g. `aac`, `libopus`, `copy`. |
| `crf` | no | — | 0–51. |
| `preset` | no | — | e.g. `ultrafast`, `fast`, `medium`, `slow`. |
| `fps` | no | — | 1–240. Applies to all output formats. |
| `gif_options` | no | | Only consulted for GIF output: `{ width?, loop? (0 = infinite) }`. `palette_mode` is accepted and ignored. GIF `fps` defaults to 12. |

### `scale` — resize

| Field | Required | Default | Notes |
|---|---|---|---|
| `file_path` / `file_url` | exactly one | — | Source. |
| `width` | yes | — | ≥ 16. |
| `height` | yes | — | ≥ 16. |
| `keep_aspect` | no | `true` | Fit inside the box and pad the rest (letterbox); `false` stretches. |

### `mux_audio` — replace / merge the audio track

| Field | Required | Default | Notes |
|---|---|---|---|
| `video_path_or_url` | yes | — | Video source (path or URL — the server sniffs `http(s)://`). |
| `audio_path_or_url` | yes | — | Audio source (path or URL). |
| `replace_existing_audio` | no | `true` | Has no effect: the output always takes only the audio track of the second input. |

### `extract_audio` — pull the audio out

| Field | Required | Default | Notes |
|---|---|---|---|
| `file_path` / `file_url` | exactly one | — | Source. |
| `audio_format` | no | `wav` | `wav` / `mp3` / `m4a` / `ogg` / `flac`. |
| `output_path` / `output_url` | one (sync) | | Standard output contract, async included. |

### `thumbnail_grid` — sprite-sheet PNG

| Field | Required | Default | Notes |
|---|---|---|---|
| `file_path` / `file_url` | exactly one | — | Source. |
| `rows` | yes | — | 1–16. |
| `cols` | yes | — | 1–16. |
| `cell_width` | no | `320` | Per-cell width. |
| `cell_height` | no | `180` | Per-cell height. |
| `output_path` / `output_url` | one (sync) | | Standard output contract, async included. The grid covers the first rows x cols x 100 frames. |

### Error Contract (ffmpeg ops)

Same envelope. `400` `BAD_REQUEST` (bad input xor, `end_sec` not after `start_sec`, fewer than 2 concat inputs, unsupported audio format), `500` `FFMPEG_FAILED` (ffmpeg exited non-zero, including a staged file that does not exist), `401` when auth is on. A missing `start_sec`/`end_sec`, `rows`/`cols` or `width`/`height` gives a plain-text 500, not a 422.

## API — `POST /v1/video/info`

ffprobe metadata. Input via `file_path` / `file_url`; no output fields.

```bash
curl -s -X POST "$FLICKIES_URL/v1/video/info" \
  -H "Content-Type: application/json" \
  -d '{"file_path": "uploads/clip.mp4"}' | jq
```

### Response

```json
{
  "duration_sec": 12.4, "width": 1920, "height": 1080, "fps": 30.0,
  "video_codec": "h264", "audio_codec": "aac", "bitrate": 4200000,
  "container_format": "mov,mp4,m4a,3gp,3g2,mj2", "size_bytes": 6510022
}
```

`audio_codec`, `bitrate`, `container_format` are nullable. Errors: `400` `BAD_REQUEST`, `401` `UNAUTHORIZED`.

## Async Job Lifecycle

Any video-producing endpoint (`lipsync`, `restore`, and the ffmpeg ops that carry `async_job`) runs fire-and-forget when you set `async_job: true`. Lipsync/restore are the ones worth doing async — they're the slow ones.

**1. Submit**: POST with `async_job: true`. The server stages the result under `jobs/` in FILES_DIR and ignores `output_path` / `output_url`. Lipsync and restore load their engine before answering, so a cold engine still holds this request. Response is `202`:

```bash
JOB=$(curl -s -X POST "$FLICKIES_URL/v1/video/lipsync" \
  -H "Content-Type: application/json" \
  -d '{
        "face_url": "https://example.com/face.mp4",
        "audio_url": "https://example.com/voice.wav",
        "engine": "latentsync-1.5",
        "async_job": true
      }' | jq -r .job_id)
```

**2. Poll** — `GET /v1/jobs/{job_id}`:

```bash
curl -s "$FLICKIES_URL/v1/jobs/$JOB" | jq
# { "job_id": "...", "status": "running", "result": null, "error": null }
```

`status` is `pending`, `running`, `complete` or `failed` (there is no cancel endpoint). On `complete`, `result` holds `{path, size}`. On `failed`, `error` holds `{code: "JOB_FAILED", message}`.

**3. Fetch**: when `status: complete`, download `result.path`. The file name is a different UUID from `job_id`, so always read it from the result:

```bash
PATH_ON_SERVER=$(curl -s "$FLICKIES_URL/v1/jobs/$JOB" | jq -r .result.path)
curl -s "$FLICKIES_URL/v1/files/$PATH_ON_SERVER" --output result.mp4
```

**Webhook alternative** — pass `webhook_url` on the async submit and the server POSTs the final job state (`{job_id, status, result, error}`) to that URL on completion instead of making you poll:

- HMAC-SHA256 over `timestamp + "." + body`, keyed by the server's `FLICKIES_WEBHOOK_SECRET`.
- Headers: `X-Webhook-Timestamp: <unix-ts>`, `X-Webhook-Signature: t=<ts>,v1=<hex>`.
- Retried on non-2xx / transport error with exponential backoff (30s, 1m, 5m, 30m, 2h, 12h), then dead-lettered to the server log.
- Receiver MUST verify the signature and de-dupe on `(timestamp, signature)`.

`GET /v1/jobs/{job_id}` returns `404` `NOT_FOUND` for an unknown id. The queue is in-process — jobs don't survive a container restart.

## MCP Endpoint

flickies mounts a [Model Context Protocol](https://modelcontextprotocol.io) server at `/v1/mcp` (streamable-HTTP JSON-RPC, same FastAPI process, same auth middleware). Point a function-calling LLM at it and it drives the pipeline.

Eleven tools mirror the REST surface: `list_engines`, `info`, `lipsync`, `restore`, `transcode`, `trim`, `concat`, `scale`, `mux_audio`, `extract_audio`, `thumbnail_grid`. Argument shapes match the REST bodies, with one difference: **MCP tools accept `output_path` only** (they write under FILES_DIR; `output_url` presigned-PUT delivery is REST-only). MCP tools run synchronously — there's no `async_job` on the MCP side.

Wire it into Claude Code:

```bash
claude mcp add --transport http flickies $FLICKIES_URL/v1/mcp
# with auth:
claude mcp add --transport http flickies $FLICKIES_URL/v1/mcp \
  --header "Authorization: Bearer $FLICKIES_AUTH_TOKEN"
```

The transport requires `Accept: application/json, text/event-stream`. Raw JSON-RPC over HTTP POST for debugging / non-MCP callers:

```bash
# tools/list
curl -s "$FLICKIES_URL/v1/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'

# tools/call — lipsync
curl -s "$FLICKIES_URL/v1/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0", "id": 2, "method": "tools/call",
    "params": {
      "name": "lipsync",
      "arguments": {
        "face_url": "https://example.com/face.mp4",
        "audio_url": "https://example.com/voice.wav",
        "engine": "latentsync-1.5",
        "output_path": "out/lipsynced.mp4"
      }
    }
  }'
```

The canonical mount path carries a trailing slash (`/v1/mcp/`); bare `/v1/mcp` redirects to it. With auth on, every MCP call needs the same `Authorization: Bearer` header.

## Bearer-Token Auth

If `FLICKIES_AUTH_TOKEN` is set on the server, every route except `/healthz` (and CORS preflight) requires `Authorization: Bearer <token>`. Wrong/missing token returns `401` `UNAUTHORIZED`.

```bash
curl -H "Authorization: Bearer $FLICKIES_AUTH_TOKEN" $FLICKIES_URL/v1/engines
```

With `FLICKIES_AUTH_TOKEN` unset the API/MCP surface is unauthenticated — anyone who can reach it gets full access. Set the token and bind to loopback / behind an authenticating proxy; for untrusted networks add a reverse proxy doing TLS + rate limiting. See [references/setup.md](references/setup.md).

## Typical Workflows

### Lipsync, then face restore

```bash
curl -s -X POST "$FLICKIES_URL/v1/video/lipsync" \
  -H "Content-Type: application/json" \
  -d '{
        "face_path": "uploads/portrait.png",
        "audio_path": "uploads/line.wav",
        "engine": "wav2lip-gan",
        "output_path": "out/talking.mp4"
      }' | jq
# NOTE: wav2lip-gan needs FLICKIES_ENABLE_NONCOMMERCIAL=1 on the server.

curl -s -X POST "$FLICKIES_URL/v1/video/restore" \
  -H "Content-Type: application/json" \
  -d '{"file_path": "out/talking.mp4", "output_path": "out/talking-restored.mp4"}' | jq
```

The REST lipsync route ignores `restore_face`; over MCP, the `lipsync` tool with `restore_face: true` does both in one call.

### Stage once, run several ops off the same file

```bash
curl -s -X PUT --data-binary @raw.mp4 "$FLICKIES_URL/v1/files/uploads/raw.mp4"

curl -s -X POST "$FLICKIES_URL/v1/video/scale" \
  -H "Content-Type: application/json" \
  -d '{"file_path":"uploads/raw.mp4","width":1280,"height":720,"output_path":"out/720p.mp4"}' | jq

curl -s -X POST "$FLICKIES_URL/v1/video/transcode" \
  -H "Content-Type: application/json" \
  -d '{"file_path":"uploads/raw.mp4","output_format":"gif","fps":12,"gif_options":{"width":480},"output_path":"out/raw.gif"}' \
  --fail | jq
```

### Concatenate several clips (mixed sources → re-encode)

```bash
curl -s -X POST "$FLICKIES_URL/v1/video/concat" \
  -H "Content-Type: application/json" \
  -d '{
        "inputs_urls": ["https://ex.com/a.mp4","https://ex.com/b.mp4"],
        "precise": true,
        "output_path": "out/joined.mp4"
      }' | jq
```

### Long lipsync, async + poll to completion

```bash
FLICKIES_URL=$FLICKIES_URL FLICKIES_AUTH_TOKEN=$FLICKIES_AUTH_TOKEN \
  bash scripts/flickies.sh lipsync \
  '{"face_url":"https://ex.com/f.mp4","audio_url":"https://ex.com/v.wav","engine":"latentsync-1.5"}' \
  result.mp4
```

See [`scripts/flickies.sh`](scripts/flickies.sh) — submits any endpoint async, polls `/v1/jobs/{id}` to a terminal state, and downloads the staged result.

### Free VRAM after a job

Frees the resident engine from VRAM. Rarely needed — engines hot-swap on demand — so only evict one the current task loaded, and remember a shared instance may have another caller using it.

```bash
curl -s -X DELETE "$FLICKIES_URL/v1/engines/latentsync-1.5"   # evict from VRAM (204)
```

## Tips

1. **`file_url` over staging** — if the source is already at a URL, pass `file_url` and skip the upload round-trip.
2. **`precise=false` is the fast path** for trim/concat but snaps to keyframes / needs matching codecs. Flip to `precise=true` when you need frame accuracy or are joining mismatched inputs — it re-encodes.
3. **One engine resident at a time**: a lipsync request after a restore evicts the restore engine (hot-swap). The MCP `lipsync` tool's `restore_face=true` chains GFPGAN second, evicting the lipsync model to free VRAM.
4. **`async_job=true` for lipsync/restore** — they're slow. Submit, then poll `/v1/jobs/{id}` or take a webhook. ffmpeg ops are fast enough to run sync.
5. **Async output is always staged**: an async submit ignores `output_path`/`output_url`; fetch the file at the job's `result.path` under `jobs/`.
6. **`wav2lip*` is gated at the server** — 403 `NONCOMMERCIAL_GATE_REFUSED` means the operator hasn't set `FLICKIES_ENABLE_NONCOMMERCIAL=1`. You can't override it per-request; `latentsync-1.5` is the ungated default.
7. **CPU image can't run `latentsync-1.5`**, which is CUDA-only. GFPGAN and Wav2Lip run on the CPU (slowly; Wav2Lip only with the gate set). Use `:latest-cuda` for the full engine set.
8. **`GET /v1/health`** shows `device`, `loaded_engine`, and `noncommercial_enabled`; check it before you get a surprise 403 or a CPU failure.
9. **Idempotency-Key** — pass an `Idempotency-Key` header on a POST for safe retries; the server replays the cached response for a repeat `(key, method, path)`.
10. **`X-Request-Id`** — send one to correlate logs across hops; the server echoes it back and mints a UUID4 if you don't.
