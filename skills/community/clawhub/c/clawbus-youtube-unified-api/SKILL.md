---
name: YouTube API
description: >
  Use when YouTube data is needed through MyBrandMetrics: search YouTube
  videos, get video metadata, inspect channel info, browse playlists, list
  comments, check live broadcasts, query YouTube Analytics, and work with
  YouTube Reporting jobs. Covers YouTube Data API v3, YouTube Analytics API v2,
  and YouTube Reporting API v1 after YouTube is connected in MyBrandMetrics.
---

# YouTube API

Search YouTube videos, get YouTube video metadata, inspect channel info, browse
playlists, list comments, check live broadcasts, query YouTube Analytics, and
work with YouTube Reporting jobs through the MyBrandMetrics Discovery API.

Use this skill when YouTube content or YouTube account data is needed after
YouTube is connected in MyBrandMetrics. It covers YouTube Data API v3, YouTube
Analytics API v2, and YouTube Reporting API v1 from one interface.

This skill is for YouTube data, analytics, reporting, and upload-route
workflows. It does not provide YouTube transcripts.

Website: [https://www.clawbus.com/](https://www.clawbus.com/)  
MyBrandMetrics API: [https://mybrandmetrics.com/](https://mybrandmetrics.com/)

## Core Capabilities

| Capability | Details |
| --- | --- |
| YouTube API access | Work with YouTube Data API v3, YouTube Analytics API v2, and YouTube Reporting API v1 from one skill. |
| YouTube search results | Search YouTube videos, channels, playlists, and live content with query, channel, date, region, and result filters. |
| Video metadata | Get YouTube video title, description, thumbnails, publish date, duration, status, and statistics. |
| Channel info | Get YouTube channel details, subscriptions, playlists, playlist items, and related resources. |
| Comments and discussions | List YouTube comment threads and related comment data for videos or channels. |
| Live broadcasts | List and inspect YouTube live broadcasts and related live resources. |
| Upload routes | Use YouTube video upload routes, including multipart and resumable upload patterns. |
| YouTube Analytics | Query YouTube Analytics reports for connected channels, videos, and creator content. |
| YouTube Reporting | List YouTube Reporting API report types, create reporting jobs, and inspect generated reporting resources. |
| Endpoint references | Use generated service references and a compact catalog for endpoint lookup. |

## Setup Flow

1. Open [https://mybrandmetrics.com/](https://mybrandmetrics.com/) and sign in
   with Google.
2. In MyBrandMetrics, open **Data sources**.
3. Connect YouTube as a data source.
4. Wait until the MyBrandMetrics YouTube connection is ready.
5. In [https://mybrandmetrics.com/](https://mybrandmetrics.com/), get the
   MyBrandMetrics API key.
6. Install the `clawbus-youtube-unified-api` skill.
7. Start a YouTube search, channel lookup, playlist workflow, analytics query,
   reporting job, or upload workflow with natural-language instructions or
   direct Discovery API requests.

## Authentication

Use the MyBrandMetrics API key for Discovery API requests.

```bash
export MYBRANDMETRICS_API_KEY="YOUR_API_KEY"
export MYBRANDMETRICS_API_BASE_URL="https://api.mybrandmetrics.com"
```

Pass the key in the request header:

```text
X-API-Key: YOUR_API_KEY
```

Do not put real API keys, account session values, or Google access tokens in
skill files, examples, logs, or chat replies.

## Discovery Routing

Use `/discovery/{service}/{path}`.

| Service | Google API | Example route |
| --- | --- | --- |
| `youtube` | YouTube Data API v3 | `/discovery/youtube/channels` |
| `youtubeAnalytics` | YouTube Analytics API v2 | `/discovery/youtubeAnalytics/reports` |
| `youtubeReporting` | YouTube Reporting API v1 | `/discovery/youtubeReporting/jobs` |

Common version prefixes are omitted in the generated examples.

## Search-Friendly Workflows

Common YouTube workflows include:

- search YouTube videos by keyword, channel, date, region, or content type;
- get YouTube video metadata, thumbnails, statistics, captions, and status;
- inspect YouTube channel info, playlists, playlist items, comments, and
  subscriptions;
- browse YouTube playlists and channel uploads;
- list YouTube comments and discussion threads;
- query YouTube Analytics metrics such as views, watch time, and engagement;
- create and inspect YouTube Reporting API jobs;
- prepare YouTube upload requests for connected channels.

## Account Selection

If the MyBrandMetrics API key is connected to more than one YouTube account,
choose the account for the request before running it.

When MyBrandMetrics returns an account selection response, show only
non-sensitive account labels such as display name, email, and connection ID.
Then include the selected account identifier, such as `oauth_connection_id`, in
the Discovery API request.

## Example Requests

Get connected channel details:

```bash
curl -H "X-API-Key: $MYBRANDMETRICS_API_KEY" \
  "${MYBRANDMETRICS_API_BASE_URL:-https://api.mybrandmetrics.com}/discovery/youtube/channels?part=snippet,contentDetails,statistics&mine=true"
```

Query YouTube Analytics:

```bash
curl -sS "${MYBRANDMETRICS_API_BASE_URL:-https://api.mybrandmetrics.com}/discovery/youtubeAnalytics/reports" \
  -H "X-API-Key: $MYBRANDMETRICS_API_KEY" \
  --url-query "ids=channel==MINE" \
  --url-query "startDate=2026-01-01" \
  --url-query "endDate=2026-01-31" \
  --url-query "metrics=views,estimatedMinutesWatched"
```

Natural-language examples:

```text
Find recent YouTube videos about creator analytics and return titles, URLs, and view counts.
```

```text
Get analytics for my connected YouTube channel for the last 30 days.
```

```text
List playlists from my connected YouTube channel and show the first 10 playlist items.
```

## Reference Files

| File | Purpose |
| --- | --- |
| `references/index.md` | Reference overview and load order. |
| `references/curl.md` | Curl workflow, request construction, upload, download, and errors. |
| `references/mybrandmetrics-api.md` | Discovery routing, account selection, and MyBrandMetrics request rules. |
| `references/services/youtube-data-v3.md` | YouTube Data API v3 endpoint reference. |
| `references/services/youtube-analytics-v2.md` | YouTube Analytics API v2 endpoint reference. |
| `references/services/youtube-reporting-v1.md` | YouTube Reporting API v1 endpoint reference. |
| `references/catalog.json` | Compact machine-readable endpoint catalog. |

Before upload, update, delete, or reporting-job workflows, confirm the connected
YouTube account, target resource, request parameters, and intended result.
