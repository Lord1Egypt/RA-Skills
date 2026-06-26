# Eversince API Reference

Complete endpoint catalog. Base URL: `https://eversince.ai/api/v1`

All requests require `Authorization: Bearer YOUR_API_KEY` header.

**Response headers** (every response): `X-Request-Id`, `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`. On 429: `Retry-After`.

**Request body limit:** 1 MB max.

---

## Projects

### POST /projects
Create a new project.

**Request:**
```json
{
  "brief": "string (required, max 8,000 chars)",
  "title": "string (max 30 chars)",
  "mode": "autonomous | collaborative",
  "aspect_ratio": "16:9 | 9:16 | 1:1 | 21:9",
  "skills": ["cinema | animation | ugc | music | photography | motion-graphics | <custom-skill-uuid>"],
  "video_model": "string (model ID)",
  "image_model": "string (model ID)",
  "agent_model": "opus-4.7 | opus-4.6 | sonnet-4.6",
  "expected_output": "assembled | assets",
  "webhook_url": "string (HTTPS URL)",
  "idempotency_key": "string",
  "references": [{"upload_id": "string"} | {"url": "string", "type": "image | video | audio | url"}],
  "extract_content": true
}
```

**Response (202):**
```json
{
  "id": "string",
  "status": "queued",
  "mode": "autonomous | collaborative",
  "project_url": "string | null",
  "credits_balance": 0,
  "created_at": "ISO 8601"
}
```

### GET /projects
List projects.

**Query:** `limit` (1-100, default 20), `offset`, `status` (filter), `title` (search)

**Response (200):**
```json
{
  "projects": [{
    "id": "string",
    "source_project_id": "string | null (original project ID when adopted via /projects/adopt)",
    "status": "string",
    "mode": "string",
    "title": "string | null",
    "brief": "string (first 200 chars)",
    "expected_output": "assembled | assets | null",
    "assembled_url": "string | null",
    "project_url": "string | null",
    "created_at": "ISO 8601",
    "updated_at": "ISO 8601"
  }],
  "total": 0,
  "limit": 20,
  "offset": 0
}
```

### GET /projects/:id
Get project status.

**Status values:**

| Status | Meaning |
|--------|---------|
| `queued` | Waiting to start |
| `running` | Agent is working |
| `generating` | Waiting for model providers |
| `rendering` | Video being assembled |
| `idle` | Agent finished its run |
| `failed` | Something went wrong |
| `cancelled` | Stopped via cancel endpoint |

**Response (200):**
```json
{
  "id": "string",
  "status": "string",
  "mode": "string",
  "output_type": "assembled (rendered video available) | assets (individual files, no render) | pending (still processing)",
  "assembled_url": "string | null",
  "assembled_url_expires_at": "ISO 8601 | null",
  "project_url": "string | null",
  "agent_message": "string | null",
  "variation_id": "string | null",
  "created_at": "ISO 8601",
  "updated_at": "ISO 8601",
  "credits_warning": "string (only when balance ≤ 100)",
  "error_message": "string (only when status is failed)"
}
```

### PATCH /projects/:id/settings
Update project settings. Blocked during active agent runs (`running`, `generating`, `rendering`).

**Request:**
```json
{
  "title": "string (max 30 chars) | null",
  "mode": "autonomous | collaborative | none",
  "video_model": "string",
  "image_model": "string",
  "agent_model": "opus-4.7 | opus-4.6 | sonnet-4.6",
  "skills": ["string (Eversince slug or custom-skill UUID)"],
  "webhook_url": "string (HTTPS URL) | null",
  "expected_output": "assembled | assets | null"
}
```

`skills` replaces the full active set. Pass `[]` to clear. Combined token budget across all active skills is 40,000.

**Response (200):**
```json
{
  "title": "string | null",
  "mode": "autonomous | collaborative | none",
  "aspect_ratio": "string",
  "video_model": "string",
  "image_model": "string",
  "agent_model": "string (opus-4.7 | opus-4.6 | sonnet-4.6)",
  "skills": ["string"],
  "webhook_url": "string | null",
  "expected_output": "assembled | assets | null"
}
```

