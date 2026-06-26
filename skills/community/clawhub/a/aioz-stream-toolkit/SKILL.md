---
name: aioz-stream-toolkit
description: Respond to user requests for AIOZ Stream API. Use provided scripts to upload videos, fetch analytics, manage media, and create livestreams.
metadata:
  openclaw:
    emoji: "🎥"
    requires:
      envVars:
        - name: STREAM_PUBLIC_KEY
          description: AIOZ Stream public API key
          required: true
          primaryCredential: true
        - name: STREAM_SECRET_KEY
          description: AIOZ Stream secret API key
          required: true
      bins:
        - curl
        - jq
        - md5sum
        - file
        - stat
        - date
---

# AIOZ Stream Operations

Interact with AIOZ Stream API quickly with API key authentication. A suite of integrated bash scripts is provided to automatically call REST APIs.

## When to use this skill

- User wants to upload or create a video on AIOZ Stream
- User mentions "upload video", "create video", "aioz stream video"
- User wants to query analytics, livestream keys, or account balances
- User wants to get an HLS/MP4 streaming link for their video
- User wants to search/list media or find a video by name

## Authentication

This skill uses API key authentication via environment variables:

- `STREAM_PUBLIC_KEY`: Your AIOZ Stream public key (provided by the platform)
- `STREAM_SECRET_KEY`: Your AIOZ Stream secret key (provided by the platform)

Credential-safe policy:

- Prefer credentials from secure environment injection.
- If missing, ask the user for credentials and set them as temporary environment variables.
- Never hardcode keys in command examples, logs, or responses.
- Avoid inline one-off commands that contain raw secrets.

If credentials are not present in the shell session, set them once before running scripts:

```bash
export STREAM_PUBLIC_KEY="YOUR_STREAM_PUBLIC_KEY"
export STREAM_SECRET_KEY="YOUR_STREAM_SECRET_KEY"
```

Header mapping used by scripts:

- `STREAM_PUBLIC_KEY` -> `stream-public-key` header
- `STREAM_SECRET_KEY` -> `stream-secret-key` header

This keeps credentials out of repeated command history and avoids accidental exposure.

## Usage Options (Available Scripts)

When the user asks for a feature, use one of the bash scripts located in the `scripts/` directory.

### Script Routing Map (for Clawbot)

- Upload local file to video: `./scripts/upload_video_file.sh FILE_PATH "TITLE"`
- Get media list (GET with optional query params): `./scripts/get_media_list.sh [SEARCH] [PAGE]`
- Get media list via POST body (search/page): `./scripts/get_total_media.sh [SEARCH] [PAGE]`
- Get all media via POST `{}`: `./scripts/get_video_list.sh`
- Search media by name via POST body: `./scripts/get_video_url_by_name.sh "VIDEO_NAME"`
- Create livestream key: `./scripts/create_livestream_key.sh "KEY_NAME"`
- Get account/user info and balance: `./scripts/get_balance.sh`
- Get usage data (fixed interval=hour): `./scripts/get_usage_data.sh FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
- Get aggregate analytics (watch_time + view_count): `./scripts/get_aggregate_metric.sh TYPE FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
- Get breakdown analytics (device/os/country/browser): `./scripts/get_breakdown_metric.sh TYPE FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
- Combined aggregate + breakdown report: `./scripts/analytic_data.sh TYPE FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`

### 1. Upload Video (Credential-Safe Default Flow)

Use this script to automatically create a video object, upload the file, and complete the flow:

```bash
./scripts/upload_video_file.sh "/path/to/video.mp4" "Video Title"
```

Actual behavior in script:

- Accepts local file path only.
- Validates video by extension (and by MIME where possible).
- File must exist on the local system.

### 2. Analytics & Usage

To get metrics or account usage:

- **Usage Data:** `./scripts/get_usage_data.sh FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
  - Calls `GET /analytics/data?from=...&to=...&interval=hour`
  - `FROM`/`TO` must be `dd/mm/yyyy` format (scripts convert to Unix timestamp)
- **Aggregate Metrics:** `./scripts/get_aggregate_metric.sh TYPE FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
  - Returns: Watch time sum + View count for selected media type
  - `TYPE` must be `video` or `audio`
- **Breakdown Metrics:** `./scripts/get_breakdown_metric.sh TYPE FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
  - Returns: Device type, Operating system, Country, Browser breakdowns (with total count and data array)
  - `TYPE` must be `video` or `audio`
