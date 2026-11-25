# Facebook Pages API endpoint reference (SocialAPIs)

Base URL: `https://api.socialapis.io` · Auth: header `x-api-token: $SOCIALAPIS_API_KEY` · All endpoints are `GET` with query parameters.

Generated from the full reference in the `socialapis` skill. Machine-readable: https://socialapis.io/openapi.json

### `GET /facebook/pages/id`

Docs and live example: https://socialapis.io/api-sources/facebook-page-id

Resolve a Facebook page URL to its numeric page ID. Use it when another tool needs a page or profile ID; use `/facebook/pages/details` for the page's data. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook page URL (e.g., https://facebook.com/nike) |

### `GET /facebook/pages/details`

Docs and live example: https://socialapis.io/api-sources/facebook-page-details

Get a Facebook page's profile: name, category, follower and like counts, bio, contact info (email, phone, website, address), rating and the ad_page_id used by the Ads Library tools. Use it when you have the page URL; to find a page by name, use `/facebook/search/pages` first. Pricing: 1 credit per call; 5 credits when exact_followers_count=true.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook page URL |
| `exact_followers_count` | no | When true, performs a deeper scrape to return the exact follower count (e.g. 38,493,217 instead of "38M"). Charges 5 credits when true, 1 credit otherwise. Default: false. |

### `GET /facebook/pages/posts`

Docs and live example: https://socialapis.io/api-sources/facebook-page-posts

List a Facebook page's recent posts, newest first, with text, media, reactions, comment and share counts. Returns 3-9 posts per call plus an end_cursor for the next page; filter by date with after_time / before_time. For reels or videos only, use `/facebook/pages/reels` or `/facebook/pages/videos`. Pricing: ceil(posts_returned / 3) credits per call, minimum 1.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook page URL |
| `limit` | no | Maximum number of posts to return. Default: 3. Minimum: 3. Maximum: 9. |
| `end_cursor` | no | Pagination cursor for next page of results |
| `after_time` | no | ISO 8601 timestamp - only return posts after this time |
| `before_time` | no | ISO 8601 timestamp - only return posts before this time |
| `timezone` | no | Timezone for timestamps (e.g., UTC, America/New_York) |

### `GET /facebook/pages/reels`

Docs and live example: https://socialapis.io/api-sources/facebook-page-reels

List a Facebook page's reels (short-form videos). Returns an end_cursor for the next page. For long-form videos, use `/facebook/pages/videos`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook page URL |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/pages/videos`

Docs and live example: https://socialapis.io/api-sources/facebook-page-videos

List videos uploaded to a Facebook page, with video_id, title, duration, view count and thumbnail. Provide the page URL (link) or its numeric profile_id. Returns an end_cursor for the next page. For short-form reels, use `/facebook/pages/reels`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook page URL |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/pages/albums`

Docs and live example: https://socialapis.io/api-sources/facebook-page-albums

List the photo albums of a Facebook page, with album_id, album_title, url, thumbnail_uri and album_items_count (text, e.g. "400 items"). Needs the numeric page ID (profile_id) from `/facebook/pages/id`. Returns an end_cursor for the next page. To get the photos in an album, pass its album_id to `/facebook/albums/items`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `profile_id` | yes | Facebook page ID, from `/facebook/pages/id` |
| `limit` | no | Maximum number of albums to return. Default: 8. Minimum: 8. Maximum: 16. |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/posts/id`

Docs and live example: https://socialapis.io/api-sources/facebook-post-id

Extract the numeric post ID from a Facebook post URL. Use it to get the post_id that `/facebook/posts/attachments` needs. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook post URL |

### `GET /facebook/posts/details`

Docs and live example: https://socialapis.io/api-sources/facebook-post-details

Get a Facebook post's text, author, timestamp, media, and reaction, comment and share counts. Start here for any post. If you need view counts, video download URLs or audio metadata (common for reels and videos), use `/facebook/posts/details/extended` instead. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook post URL |

### `GET /facebook/posts/details/extended`

Docs and live example: https://socialapis.io/api-sources/facebook-post-details-extended

Get everything `/facebook/posts/details` returns plus view counts, HD/SD video URLs, music/audio metadata and author verification status. Use it for reels and video posts, or when the standard details lack view_count, video_hd_src or attached_track. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook post URL (works for reels, video posts, and regular posts) |

### `GET /facebook/posts/attachments`

Docs and live example: https://socialapis.io/api-sources/facebook-post-attachment-details

List every media attachment (images and videos, with URLs and dimensions) on a Facebook post, including all items in multi-photo posts. Needs the numeric post_id from `/facebook/posts/id`. For the post's text and engagement, use `/facebook/posts/details`. Pricing: 5 credits per call (deeper scrape than standard post details).

