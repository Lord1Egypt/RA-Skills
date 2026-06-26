# Atlas API reference (OpenClaw / agents)

**Base:** `ATLAS_API_BASE` (default `https://api.atlasv1.com`)  
**Auth:** `Authorization: Bearer <ATLAS_API_KEY>`

**Canonical docs (full field tables, pricing copy, error enum):** [northmodellabs.com/api](https://www.northmodellabs.com/api)  
**Hosted demos (try flows in the browser):** [northmodellabs.com/examples](https://www.northmodellabs.com/examples)

---

## Index & health

| Method | Path | Auth |
|--------|------|------|
| GET | `/` | No — API info, `version`, `endpoints` map |
| GET | `/v1/health` | No — deep health (GPU/TTS/DB signals) |
| GET | `/v1/status` | Yes — `avatar_generation` / `voice_synthesis` busy vs available |
| GET | `/v1/me` | Yes — key prefix, tier, rate limit window, billing hint |

---

## Offline generation & jobs

### `POST /v1/generate`

Multipart: **`audio`**, **`image`** (required). Returns **202** with `job_id`, `pending`.

- **Billing:** see live `pricing` strings and [dashboard](https://dashboard.northmodellabs.com/dashboard/keys); do not hardcode rates in agents.
- Combined upload limit ~**50 MB** (see live docs).
- **BYOB TTS:** generate speech with any provider; pass the audio file here.

**Webhook:** header **`X-Callback-URL`** (HTTPS, validated; no localhost). Body fields may also support `callback_url` on some JSON TTS endpoints — prefer header for multipart `/v1/generate`.

### `GET /v1/jobs`

Query: `limit` (default 20, max 100), `offset`. Newest first.

### `GET /v1/jobs/{job_id}`

Statuses: `pending`, `processing`, `completed`, `failed`. May include presigned `url` when completed.

### `GET /v1/jobs/{job_id}/result`

Presigned download JSON: `url`, `content_type`, `expires_in`.

- **409 `not_ready`** if job not `completed` yet.

---

## Realtime

### `POST /v1/realtime/session`

**This monorepo / skill uses `mode: "passthrough"` only** (BYO STT/LLM/TTS; you publish audio to LiveKit). The public API may document other modes on [northmodellabs.com/api](https://www.northmodellabs.com/api).

**JSON:** `{ "mode": "passthrough", "face_url": "https://..." }`  
**Multipart:** `mode=passthrough`, optional `face` file.

**200:** `session_id`, `livekit_url`, `token`, `room`, `mode`, `max_duration_seconds`, **`pricing`** (API-defined string; see dashboard).

**Passthrough audio:** use a **persistent audio track** — publish a single `MediaStreamDestination` track for the entire session (silence when idle, TTS audio when speaking). Do **not** call `publishAudio()` repeatedly — it tears down the track after each call, causing the avatar to freeze. See the [realtime example app](https://github.com/NorthModelLabs/atlas-realtime-example) README for the full pattern.

### `GET /v1/realtime/session/{id}`

`status`, `room`, `started_at`, `ended_at`, `duration_seconds`, `max_duration_seconds`.

### `PATCH /v1/realtime/session/{id}`

**Multipart only:** field **`face`** (file). No `face_url` on PATCH (security). Use POST create for HTTPS URLs.

**200:** `face_updated`, `metadata_pushed`, `message`.

**409:** `session_not_active` if not `active`.

### `DELETE /v1/realtime/session/{id}`

**200:** `status`, `duration_seconds`, `estimated_cost`, `credits_deducted_cents`.

**409:** `already_ended` if session already ended.

### `POST /v1/realtime/session/{id}/viewer` (multi-viewer)

**Body:** none (empty POST).

**200:** View-only LiveKit join bundle — typically includes **`token`**, **`livekit_url`**, **`room`**, plus fields such as **`viewer_id`**, **`role`** (`viewer`). Same API key that created the session must call this endpoint.

**Use case:** One client drives the session (host token from create); **additional browsers** get a **subscribe-only** token so many people can watch the same stream **without extra GPU** (see website realtime section).

**Client:** Connect with [`livekit-client`](https://www.npmjs.com/package/livekit-client) (or any LiveKit SDK), attach remote **video** / **audio** tracks. Do not paste these JWTs into public chat — mint them server-side or use a private viewer page ([realtime example](https://github.com/NorthModelLabs/atlas-realtime-example) includes `/watch/[id]`).

**CLI:** `python3 core/atlas_cli.py realtime viewer SESSION_ID` or `python3 skills/atlas-avatar/scripts/atlas_session.py viewer-token --session-id SESSION_ID`.

---

## Webhooks (async completion)

When you pass **`X-Callback-URL`** (HTTPS; **no localhost**) on **`POST /v1/generate`**, Atlas can `POST` JSON to your URL when the job finishes.

**Verify origin:** each delivery includes **`X-Atlas-Signature`** and **`X-Atlas-Timestamp`**. Validate the signature with your webhook secret before trusting the body — full algorithm and examples: [API docs → Webhooks](https://www.northmodellabs.com/api#webhooks).

---

## Plugin (often omitted from `GET /` index)

### `POST /v1/avatar/session`

Production `GET /` currently lists generate, jobs, realtime, TTS, health, me, status — **not** this path. Treat it as **deployment- or product-specific** (e.g. **livekit-plugins-atlas** when the customer hosts the LiveKit room); confirm it exists on your base URL before relying on `atlas_cli.py avatar-session`.

Multipart: `livekit_url`, `livekit_token`, `room_name` (strings); optional `avatar_image` file.

**200:** `{ "session_id", "status": "ok" }` (shape per your deployment).

---

## TTS job endpoints

`POST /v1/tts/generate`, `/v1/tts/generate-wav`, `/v1/tts/generate-video` — async jobs; same poll/result pattern. See website for multipart vs JSON.

---

## Errors

Standard shape:

```json
{ "error": "code", "message": "Human-readable text" }
```

Full enum table lives on the **website** API docs ([Error Responses](https://www.northmodellabs.com/api#errors)). This file stays short for token budget.

---

## OpenClaw / agents

Prefer **`python3 core/atlas_cli.py …`** from the monorepo root (see `skills/atlas-avatar/SKILL.md`) for a single maintained client; **`curl`** remains valid for minimal environments. For production, a typed OpenClaw **plugin** avoids shell entirely.
