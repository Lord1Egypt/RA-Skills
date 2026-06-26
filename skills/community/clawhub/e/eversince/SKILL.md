---
name: eversince
description: >
  Eversince is a creative agent that plans and executes across image, video, and audio.
  It orchestrates the latest AI models and operates in a purpose-built environment with tools, skills, and memory.
  Works for one-off tasks or as a creative employee in any agent-to-agent workflow.
version: 1.0.5
metadata:
  openclaw:
    requires:
      env:
        - EVERSINCE_API_KEY
      bins:
        - curl
    primaryEnv: EVERSINCE_API_KEY
    homepage: https://eversince.ai
allowed-tools: Bash Read Write WebFetch
---

# Eversince: Creative Agent API

You are briefing a creative agent. It reasons through your brief, makes creative decisions, selects AI models, generates images, videos, voiceovers, music, sound effects, motion graphics, and delivers either rendered assembled video or standalone assets as requested. Generate from scratch or hand off your own assets (images, video, audio, URLs) and the agent builds around them.

**Full documentation:** https://docs.eversince.ai

## Requirements

- **API key required.** This skill authenticates with an Eversince account via `EVERSINCE_API_KEY`. Get one at https://eversince.ai/app/settings.
- **Paid usage.** Generations consume credits from the user's Eversince account. Use `POST /estimate-cost` to preview costs and `GET /account/credits` to check balance before running.
- **External calls.** All requests go to `https://eversince.ai/api/v1`. Optional `webhook_url` sends status updates to a user-specified URL.

## Setup

**Base URL:** `https://eversince.ai/api/v1`

**Authentication:** API key in the Authorization header.
```
Authorization: Bearer YOUR_API_KEY
```

Get your API key at https://eversince.ai/app/settings. Once you have a key, you can create additional keys via `POST /keys`, list them via `GET /keys`, and revoke via `DELETE /keys/:id`.

## Quick Start

### 1. Create a project

```bash
curl -X POST https://eversince.ai/api/v1/projects \
  -H "Authorization: Bearer $EVERSINCE_API_KEY" \
  -H "X-Eversince-Source: plugin" \
  -H "Content-Type: application/json" \
  -d '{
    "brief": "Your creative brief here",
    "mode": "autonomous"
  }'
```

Response (202):
```json
{
  "id": "abc12345-def6-7890-abcd-ef1234567890",
  "status": "queued",
  "mode": "autonomous",
  "project_url": null,
  "credits_balance": 4200,
  "created_at": "2026-03-30T12:00:00Z"
}
```

### 2. Poll for status

```bash
curl https://eversince.ai/api/v1/projects/PROJECT_ID \
  -H "Authorization: Bearer $EVERSINCE_API_KEY" \
  -H "X-Eversince-Source: plugin"
```

Poll until the status reaches `idle`, `failed`, or `cancelled`. The status can be one of:

| Status | Meaning |
|--------|---------|
| `queued` | Waiting to start |
| `running` | Agent is working |
| `generating` | Waiting for model providers |
| `rendering` | Video being assembled |
| `idle` | Agent finished its run. Check the response |
| `failed` | Something went wrong |
| `cancelled` | Stopped via cancel endpoint |

### 3. Get the result

When status is `idle`, the response includes:
- `output_type`: `assembled` (rendered video available), `assets` (individual files, no render), or `pending` (still processing)
- `assembled_url`: the rendered video from the active state of the timeline, if the project produced one (expires after 24 hours, re-render to refresh)
- `agent_message`: the agent's latest message
- `project_url`: link to the project in the Eversince studio
- `variation_id`: the active variation ID

To get all generated assets (images, videos, audio): `GET /projects/:id/assets`
To get the full timeline structure of the active variation: `GET /projects/:id/timeline`
To get the conversation history: `GET /projects/:id/messages`
To get all variations: `GET /projects/:id/variations`
To read the agent's working memory: `GET /projects/:id/memory`
If the project has an `assembled_url`, a permanent shareable link can be created via `POST /projects/:id/share`

## What the Agent Can Do

