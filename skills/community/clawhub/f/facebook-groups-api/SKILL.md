---
name: facebook-groups-api
description: Read public Facebook groups: a group's details (members, description, privacy), its posts, videos and photo albums, through the SocialAPIs REST API. Use when the user wants to see what a public community talks about, track questions or mentions in groups, or write code that reads public group posts. Private groups are not accessible.
---

# Facebook Groups API (SocialAPIs)

Public Facebook group data as JSON: details, posts, videos and albums of any public group. No login, no group membership.

- Website: https://socialapis.io · this API: https://socialapis.io/api-sources/facebook-group-posts
- Free API key: https://socialapis.io/auth/signup (200 credits a month, no card)
- Every parameter: [references/endpoints.md](references/endpoints.md) · OpenAPI: https://socialapis.io/openapi.json · llms.txt: https://socialapis.io/llms.txt

## Setup

1. The user needs an API key from https://socialapis.io/dashboard.
2. Read it from the environment, `SOCIALAPIS_API_KEY`. **Never** hard-code it, print it, or ask the user to paste it into the chat. If it is missing, tell the user to set it.
3. Send it in the **`x-api-token` header**, never in the URL.

If SocialAPIs MCP tools are available in this session (`facebook_page`, `facebook_ads`, `instagram_profile`, …), use them instead of raw HTTP. Hosted MCP server: `https://mcp.socialapis.io/mcp`.

## Making a call

```bash
curl -s -H "x-api-token: $SOCIALAPIS_API_KEY" \
  "https://api.socialapis.io/facebook/groups/details?link=https://www.facebook.com/groups/<group>"
```

```python
import os, requests

r = requests.get(
    "https://api.socialapis.io/facebook/groups/details",
    params={"link": "https://www.facebook.com/groups/<group>"},
    headers={"x-api-token": os.environ["SOCIALAPIS_API_KEY"]},
    timeout=120,
)
r.raise_for_status()
data = r.json()
```

SDKs: Python `pip install socialapis-sdk`, JavaScript `npm install socialapis-sdk`, PHP `composer require socialapishub/socialapis`.

## Endpoints

All `GET`, base URL `https://api.socialapis.io`. Each link opens the endpoint's page with a live example.

| Endpoint | What it returns | Credits |
|---|---|---|
| [`/facebook/groups/id`](https://socialapis.io/api-sources/facebook-group-id) | Resolve a Facebook group URL to its numeric group ID. | 1 credit per call |
| [`/facebook/groups/details`](https://socialapis.io/api-sources/facebook-group-details) | Get a public Facebook group's profile: name, description, member count, privacy, rules and activity stats. | 1 credit per call |
| [`/facebook/groups/posts`](https://socialapis.io/api-sources/facebook-group-posts) | List recent posts from a public Facebook group, with text, media, author, reactions and comment counts. | ceil(posts_returned / 3) credits per call, minimum 1 |
| [`/facebook/groups/videos`](https://socialapis.io/api-sources/facebook-group-videos) | List videos posted in a public Facebook group, with video_id, title, duration, view count and thumbnail. | 1 credit per call |
| [`/facebook/groups/albums`](https://socialapis.io/api-sources/facebook-group-albums) | List the photo albums of a public Facebook group, with album_id, album_title, url, thumbnail_uri, photos_count and videos_count. | 1 credit per call |
| [`/facebook/albums/items`](https://socialapis.io/api-sources/facebook-album-items) | Get the photos and videos inside a Facebook album (from a page or a group): media_id, media_type, url, thumbnail_uri and timestamp (Unix seconds). | 1 credit per call |

## Things that matter

- Only public groups. A private group returns an error, not an empty list: tell the user it is private.
- Albums need the numeric group ID: `/facebook/groups/id` first, then `/facebook/groups/albums?group_id=…`, then `/facebook/albums/items?album_id=…`.
- **Credits:** the response headers `X-SocialAPIs-Credits-Deducted` and `X-SocialAPIs-Credits-Remaining` say what a call cost. Before a large batch, check `/usage` (free) and tell the user roughly what it will cost.
- **Pagination:** list endpoints return a page plus `end_cursor`; pass it back as `end_cursor` until it is missing or the user has enough.
- **Slow calls:** a call can take up to about 90 seconds. Use a timeout of at least 120 s and don't fire hundreds of calls in parallel (`/usage/limits` shows the plan's rate limit).
- **Errors:** `401` bad or missing key · `403` out of credits or account paused · `429` rate limit, retry with backoff · `502` / `504` the source failed or timed out, retry once later. Failed calls are not charged.

Other SocialAPIs skills: `facebook-pages-api` (Facebook pages, posts and comments), `facebook-ads-library-api` (Meta Ads Library), `facebook-marketplace-api` (Facebook Marketplace), `instagram-api` (Instagram), and `socialapis` for every endpoint at once.
