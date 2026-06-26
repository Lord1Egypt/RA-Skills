---
name: aioz-stream
description: Interact with the AIOZ Stream API to manage videos, audio, playlists, players, webhooks, analytics, payments, chapters, and transcripts on the AIOZ decentralized streaming platform.
metadata:
openclaw:
---
# AIOZ Stream API Skill
Interact with the **AIOZ Stream API** — a Web3 decentralized streaming platform — using the user's API key pair.
**Base URL:** `https://api.aiozstream.network/api`
---
## Credential Collection
Before performing any API action, Clawbot **must** collect the user's API credentials if they have not already been provided.
Clawbot should prompt the user with two separate open-ended text input fields:
1. **AIOZ Stream Public Key** — Ask: *"Please enter your AIOZ Stream Public Key:"*
2. **AIOZ Stream Secret Key** — Ask: *"Please enter your AIOZ Stream Secret Key:"*
Rules:
- Use **open-ended text input** (not dropdowns or multiple choice) so the user can type or paste their actual key values.
- Do **not** proceed with any API call until both keys have been provided.
- Store them in session as `$AIOZ_PUBLIC_KEY` and `$AIOZ_SECRET_KEY` for use in all subsequent requests.
- Remind the user: *"Keep your keys safe — treat them like passwords and consider rotating them after this session."*
---
## Authentication
Every request **must** include these two headers:
```
stream-public-key: $AIOZ_PUBLIC_KEY
stream-secret-key: $AIOZ_SECRET_KEY
```
Helper function for all `curl` calls:
```bash
AIOZ_HEADERS=(
  -H "stream-public-key: ${AIOZ_PUBLIC_KEY}"
  -H "stream-secret-key: ${AIOZ_SECRET_KEY}"
)
```
---
## How Clawbot Should Respond to Upload Actions
When Clawbot performs any upload or encoding action on behalf of the user, it **must** use the following response templates exactly. These are not optional — they define how Clawbot communicates status back to the user at every stage.

---

### 📤 During Upload — Chunked Upload Progress

While uploading chunks, Clawbot must display a live progress block after each successful chunk:

```
## 📤 Uploading: {title}

Progress: {bar} {percent}% ({done} of {total} chunks)

| Chunk | Size   | MD5 Status | Upload Status |
|-------|--------|------------|---------------|
| 0     | 50 MB  | ✅ Valid    | ✅ Done        |
| 1     | 50 MB  | ✅ Valid    | ✅ Done        |
| 2     | 50 MB  | ✅ Valid    | ✅ Done        |
| 3     | 50 MB  | ✅ Valid    | ✅ Done        |
| 4     | 10 MB  | ✅ Valid    | ⏳ Uploading   |

> ⚠️ Clawbot will only call `/complete` after **all chunks** succeed.
```

- Replace `{title}` with the actual media title.
- Replace `{bar}` with a Unicode progress bar (e.g., `████████░░`).
- Replace `{percent}`, `{done}`, `{total}` with real values.
- Show ✅ for completed chunks, ⏳ for the current one, ❌ for failed ones.

---

### ✅ After `/media/:id/complete` — Upload Complete

When `/complete` returns successfully, Clawbot must respond with:

```
## 🎉 Upload Complete!

Your media has been successfully uploaded and is now being processed.

| Field        | Value                  |
|--------------|------------------------|
| **Media ID** | {media_id}             |
| **Title**    | {title}                |
| **Type**     | {type}                 |
| **Status**   | `transcoding`          |
| **Uploaded** | {timestamp} UTC        |

### ⏳ What's Next?
Transcoding is in progress. You will be notified via webhook once encoding is finished.

> Estimated time depends on media length and selected quality presets.
```

---

### 📡 Webhook Response Templates

When Clawbot receives or reports on a webhook event, it must use the matching template below.

#### `file_received`

```
## 📥 File Received

Your file has been received by the server and is queued for transcoding.

| Field         | Value               |
|---------------|---------------------|
| **Media ID**  | {media_id}          |
| **Title**     | {title}             |
| **Event**     | `file_received`     |
| **Status**    | `new`               |
| **Timestamp** | {timestamp} UTC     |

> Transcoding will begin shortly.
```

---

#### `encoding_started`