### Production
- **Image generation:** text-to-image, image-to-image, reference-based (multiple references for character consistency, style matching), multiple variants per call
- **Video generation:** text-to-video, image-to-video, video-to-video, multi-shot direction across multiple segments, audio-synced generation (lip-sync, rhythm), camera motion presets
- **Video production:** multi-scene timelines, storytelling structure, pacing, scene management, generation selection, fade control
- **Voiceover:** script writing and speech generation in 60+ languages, voice selection, speed control, voice transformation
- **Music:** instrumental or with lyrics across three models (ElevenLabs, MiniMax, Google Lyria), each with different strengths
- **Sound effects:** ambient audio, impacts, transitions, duration and loop control
- **Captions:** three presets (impact, clean, kinetic), word-level sync
- **Text and logo overlays:** titles, taglines, CTAs, brand elements, positioned and timed on the timeline
- **Motion overlays:** animated graphics, kinetic text, data visualizations via Remotion

### Post-production
- **Variations:** parallel creative directions, A/B testing, multi-format delivery from the same project
- **Aspect ratio:** 16:9, 9:16, 1:1, 21:9 with timeline reframing (creates a new variation)
- **Language change:** translate voiceover + text overlays to 60+ languages (creates a new variation)
- **Upscaling:** 4x image upscale, video upscale to 4K
- **Background removal:** transparent PNGs from any generated or uploaded image
- **Image cropping:** extract panels from grid images or crop custom regions

### Intelligence
- **Media analysis:** multimodal analysis of generated images, videos, and audio to evaluate results
- **Audio transcription:** word-level timestamps for caption alignment and lyric sync
- **Web research:** search the web for trends, competitors, and cultural context
- **X/Twitter search:** trending topics, cultural moments, brand sentiment, competitor activity
- **URL extraction:** drop a URL as a reference, the agent extracts content and media
- **Cost estimation:** estimate credit costs for planned operations before executing

For long-term projects (campaigns, series, catalogs), see [references/advanced-patterns.md](references/advanced-patterns.md).

## Project Options

The brief is your primary input. The agent makes all creative decisions from it: concept, visuals, models, pacing, audio, everything. Include production preferences (voiceover, music, captions, duration, style) in the brief text. There are no separate fields for these. You can also attach reference files and URLs.

`brief` is the only required field. Everything else is optional:

| Field | Purpose | Default |
|-------|---------|---------|
| `brief` | What you want produced (required, max 8,000 chars) | None |
| `title` | Project title (max 30 characters) | None |
| `mode` | `autonomous` (agent runs end-to-end) or `collaborative` (agent stops for feedback) | `autonomous` |
| `aspect_ratio` | `16:9`, `9:16`, `1:1`, `21:9` | `16:9` |
| `skills` | Array of skills to activate. Each entry is an Eversince skill (`cinema`, `animation`, `ugc`, `music`, `photography`, `motion-graphics`) or a custom-skill UUID from `GET /account/skills`. Stack freely up to the 40,000-token combined budget. | `[]` |
| `video_model` | Specific video model ID (see `GET /models`). Models expose capability flags (`supports_multi_shot`, `supports_camera_motion`, `has_sound`, etc.) for informed selection | Agent decides |
| `image_model` | Specific image model ID (see `GET /models`). Models expose capability flags (`supports_reference_images`, `max_reference_images`, etc.) for informed selection | Agent decides |
| `agent_model` | `opus-4.7`, `opus-4.6`, or `sonnet-4.6` | — |
| `reasoning_mode` | `thinking` (deeper reasoning) or `fast` (quicker turns) | `thinking` |
| `expected_output` | `assembled` (rendered video from timeline), `assets` (standalone assets, no render) | Auto-detected |
| `webhook_url` | URL for status change notifications | None |
| `idempotency_key` | Unique string to prevent duplicate projects on retries | None |
| `references` | Array of `{upload_id}` or `{url, type}` for reference materials. Type: `image`, `video`, `audio`, `url` | None |
| `extract_content` | When `true`, URLs passed as references are fetched and their content extracted for the agent. Set `false` to pass URLs through as-is | `true` |

**File uploads:** To attach files as references, use the three-step presigned upload flow: `POST /uploads` → PUT the file to the returned `upload_url` (no auth header, `Content-Type` must match what you specified) → `POST /uploads/confirm` → use the returned `upload_id` in references. URLs can also be passed directly as references without uploading: `{"url": "https://...", "type": "url"}` (max 3 per request). See [references/api-reference.md](references/api-reference.md) for accepted file types, size limits, and full request/response shapes.

