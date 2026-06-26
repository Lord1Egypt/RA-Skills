# AIOZ Stream API Reference

## Authentication

All requests require HTTP headers:

- `stream-public-key`: Your AIOZ Stream public API key
- `stream-secret-key`: Your AIOZ Stream secret API key

Base URL: `https://api.aiozstream.network/api`

## Script-to-API Mapping

- `upload_video_file.sh`
  - `POST /media/create`
  - `POST /media/{id}/part`
  - `GET /media/{id}/complete`
  - `GET /media/{id}`
- `get_media_list.sh`
  - `GET /media?search={SEARCH}&page={PAGE}`
- `get_total_media.sh`
  - `POST /media` with optional JSON body `{ "search": "...", "page": n }`
- `get_video_list.sh`
  - `POST /media` with body `{}`
- `get_video_url_by_name.sh`
  - `POST /media` with body `{ "search": "VIDEO_NAME" }`
- `create_livestream_key.sh`
  - `POST /live_streams`
- `get_balance.sh`
  - `GET /user/me`
- `get_usage_data.sh`
  - `GET /analytics/data?from=...&to=...&interval=hour`
- `get_aggregate_metric.sh`
  - `POST /analytics/metrics/data/watch_time/sum`
  - `POST /analytics/metrics/data/view/count`
- `get_breakdown_metric.sh` / `analytic_data.sh`
  - `POST /analytics/metrics/bucket/view/device-type`
  - `POST /analytics/metrics/bucket/view/operator-system`
  - `POST /analytics/metrics/bucket/view/country`
  - `POST /analytics/metrics/bucket/view/browser`

## Media Configurations

### Media Types

- `video`
- `audio`

### Live Streams

- `type`: `video`
- `save`: `true`

## Example API Calls (Underlying Scripts)

### Create Media Payload

```json
{
  "title": "Video Title",
  "type": "video"
}
```

### Livestream Create Payload

```json
{
  "save": true,
  "type": "video",
  "name": "My Stream Key"
}
```

### Search/List Media Payloads (`POST /media`)

```json
{}
```

```json
{
  "search": "keyword"
}
```

```json
{
  "search": "keyword",
  "page": 1
}
```

### Upload Part Configuration

Required headers and form fields for `POST /media/{id}/part`:

- Header: `Content-Range: bytes 0-{end}/{total}`
- Field: `file` (binary)
- Field: `index` (0-based)
- Field: `hash` (MD5 of the chunk)

### Analytics Query Payload

Used for `watch_time/sum`, `view/count`, and bucket breakdowns:

```json
{
  "from": 1672531200,
  "to": 1675209600,
  "filter_by": {
    "media_type": "video"
  }
}
```

### Usage Data Query (`GET /analytics/data`)

Query params used by script:

- `from` (Unix timestamp, converted from dd/mm/yyyy input)
- `to` (Unix timestamp, converted from dd/mm/yyyy input)
- `interval=hour` (fixed in script)

Example input: `./get_usage_data.sh PUBLIC_KEY SECRET_KEY 01/01/2024 31/12/2024`
Converts to:
`/analytics/data?from=1704067200&to=1735689600&interval=hour`

## Script Input Expectations

- `upload_video_file.sh`: `PUBLIC_KEY SECRET_KEY FILE_PATH TITLE`
  - Accepts local file path only.
- `get_usage_data.sh`: `PUBLIC_KEY SECRET_KEY FROM(dd/mm/yyyy) TO(dd/mm/yyyy)`
  - `FROM/TO` must be `dd/mm/yyyy` format (scripts convert to Unix timestamp).
- `get_aggregate_metric.sh`, `get_breakdown_metric.sh`, `analytic_data.sh`:
  - `TYPE` must be `video` or `audio`
  - `FROM/TO` must be `dd/mm/yyyy` (scripts convert to Unix time)
- `get_media_list.sh`, `get_total_media.sh`:
  - `PAGE` must be non-negative integer if provided.

## API Response Fields

### Media Detail Response

```json
{
  "data": {
    "id": "media_id_here",
    "title": "Video Title",
    "type": "video",
    "status": "ready",
    "assets": {
      "hls_url": "https://cdn.example.com/video.m3u8",
      "hls_player_url": "https://player.example.com/?v=...",
      "mp4_url": "https://cdn.example.com/video.mp4"
    }
  }
}
```

**Key fields:**

- `data.id` — Media ID (used for parts/complete ops)
- `data.status` — Processing status (`transcoding`, `ready`, etc.)
- `data.assets.hls_player_url` — Player URL suitable for direct playback
- `data.assets.hls_url` — HLS streaming link
- `data.assets.mp4_url` — MP4 file link

### Analytics Response

```json
{
  "status": "success",
  "data": {
    "total": 100,
    "data": [
      {
        "metric_value": 50,
        "dimension_value": "chrome"
      }
    ]
  }
}
```

## Error Codes

- `401` — Invalid API keys (public or secret key incorrect)
- `400` — Bad request (missing fields, wrong range format)
- `404` — Media or endpoint not found
- `500` — Server error (retry recommended)

## Practical Notes for Clawbot

- `get_video_list.sh` currently calls `POST /media` with `{}` and is not hard-filtered to only `type=video`.
- `get_video_url_by_name.sh` returns search result JSON; caller should parse `data[*].assets.*` fields.
- After upload complete, media may stay in `transcoding` before URLs are fully available.
