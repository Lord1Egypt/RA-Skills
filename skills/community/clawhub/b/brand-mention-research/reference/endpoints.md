# brand-mention-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**9 endpoints across 3 platform group(s).**

## Reddit (3)

### `reddit_comments`

- **HTTP:** `GET /reddit/comments/{id}`
- **What:** Get Reddit post comments. Returns a Reddit post with its public comments. The default mode is 1 credit. Set `include_metrics=true` to return the comments with public net score and award count plus post engagement metrics for 3 credits. Large threads may expose only an initial comment subset. Reddit does not expose per-comment upvote ratios or exact upvote/downvote totals anonymously. A post that exists but has no comments yet returns a 200 response with an empty comments list; a post that does not exist returns 404, and a temporary block or upstream failure returns 503 (retryable) rather than 404. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `depth` (integer, optional) — Maximum flat comment depth returned in metrics mode.; `id` (string, **required**) — Reddit post id or t3_ id; `include_metrics` (boolean, optional) — Include public post and per-comment engagement metrics; costs 3 credits instead of 1; `limit` (integer, optional) — Maximum comments returned, defaults to 25 and clamps to 100; `sort` (string, optional) — Comment order: confidence, top, new, controversial, old, or qa. Applied to the anonymous HTML request when metrics are enabled.

### `reddit_post`

- **HTTP:** `GET /reddit/post/{id}`
- **What:** Get Reddit post. Returns a public Reddit post. The default mode is 1 credit. Set `include_metrics=true` to return public net score, upvote ratio, comment count, award count, and estimated upvote/downvote totals for 3 credits. Reddit fuzzes voting data, so estimates are approximate; share, repost/crosspost, and view counts are not exposed anonymously. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `id` (string, **required**) — Reddit post id or t3_ id; `include_metrics` (boolean, optional) — Include public engagement metrics; costs 3 credits instead of 1

### `reddit_search`

- **HTTP:** `GET /reddit/search`
- **What:** Search Reddit posts. Searches public Reddit content and returns public post entries. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `after` (string, optional) — Reddit pagination token; `limit` (integer, optional) — Maximum posts, defaults to 25 and clamps to 100; `q` (string, **required**) — Search keywords; `sort` (string, optional) — Sort: relevance, hot, new, top, or comments; `subreddit` (string, optional) — Restrict search to a subreddit name, without r/; `time` (string, optional) — Time window for top/comments sorts: hour, day, week, month, year, or all

## TikTok (3)

### `tiktok_comments`

- **HTTP:** `GET /tiktok/comments`
- **What:** Retrieve TikTok video comments. Returns the top-level comments on a TikTok video, by the video id from its URL (`aweme_id`). Results are paged by cursor: pass the `cursor` from one response to get the next page, and read `has_more` to see whether more remain. The response also carries the total comment count.
- **Params:** `aweme_id` (string, **required**) — TikTok video id from the video URL; `cursor` (integer, optional) — Pagination cursor

### `tiktok_post`

- **HTTP:** `GET /tiktok/post/{id}`
- **What:** Retrieve TikTok video details. Returns TikTok's detail record for one video by video id. `itemInfo.itemStruct` holds the video's description, the author's profile and the author's statistics (such as followers, following and hearts) along with the rest of TikTok's video object; `shareMeta` holds the share title and description.
- **Params:** `id` (string, **required**) — TikTok video id

### `tiktok_search`

- **HTTP:** `GET /tiktok/search`
- **What:** Search TikTok videos. Searches TikTok videos for `keyword`. `cursor` defaults to 0 and `count` defaults to 20, capped at 50. The response has the matching video items, a `cursor` and `has_more` for paging. An empty, blocked or malformed result from TikTok returns an upstream error.
- **Params:** `count` (integer, optional) — Result count, clamped to 50; `cursor` (integer, optional) — Pagination cursor; `keyword` (string, **required**) — Search keyword

## YouTube (3)

### `youtube_comments`

- **HTTP:** `GET /youtube/comments/{id}`
- **What:** Retrieve top-level video comments. Returns one page of top-level comments for a YouTube video by its 11-character `id`. Each comment has its id, content, author `user_name` and `channel_id`, `likes_count`, `reply_count` and `published_time`. Comments with replies may include their own `continuation_token`; pass that token to `/youtube/comments/{id}/replies`. Pass the response-level `continuation_token` here for deterministic pagination. If omitted, the service discovers an initial cursor or may resume the most recently cached cursor for this video.
- **Params:** `continuation_token` (string, optional) — Opaque pagination token returned by a previous request; pass it for deterministic pagination; `id` (string, **required**) — YouTube video ID (11-character code)

### `youtube_search`

- **HTTP:** `GET /youtube/search`
- **What:** Search YouTube. Returns normalized YouTube search results using YouTube's InnerTube search API. Pass `continuation_token` from a previous response to retrieve the next page. Use `q` as the primary query parameter; `search_query` is accepted as an alias. `hl` and `gl` localize ranking and result context; they default to `en` and `US`. Named filters cover the public web search filters. Account-only chips such as Watched and Unwatched are not exposed.
- **Params:** `continuation_token` (string, optional) — Pagination token returned by a previous request; `duration` (string, optional) — Filter by duration; short, medium, and long preserve their previous upstream encodings; `features` (string, optional) — Comma-separated feature filters. Allowed values: live, 4k, hd, subtitles, cc, creative_commons, 360, vr180, 3d, hdr, location, purchased; `gl` (string, optional) — Two-letter YouTube region code; `hl` (string, optional) — YouTube interface language; `params` (string, optional) — Raw protobuf-encoded search filter (base64); `q` (string, optional) — Search query; `search_query` (string, optional) — Alias for q; `sort_by` (string, optional) — Sort results; `type` (string, optional) — Filter by type; `upload_date` (string, optional) — Filter by upload date

### `youtube_video`

- **HTTP:** `GET /youtube/video/{id}`
- **What:** Retrieve video metadata & captions. Returns the metadata of a YouTube video by its 11-character `id`: title, description, channel id and title, publication time, duration in seconds, and view, like and comment counts. Some fields are best-effort.
- **Params:** `id` (string, **required**) — YouTube video ID (11-char code)
