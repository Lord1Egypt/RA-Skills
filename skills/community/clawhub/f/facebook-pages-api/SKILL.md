---
name: facebook-pages-api
description: Read public Facebook page data: page details (followers, category, contact info), posts, reels, videos, photo albums, a post's comments and replies, and Facebook search for pages, people, posts and videos, through the SocialAPIs REST API. Use when the user wants to look up, monitor or compare public Facebook pages or posts, collect comments, or write code that does, without a Meta developer app.
---

# Facebook Pages API (SocialAPIs)

Public Facebook page and post data as JSON: one API key, no Meta developer app, no OAuth, no page access token.

- Website: https://socialapis.io · this API: https://socialapis.io/api-sources/facebook-page-details
- Free API key: https://socialapis.io/auth/signup (200 credits a month, no card)
- Free follower count lookup, no signup: https://socialapis.io/tools/facebook-follower-count
- Every parameter: [references/endpoints.md](references/endpoints.md) · OpenAPI: https://socialapis.io/openapi.json · llms.txt: https://socialapis.io/llms.txt

## Setup

1. The user needs an API key from https://socialapis.io/dashboard.
2. Read it from the environment, `SOCIALAPIS_API_KEY`. **Never** hard-code it, print it, or ask the user to paste it into the chat. If it is missing, tell the user to set it.
3. Send it in the **`x-api-token` header**, never in the URL.

If SocialAPIs MCP tools are available in this session (`facebook_page`, `facebook_ads`, `instagram_profile`, …), use them instead of raw HTTP. Hosted MCP server: `https://mcp.socialapis.io/mcp`.

## Making a call

```bash
curl -s -H "x-api-token: $SOCIALAPIS_API_KEY" \
  "https://api.socialapis.io/facebook/pages/details?link=https://www.facebook.com/nike"
```

```python
import os, requests

r = requests.get(
    "https://api.socialapis.io/facebook/pages/details",
    params={"link": "https://www.facebook.com/nike"},
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
| [`/facebook/pages/id`](https://socialapis.io/api-sources/facebook-page-id) | Resolve a Facebook page URL to its numeric page ID. | 1 credit per call |
| [`/facebook/pages/details`](https://socialapis.io/api-sources/facebook-page-details) | Get a Facebook page's profile: name, category, follower and like counts, bio, contact info (email, phone, website, address), rating and the ad_page_id used by the Ads Library tools. | 1 credit per call; 5 credits when exact_followers_count=true |
| [`/facebook/pages/posts`](https://socialapis.io/api-sources/facebook-page-posts) | List a Facebook page's recent posts, newest first, with text, media, reactions, comment and share counts. | ceil(posts_returned / 3) credits per call, minimum 1 |
| [`/facebook/pages/reels`](https://socialapis.io/api-sources/facebook-page-reels) | List a Facebook page's reels (short-form videos). | 1 credit per call |
| [`/facebook/pages/videos`](https://socialapis.io/api-sources/facebook-page-videos) | List videos uploaded to a Facebook page, with video_id, title, duration, view count and thumbnail. | 1 credit per call |
| [`/facebook/pages/albums`](https://socialapis.io/api-sources/facebook-page-albums) | List the photo albums of a Facebook page, with album_id, album_title, url, thumbnail_uri and album_items_count (text, e.g. | 1 credit per call |
| [`/facebook/posts/id`](https://socialapis.io/api-sources/facebook-post-id) | Extract the numeric post ID from a Facebook post URL. | 1 credit per call |
| [`/facebook/posts/details`](https://socialapis.io/api-sources/facebook-post-details) | Get a Facebook post's text, author, timestamp, media, and reaction, comment and share counts. | 1 credit per call |
| [`/facebook/posts/details/extended`](https://socialapis.io/api-sources/facebook-post-details-extended) | Get everything `/facebook/posts/details` returns plus view counts, HD/SD video URLs, music/audio metadata and author verification status. | 1 credit per call |
| [`/facebook/posts/attachments`](https://socialapis.io/api-sources/facebook-post-attachment-details) | List every media attachment (images and videos, with URLs and dimensions) on a Facebook post, including all items in multi-photo posts. | 5 credits per call (deeper scrape than standard post details) |
| [`/facebook/posts/video`](https://socialapis.io/api-sources/facebook-video-post-details) | Get a Facebook video post's metadata: title, message text and hashtags, owner, reactions and view count. | 1 credit per call |
| [`/facebook/posts/comments`](https://socialapis.io/api-sources/facebook-post-comments) | List top-level comments on a Facebook post or reel, with author, text, timestamp and reaction count. | 1 credit per call |
| [`/facebook/posts/comments/replies`](https://socialapis.io/api-sources/facebook-post-comment-replies) | List replies to one Facebook comment. | 1 credit per call |
| [`/facebook/albums/items`](https://socialapis.io/api-sources/facebook-album-items) | Get the photos and videos inside a Facebook album (from a page or a group): media_id, media_type, url, thumbnail_uri and timestamp (Unix seconds). | 1 credit per call |
| [`/facebook/search/pages`](https://socialapis.io/api-sources/facebook-search-pages) | Find Facebook pages by keyword (brand, business or topic name), optionally near a location. | 1 credit per call |
| [`/facebook/search/people`](https://socialapis.io/api-sources/facebook-search-people) | Find public Facebook profiles by name or keyword, optionally near a location (location_uid from `/facebook/search/locations`). | 1 credit per call |
| [`/facebook/search/locations`](https://socialapis.io/api-sources/facebook-search-locations) | Look up Facebook places by name (city, region, venue) and get their location_uid. | 1 credit per call |
| [`/facebook/search/posts`](https://socialapis.io/api-sources/facebook-search-posts) | Search public Facebook posts by keyword, optionally filtered by location (location_uid from `/facebook/search/locations`) and date range. | 1 credit per call |
| [`/facebook/search/videos`](https://socialapis.io/api-sources/facebook-search-videos) | Search public Facebook videos by keyword, optionally most recent first or live videos only. | 1 credit per call |
| [`/facebook/media/download`](https://socialapis.io/api-sources/facebook-download-media) | Resolve a Facebook media URL (image, video or audio, e.g. | 1 credit per call |

## Things that matter

- Have a page name but no URL? `/facebook/search/pages?query=<name>` first, then use the returned link.
- `/facebook/pages/posts` returns 3 to 9 posts per call and costs one credit per 3 posts returned; page with `end_cursor`, filter by date with `after_time` / `before_time`.
- Views, video URLs and audio of a reel or video post come from `/facebook/posts/details/extended`, not `/facebook/posts/details`.
- **Credits:** the response headers `X-SocialAPIs-Credits-Deducted` and `X-SocialAPIs-Credits-Remaining` say what a call cost. Before a large batch, check `/usage` (free) and tell the user roughly what it will cost.
- **Pagination:** list endpoints return a page plus `end_cursor`; pass it back as `end_cursor` until it is missing or the user has enough.
- **Slow calls:** a call can take up to about 90 seconds. Use a timeout of at least 120 s and don't fire hundreds of calls in parallel (`/usage/limits` shows the plan's rate limit).
- **Errors:** `401` bad or missing key · `403` out of credits or account paused · `429` rate limit, retry with backoff · `502` / `504` the source failed or timed out, retry once later. Failed calls are not charged.

Other SocialAPIs skills: `facebook-ads-library-api` (Meta Ads Library), `facebook-marketplace-api` (Facebook Marketplace), `facebook-groups-api` (public Facebook groups), `instagram-api` (Instagram), and `socialapis` for every endpoint at once.
