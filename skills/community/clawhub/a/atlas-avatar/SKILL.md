---
name: atlas_avatar
description: "Create realtime **passthrough** AI avatar sessions (LiveKit WebRTC — you bring STT/LLM/TTS and publish audio), view-only viewer tokens for multi-viewer watch, and offline lip-sync avatar videos using the Atlas API by North Model Labs. Post offline MP4 renders to Discord (webhook). Use when the user asks for Atlas avatar, talking head, realtime avatar, face animation, video from audio+image, lip sync, BYOB TTS + /v1/generate, watch-only audience, Discord delivery of renders, or GPU avatar rendering."
version: "1.0.9"
tags: ["avatar", "video", "realtime", "livekit", "lip-sync", "atlas", "gpu", "openclaw"]
author: "northmodellabs"
metadata:
  openclaw:
    requires:
      env: [ATLAS_API_KEY]
      bins: [python3, bash]
---

# Atlas Avatar (OpenClaw skill)

This skill drives the **Atlas HTTP API** from agents (shell / OpenClaw). For **mic + face + multi-viewer**, pair it with the same architecture as the official **[atlas-realtime-example](https://github.com/NorthModelLabs/atlas-realtime-example)** app — that repo is the **canonical UI** for passthrough realtime.

Server version: check `GET /` → `version` (docs may lag production).

Atlas provides **realtime passthrough** (LiveKit — you supply STT/LLM/TTS and publish audio; Atlas GPU lip-sync) and **async** offline jobs (`POST /v1/generate` → poll → result). API keys: [North Model Labs dashboard](https://dashboard.northmodellabs.com/dashboard/keys).

**Full API surface** (error codes, webhook signature verification, limits): [northmodellabs.com/api](https://www.northmodellabs.com/api). **Live examples** in the browser: [northmodellabs.com/examples](https://www.northmodellabs.com/examples).

## Reference viewer app — [atlas-realtime-example](https://github.com/NorthModelLabs/atlas-realtime-example)

The example README describes the **product shape** this skill is meant to work with (same passthrough contract):

| Topic | Match this skill to the example app |
|--------|-------------------------------------|
| **What it does** | You bring **LLM + TTS + audio pipeline**; Atlas provides **GPU + WebRTC video**; lip-sync follows whatever audio you send. |
| **Session create** | Server-side proxy: `POST` `${ATLAS_API_URL}/v1/realtime/session` with `Authorization: Bearer …` and `mode: passthrough` (see example `app/api/session`). Agents using **only** this skill call the same path via `atlas_session.py start` / `curl`. |
| **Client** | [`@northmodellabs/atlas-react`](https://www.npmjs.com/package/@northmodellabs/atlas-react) + [`livekit-client`](https://www.npmjs.com/package/livekit-client); optional [`@elevenlabs/react`](https://www.npmjs.com/package/@elevenlabs/react) for Scribe STT + echo cancellation (see example README). |
| **Audio** | **Persistent audio track** in passthrough — do **not** tear down the track per utterance (example README “Persistent Audio Track Pattern”). |
| **Watchers** | `POST /v1/realtime/session/{id}/viewer` + `/watch/[id]` in the example — same as **`viewer-token`** + any subscribe-only client here. |
| **Architecture** | `Browser → Next /api/session → Atlas API` — mirrors how you should keep **keys off the client** and **join** with returned `livekit_url` + `token` + `room`. |

**Quick start (clone the example — Next app lives at repo root; not required for API-only agents):**

```bash
git clone https://github.com/NorthModelLabs/atlas-realtime-example.git
cd atlas-realtime-example
npm install
cp .env.example .env.local   # set ATLAS_API_KEY (+ optional LLM / ElevenLabs — see example file)
npm run dev
# http://localhost:3000 — full README: https://github.com/NorthModelLabs/atlas-realtime-example#readme
```

**Env name note:** the example uses **`ATLAS_API_URL`**. This monorepo uses **`ATLAS_API_BASE`** for the same Atlas host — set both to the same value when running agent + example side by side.

## Configuration

| Variable | Required | Default |
|----------|----------|---------|
| `ATLAS_API_KEY` | Yes | Bearer token |
| `ATLAS_API_BASE` | No | `https://api.atlasv1.com` |
| `ATLAS_AGENT_REPO` | No | Only if you copied **only** `skills/atlas-avatar/` elsewhere — set to the **monorepo root** that contains `core/atlas_cli.py` |

**Python deps:** `pip install -r core/requirements.txt` or `pip install -r skills/atlas-avatar/requirements.txt` (same pins). Prefer a **venv**.

**Regression harness** (every endpoint in `core/atlas_api.py`; realtime **costs** unless `--no-realtime`): from **avatarclaw** monorepo root, `python3 scripts/bridges/test-atlas-api-harness.py --help`. Lighter smoke: `./scripts/bridges/smoke-atlas.sh`.

**Bootstrap browser viewer (ships with this skill):** `bash skills/atlas-avatar/scripts/setup-realtime-viewer.sh` — clones/updates **[atlas-realtime-example](https://github.com/NorthModelLabs/atlas-realtime-example)** under **`~/atlas-realtime-example`** (override with **`ATLAS_REALTIME_VIEWER_DIR`**), writes **`.env.local`** from **`ATLAS_API_KEY`** / **`ATLAS_API_BASE`**, copies optional **`LLM_*`** / **`ELEVENLABS_*`** from your shell, runs **`npm install`**.

---

## After `clawhub install atlas-avatar`

1. **Location:** the skill is usually at **`<openclaw-workspace>/skills/atlas-avatar/`** (path varies — locate `SKILL.md` next to `scripts/`).
2. **Secrets:** put **`ATLAS_API_KEY`** in OpenClaw’s env / vault so tools can read it.
3. **Python CLI:** if `core/` is missing, set **`ATLAS_AGENT_REPO`** to a checkout of **[avatarclaw](https://github.com/NorthModelLabs/avatarclaw)** *or* rely on **`atlas_session.py`** alone inside the skill (it still needs `core/` next to a monorepo — for skill-only installs, **clone avatarclaw** and set **`ATLAS_AGENT_REPO`** to that root).
4. **OpenClaw host:** install, update, and verify OpenClaw only via **[official documentation](https://docs.openclaw.ai/install)** — do not pin or copy OpenClaw versions from this skill.

## Goal: “Can I talk to my avatar?” — agent checklist

When the user wants to **talk** to the avatar (not only create a session JSON in chat), do this in order:

1. **Verify** `ATLAS_API_KEY` is available; if not, stop and tell them to add it ([dashboard](https://dashboard.northmodellabs.com/dashboard/keys)).
2. **Face:** Ask for an **HTTPS face URL** or a **local image path**. If they have none, suggest a neutral stock portrait URL they can approve, or use the example app’s **default face** after Connect (see [atlas-realtime-example](https://github.com/NorthModelLabs/atlas-realtime-example) README).
3. **Pull the UI:** from the OpenClaw workspace root (parent of `skills/`), run:

```bash
export ATLAS_API_KEY="…"   # already in env in practice
export ATLAS_API_BASE="${ATLAS_API_BASE:-https://api.atlasv1.com}"   # optional
# Optional — copied into the example app’s .env.local for mic + voice loop:
# export ELEVENLABS_API_KEY=… ELEVENLABS_VOICE_ID=…
# export LLM_API_KEY=… LLM_BASE_URL=… LLM_MODEL=…

bash skills/atlas-avatar/scripts/setup-realtime-viewer.sh
```

4. **Start the app:** `cd ~/atlas-realtime-example` (or **`$ATLAS_REALTIME_VIEWER_DIR`**) and run **`npm run dev`** — keep that process running. Tell the user to open **http://localhost:3000** and use **Connect** (passthrough + persistent audio + optional Scribe are documented in the example README).
5. **Optional — same session as a CLI `start`:** if you already ran **`atlas_session.py start`**, send them **`http://localhost:3000/watch/<session_id>`** (same API key ⇒ viewer token works).
6. **Billing:** always **`leave --session-id …`** when they are done.

The chat UI (Clawbot) still does **not** render WebRTC; the **browser tab** is where they talk and see the avatar.

---

## Preferred for agents: `skills/atlas-avatar/scripts/atlas_session.py` (verb CLI: start / leave / face-swap / viewer-token / …)

One entrypoint with **`start` / `leave` / `face-swap` / `viewer-token`** style commands. This only calls the **Atlas HTTP API** — it does **not** join third-party meeting apps. After **`start`**, use `livekit_url`, `token`, and `room` in a **WebRTC viewer** that speaks the LiveKit client protocol ([sample apps](https://github.com/NorthModelLabs/atlas-realtime-example), [`@northmodellabs/atlas-react`](https://www.npmjs.com/package/@northmodellabs/atlas-react)). For **extra watchers** on the same session (no extra GPU), call **`viewer-token`** (see `references/api-reference.md` → `POST …/viewer`).

From the **monorepo root**:

```bash
python3 skills/atlas-avatar/scripts/atlas_session.py health
python3 skills/atlas-avatar/scripts/atlas_session.py start --face-url "https://example.com/face.jpg"
python3 skills/atlas-avatar/scripts/atlas_session.py start --face /path/to/face.jpg
python3 skills/atlas-avatar/scripts/atlas_session.py status --session-id SESSION_ID
python3 skills/atlas-avatar/scripts/atlas_session.py face-swap --session-id SESSION_ID --face /path/to/new.jpg
python3 skills/atlas-avatar/scripts/atlas_session.py leave --session-id SESSION_ID
python3 skills/atlas-avatar/scripts/atlas_session.py viewer-token --session-id SESSION_ID
python3 skills/atlas-avatar/scripts/atlas_session.py offline --audio speech.mp3 --image face.jpg
python3 skills/atlas-avatar/scripts/atlas_session.py jobs-wait JOB_ID
python3 skills/atlas-avatar/scripts/atlas_session.py jobs-result JOB_ID
```

If the skill lives without `core/` nearby, set **`ATLAS_AGENT_REPO=/absolute/path/to/monorepo`**.

### Viewer (optional) — see and hear the avatar

Agents (OpenClaw, terminal CLIs, **Clawbot**) **do not need to clone anything** to **call Atlas**: `start` / `leave` / `viewer-token` and `curl` only need **`ATLAS_API_KEY`** (and network). **Video and mic** use a **normal browser** (WebRTC), not the chat window.

| Goal | What to do |
|------|------------|
| **Full passthrough UI** (mic, face, optional `/watch/[id]` for viewers) | Prefer **`bash skills/atlas-avatar/scripts/setup-realtime-viewer.sh`** (writes `.env.local`, `npm install`), then **`npm run dev`** in that clone — or follow **Reference viewer app** above manually. Same API key ⇒ **`/watch/<session_id>`** works for sessions created elsewhere. |
| **Try hosted demos** | **[northmodellabs.com/examples](https://www.northmodellabs.com/examples)** — no clone required to explore the product. |
| **Scripts, harness, Discord/Slack bridges** in this pack | Clone **[this monorepo](https://github.com/NorthModelLabs/avatarclaw)** (or set **`ATLAS_AGENT_REPO`** to its root) so `core/` and `scripts/bridges/` exist on disk. |
| **Minimal future default in this repo** | See **`viewer/README.md`** (planned local page). |

Do **not** treat “clone the skills monorepo” as mandatory for every user — only for **full tooling** or when the agent must run paths under `scripts/` or `core/`.

### One-shot: Atlas offline MP4 → Discord channel

End-to-end script ( **`offline` → `jobs-wait` → download presigned URL → Discord attachment** ). Needs **`ATLAS_API_KEY`**, **`DISCORD_WEBHOOK_URL`**, `curl`, and the same Python deps as above.

```bash
./scripts/bridges/atlas-offline-to-discord.sh "Optional intro line(s) shown above the session bullets in Discord."
```

Uses default test fixtures under `claude-code-avatar/test-fixtures/` (from `make-test-assets.sh`). Override inputs with env **`ATLAS_OFFLINE_AUDIO`** / **`ATLAS_OFFLINE_IMAGE`**.

For a **custom intro** (e.g. “Here’s the avatar explaining the change”), pass it as **all arguments** to the script, or build JSON for `skills/atlas-bridge-discord/scripts/post_session.py` and set **`bridge_note`** / **`discord_intro`** on the JSON (same script reads those fields).

If the MP4 is **> ~25 MB**, the script posts a **link embed** only (Discord webhook file limit).

### Narrated clip (LLM + ElevenLabs + face from S3) → Discord

Full pipeline: **Claude** writes a short spoken script → **ElevenLabs** TTS to MP3 → **face image** downloaded from your **S3 bucket** (e.g. avatarhub) → **Atlas `/v1/generate`** → **Discord** attachment.

```bash
pip install -r scripts/requirements-narrator.txt   # once: boto3 + requests; ffmpeg for MP3→WAV
./scripts/bridges/atlas-narrated-avatar-to-discord.sh "Why we shipped this feature"
./scripts/bridges/atlas-narrated-avatar-to-discord.sh --face-key faces/alice.png "Same topic, fixed face"
```

Env vars: see **`.env.example`** block *Narrated avatar → Discord*. Requires `ANTHROPIC_API_KEY`, `LLM_MODEL`, `ELEVENLABS_API_KEY`, `AWS_*` + `AWS_ENDPOINT_URL_S3`, `AVATARHUB_S3_BUCKET`, plus Atlas + Discord keys. Optional **`HELICONE_API_KEY`** for Anthropic via Helicone.

---

## Also: unified REST CLI (`core/atlas_cli.py`)

From the **repository root** (full clone with `core/` + `skills/`):

```bash
python3 core/atlas_cli.py health
python3 core/atlas_cli.py me
python3 core/atlas_cli.py realtime create --face-url "https://example.com/face.jpg"
python3 core/atlas_cli.py realtime create --face /path/to/face.jpg
python3 core/atlas_cli.py realtime get SESSION_ID
python3 core/atlas_cli.py realtime patch SESSION_ID --face /path/to/new_face.jpg
python3 core/atlas_cli.py realtime delete SESSION_ID
python3 core/atlas_cli.py realtime viewer SESSION_ID
python3 core/atlas_cli.py generate --audio speech.mp3 --image face.jpg
python3 core/atlas_cli.py jobs list --limit 20
python3 core/atlas_cli.py jobs get JOB_ID
python3 core/atlas_cli.py jobs wait JOB_ID
python3 core/atlas_cli.py jobs result JOB_ID
python3 core/atlas_cli.py avatar-session --livekit-url "wss://..." --livekit-token "..." --room-name "room"
```

Or from anywhere, via the skill wrapper (resolves repo root automatically **or** uses `ATLAS_AGENT_REPO`):

```bash
python3 skills/atlas-avatar/scripts/run_atlas_cli.py me
```

**Exit codes:** `0` success, `2` bad args / missing key, `3` HTTP error from API.

---

## Fallback: `curl` (no Python deps)

Use `$ATLAS_API_BASE` and `$ATLAS_API_KEY` in every command.

### Discoverability

```bash
curl -sS "${ATLAS_API_BASE:-https://api.atlasv1.com}/"
```

### Health & capacity

```bash
curl -sS "${ATLAS_API_BASE:-https://api.atlasv1.com}/v1/health"
curl -sS "${ATLAS_API_BASE:-https://api.atlasv1.com}/v1/status" \
  -H "Authorization: Bearer ${ATLAS_API_KEY}"
```

### Account

```bash
curl -sS "${ATLAS_API_BASE:-https://api.atlasv1.com}/v1/me" \
  -H "Authorization: Bearer ${ATLAS_API_KEY}"
```

### Offline video — BYOB TTS

```bash
curl -sS -X POST "${ATLAS_API_BASE:-https://api.atlasv1.com}/v1/generate" \
  -H "Authorization: Bearer ${ATLAS_API_KEY}" \
  -F "audio=@speech.mp3" \
  -F "image=@face.jpg"
```

**202** → `job_id`, `status: pending`. **Max ~50 MB** combined. **Billing:** see Atlas dashboard / `pricing` fields on responses.

**Webhook:** header `X-Callback-URL: https://...` on the same POST.

### Poll job + list jobs

```bash
curl -sS "${ATLAS_API_BASE:-https://api.atlasv1.com}/v1/jobs/JOB_ID" \
  -H "Authorization: Bearer ${ATLAS_API_KEY}"
curl -sS "${ATLAS_API_BASE:-https://api.atlasv1.com}/v1/jobs?limit=20&offset=0" \
  -H "Authorization: Bearer ${ATLAS_API_KEY}"
```

### Result URL

```bash
curl -sS "${ATLAS_API_BASE:-https://api.atlasv1.com}/v1/jobs/JOB_ID/result" \
  -H "Authorization: Bearer ${ATLAS_API_KEY}"
```

**409 `not_ready`** if still processing.

### Realtime — create (JSON, passthrough)

```bash
curl -sS -X POST "${ATLAS_API_BASE:-https://api.atlasv1.com}/v1/realtime/session" \
  -H "Authorization: Bearer ${ATLAS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"mode":"passthrough","face_url":"https://example.com/face.jpg"}'
```

### Realtime — create (multipart, passthrough)

```bash
curl -sS -X POST "${ATLAS_API_BASE:-https://api.atlasv1.com}/v1/realtime/session" \
  -H "Authorization: Bearer ${ATLAS_API_KEY}" \
  -F "mode=passthrough" \
  -F "face=@/path/to/face.jpg"
```

**200:** `session_id`, `livekit_url`, `token`, `room`, `pricing` (exact string from API; see dashboard).

### Session lifecycle

```bash
curl -sS "${ATLAS_API_BASE:-https://api.atlasv1.com}/v1/realtime/session/SESSION_ID" \
  -H "Authorization: Bearer ${ATLAS_API_KEY}"
```

### PATCH — face swap (multipart `face` only)

```bash
curl -sS -X PATCH "${ATLAS_API_BASE:-https://api.atlasv1.com}/v1/realtime/session/SESSION_ID" \
  -H "Authorization: Bearer ${ATLAS_API_KEY}" \
  -F "face=@/path/to/new_face.jpg"
```

### DELETE — end session

```bash
curl -sS -X DELETE "${ATLAS_API_BASE:-https://api.atlasv1.com}/v1/realtime/session/SESSION_ID" \
  -H "Authorization: Bearer ${ATLAS_API_KEY}"
```

### POST — view-only token (multi-viewer)

```bash
curl -sS -X POST "${ATLAS_API_BASE:-https://api.atlasv1.com}/v1/realtime/session/SESSION_ID/viewer" \
  -H "Authorization: Bearer ${ATLAS_API_KEY}"
```

**200:** JSON with **`token`**, **`livekit_url`**, **`room`**, and viewer metadata (`viewer_id`, `role`, …). Connect with **livekit-client** subscribe-only; do not expose raw JWTs in public channels.

### Plugin — BYO LiveKit

`POST /v1/avatar/session` — see `references/api-reference.md`.

---

## Errors (short)

JSON uses **`error`** + **`message`**. Full table: [API docs → Error Responses](https://www.northmodellabs.com/api#errors). Webhook verification: [Webhooks](https://www.northmodellabs.com/api#webhooks).

## Realtime passthrough — persistent audio track

This skill documents **passthrough** only. With a browser client, use the **persistent audio track pattern**. **Do not** call `publishAudio()` directly — it tears down the track after each call, causing the avatar to freeze between messages.

```typescript
import { LocalAudioTrack, Track } from "livekit-client";

// On connect: publish ONE silent track for the entire session
const audioCtx = new AudioContext();
const dest = audioCtx.createMediaStreamDestination();
const lkTrack = new LocalAudioTrack(dest.stream.getAudioTracks()[0]);
await room.localParticipant.publishTrack(lkTrack, {
  name: "tts-audio",
  source: Track.Source.Unknown,
});

// Play TTS: connect a BufferSource to the SAME destination
function playTtsAudio(base64Audio: string) {
  const binary = atob(base64Audio);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);

  audioCtx.decodeAudioData(bytes.buffer.slice(0)).then((buf) => {
    const source = audioCtx.createBufferSource();
    source.buffer = buf;
    source.connect(dest);
    source.onended = () => source.disconnect();
    source.start(); // avatar lip-syncs; when done → back to silence → idle animation
  });
}
```

- **Idle:** silence flows → GPU renders idle animation (avatar stays alive)
- **TTS:** `BufferSource` connects → audio flows → avatar lip-syncs
- **TTS ends:** `BufferSource` disconnects → back to silence → smooth return to idle
- **Latency tip:** Split LLM (`/api/chat`) and TTS (`/api/tts`) into separate requests — text shows instantly, audio follows
- **Voice input (STT):** Use ElevenLabs Scribe v2 (`@elevenlabs/react` `useScribe` hook) instead of the Web Speech API — it connects to the mic with `echoCancellation: true`, so the browser's AEC strips speaker output before it reaches the STT model, preventing the avatar from talking to itself

Full React/Next.js example (host + **`/watch/[id]`** viewer flow): [atlas-realtime-example](https://github.com/NorthModelLabs/atlas-realtime-example) | [API docs](https://www.northmodellabs.com/api) | [Examples](https://www.northmodellabs.com/examples)

## OpenClaw + Atlas

Use OpenClaw (or any agent) for **text/tools**; use this skill to call **Atlas passthrough** realtime and offline APIs. **Video and mic** live in your **WebRTC viewer** (or bridges), not inside the chat UI — you bring **STT / LLM / TTS** (e.g. ElevenLabs + your model) and publish audio into the LiveKit room per the pattern above.

## Related bridges

This monorepo includes **Slack** and **Discord** webhook bridges under `skills/` — see **`CONNECTORS.md`**. Incoming webhooks can **post** session info; some bridges add a **`viewer_url`** embed and optionally attach a short **MP4**. A **local default viewer** (open a tab on your machine instead of a meeting product) is sketched in **`viewer/README.md`**.