**Voices:** `GET /voices` lists available voiceover voices with name, gender, age, accent, style, and description. Filter by gender with `?gender=male|female|neutral`. Include the voice name in your brief to request a specific voice.

**Skill values:** (omit `skills` or pass `[]` to start with no skill active)
- `cinema`: shot design, camera movement, emotional pacing
- `ugc`: platform-native for TikTok, Reels, Shorts
- `photography`: hero shots, detail work, lifestyle compositions
- `animation`: character-driven storytelling, expressive motion
- `music`: song generation, music videos, beat-synced visuals
- `motion-graphics`: animated text, data visualization, graphic storytelling

Stack multiple in one call: `"skills": ["cinema", "photography"]`. Combine with custom skills by passing their UUIDs from `GET /account/skills` in the same array. Total active skills must stay under 40,000 tokens.

## Two Modes

### Autonomous (default)
The agent handles everything from start to finish. For video projects: plans → generates → verifies → renders → done. For asset projects: plans → generates → done.

### Collaborative
The agent stops at key decision points, returning `idle` status with its response in `agent_message`. Send feedback via `POST /projects/:id/messages`, and the agent continues.

Switch modes mid-project: `PATCH /projects/:id/settings` with `{"mode": "collaborative"}` or `{"mode": "autonomous"}`.

## Working with the Agent Over Time

Supports ongoing collaboration as well as one-off creative work.

- **Skills:** teach the agent persistent knowledge (brand guidelines, style rules, workflow preferences, etc.) via `POST /account/skills`. List via `GET /account/skills`, read via `GET /account/skills/:id`, toggle on/off via `PATCH /account/skills/:id`, delete via `DELETE /account/skills/:id`. Apply across all projects.
- **Learned preferences:** the agent learns preferences, brand voice, and creative patterns across projects. Read via `GET /account/learned-preferences`, update via `PUT /account/learned-preferences`.
- **Project history:** list all projects via `GET /projects` with `?status=`, `?title=`, `?limit=`, `?offset=` filters.
- **Shared content:** list all public share links and view counts via `GET /account/shares`.
- **Long-term projects:** for campaigns, series, or ongoing creative work, manage the long-term plan externally and hand the agent focused tasks. See [references/advanced-patterns.md](references/advanced-patterns.md).
- **Project discovery:** adopt projects created in the studio for API management via `GET /projects/discover` and `POST /projects/adopt`. See [references/advanced-patterns.md](references/advanced-patterns.md).

## Polling Strategy

Use status-aware intervals:

| Status | Interval | What's happening |
|--------|----------|-----------------|
| `queued` | 5s | Waiting to start |
| `running` | 30s | Agent reasoning |
| `generating` | 30-60s | Image: 30s-3 min, Video: 3-15 min |
| `rendering` | 30s | Video render, 1-5 min |
| `idle` | Stop polling | Agent finished its run. Check the result |
| `failed` / `cancelled` | Stop polling | Terminal |

**Webhooks** are available as an alternative to polling. Set `webhook_url` at project creation. Webhooks fire on status transitions (`running`, `generating`, `idle`, `failed`, `rendering`) with the full project state including `agent_message`, `timeline`, and `assets`. Note: `cancelled` does not fire a webhook.

Webhooks include `X-Eversince-Signature` (HMAC-SHA256) and `X-Eversince-Timestamp` headers for verification. Contact support@eversince.ai to set up a signing secret. 10-second timeout, no retries. If your endpoint is unavailable, the event is lost.

See [references/api-reference.md](references/api-reference.md) for webhook event details.

## Credits and Costs

- **Check balance:** `GET /account/credits` returns `credits_balance`. Check before starting work.
- **Estimate costs before executing:**

```bash
curl -X POST https://eversince.ai/api/v1/estimate-cost \
  -H "Authorization: Bearer $EVERSINCE_API_KEY" \
  -H "X-Eversince-Source: plugin" \
  -H "Content-Type: application/json" \
  -d '{"operations": [
    {"tool": "generate_image", "model": "nano-banana-pro", "count": 2},
    {"tool": "generate_video", "model": "seedance-2.0", "duration": 5, "count": 1}
  ]}'
```