```
## ⚙️ Encoding Started

Your media is now being transcoded.

| Field         | Value               |
|---------------|---------------------|
| **Media ID**  | {media_id}          |
| **Title**     | {title}             |
| **Event**     | `encoding_started`  |
| **Status**    | `transcoding`       |
| **Timestamp** | {timestamp} UTC     |

> Please wait while your media is being processed across all selected quality presets.
```

---

#### `partial_finished`

```
## 🔄 Partial Quality Ready

One quality preset has finished encoding and is available for streaming.

| Field         | Value               |
|---------------|---------------------|
| **Media ID**  | {media_id}          |
| **Title**     | {title}             |
| **Event**     | `partial_finished`  |
| **Status**    | `transcoding`       |
| **Timestamp** | {timestamp} UTC     |

> Remaining quality presets are still processing. Full availability coming soon.
```

---

#### `encoding_finished`

```
## ✅ Encoding Finished — Media is Live!

| Field         | Value                |
|---------------|----------------------|
| **Media ID**  | {media_id}           |
| **Title**     | {title}              |
| **Event**     | `encoding_finished`  |
| **Status**    | `done`               |
| **Timestamp** | {timestamp} UTC      |

### 🔗 Your media is ready to stream!

**HLS**
- Stream URL:  `https://api.aiozstream.network/api/media/{media_id}/manifest.m3u8`
- Player URL:  `https://embed.aiozstream.network/vod/hls/{media_id}`
- Embed:       `<iframe src="https://embed.aiozstream.network/vod/hls/{media_id}" width="100%" height="100%" frameborder="0" scrolling="no" allowfullscreen="true"></iframe>`

**DASH**
- Stream URL:  `https://api.aiozstream.network/api/media/{media_id}/manifest`
- Player URL:  `https://embed.aiozstream.network/vod/dash/{media_id}`
- Embed:       `<iframe src="https://embed.aiozstream.network/vod/dash/{media_id}" width="100%" height="100%" frameborder="0" scrolling="no" allowfullscreen="true"></iframe>`

**Other**
- Thumbnail:   `https://api.aiozstream.network/api/media/{media_id}/thumbnail?resolution=original`
- MP4:         `https://api.aiozstream.network/api/media/{media_id}/mp4`
- Source:      `https://api.aiozstream.network/api/media/{media_id}/source`

### 🛠️ Suggested Next Steps
- [ ] Assign a Player Theme  →  ask Clawbot: "assign a player to my video"
- [ ] Add Chapters           →  ask Clawbot: "add chapters to my video"
- [ ] Add Subtitles          →  ask Clawbot: "add subtitles to my video"
- [ ] Add to a Playlist      →  ask Clawbot: "add my video to a playlist"
- [ ] Review Analytics       →  ask Clawbot: "show me analytics for my video"
```

---

#### `encoding_failed`

```
## ❌ Encoding Failed

Something went wrong during transcoding.

| Field         | Value               |
|---------------|---------------------|
| **Media ID**  | {media_id}          |
| **Title**     | {title}             |
| **Event**     | `encoding_failed`   |
| **Status**    | `fail`              |
| **Timestamp** | {timestamp} UTC     |

### ⚠️ How to Retry
Clawbot will automatically guide you through the following steps:

1. Delete the failed media object       →  `DELETE /media/{media_id}`
2. Re-create the media object           →  `POST /media/create`
3. Check transcode cost before retrying →  `GET /media/cost` (verify `is_enough: true`)
4. Re-upload all chunks                 →  `POST /media/:id/part` (one per chunk with MD5)
5. Signal completion                    →  `GET /media/:id/complete`

> Ask Clawbot: "retry my failed upload" to start the process automatically.
```

---

### 🔔 Webhook Event Quick Reference

| Event               | Status After  | Clawbot Response                      |
|---------------------|---------------|---------------------------------------|
| `file_received`     | `new`         | 📥 File received, queuing transcode…  |
| `encoding_started`  | `transcoding` | ⚙️ Encoding started…                  |
| `partial_finished`  | `transcoding` | 🔄 Partial quality preset ready       |
| `encoding_finished` | `done`        | ✅ Your media is ready to stream!     |
| `encoding_failed`   | `fail`        | ❌ Encoding failed. Clawbot will guide you through a retry. |

---

## 1. VIDEO MANAGEMENT

### Create a video object

```bash
curl -s -X POST "https://api.aiozstream.network/api/media/create" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Video",
    "type": "video",
    "description": "optional",
    "is_public": true,
    "tags": ["tag1"],
    "metadata": [{"key": "genre", "value": "rock"}],
    "qualities": [
      {
        "resolution": "1080p",
        "type": "hls",
        "container_type": "mpegts",
        "video_config": { "codec": "h264", "bitrate": 5000000, "index": 0 },
        "audio_config": { "codec": "aac", "bitrate": 192000, "channels": "2", "sample_rate": 48000, "language": "en", "index": 0 }
      }
    ]
  }'
