# ControlFoley Audio Generator API Reference

Base URL: `https://controlfoley.ai.xiaomi.com`  
Auth: None required

**Known API quirks (from real testing):**
- Submit response may return either `task_id` or `taskId` (camelCase); code handles both
- Status success may return either `processed_urls` or `urls`; code checks both
- Result URLs may use internal `.xiaomi.srv` domains; use download endpoint as fallback

## Endpoints

### POST `/api/v1/v2a/submit` — Submit Task

Content-Type: `multipart/form-data`

#### T2A (Text-to-Audio)

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| prompt | string | Yes | — | Audio description (e.g. `dog barking in park`) |
| negative | string | Optional | — | What to avoid; omitted if empty |
| duration | float | Optional | `8.0` | Audio length in seconds (max 30) |
| count | int | Optional | `1` | Number of results (1–5) |
| seed | int | Optional | — | Fixed seed for reproducibility; omitted if not set |
| cfg | float | Optional | `4.5` | CFG strength |
| outdir | string | Optional | "./output" | Output directory |

#### V2A (Video-to-Audio)

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| video | file | Yes | — | Video file (.mp4/.webm/.mov) |
| prompt | string | Optional | — | Text prompt to guide audio generation; omitted if empty |
| negative | string | Optional | — | What to avoid; omitted if empty |
| ref_audio | file | Optional | — | Reference audio for AC-V2A task; omitted if file not found |
| count | int | Optional | `1` | Number of results (1–5) |
| seed | int | Optional | — | Fixed seed for reproducibility; omitted if not set |
| cfg | float | Optional | `4.5` | CFG strength |
| outdir | string | Optional | "./output" | Output directory |

> Note: `seed` is accepted in the V2A function signature but not currently forwarded to the API.

**Response (202):**
```json
{"task_id": "uuid", "status": "pending", "queue_pos": 2, "message": "Task submitted successfully"}
```
> Note: field may appear as `taskId` (camelCase) — handle both.

### GET `/api/v1/v2a/status/{task_id}` — Poll Status

**Pending/Processing:**
```json
{"status": "pending|processing", "queue_pos": 3}
```

**Success:**
```json
{
  "status": "success", "done": true,
  "processed_urls": ["http://.../uuid.flac", "http://.../uuid.mp4"]
}
```
> Note: result URLs field may appear as `urls` — handle both `processed_urls` and `urls`.

**Failed:**
```json
{"status": "failed", "done": true, "error": "reason"}
```

### GET `/api/v1/v2a/ControlFoley_output/{task_id}/{filename}` — Download Result

Fallback download endpoint for internal URLs that are not directly accessible.  
Returns binary file stream (.flac at 44100 Hz or .mp4).

### GET `/api/v1/v2a/models` — List Models

```json
{"models": [{"name": "ControlFoley", "enabled": true}]}
```

### GET `/health` — Health Check

```json
{"status": "ok", "queue_size": 3}
```

## Models

| Model | Use Case |
|-------|----------|
| ControlFoley | General T2A and V2A (default) |

## Modes

| Mode | Input | Output | Description |
|------|-------|--------|-------------|
| T2A | prompt | .flac | Generate audio from text descriptions |
| V2A | video file | .mp4 + .flac | Generate audio that matches video content |
| TC-V2A | prompt + video file | .mp4 + .flac | Generate audio aligned with text prompts while staying synchronized with the video |
| AC-V2A | reference_audio + video file | .mp4 + .flac | Generate audio with timbre matching reference audio while staying synchronized with the video |
