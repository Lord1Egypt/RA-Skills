---
name: schedule-post
description: Create, schedule, or publish social media posts via BulkPublish MCP. Use when the user wants to post to social media.
---

# BulkPublish — Post Creation Reference

## create_post parameters

```
content        (string, optional) — post text; may be omitted for a media-only post
channels       (array, required)  — [{channelId: number, platform: string}]
                                    Get these from list_channels first
status         ("draft"|"scheduled") — default "draft"
scheduledAt    (ISO 8601 string)  — required when status is "scheduled"
timezone       (string)           — e.g. "America/New_York", "Asia/Karachi"
mediaFileIds   (number[])         — IDs from upload_media
platformContent (object)          — per-platform text: {"x": "Short", "linkedin": "Longer version"}
postTypeOverrides (object)        — per-platform format: {"instagram": "reel", "facebook": "story"}
postFormat     ("post"|"video"|"reel"|"story"|"carousel"|"thread") — "thread" requires threadParts
threadParts    (array)            — [{content: string, mediaFileIds?: number[]}], min 2 parts.
                                    EVERY part is length-checked against every target platform,
                                    not just the first — an over-long part 400s the whole request
platformSpecific (object)         — per-platform options; see the
                                    platform-reference skill. Auto-reply after
                                    publishing goes here as the top-level key
                                    "_firstComment", NOT a firstComment param:
                                    {"_firstComment": "Link in bio!"}
                                    Unsupported on discord, pinterest, tiktok,
                                    gmb, tumblr and snapchat (recorded as failed; the main
                                    post still publishes)
requestApproval (boolean)         — default false; hold a scheduled post for team
                                    approval (approvalStatus becomes "pending")
publishWhenApproved (boolean)     — default false; with requestApproval, publish
                                    the post as soon as it is approved even if
                                    that is after its scheduled time
linkTrackingOverride (boolean|null) — default null; per-post override for
                                    bulkpubli.sh link tracking. true shortens the
                                    post's links and counts clicks, false posts
                                    them as written, null inherits the org setting.
                                    Pro and Business only: on Free, links always
                                    publish as written
```

`linkTrackingOverride` is tri-state, so **omit it unless the user actually asked
for one behaviour or the other** — sending `false` is an explicit "post the links
as written" and is not the same as leaving it unset. Shortening happens at
publish time, per channel, and is **skipped** for any channel where the rewrite
would push the post past that platform's character limit: a short URL is 28
characters and can be longer than the link it replaces, so on X (280) or Bluesky
(300) tracking may silently not apply. The post still publishes, with its
original links.

Every post object returned by the API also carries the read-only approval fields
`approvalStatus` (`"none"` default | `"pending"` | `"approved"` | `"rejected"`),
`approvedBy` (string|null), `approvedAt` (date-time|null) and `rejectionReason`
(string|null). See "Team approval" below.

## Post type overrides

| Platform | Types |
|---|---|
| Instagram | `reel`, `story`, `carousel` |
| Facebook | `story`, `reel` |
| TikTok | `photo_slideshow` |
| YouTube | `short` |
| X/Twitter | `thread` |
| Threads | `thread` |
| Bluesky | `thread` |
| Mastodon | `thread` |

## Team approval

`approvalStatus` is **orthogonal to `status`**: `pending` and `rejected` posts do
not publish, even when they are scheduled and overdue. Default is `"none"`.

- **Requesting approval** — pass `requestApproval: true` on `create_post` or
  `update_post` (default `false`) to hold a scheduled post for team approval;
  `approvalStatus` becomes `"pending"`. For API keys belonging to members whose
  role lacks `post:publish` (contributors), this is **forced server-side
  regardless of the flag** — their scheduled posts always land in the approval
  queue. Never tell such a user their post was scheduled: check the returned
  `approvalStatus` and say it is awaiting approval. Approval applies only to
  scheduled posts: a `draft` ignores `requestApproval` (it stays `"none"`).
- **The approval queue** — `list_posts` with `approvalStatus: "pending"` (the
  filter accepts `none` | `pending` | `approved` | `rejected`), or
  `GET /api/posts?approvalStatus=pending`.
- **Approving** — `approve_post` (postId), i.e. `POST /api/posts/{id}/approve`,
  optional `whenLate` and `ifUnmodifiedSince`. Requires a role with `post:approve` (owner, admin, approver).
  Releases the post: it publishes at its scheduled time, or immediately if that
  time passed less than 15 minutes ago. If it passed more than 15 minutes ago,
  the post is approved but NOT published: it comes back with `status` `"draft"`
  (`approvalStatus` `"approved"`, `scheduledAt` unchanged) and the author is
  notified to choose a new time — unless the approver says otherwise with
  `whenLate`: `"publish"` publishes it now, `"hold"` returns it to draft. Left
  out, the post's `publishWhenApproved` decides (`true` publishes, otherwise it
  goes back to draft). Only pass `whenLate` when the user says what they want
  for a late post. Check the returned `status` and tell the user
  it needs rescheduling rather than saying it went out. The author is notified
  in-app either way.