```

**Rules:**
- `type` must be `"video"` (required)
- Supported resolutions: `240p`, `360p`, `480p`, `720p`, `1080p`, `1440p`, `2160p`, `4320p`
- Video codecs: `h264` (max 4K), `h265` (max 8K)
- ⚠️ H.265 on Apple (Safari/iOS): **must** use `container_type: "fmp4"`, NOT `"mpegts"`
- If `qualities` is omitted, the server applies default encoding

**Before creating a video with custom qualities**, Clawbot must check transcode cost first:

```bash
curl -s "https://api.aiozstream.network/api/media/cost?type=video&duration=60&qualities=360p,1080p" \
  "${AIOZ_HEADERS[@]}"
# Returns: { "price": 1.23, "is_enough": true }
# Only proceed if is_enough is true
```

If `is_enough` is `false`, Clawbot must inform the user:
> ⚠️ Your account balance is insufficient to transcode with the requested quality presets. Please top up your AIOZ wallet before proceeding.

### List / Search videos

```bash
curl -s -X POST "https://api.aiozstream.network/api/media" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "video",
    "limit": 25,
    "offset": 0,
    "sort_by": "created_at",
    "order_by": "desc",
    "search": "keyword",
    "status": "done",
    "tags": "tag1,tag2",
    "metadata": {"genre": "rock"}
  }'
```

`status` options: `new`, `transcoding`, `done`, `fail`, `deleted`

### Get video detail

```bash
curl -s "https://api.aiozstream.network/api/media/${VIDEO_ID}" \
  "${AIOZ_HEADERS[@]}"
```

### Upload video (chunked — 50MB–200MB per chunk)

**Step 1 — Upload each chunk:**

```bash
# For each chunk (0-indexed):
CHUNK_INDEX=0
CHUNK_START=0
CHUNK_END=52428799   # end byte (inclusive)
TOTAL_SIZE=104857600
CHUNK_MD5=$(md5sum chunk_file | awk '{print $1}')

curl -s -X POST "https://api.aiozstream.network/api/media/${VIDEO_ID}/part" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Range: bytes ${CHUNK_START}-${CHUNK_END}/${TOTAL_SIZE}" \
  -F "file=@chunk_file" \
  -F "index=${CHUNK_INDEX}" \
  -F "hash=${CHUNK_MD5}"
```

**Step 2 — Signal completion (after ALL chunks uploaded):**

```bash
curl -s "https://api.aiozstream.network/api/media/${VIDEO_ID}/complete" \
  "${AIOZ_HEADERS[@]}"
```

> ⚠️ Clawbot must always compute the correct MD5 hash per chunk. Call `/complete` only after all chunks succeed.

### Update video info

```bash
curl -s -X PATCH "https://api.aiozstream.network/api/media/${VIDEO_ID}" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Title",
    "description": "...",
    "is_public": true,
    "tags": ["tag1"],
    "metadata": [{"key": "k", "value": "v"}],
    "player_theme_id": "optional"
  }'
```

### Upload video thumbnail

```bash
curl -s -X POST "https://api.aiozstream.network/api/media/${VIDEO_ID}/thumbnail" \
  "${AIOZ_HEADERS[@]}" \
  -F "file=@thumbnail.png"
# File must be .png or .jpg
```

### Delete video

```bash
curl -s -X DELETE "https://api.aiozstream.network/api/media/${VIDEO_ID}" \
  "${AIOZ_HEADERS[@]}"