### POST /projects/:id/cancel
Stop the agent. Valid for: `queued`, `running`, `generating`, `idle`. Returns 400 if status is not cancellable. Returns 409 if status changed between check and update (race condition, re-check status).

**Response (200):**
```json
{"id": "string", "status": "cancelled"}
```

---

## Messages

### GET /projects/:id/messages
Get conversation history.

**Query:** `limit` (1-50, default 20), `before` (cursor for older), `after` (cursor for newer, use for efficient polling)

**Response (200):**
```json
{
  "messages": [{
    "id": "string",
    "role": "user | assistant",
    "content": "string",
    "source": "string",
    "created_at": "ISO 8601"
  }],
  "has_more": true
}
```

Note: the agent may emit messages with empty `content` during processing (e.g. when dispatching generations). These are internal status markers; filter or skip them when displaying conversation history.

### POST /projects/:id/messages
Send feedback or instructions to the agent. Valid for: `idle`. Returns 400 for any other status. Wait for the agent to finish if active, or check terminal status. Requires minimum 10 credits.

**Request:**
```json
{
  "message": "string (required, max 8,000 chars)",
  "references": [{"upload_id": "string"} | {"url": "string", "type": "image | video | audio | url"}],
  "extract_content": true
}
```

**Response (202):**
```json
{"id": "string", "status": "running"}
```

---

## Content

### GET /projects/:id/timeline
Full timeline state. Pass `?variation_id=ID` for non-active variations.

**Response (200):**
```json
{
  "timeline": {
    "duration_seconds": 0,
    "aspect_ratio": "string",
    "skills": ["string"],
    "scenes": [{
      "id": "string",
      "ref": "string",
      "type": "video | image | solid_frame_black | solid_frame_white | empty",
      "position": 0,
      "duration": 0,
      "description": "string",
      "image_url": "string | null",
      "video_url": "string | null",
      "video_model": "string | null",
      "image_model": "string | null",
      "prompt": "string | null",
      "volume": 1,
      "fade_in": "number | null",
      "fade_out": "number | null"
    }],
    "audio": {
      "voiceover": "object | null",
      "music": "object | null",
      "tracks": [{
        "id": "string",
        "type": "voiceover | music | sound_effect",
        "url": "string",
        "duration": 0,
        "volume": 1,
        "start_time": 0,
        "name": "string | null",
        "voice": "string | null",
        "voice_id": "string | null",
        "language": "string | null",
        "script": "string | null",
        "genre": "string | null",
        "mood": "string | null",
        "bpm": "number | null"
      }]
    },
    "overlays": [{
      "id": "string",
      "type": "text | logo | motion",
      "content": "string",
      "start_time": 0,
      "duration": 0,
      "position": "string",
      "font_size": "number | null",
      "color": "string | null",
      "background_color": "string | null",
      "width": "number | null",
      "opacity": "number | null"
    }],
    "captions": {
      "enabled": false,
      "preset": "impact | clean | kinetic | null"
    }
  }
}
```

### GET /projects/:id/assets
Generated assets with pagination.

**Query:** `limit` (1-50, default 20), `offset`

**Response (200):**
```json
{
  "assets": [{
    "ref": "string",
    "type": "image | video | audio",
    "url": "string",
    "model": "string",
    "prompt": "string",
    "duration": "number | null",
    "aspect_ratio": "string | null",
    "source_image_url": "string | null",
    "source_video_url": "string | null",
    "reference_image_url": "string | null",
    "created_at": "ISO 8601"
  }],
  "total": 0,
  "limit": 20,
  "offset": 0
}
```

### GET /projects/:id/variations
List all variations. Read-only; create/switch/delete variations by sending messages to the agent.

**Response (200):**
```json
{
  "variations": [{
    "id": "string",
    "title": "string",
    "description": "string | null",
    "aspect_ratio": "string",
    "language": "string | null",
    "scene_count": 0,
    "is_active": true,
    "created_at": "ISO 8601"
  }]
}
```

