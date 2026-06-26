# Curl Usage

## Authentication

Use a MyBrandMetrics API key in the `X-API-Key` header.

```bash
export MYBRANDMETRICS_API_KEY="YOUR_API_KEY"
export MYBRANDMETRICS_API_BASE_URL="https://api.mybrandmetrics.com"
```

Simple example:

```bash
curl -H "X-API-Key: YOUR_API_KEY" "https://api.mybrandmetrics.com/discovery/youtube/channels?part=snippet,contentDetails,statistics&mine=true"
```

Environment variable example:

```bash
curl -H "X-API-Key: $MYBRANDMETRICS_API_KEY" "${MYBRANDMETRICS_API_BASE_URL:-https://api.mybrandmetrics.com}/discovery/youtube/channels?part=snippet,contentDetails,statistics&mine=true"
```

## Discovery API

Route shape:

```text
/discovery/{service}/{path}
```

Supported service names:

- `youtube`
- `youtubeAnalytics`
- `youtubeReporting`

## Query Parameters

Prefer `--url-query` for query strings. It appends parameters to the URL
without changing the request body, so it works for GET, POST, PATCH, PUT, and
DELETE.

```bash
curl -sS "${MYBRANDMETRICS_API_BASE_URL:-https://api.mybrandmetrics.com}/discovery/youtube/channels" \
  -H "X-API-Key: $MYBRANDMETRICS_API_KEY" \
  --url-query "part=snippet,statistics" \
  --url-query "mine=true"
```

The method references list each parameter's location. Path parameters appear
inside the URL path. Query parameters should be passed with `--url-query`.

## JSON Bodies

For methods with a request schema, place the JSON request body in `body.json`
and call:

```bash
curl -sS -X POST "${MYBRANDMETRICS_API_BASE_URL:-https://api.mybrandmetrics.com}/discovery/youtube/playlists" \
  -H "X-API-Key: $MYBRANDMETRICS_API_KEY" \
  --json "@body.json" \
  --url-query "part=snippet,status"
```

If the local curl version does not support `--json`, use:

```bash
-H "Content-Type: application/json" --data-binary "@body.json"
```

## Uploads

Methods with media upload support include upload examples in the service
references. Set:

```bash
export MEDIA_FILE="video.mp4"
export MIME_TYPE="video/mp4"
```

For multipart uploads, use `-F` and explicitly define the metadata content
type. For resumable uploads, include upload content headers and then upload
bytes to the resumable upload session URL when the API returns one.

## Downloads

Methods marked as supporting media download may require `alt=media`. Save
binary output with `-o`.

## Error Handling

Use `-fS` when scripts should fail on non-2xx responses, or capture both body
and status:

```bash
curl -sS -w "\n%{http_code}\n" -o response.json "${MYBRANDMETRICS_API_BASE_URL:-https://api.mybrandmetrics.com}/discovery/youtube/channels"
```

Errors generally return a JSON object with an `error` field. If the connected
YouTube account needs more access, ask the user to reconnect YouTube in
MyBrandMetrics.