```

---

## 2. AUDIO MANAGEMENT

Audio uses the **same endpoints** as video but with `type: "audio"`. Key differences:
- `resolution` uses presets: `standard`, `good`, `highest`, `lossless`
- Only `audio_config` is needed (no `video_config`)
- Response does **not** include `mp4_url`

### Create an audio object

```bash
curl -s -X POST "https://api.aiozstream.network/api/media/create" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Podcast",
    "type": "audio",
    "qualities": [
      {
        "resolution": "highest",
        "type": "hls",
        "container_type": "mpegts",
        "audio_config": { "codec": "aac", "bitrate": 320000, "channels": "2", "sample_rate": 44100, "language": "en", "index": 0 }
      }
    ]
  }'
```

### Calculate audio transcode price

```bash
curl -s "https://api.aiozstream.network/api/media/cost?type=audio&duration=60&qualities=highest,standard" \
  "${AIOZ_HEADERS[@]}"
```

All other operations (list, detail, upload part, complete, update, delete) use the same endpoints as video, with `AUDIO_ID` in place of `VIDEO_ID`.

---

## 3. MEDIA CHAPTERS

Chapters are stored per language in `.vtt` format. Each `(media_id, language)` pair holds at most **one** chapter.

`lan` accepts BCP 47 tags: `en`, `vi`, `en-US`, `fr-CA`, etc.

### Add chapter

```bash
curl -s -X POST "https://api.aiozstream.network/api/media/${MEDIA_ID}/chapters/${LAN}" \
  "${AIOZ_HEADERS[@]}" \
  -F "file=@chapters.vtt"
```

### List chapters

```bash
curl -s "https://api.aiozstream.network/api/media/${MEDIA_ID}/chapters?offset=0&limit=10" \
  "${AIOZ_HEADERS[@]}"
```

### Delete chapter

```bash
curl -s -X DELETE "https://api.aiozstream.network/api/media/${MEDIA_ID}/chapters/${LAN}" \
  "${AIOZ_HEADERS[@]}"
```

---

## 4. MEDIA TRANSCRIPTS (Subtitles / Captions)

Transcripts are `.vtt` files, one per language per media. Can be set as default for the player.

> ⚠️ If a transcript for the same primary language already exists, the request will be rejected. Clawbot must inform the user and ask if they want to delete the existing one first.

### Add transcript

```bash
curl -s -X POST "https://api.aiozstream.network/api/media/${MEDIA_ID}/transcripts/${LAN}" \
  "${AIOZ_HEADERS[@]}" \
  -F "file=@transcript.vtt"
```

### List transcripts

```bash
curl -s "https://api.aiozstream.network/api/media/${MEDIA_ID}/transcripts?offset=0&limit=10" \
  "${AIOZ_HEADERS[@]}"
```

### Set default transcript

```bash
curl -s -X PATCH "https://api.aiozstream.network/api/media/${MEDIA_ID}/transcripts/${LAN}" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{"is_default": true}'
```

### Delete transcript

```bash
curl -s -X DELETE "https://api.aiozstream.network/api/media/${MEDIA_ID}/transcripts/${LAN}" \
  "${AIOZ_HEADERS[@]}"
```

> If the deleted transcript was the default, the system clears the default. Clawbot must remind the user to set a new default manually.

---

## 5. API KEY MANAGEMENT

### Create API key

```bash
curl -s -X POST "https://api.aiozstream.network/api/api_keys" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key_name": "my key",
    "ttl": "100000000",
    "type": "full_access"
  }'
# type: "full_access" or "only_upload"
# ttl: seconds, max 2147483647
```

> ⚠️ **The `secret` is shown only once. Clawbot must immediately display it to the user and explicitly warn them it cannot be retrieved again.**

### List API keys

```bash
curl -s "https://api.aiozstream.network/api/api_keys?search=name&limit=25&offset=0&sort_by=created_at&order_by=asc" \
  "${AIOZ_HEADERS[@]}"
```

### Update API key name

```bash
curl -s -X PATCH "https://api.aiozstream.network/api/api_keys/${API_KEY_ID}" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{"api_key_name": "new name"}'
```

### Delete API key

```bash
curl -s -X DELETE "https://api.aiozstream.network/api/api_keys/${API_KEY_ID}" \
  "${AIOZ_HEADERS[@]}"
```

---

## 6. USER INFO

### Get current user

```bash
curl -s "https://api.aiozstream.network/api/user/me" \
  "${AIOZ_HEADERS[@]}"