- **All-in-one Analytics:** `./scripts/analytic_data.sh TYPE FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
  - Returns: Combined aggregate metrics + all breakdown metrics in one call
  - `TYPE` must be `video` or `audio`

Date format notes:

- `FROM` and `TO` must be `dd/mm/yyyy` (scripts convert to Unix timestamp internally)

### 3. Media & Livestream Management

To search existing media, get balance, or create keys:

- **List Media:** `./scripts/get_media_list.sh [SEARCH] [PAGE]`
- **Total Media:** `./scripts/get_total_media.sh [SEARCH] [PAGE]`
- **Video List:** `./scripts/get_video_list.sh`
- **Search Video URL:** `./scripts/get_video_url_by_name.sh "Video Name"`
- **Livestream Key:** `./scripts/create_livestream_key.sh "Key Name"`
- **Balance:** `./scripts/get_balance.sh`

Notes:

- `get_video_list.sh` currently returns all media (`POST /media` with empty body), not strictly video-only filtering.
- `get_video_url_by_name.sh` currently returns search results JSON; it does not extract one URL field automatically.

## Full Upload Flow (Common Operational Path)

For a typical upload lifecycle, use this sequence:

1. Create media object
2. Upload media part
3. Complete upload
4. Fetch media detail
5. Print status and URLs (`hls_player_url`, `hls_url`, `mp4_url`)

If using manual `curl`, the core upload flow is the first 3 steps below.

### Step 1: Create Video Object

```bash
curl -s -X POST 'https://api.aiozstream.network/api/media/create' \
  -H "stream-public-key: $STREAM_PUBLIC_KEY" \
  -H "stream-secret-key: $STREAM_SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "VIDEO_TITLE",
    "type": "video"
  }'
```

Response: extract `data.id` as `VIDEO_ID` for the next steps.

### Step 2: Upload File Part

Upload the actual video file binary to the created video object.
First, get the file size and compute the MD5 hash:

```bash
# Get file size (cross-platform compatible)
FILE_SIZE=$(stat -f%z /path/to/video.mp4 2>/dev/null || stat -c%s /path/to/video.mp4)
END_POS=$((FILE_SIZE - 1))

# Compute MD5 hash
HASH=$(md5sum /path/to/video.mp4 | awk '{print $1}')
```

Then upload via multipart form-data with the Content-Range header:

```bash
curl -s -X POST "https://api.aiozstream.network/api/media/VIDEO_ID/part" \
  -H "stream-public-key: $STREAM_PUBLIC_KEY" \
  -H "stream-secret-key: $STREAM_SECRET_KEY" \
  -H "Content-Range: bytes 0-$END_POS/$FILE_SIZE" \
  -F "file=@/path/to/video.mp4" \
  -F "index=0" \
  -F "hash=$HASH"
```

**Important:** The `Content-Range` header is required for the upload to succeed. Format: `bytes {start}-{end}/{total_size}`.
Form-data fields:

- `file`: the video file binary (use `@/path/to/video.mp4`)
- `index`: 0 (for single-part upload)
- `hash`: MD5 hash of the file part

### Step 3: Complete Upload

After the file part is uploaded, call the complete endpoint to finalize:

```bash
curl -s -X GET "https://api.aiozstream.network/api/media/VIDEO_ID/complete" \
  -H 'accept: application/json' \
  -H "stream-public-key: $STREAM_PUBLIC_KEY" \
  -H "stream-secret-key: $STREAM_SECRET_KEY"
```

This triggers transcoding. The upload is now considered successful.

## After Upload — Get Video Link

After completing the upload, fetch the video detail to get the streaming URL:

```bash
curl -s "https://api.aiozstream.network/api/media/VIDEO_ID" \
  -H "stream-public-key: $STREAM_PUBLIC_KEY" \
  -H "stream-secret-key: $STREAM_SECRET_KEY"
```

Parse the response to find the HLS or MP4 URL from the `assets` field and return it to the user.

## Custom Upload Config Reference

_(Applicable if implementing custom logic via API directly)_

### Quality Presets (`resolution` field):

- `standard` — Standard quality
- `good` — Good quality
- `highest` — Highest quality
- `lossless` — Lossless quality

### Streaming Formats (`type` field):

- `hls` — HTTP Live Streaming (container: `mpegts` or `mp4`)
- `dash` — Dynamic Adaptive Streaming (container: `fmp4`)

## Response Handling

1. Run the appropriate script from the `scripts/` directory.
2. **Media/Search scripts** return raw JSON: `get_video_list`, `get_video_url_by_name`, `get_total_media`, `get_media_list`
3. **Metrics scripts** return structured output:
   - `get_aggregate_metric.sh`: Two labeled outputs (Watch Time Sum, View Count)
   - `get_breakdown_metric.sh`: Four labeled JSON blocks (=== device_type ===, === operator_system ===, === country ===, === browser ===)
   - `analytic_data.sh`: Combined aggregate + breakdown output
   - `get_usage_data.sh`: Raw JSON response with pretty-printed format
4. **Upload/Management scripts**: `upload_video_file.sh` prints step-by-step status with final URLs
5. Return useful fields explicitly (IDs, status, URLs, totals). If upload status is `transcoding` or URLs are empty, inform the user to check again later.

## Error Handling

- **401**: Invalid API keys. Ask user to verify `STREAM_PUBLIC_KEY` and `STREAM_SECRET_KEY`.
- **Missing Parameters**: Scripts validate arguments; pass exactly what they require.
- **404**: Resource not found (invalid media ID or livestream ID).
- **500**: Server error; suggest retrying.
- **Connection timeout/refused**: API endpoint may be unavailable; retry and verify `https://api.aiozstream.network/api/` accessibility.

## Example Interaction Flow

1. User: "Upload my video to AIOZ Stream"
2. Ensure `STREAM_PUBLIC_KEY` and `STREAM_SECRET_KEY` exist in environment (ask user only if missing)
3. Ask for the video file path and title
4. Execute: `./scripts/upload_video_file.sh "FILE_PATH" "TITLE"`
5. Extract the outputted HLS/MP4 link
6. Return the video link to the user