| Parameter | Required | Description |
|---|---|---|
| `post_id` | yes | Numeric Facebook post ID, from `/facebook/posts/id` |

### `GET /facebook/posts/video`

Docs and live example: https://socialapis.io/api-sources/facebook-video-post-details

Get a Facebook video post's metadata: title, message text and hashtags, owner, reactions and view count. Needs the numeric video_id (the number in a facebook.com/.../videos/<id> URL, or from `/facebook/pages/videos`). Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `video_id` | yes | Numeric Facebook video ID, e.g. the number in a facebook.com/.../videos/<id> URL |

### `GET /facebook/posts/comments`

Docs and live example: https://socialapis.io/api-sources/facebook-post-comments

List top-level comments on a Facebook post or reel, with author, text, timestamp and reaction count. Returns up to 30 per call plus an end_cursor for the next page. Set include_reply_info=true to get the comment_feedback_id and expansion_token that `/facebook/posts/comments/replies` needs. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook post or reel URL |
| `end_cursor` | no | Pagination cursor for next page of comments |
| `include_reply_info` | no | When "true", includes comment_feedback_id and expansion_token for fetching replies |

### `GET /facebook/posts/comments/replies`

Docs and live example: https://socialapis.io/api-sources/facebook-post-comment-replies

List replies to one Facebook comment. Needs comment_feedback_id and expansion_token, which `/facebook/posts/comments` returns when called with include_reply_info=true. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `comment_feedback_id` | yes | Feedback ID from the comments endpoint with include_reply_info=true |
| `expansion_token` | yes | Expansion token from the comments endpoint with include_reply_info=true |

### `GET /facebook/albums/items`

Docs and live example: https://socialapis.io/api-sources/facebook-album-items

Get the photos and videos inside a Facebook album (from a page or a group): media_id, media_type, url, thumbnail_uri and timestamp (Unix seconds). Needs an album_id from `/facebook/pages/albums` or `/facebook/groups/albums`. Returns an end_cursor for the next page. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `album_id` | yes | Album ID, from `/facebook/pages/albums` or `/facebook/groups/albums` |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/search/pages`

Docs and live example: https://socialapis.io/api-sources/facebook-search-pages

Find Facebook pages by keyword (brand, business or topic name), optionally near a location. Returns page names, URLs, categories and follower counts, 3 per call, plus an end_cursor. Use it when you don't have the page URL; then call `/facebook/pages/details` with a result's URL. For locations, get a location_uid from `/facebook/search/locations`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | yes | Keyword to search for, e.g. a brand or business name |
| `location_uid` | no | Location UID for filtering (from search/locations endpoint) |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/search/people`

Docs and live example: https://socialapis.io/api-sources/facebook-search-people

Find public Facebook profiles by name or keyword, optionally near a location (location_uid from `/facebook/search/locations`). Returns names, profile URLs and pictures, plus work, education and location where public, and an end_cursor. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | yes | Name or keyword to search for |
| `location_uid` | no | Location UID for filtering |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/search/locations`

Docs and live example: https://socialapis.io/api-sources/facebook-search-locations

Look up Facebook places by name (city, region, venue) and get their location_uid. The location_uid is only used to filter `/facebook/search/pages`, `/facebook/search/people` and `/facebook/search/posts`; it is not a Marketplace location (use `/facebook/marketplace/city-coordinates` for that). Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | yes | Search query (city, place, landmark) |

### `GET /facebook/search/posts`

Docs and live example: https://socialapis.io/api-sources/facebook-search-posts

Search public Facebook posts by keyword, optionally filtered by location (location_uid from `/facebook/search/locations`) and date range. Returns posts with text, author and engagement, plus an end_cursor. To list one page's posts, use `/facebook/pages/posts` instead. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | yes | Keyword or phrase to search post text for |
| `location_uid` | no | Location UID for filtering |
| `start_time` | no | Filter posts after this date (YYYY-MM-DD) |
| `end_time` | no | Filter posts before this date (YYYY-MM-DD) |
| `recent_posts` | no | When "true", shows only recent posts |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/search/videos`

Docs and live example: https://socialapis.io/api-sources/facebook-search-videos

Search public Facebook videos by keyword, optionally most recent first or live videos only. Returns video titles, URLs and view counts, plus an end_cursor. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | yes | Keyword or phrase to search videos for |
| `most_recent` | no | When "true", shows most recent videos first |
| `videos_live` | no | When "true", filters for live videos only |
| `fields` | no | Comma-separated list of response fields to include |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/media/download`

Docs and live example: https://socialapis.io/api-sources/facebook-download-media

Resolve a Facebook media URL (image, video or audio, e.g. from a post or reel) to direct downloadable file URLs. Returns URLs, not file bytes. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `url` | yes | Facebook media URL to download |