# Returns: id, first_name, last_name, email, wallet_address, balance, debt, etc.
```

---

## 7. WEBHOOKS

Events available: `file_received`, `encoding_started`, `partial_finished`, `encoding_finished`, `encoding_failed`

### Create webhook

```bash
curl -s -X POST "https://api.aiozstream.network/api/webhooks" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my webhook",
    "url": "https://your-server.com/hook",
    "file_received": false,
    "encoding_started": true,
    "partial_finished": true,
    "encoding_finished": true,
    "encoding_failed": true
  }'
```

### List webhooks

```bash
curl -s "https://api.aiozstream.network/api/webhooks?limit=25&offset=0&sort_by=created_at&order_by=asc" \
  "${AIOZ_HEADERS[@]}"
```

### Get webhook detail

```bash
curl -s "https://api.aiozstream.network/api/webhooks/${WEBHOOK_ID}" \
  "${AIOZ_HEADERS[@]}"
```

### Update webhook

```bash
curl -s -X PATCH "https://api.aiozstream.network/api/webhooks/${WEBHOOK_ID}" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://new-url.com",
    "name": "updated name",
    "encoding_started": false,
    "encoding_finished": true,
    "encoding_failed": true,
    "partial_finished": true,
    "file_received": false
  }'
```

### Test / trigger webhook

```bash
curl -s -X POST "https://api.aiozstream.network/api/webhooks/check/${WEBHOOK_ID}" \
  "${AIOZ_HEADERS[@]}"
```

> Clawbot must use `/webhooks/check/:id` to verify a webhook URL is reachable before confirming it to the user.

### Delete webhook

```bash
curl -s -X DELETE "https://api.aiozstream.network/api/webhooks/${WEBHOOK_ID}" \
  "${AIOZ_HEADERS[@]}"
```

---

## 8. PLAYERS

Player themes allow full visual customization of the embedded player.

**Color rule:** all colors must be `rgba(...)` format.  
**Size rule:** all sizes must be `px` format.  
Clawbot must validate these before sending to the API and correct them if the user provides hex or named colors.

### Create player theme

```bash
curl -s -X POST "https://api.aiozstream.network/api/players" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Brand Player",
    "theme": {
      "main_color": "rgba(255, 0, 0, 1)",
      "text_color": "rgba(255, 255, 255, 1)",
      "control_bar_background_color": "rgba(0, 0, 0, 0.7)",
      "menu_background_color": "rgba(30, 30, 30, 1)",
      "menu_item_background_hover": "rgba(60, 60, 60, 1)",
      "text_track_color": "rgba(255, 255, 255, 1)",
      "text_track_background": "rgba(0, 0, 0, 0.5)",
      "control_bar_height": "40px",
      "progress_bar_height": "4px",
      "progress_bar_circle_size": "12px"
    }
  }'
```

### List player themes

```bash
curl -s "https://api.aiozstream.network/api/players?limit=25&offset=0&sort_by=created_at&order_by=asc&search=name" \
  "${AIOZ_HEADERS[@]}"
```

### Get player theme detail

```bash
curl -s "https://api.aiozstream.network/api/players/${PLAYER_THEME_ID}" \
  "${AIOZ_HEADERS[@]}"
```

### Update player theme

```bash
curl -s -X PATCH "https://api.aiozstream.network/api/players/${PLAYER_THEME_ID}" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "updated name",
    "theme": { "main_color": "rgba(0, 128, 255, 1)" },
    "controls": {
      "enable_api": true,
      "enable_controls": true,
      "force_autoplay": false,
      "hide_title": false,
      "force_loop": false
    },
    "is_default": true
  }'
# Setting is_default: true automatically clears is_default on all other players
# CDN propagation may take up to 10 minutes
```

> Clawbot must warn the user: CDN propagation for player theme changes may take up to **10 minutes**.

### Upload player logo

```bash
curl -s -X POST "https://api.aiozstream.network/api/players/${PLAYER_THEME_ID}/logo" \
  "${AIOZ_HEADERS[@]}" \
  -F "file=@logo.png" \
  -F "logo_link=https://yoursite.com"