### GET /projects/:id/memory
Read the agent's working memory.

**Response (200):**
```json
{
  "sections": {
    "creative": {"content": "string", "tokens": 0},
    "todos": {"content": "string", "tokens": 0},
    "assets": {"content": "string", "tokens": 0}
  },
  "total_tokens": 0
}
```

- `creative` — markdown of the locked creative direction and chosen production settings.
- `todos` — checklist of what's done and what's next.
- `assets` — structured ledger of characters, products, environments, and references the agent is using.

---

## Output

### POST /projects/:id/render
Trigger video render. Valid for: `idle`. Rate limit: 50/day. Minimum 10 credits. 4K requires Pro subscription.

**Request:**
```json
{"quality": "1080p | 4k"}
```

**Response (202):**
```json
{"id": "string", "status": "rendering", "quality": "1080p"}
```

### POST /projects/:id/share
Create a public shareable link. Requires a render to have been completed.

**Request:**
```json
{"title": "string (optional)", "description": "string (optional)"}
```

**Response (201):**
```json
{"share_url": "https://eversince.ai/share/...", "video_url": "string"}
```

---

## File Uploads

To attach files (images, videos, audio) to a brief or message, use the three-step presigned upload flow:

1. **Get upload URL** → 2. **PUT the file to the upload URL** → 3. **Confirm** → use the `upload_id` in your brief or message references.

Max 10 references per request. URLs (max 3) can also be passed directly as references with `{"url": "https://...", "type": "url"}`. Set `"extract_content": false` at the request level to skip content extraction and pass URLs through as-is.

### POST /uploads
Get a presigned upload URL.

**Request:**
```json
{
  "file_name": "string",
  "content_type": "string",
  "file_size": 0
}
```

**Accepted types:** Images (jpeg, png, webp) max 10MB. Videos (mp4, webm, quicktime) max 500MB. Audio (mp3, wav, m4a) max 50MB.

**Response (200):**
```json
{"upload_url": "string", "r2_key": "string", "expires_in": 3600}
```

### Step 2: PUT the file
Upload the file directly to the presigned URL. Use the same content type you specified in step 1:

```bash
curl -X PUT "UPLOAD_URL_FROM_STEP_1" \
  -H "Content-Type: image/jpeg" \
  --data-binary @file.jpg
```

No authorization header; the URL is pre-authenticated. The response is empty on success (200).

### POST /uploads/confirm
Confirm upload and get an upload_id for use in briefs/messages.

**Request:**
```json
{
  "r2_key": "string",
  "file_name": "string",
  "file_size": 0,
  "content_type": "string"
}
```

**Response (201, or 200 if already confirmed):**
```json
{"upload_id": "string", "type": "image | video | audio"}
```

---

## Account

### GET /account/credits
Get current credit balance.

**Response (200):**
```json
{"credits_balance": 0}
```

### GET /account/credit-packages
List purchasable credit packages.

**Response (200):**
```json
{
  "credits_balance": 0,
  "has_subscription": true,
  "subscription_required": false,
  "packages": [{"id": "string", "credits": 0, "price": "string", "price_cents": 0, "purchase_url": "string"}]
}
```

### GET /account/learned-preferences
Read the agent's cross-project learned preferences.

**Response (200):**
```json
{"content": "string", "enabled": true, "characters": 0}
```

### PUT /account/learned-preferences
Update preferences content and/or toggle.

**Request:**
```json
{"content": "string", "enabled": true}
```

**Response (200):**
```json
{"content": "string", "enabled": true, "characters": 0}
```

### GET /account/shares
List public share links.

**Query:** `limit` (1-50, default 10), `offset`

**Response (200):**
```json
{
  "shares": [{"share_url": "string", "video_url": "string", "title": "string", "aspect_ratio": "string", "view_count": 0, "created_at": "ISO 8601"}],
  "total": 0,
  "total_views": 0,
  "has_more": true
}
```