- **Rejecting** — `reject_post` (postId, optional `reason` max 2000 chars,
  optional `ifUnmodifiedSince`), i.e.
  `POST /api/posts/{id}/reject`. The post returns to draft with `approvalStatus`
  `"rejected"` and the reason; the author is notified and can edit + reschedule
  to resubmit for approval.
- **Approve the version the user saw** — both tools take an optional
  `ifUnmodifiedSince`: pass the `updatedAt` of the post exactly as you showed it
  to the user. If the post changed since, nothing is written and you get **409**
  (`error.updatedAt` is the current value), so an edit nobody reviewed is never
  approved. Omit it to act on whatever version is current. Both approving and
  rejecting set `publishWhenApproved` to `false`.
- Both return the post on 200; **400** if the post is not awaiting approval or
  `ifUnmodifiedSince` is not an ISO 8601 timestamp, **403** if the role lacks
  `post:approve`, **404** if not found, **409** if the post changed since you
  loaded it (checked when `ifUnmodifiedSince` is sent) or is no longer awaiting
  approval — reload it with `get_post`, show the user what is there now, and
  review again.
- **Publish as soon as approved** — `publishWhenApproved: true` on `create_post`
  or `update_post` (default `false`, kept only while the post awaits approval)
  means a late approval publishes the post straight away instead of returning it
  to draft. Set it when the user wants the post out "now, once it's approved":
  schedule it for the current time with `requestApproval: true` and
  `publishWhenApproved: true`. Do NOT set it when the user picked a specific
  time: a post meant for Friday 9am should not go out on Monday just because
  that is when it was approved. Post responses carry `publishWhenApproved`.
- **`APPROVAL_REQUIRED`** — `publish_post` and `retry_post` return **403** with
  error code `APPROVAL_REQUIRED` for roles without `post:publish`. Do not retry:
  create/update the post with `requestApproval: true` and tell the user a
  teammate has to approve it. Publishing a pending/rejected post *as an
  approver* implicitly approves it.

## Publishing flow

- **Draft then publish**: `create_post` (status: "draft") → `publish_post` (postId)
- **Schedule for later**: `create_post` (status: "scheduled", scheduledAt: "2026-04-12T09:00:00Z")
- **Schedule with review**: `create_post` (status: "scheduled", scheduledAt: ..., requestApproval: true) → a teammate calls `approve_post`
- **Publish now, with review**: `create_post` (status: "scheduled", scheduledAt: <current time>, requestApproval: true, publishWhenApproved: true) → it publishes the moment a teammate approves it
- **Optimal timing**: call `get_queue_slot` (optionally pass `timezone`, default UTC) to get the best next slot. It returns `{scheduledAt, dayLabel}`: pass `scheduledAt` straight to `create_post`. It does NOT take a channelId or date (any such args are ignored).
- **Retry failures**: `retry_post` (postId, optional `republish`) re-queues the
  post's `failed` platforms. A platform can also end in status `unconfirmed` —
  terminal: the publish request may have reached the platform but its response
  was lost, so the post **may already be live**; it is never auto-retried. If
  the post has unconfirmed platforms and no failed ones, `retry_post` returns
  **400** with code `UNCONFIRMED_REQUIRES_REPUBLISH` — ask the user to check
  the account on the platform, and only pass `republish: true` (default false)
  after they confirm the post is not live; it also retries the unconfirmed
  platforms and **can duplicate the post**.
- **Publish as story**: set `postTypeOverrides` to `"story"` for Facebook/Instagram — publishes directly as a story, no separate call needed
- **Re-publish existing post as story**: use `publish_story` (postId, platform) — for posts already created as regular posts

## Stories vs postTypeOverrides

To publish as a story, use `postTypeOverrides` at creation time:
```json
{ "postTypeOverrides": { "facebook": "story", "instagram": "story" } }
```
This publishes the post AS a story. The separate `publish_story` tool is only for re-publishing an already-created post as an additional story after the fact.

## Character limits

| Platform | Limit |
|---|---|
| X/Twitter | 280 (25,000 long posts) |
| Instagram | 2,200 |
| Facebook | 63,206 |
| LinkedIn | 3,000 |
| TikTok | 2,200 |
| YouTube | 5,000 (description) |
| Threads | 500 |
| Bluesky | 300 |
| Pinterest | 500 |
| Google Business | 1,500 |
| Mastodon | 500 |

## Platform media requirements

| Platform | Requires | Notes |
|---|---|---|
| YouTube | Video ONLY | Do NOT include YouTube for image-only posts |
| TikTok | Video ONLY | Or images for `photo_slideshow` type |
| Instagram | Depends on type | `feed_photo`=image, `reel`/`feed_video`=video, `carousel`=2-10 mixed |
| Pinterest | Image or video | Needs board ID in `platformSpecific` or channel default |
| Facebook/X/LinkedIn/Threads/Bluesky/Mastodon | Any or none | Text-only posts OK |

## RSS Autopost (REST API)