# JPEG or PNG only, max 100KB, max 200×100px
```

### Delete player logo

```bash
curl -s -X DELETE "https://api.aiozstream.network/api/players/${PLAYER_THEME_ID}/logo" \
  "${AIOZ_HEADERS[@]}"
```

### Assign player theme to video

```bash
curl -s -X POST "https://api.aiozstream.network/api/players/add-player" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{"video_id": "VIDEO_ID", "player_theme_id": "PLAYER_THEME_ID"}'
```

### Delete player theme

```bash
curl -s -X DELETE "https://api.aiozstream.network/api/players/${PLAYER_THEME_ID}" \
  "${AIOZ_HEADERS[@]}"
# Cannot delete if the player is currently assigned to a video
```

> If the delete fails because the player is assigned to a video, Clawbot must inform the user and ask if they want to unassign it first.

---

## 9. ANALYTICS

All analytics endpoints are `POST` with time range in **UNIX timestamps**.

> Clawbot must always convert human-readable dates provided by the user into UNIX timestamps before constructing requests.

### Aggregated metrics (single number)

```bash
# metric: play, start, end, impression, watch_time, view
# aggregation: count, rate (play only), total, average, sum
curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/data/${METRIC}/${AGGREGATION}" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "from": 1726001314,
    "to": 1726201314,
    "filter_by": {
      "media_ids": ["id1", "id2"],
      "media_type": "video",
      "continents": ["AS", "EU"],
      "countries": ["VN", "US"],
      "device_types": ["computer", "phone"],
      "os": ["windows", "android"],
      "browsers": ["chrome", "firefox"],
      "tags": ["tag1"]
    }
  }'
```

### Breakdown by dimension

```bash
# metric: play, play_rate, start, end, impression, watch_time, retention, view
# breakdown: media-id, media-type, continent, country, device-type, operating-system, browser
curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/bucket/${METRIC}/${BREAKDOWN}" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "from": 1726001314,
    "to": 1726201314,
    "limit": 100,
    "offset": 0,
    "sort_by": "metric_value",
    "order_by": "desc",
    "filter_by": {}
  }'
```

### Time series (metrics over time)

```bash
# interval: hour, day
curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/timeseries/${METRIC}/${INTERVAL}" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "from": 1726001314,
    "to": 1726201314,
    "limit": 100,
    "offset": 0,
    "sort_by": "metric_value",
    "order_by": "desc",
    "filter_by": {}
  }'
```

---

## 10. PAYMENTS

### Get usage statistics

```bash
curl -s "https://api.aiozstream.network/api/payment/usage?from=1714232234&to=1824232234" \
  "${AIOZ_HEADERS[@]}"
# Returns: storage (bytes), delivery (bytes), transcode (seconds), and their costs
```

### Get top-up history

```bash
curl -s "https://api.aiozstream.network/api/payment/top_ups?limit=10&offset=0&orderBy=desc&sortBy=created_at" \
  "${AIOZ_HEADERS[@]}"
# transaction_id: on-chain tx hash viewable on AIOZ Explorer
# status: pending, success, failed
```

### Get billing history

```bash
curl -s "https://api.aiozstream.network/api/payment/billings?limit=10&offset=0&orderBy=desc" \
  "${AIOZ_HEADERS[@]}"
# Returns monthly breakdown: storage, delivery, transcode + costs
```

---

## 11. PLAYLISTS

Playlists use a **linked-list** structure internally (`next_id` / `previous_id`) for item ordering.

> Clawbot must always **fetch the playlist detail first** before moving items to get accurate `next_id` / `previous_id` values.

### Create playlist

```bash
curl -s -X POST "https://api.aiozstream.network/api/playlists/create" \
  "${AIOZ_HEADERS[@]}" \
  -F "name=My Playlist" \
  -F "tags=tag1,tag2" \
  -F 'metadata={"key":"val"}'
```

### List playlists

```bash
curl -s -X POST "https://api.aiozstream.network/api/playlists" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "limit": 10,
    "offset": 0,
    "sort_by": "name",
    "order_by": "asc",
    "search": "playlist name",
    "tags": "tag1",
    "metadata": {"key": "val"}
  }'
```

### Get playlist detail (with video items)

```bash
curl -s "https://api.aiozstream.network/api/playlists/${PLAYLIST_ID}?sort_by=created_at&order_by=asc" \
  "${AIOZ_HEADERS[@]}"
