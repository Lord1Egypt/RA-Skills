# MyBrandMetrics Discovery API

Use the MyBrandMetrics Discovery API when the user provides a MyBrandMetrics API
key and wants to call YouTube Data, Analytics, or Reporting endpoints.

## Base URL And Header

```bash
export MYBRANDMETRICS_API_BASE_URL="https://api.mybrandmetrics.com"
export MYBRANDMETRICS_API_KEY="YOUR_API_KEY"
```

Send:

```bash
-H "X-API-Key: $MYBRANDMETRICS_API_KEY"
```

## Route Mapping

Route:

```text
/discovery/{service}/{path}
```

Services:

| Service | Google API | Common prefix omitted in generated examples |
| --- | --- | --- |
| `youtube` | YouTube Data API v3 | `youtube/v3/` |
| `youtubeAnalytics` | YouTube Analytics API v2 | `v2/` |
| `youtubeReporting` | YouTube Reporting API v1 | `v1/` |

Examples:

```text
/discovery/youtube/channels
/discovery/youtube/videos
/discovery/youtubeAnalytics/reports
/discovery/youtubeReporting/jobs
```

## Account Selection

Some API keys may have more than one connected YouTube account. If
MyBrandMetrics indicates account selection is required, ask the user which
account to use. Present only non-sensitive account labels such as display name,
email, and connection ID.

Use the selected account identifier in the Discovery API request, for example:

```bash
curl -H "X-API-Key: YOUR_API_KEY" "https://api.mybrandmetrics.com/discovery/youtube/channels?part=snippet,contentDetails,statistics&mine=true&oauth_connection_id=42"
```

Supported selector query parameters may include:

```text
oauth_connection_id
google_sub
email
connection_id
account_id
channel_id
```

## Scope Behavior

The target user must have a connected YouTube account with the required
permissions for the task.

- Data API: read, write, or upload permissions depending on the endpoint.
- Analytics API: analytics read permissions.
- Reporting API: reporting read permissions.

If permissions are missing, ask the user to reconnect YouTube in MyBrandMetrics
with the required access.