---

## Skills

### GET /account/skills
List all skills (platform + user). Active skills share a 40,000-token budget (roughly 160,000 characters).

**Response (200):**
```json
{
  "skills": [{"id": "string", "name": "string", "is_active": true, "source": "eversince | user", "description": "string | null", "tokens": 0, "sort_order": 0}],
  "budget": {"used": 0, "limit": 40000}
}
```

### POST /account/skills
Create a custom skill. Name max 100 chars. No per-skill instruction cap; active skills share the 40,000-token budget.

**Request:**
```json
{"name": "string", "instructions": "string", "is_active": true}
```

**Response (201):**
```json
{
  "skill": {"id": "string", "name": "string", "instructions": "string", "is_active": true, "source": "user", "characters": 0, "sort_order": 0, "created_at": "ISO 8601", "updated_at": "ISO 8601"},
  "budget": {"used": 0, "limit": 40000}
}
```

### GET /account/skills/:id
Get skill detail.

**Response (200):**
```json
{
  "skill": {"id": "string", "name": "string", "is_active": true, "source": "eversince | user", "description": "string | null", "instructions": "string | null", "characters": 0, "sort_order": 0, "created_at": "ISO 8601", "updated_at": "ISO 8601"}
}
```

### PATCH /account/skills/:id
Update custom skill or toggle Eversince skill on/off. Skills stack freely; activating one does not deactivate the others. Active skills share the 40,000-token budget; activations that would exceed it return 400. Skill names must be unique; duplicate names return 400.

**Request:**
```json
{"name": "string", "instructions": "string", "is_active": true}
```

**Response (200), custom skill:**
```json
{
  "skill": {"id": "string", "name": "string", "instructions": "string", "is_active": true, "source": "user", "characters": 0, "sort_order": 0, "created_at": "ISO 8601", "updated_at": "ISO 8601"},
  "budget": {"used": 0, "limit": 40000}
}
```

**Response (200), Eversince skill toggle:**
```json
{
  "skill": {"id": "string", "name": "string", "is_active": true, "source": "eversince"}
}
```

### DELETE /account/skills/:id
Delete a custom skill. Cannot delete Eversince skills.

**Response (200):**
```json
{"deleted": true}
```

---

## Discovery

### GET /models
List available models. Fields differ by type.

**Query:** `type` (`video` or `image`)

**Response (200), video models:**
```json
{
  "models": [{
    "id": "string",
    "name": "string",
    "type": "video",
    "generation_types": ["text-to-video", "image-to-video"],
    "aspect_ratios": ["string"],
    "durations": ["4s", "6s", "8s"],
    "resolutions": ["720p", "1080p"],
    "has_sound": false,
    "supports_audio_toggle": false,
    "supports_audio_input": false,
    "supports_image_input": false,
    "supports_end_frame": false,
    "supports_multi_shot": false,
    "supports_reference_images": false,
    "max_reference_images": "number | null",
    "supports_reference_videos": false,
    "max_reference_videos": "number | null",
    "supports_video_input": false,
    "max_input_video_duration": "number | null",
    "supports_negative_prompt": false,
    "supports_camera_fixed": false,
    "supports_camera_motion": false,
    "camera_motion_options": "string[] | null",
    "max_prompt_length": 5000
  }]
}
```

**Response (200), image models:**
```json
{
  "models": [{
    "id": "string",
    "name": "string",
    "type": "image",
    "generation_types": ["text-to-image", "image-to-image"],
    "aspect_ratios": ["string"],
    "supports_image_input": false,
    "supports_reference_images": false,
    "max_reference_images": "number | null",
    "max_prompt_length": 5000
  }]
}
```

### GET /voices
List voiceover voices.

**Query:** `gender` (`male`, `female`, or `neutral`)

**Response (200):**
```json
{
  "voices": [{"name": "string", "gender": "string", "age": "string", "accent": "string", "style": "string", "description": "string"}]
}
```

### POST /estimate-cost
Estimate credit costs for planned operations.

