# Video Module Rules

## 1. Module Scope

All video-related questions should be routed through this module first. Typical examples include:

- discovering high-performing commerce, AI, or ad videos
- retrieving video detail records
- analyzing video trend, comments, or captions
- tracing products attached to a video
- reading video leaderboard data
- retrieving videos related to a hashtag

## 2. Video List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/video/list.md`
- Purpose: retrieve large volumes of offline commerce, AI, and ad videos from the EchoTik video library

### Best Suited For

- large-scale video discovery
- commerce-video screening
- AI-video screening
- ad-video screening
- creator-filtered video research
- ranking-like list retrieval through sorting and filters

### Rules

- This is an offline EchoTik library that supports large-batch retrieval.
- It can also be used as a leaderboard-style query through sorting and filtering.
- Supported filtering directions include:
  - creator filters
  - commerce-video flag
  - AI-video flag
  - publish-date range
  - publish-duration range
  - view-count range
  - product category ID
  - ad-video flag
  - attached product ID

## 3. Video Trend Snapshot - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/video/trend.md`
- Purpose: retrieve historical trend snapshots for a video through `video_id`

### Rules

- Prefer the realtime 14-day interaction trend endpoint first because it is more accurate and directly reflects official realtime trend data.
- Use the offline video trend snapshot when the user needs longer history beyond the realtime 14-day window.
- Follows the offline trend-snapshot behavior in `global-rules.md` (180-day lookback, non-contiguous dates).

## 4. Batch Video Detail - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/video/detail.md`
- Purpose: batch-retrieve video detail records through `video_id`

### Rules

- Supports up to `10` video IDs per request.
- Multiple video IDs must be comma-separated.
- The offline detail payload can include:
  - interaction metrics
  - video sales
  - GMV
  - recent interaction deltas
- If this endpoint returns `code=0` with empty `data`, switch to `Video Detail - Realtime`.
- When the user asks for video detail, ask whether they want realtime or EchoTik offline mode before execution.

## 5. Video Product List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/video/product/list.md`
- Purpose: retrieve the products attached to one or multiple videos

### Rules

- `video_ids` may be passed in batch form with comma-separated values.
- Returned video and product fields are basic summary fields only.
- If the user needs richer product or video data, follow up with product-detail or video-detail retrieval.

## 6. Video Rank List - EchoTik

- Documentation: `https://opendocs.echotik.live/echotik/video/ranklist.md`
- Purpose: retrieve leaderboard-style video rankings

### Rules

- Supports L1 product-category filtering for commerce-video ranking segmentation.
- Supports AI-video filtering.
- Ranking is primarily based on periodic view or sales ordering.
- The `date` interpretation follows the same T+1 periodic logic used by creator, product, and seller leaderboards.

## 7. Video Detail - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/video/detail.md`
- Purpose: retrieve realtime video detail through `video_id`

## 8. Video Captions - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/video/captions.md`
- Purpose: retrieve realtime captions or script text for a video

### Rules

- The response may contain multiple language scripts.
- Use this endpoint when the user wants to analyze the spoken or written content of a video.

## 9. Hashtag Video List - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/hashtag/video/list.md`
- Purpose: retrieve videos associated with a `hashtag_id`

### Rules

- If the user only knows the hashtag text, use `Hashtag Search - Realtime` first to resolve the correct `hashtag_id`.
- Then call the hashtag video-list endpoint.

## 10. Video Comments - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/video/comments.md`
- Purpose: retrieve the comment list for a video through `video_id`

### Rules

- When the user wants comment analysis rather than raw comment retrieval, prefer `Video Comment Keyword Insight - Realtime` before pulling the full comment list.

## 11. Video Comment Replies - Realtime

- Documentation: `https://opendocs.echotik.live/realtime/video/comments/replies.md`
- Purpose: retrieve replies for a specific comment under a video

### Rules

- Requires both `video_id` and `comment_id`.

## 12. Video Download URL

- Documentation: `https://opendocs.echotik.live/realtime/video/downloadurl.md`
- Purpose: resolve cover, playback, and download URLs from a web or app share link

## 13. Orchestration

For multi-step video workflows (discovery, performance analysis, hashtag exploration), see `orchestration-playbooks.md`.