# Omit sort_by/order_by to get items in their custom linked-list order
```

### Update playlist

```bash
curl -s -X PATCH "https://api.aiozstream.network/api/playlists/${PLAYLIST_ID}" \
  "${AIOZ_HEADERS[@]}" \
  -F "name=New Name" \
  -F "file=@thumbnail.jpg" \
  -F "tags=tag1" \
  -F 'metadata={"key":"val"}'
# file: optional thumbnail (.jpg, .jpeg, .png)
```

### Add video to playlist

```bash
curl -s -X POST "https://api.aiozstream.network/api/playlists/${PLAYLIST_ID}/items" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{"video_id": "VIDEO_ID"}'
```

### Move video position in playlist

```bash
curl -s -X PUT "https://api.aiozstream.network/api/playlists/${PLAYLIST_ID}/items" \
  "${AIOZ_HEADERS[@]}" \
  -H "Content-Type: application/json" \
  -d '{
    "current_id": "ITEM_TO_MOVE_ID",
    "next_id": "ITEM_THAT_WILL_COME_AFTER",
    "previous_id": "ITEM_THAT_WILL_COME_BEFORE"
  }'
```

**Positioning reference (`current_id` is always required):**
- Move to **top**: set only `next_id` to the current first item's ID
- Move to **bottom**: set only `previous_id` to the current last item's ID
- Move **between** two items: set both `next_id` and `previous_id`

### Remove video from playlist

```bash
curl -s -X DELETE "https://api.aiozstream.network/api/playlists/${PLAYLIST_ID}/items/${ITEM_ID}" \
  "${AIOZ_HEADERS[@]}"
```

### Delete playlist thumbnail

```bash
curl -s -X DELETE "https://api.aiozstream.network/api/playlists/${PLAYLIST_ID}/thumbnail" \
  "${AIOZ_HEADERS[@]}"
```

### Delete playlist

```bash
curl -s -X DELETE "https://api.aiozstream.network/api/playlists/${PLAYLIST_ID}" \
  "${AIOZ_HEADERS[@]}"