Returns `total_credits` and per-item breakdown. Tools: `generate_image`, `generate_video`, `generate_audio`, `upscale_media`, `analyze_media`, `remove_background`, `motion_overlay`. See [references/api-reference.md](references/api-reference.md) for the full operation schema.

- **Low balance warning:** when balance drops to 100 or below, `GET /projects/:id` responses include a `credits_warning` field. When you see it, proactively fetch purchase options and present a link to the user before the balance hits zero.
- **When credits run out:** on `insufficient_credits` (402), fetch purchase options and present the link to the user:

```bash
curl https://eversince.ai/api/v1/account/credit-packages \
  -H "Authorization: Bearer $EVERSINCE_API_KEY" \
  -H "X-Eversince-Source: plugin"
```

Returns `packages[]` with `credits`, `price`, and `purchase_url` for each option.

## Error Handling

Errors return `{"error": {"code": "string", "message": "string", "status": 400}}`. Key codes: `validation_error` (400), `insufficient_credits` (402), `project_limit` (429), `rate_limited` (429/503). When status is `failed`, the response includes `error_message`.

**When a project fails:** Create a new project. Failed projects cannot be resumed or retried. Start fresh with the same or adjusted brief. Check `error_message` for what went wrong.

**When `POST /messages` returns 400:** The agent isn't `idle` yet. Poll `GET /projects/:id` until status reaches `idle`, `failed`, or `cancelled` before sending another message.

See [references/api-reference.md](references/api-reference.md) for the full error format, response headers, and rate limits.

## Feedback

Report bugs, suggestions, or questions directly via `POST /feedback` with `{"type": "bug | suggestion | question", "message": "string"}`.

## Settings: API vs Agent Messages

Some settings are changed via the API, others must go through the agent because they affect the timeline:

**Via `PATCH /projects/:id/settings`** (project-level config):
- `mode`, `video_model`, `image_model`, `agent_model`, `reasoning_mode`, `skills`, `webhook_url`, `title`, `expected_output`

**Via `POST /projects/:id/messages`** (timeline operations the agent performs. `PATCH /settings` will reject these with a validation error):
- Aspect ratio: "Change aspect ratio to 9:16"
- Language: "Change language to Spanish"
- Captions: "Enable kinetic captions" / "Turn off captions"
- Variations: "Duplicate the current variation" / "Switch to variation [id]"

## Limits

- **Minimum credits:** 30 to create a project, 10 to send a message, 10 to render.
- **Concurrent projects:** up to 5 projects in `queued`, `running`, `generating`, or `rendering` at the same time. Daily limit: 500 projects.
- **Agent runs in cycles:** the agent works, dispatches generations, waits for results, then continues automatically until the run completes or fails. Monitor progress via status polling or webhooks. Cancel at any time via `POST /projects/:id/cancel`.
- **`assembled_url` expires after 24 hours.** Re-render via `POST /projects/:id/render` (rate-limited per day: 10 non-sub, 50 sub). Create a permanent link via `POST /projects/:id/share`.
- **1080p rendering** is free (rate-limited per day). **4K rendering** charges credits. 1080p is the default.
- **Cancel stops the agent, not in-progress generations.** Already-dispatched generations will complete, but the agent won't continue after them.
- **No project deletion.** Projects cannot be deleted via the API. Cancel active ones with `POST /projects/:id/cancel`.
- **Idempotency:** if you send an `idempotency_key` and a non-failed project exists for that key, the API returns 200 with the existing project instead of creating a new one.
- **JSON payload limit:** 1 MB max per request. File uploads have separate limits (see `POST /uploads`).

## Studio Handoff

When iteration is complete and the user wants to continue working in the Eversince studio, clear the API context:

```bash
curl -X PATCH https://eversince.ai/api/v1/projects/PROJECT_ID/settings \
  -H "Authorization: Bearer $EVERSINCE_API_KEY" \
  -H "X-Eversince-Source: plugin" \
  -H "Content-Type: application/json" \
  -d '{"mode": "none"}'
```

## Reference Files

For the full endpoint catalog and request/response shapes: [references/api-reference.md](references/api-reference.md).

For long-term projects, parallel projects, variation workflows, and teaching the agent: [references/advanced-patterns.md](references/advanced-patterns.md).