Auto-create posts from an RSS/Atom feed — BulkPublish checks each feed on a plan-dependent interval (every 60 minutes on Free and Lifetime, 30 on Pro, 15 on Business) and turns new items into posts. MCP tools `list/create/update/delete_rss_feed` exist (mcp-server ≥1.5.0); the REST API is `Authorization: Bearer bp_your_key`, base `https://app.bulkpublish.com`.

| Endpoint | Use for |
|---|---|
| `GET /api/rss-feeds` | List feeds (ordered by name) |
| `POST /api/rss-feeds` | Create — body `{name, feedUrl, channelIds, mode?, fieldMapping?}` |
| `PUT /api/rss-feeds/{id}` | Partial update — body `{name?, feedUrl?, channelIds?, mode?, fieldMapping?, enabled?}` |
| `DELETE /api/rss-feeds/{id}` | Delete |

- `mode` is `"draft"` or `"publish"`, **default `"draft"`** — draft: new feed items land as draft posts for review; publish: they are auto-published. `"publish"` needs a plan with RSS auto-publish (not Free): otherwise **403** `FEATURE_DISABLED`
- `feedUrl` must be a public http(s) RSS 2.0/Atom URL — the server validates it is reachable at create time
- `channelIds` needs at least 1 org-owned channel id; `name` max 100 chars
- The number of feeds is capped by plan (Free 1, Lifetime 3, Pro 10, Business 50); creating beyond it returns **403** with `error.code: "QUOTA_EXCEEDED"`
- **Changing `feedUrl` re-baselines the feed** (resets `lastCheckedAt`): only items newer than the change are posted — the old backlog is never flooded
- Feed object includes `enabled`, `lastCheckedAt`, `lastError` for troubleshooting
- **`fieldMapping`** (optional; `null` = default `{title}` + blank line + `{link}`, no enclosure attached, article image taken when a channel needs one) controls how an item becomes a post:
  - `template` — tokens `{title} {link} {description} {content} {author} {categories} {feedName}` plus any extra leaf field on the feed item as `{fieldName}`; a line whose tokens all render empty is dropped (max 2000 chars)
  - `mediaField` — `"none"` (default) / `"image"` / `"video"` / `"auto"` (video, else image); the enclosure is re-hosted to the org media library
  - `articleImage` — `"when_needed"` (default) / `"always"` / `"never"`; where a picture comes from when the item has no usable enclosure. `when_needed` takes one from the article the item links to, but only when a channel on the feed is on a platform that cannot publish without an image. Candidates: the article's share image, then a picture embedded in the item, then the largest pictures on the page; first one that imports cleanly and is at least 200x200 wins, max four tried. Post-level like `mediaField`, so it reaches every channel of the feed. Image-required platforms (Instagram, Pinterest, Snapchat) are skipped only when this finds nothing too; the video-only ones (TikTok, YouTube) are always skipped for items with no video — the reason lands in the activity log
  - `stripHtml` (default `true`); `truncate` — `"smart"` (default, word-boundary trim keeping a trailing link line) / `"hard"` / `"skip"` (drop that channel); `hashtags` (max 500 chars, appended)
  - `channelOverrides` — per-channel **text** overrides keyed by channel id *string* (`template`, `hashtags`, `stripHtml`, `truncate`); neither `mediaField` nor `articleImage` can be overridden per channel, and same-platform channels share one rendered text (written to the post's `platformContent`)
  - On `PUT`, send `"fieldMapping": null` to clear back to the default

## Common mistakes

- `channels` takes objects `{channelId, platform}`, NOT just IDs
- A scheduled post naming a disconnected channel returns **400** with
  `error.code: "CHANNEL_INACTIVE"` and `error.channelIds` listing them. Ask the
  user to reconnect those accounts or drop them from `channels`; a draft may
  still name one.
- Always call `list_channels` first to get valid channelId + platform pairs
- `scheduledAt` is ISO 8601. A time that is now or already past is accepted and publishes immediately, so double-check the date before sending.
- To publish immediately: create as draft, then call `publish_post`
- `mediaFileIds` are numbers from `upload_media`, not file paths
- **Do NOT send image-only posts to YouTube or TikTok** — they will fail
- **Instagram defaults to `feed_photo`** — set `postTypeOverrides.instagram` to `reel` or `feed_video` for video
- **Pinterest needs a board ID** — set via `platformSpecific.pinterest.boardId` or it tries to auto-create one
- **Never assume a scheduled post will go out** — if the response has
  `approvalStatus: "pending"`, it is held until someone approves it. Report that,
  not "scheduled".
- **`requestApproval` defaults to `false`** and `approvalStatus` defaults to
  `"none"` — only set the flag when the user asks for review, but always read the
  response back because contributors get it forced on.
- **Do not call `publish_post` again after a 403 `APPROVAL_REQUIRED`** — the role
  cannot publish; submit for approval instead.
- **Content char limits** are enforced per-platform — use `platformContent` for shorter overrides on Pinterest (500), Bluesky (300), etc.