```

---

## Behavior Guidelines

Clawbot must follow these rules when operating this skill:

1. **Always include both auth headers** (`stream-public-key` and `stream-secret-key`) on every request, including `/user/me`.
2. **Chunked uploads:** calculate chunk boundaries correctly. Each chunk needs its MD5. Call `/complete` only after all chunks succeed. Display the chunked upload progress template at each step.
3. **Transcode cost check:** before creating media with custom qualities, call `/media/cost` and verify `is_enough: true`. If `false`, block the action and notify the user to top up.
4. **Player colors/sizes:** validate that colors are in `rgba(...)` format and sizes are in `px`. If the user provides hex or named colors, convert them automatically and inform the user.
5. **Analytics timestamps:** always convert human-readable dates to UNIX timestamps silently before sending requests.
6. **Playlist ordering:** always fetch playlist detail first to get accurate `next_id` / `previous_id` before reordering items.
7. **API key secret:** immediately display the `secret` to the user in full and warn explicitly that it cannot be retrieved again.
8. **Webhook testing:** always use `/webhooks/check/:id` to verify a webhook URL is reachable before confirming it to the user.
9. **H.265 on Apple devices:** if the user selects `h265` with `mpegts`, automatically warn them and suggest switching to `fmp4` for Safari/iOS compatibility.
10. **Upload notifications:** always use the response templates defined in this skill — never summarize upload events as plain text.

---

## Quick Reference — Endpoints

| Module     | Method | Path                                              |
|------------|--------|---------------------------------------------------|
| Video      | POST   | `/media/create`                                   |
| Video      | POST   | `/media` (list)                                   |
| Video      | GET    | `/media/:id`                                      |
| Video      | GET    | `/media/cost`                                     |
| Video      | POST   | `/media/:id/part`                                 |
| Video      | GET    | `/media/:id/complete`                             |
| Video      | PATCH  | `/media/:id`                                      |
| Video      | POST   | `/media/:id/thumbnail`                            |
| Video      | DELETE | `/media/:id`                                      |
| Audio      | —      | (same paths as Video, `type=audio`)               |
| Chapter    | POST   | `/media/:id/chapters/:lan`                        |
| Chapter    | GET    | `/media/:id/chapters`                             |
| Chapter    | DELETE | `/media/:id/chapters/:lan`                        |
| Transcript | POST   | `/media/:id/transcripts/:lan`                     |
| Transcript | GET    | `/media/:id/transcripts`                          |
| Transcript | PATCH  | `/media/:id/transcripts/:lan`                     |
| Transcript | DELETE | `/media/:id/transcripts/:lan`                     |
| API Keys   | POST   | `/api_keys`                                       |
| API Keys   | GET    | `/api_keys`                                       |
| API Keys   | PATCH  | `/api_keys/:id`                                   |
| API Keys   | DELETE | `/api_keys/:id`                                   |
| Users      | GET    | `/user/me`                                        |
| Webhooks   | POST   | `/webhooks`                                       |
| Webhooks   | GET    | `/webhooks`                                       |
| Webhooks   | GET    | `/webhooks/:id`                                   |
| Webhooks   | PATCH  | `/webhooks/:id`                                   |
| Webhooks   | DELETE | `/webhooks/:id`                                   |
| Webhooks   | POST   | `/webhooks/check/:id`                             |
| Players    | POST   | `/players`                                        |
| Players    | GET    | `/players`                                        |
| Players    | GET    | `/players/:id`                                    |
| Players    | PATCH  | `/players/:id`                                    |
| Players    | DELETE | `/players/:id`                                    |
| Players    | POST   | `/players/:id/logo`                               |
| Players    | DELETE | `/players/:id/logo`                               |
| Players    | POST   | `/players/add-player`                             |
| Analytics  | POST   | `/analytics/metrics/data/:metric/:aggregation`    |
| Analytics  | POST   | `/analytics/metrics/bucket/:metric/:breakdown`    |
| Analytics  | POST   | `/analytics/metrics/timeseries/:metric/:interval` |
| Payments   | GET    | `/payment/usage`                                  |
| Payments   | GET    | `/payment/top_ups`                                |
| Payments   | GET    | `/payment/billings`                               |
| Playlists  | POST   | `/playlists/create`                               |
| Playlists  | POST   | `/playlists` (list)                               |
| Playlists  | GET    | `/playlists/:id`                                  |
| Playlists  | PATCH  | `/playlists/:id`                                  |
| Playlists  | POST   | `/playlists/:id/items`                            |
| Playlists  | PUT    | `/playlists/:id/items` (reorder)                  |
| Playlists  | DELETE | `/playlists/:id/items/:item_id`                   |
| Playlists  | DELETE | `/playlists/:id/thumbnail`                        |
| Playlists  | DELETE | `/playlists/:id`                                  |

---

## ⚠️ General Warnings & Reminders

| Scenario                      | Clawbot Action Required                                                                        |
|-------------------------------|-----------------------------------------------------------------------------------------------|
| H.265 on Apple devices        | Warn user and suggest `container_type: "fmp4"` — `"mpegts"` will NOT work on Safari/iOS      |
| Insufficient balance          | Block the action and tell user to top up before proceeding                                    |
| Custom quality presets        | Always call `/media/cost` first — only proceed if `is_enough: true`                           |
| Chunked upload                | Compute MD5 per chunk. Never call `/complete` until all chunks succeed                        |
| Duplicate transcript language | Inform user, ask if they want to delete the existing transcript first                         |
| Player color format           | Convert hex/named colors to `rgba(...)` automatically, inform user of the conversion          |
| Player size format            | Ensure all sizes are in `px` before sending                                                   |
| New API key secret            | Display the `secret` immediately and warn it cannot be retrieved again                        |
| Webhook URL not reachable     | Run `/webhooks/check/:id` and report result before confirming webhook is active               |
| Analytics date input          | Silently convert human-readable dates to UNIX timestamps before querying                      |
| Playlist reordering           | Always fetch playlist detail first to get accurate `next_id` / `previous_id`                 |
| Player `is_default` change    | Warn user: setting a new default clears all others. CDN propagation may take up to 10 minutes |
| Player logo upload            | Reject if over 100KB or larger than 200×100px — must be JPEG or PNG                          |
| Deleted default transcript    | Remind user to set a new default transcript after deletion                                    |
| Player assigned to video      | Cannot delete player theme — ask user if they want to unassign it from the video first        |