**Request:**
```json
{
  "operations": [{
    "tool": "generate_image | generate_video | generate_audio | upscale_media | analyze_media | remove_background | motion_overlay",
    "model": "string (for image/video)",
    "type": "string (for audio: voiceover | music | sound_effect; for upscale: image | video)",
    "duration": 0,
    "count": 1,
    "sound": false,
    "resolution": "string (optional)",
    "music_model": "string (optional)"
  }]
}
```

Max 50 operations per request. Max count of 100 per operation.

**Response (200):**
```json
{
  "items": [{"operation": "string", "credits_per_unit": 0, "count": 0, "subtotal": 0, "error": "string | undefined"}],
  "total_credits": 0,
  "is_partial": false,
  "note": "string"
}
```

---

## Project Discovery & Adoption

### GET /projects/discover
List existing projects available for API adoption.

**Query:** `limit` (1-100, default 20), `offset`, `title` (search)

**Response (200):**
```json
{
  "projects": [{"project_id": "string", "title": "string | null", "aspect_ratio": "string", "project_url": "string", "created_at": "ISO 8601", "updated_at": "ISO 8601"}],
  "total": 0,
  "limit": 20,
  "offset": 0
}
```

### POST /projects/adopt
Adopt an existing project for API management.

**Request:**
```json
{"project_id": "string", "mode": "autonomous | collaborative"}
```

**Response (201, or 200 if already adopted):**
```json
{"id": "string", "status": "idle", "mode": "string", "project_url": "string"}
```

---

## API Keys

### POST /keys
Create an API key. Max 10 per account.

**Request:**
```json
{"name": "string (max 100 chars)"}
```

**Response (201):**
```json
{"id": "string", "name": "string", "key": "string (shown once)", "key_prefix": "string", "created_at": "ISO 8601", "message": "string"}
```

### GET /keys
List API keys (prefix only, no full keys).

**Response (200):**
```json
{
  "keys": [{"id": "string", "name": "string", "key_prefix": "string", "last_used_at": "ISO 8601 | null", "created_at": "ISO 8601"}]
}
```

### DELETE /keys/:id
Revoke an API key.

**Response (200):**
```json
{"id": "string", "revoked": true}
```

---

## Feedback

### POST /feedback
Report bugs or suggestions.

**Request:**
```json
{"type": "bug | suggestion | question", "message": "string (max 5,000 chars)", "project_id": "string (optional)"}
```

**Response (201):**
```json
{"received": true}
```

---

## Webhook Events

Set `webhook_url` on project creation or via settings. Webhooks fire on the following status transitions (note: `cancelled` does not fire a webhook):

| Event | Meaning |
|-------|---------|
| `running` | Agent started working |
| `generating` | Generations dispatched |
| `idle` | Agent finished its run |
| `failed` | Production failed |
| `rendering` | Video render in progress |

Payload includes all fields from `GET /projects/:id`, plus `timeline`, `assets`, and an `event` field matching the status.

**Signing:** Webhooks include `X-Eversince-Signature: sha256=<hex>` and `X-Eversince-Timestamp` headers. Verify by computing `HMAC-SHA256(signing_secret, "${timestamp}.${body}")` and comparing to the signature. Contact support@eversince.ai to set up a signing secret for your account.

**Reliability:** 10-second timeout, no retries. If your endpoint is unavailable, the event is lost. Use webhooks as optimization, fall back to polling.

---

## Error Format

All errors return:
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "status": 400
  }
}
```

Validation errors join all field errors into a single `message` string, semicolon-separated: `"brief: brief is required; mode: mode must be one of: autonomous, collaborative"`. Parse on `; ` to extract individual field errors.

---

## Rate Limits

- 30 requests per minute per user (shared across all API keys on the same account)
- 50 renders per day (`POST /projects/:id/render`)
- 500 projects per day
- 5 concurrent active projects: projects in `queued`, `running`, `generating`, or `rendering` status count toward this limit (default, configurable)

Need higher limits? Contact support@eversince.ai.
