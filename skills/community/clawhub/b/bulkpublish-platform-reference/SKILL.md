---
name: platform-reference
description: Complete reference for the 15 BulkPublish platforms — post types, media requirements, required fields, character limits, and platformSpecific options. ALWAYS consult before creating posts.
---

# BulkPublish — Platform Reference

## Quick Rules

- **YouTube & TikTok** require video — NEVER include them for image-only posts
- **Pinterest** requires a title — set `platformSpecific.pinterest.title`
- **YouTube** requires a title — set `platformSpecific.youtube.title`
- **Instagram** defaults to `feed_photo` — set `postTypeOverrides.instagram` for video content
- Use `platformContent` for shorter text on platforms with low char limits (Bluesky 300, Pinterest/Threads/Mastodon 500)

---

## Facebook

| Field | Value |
|---|---|
| Platform key | `facebook` |
| Char limit | 63,206 |
| Title required | No |

**Post types:**

| Type | Media | Notes |
|---|---|---|
| `post` (default) | 0-10 images OR 0-1 video | Text-only OK. No mixing images+video |
| `reel` | 1 video required | Vertical short-form video |
| `story` | 1 image OR 1 video required | Disappears after 24h |

**Media specs:** Image max 10MB (jpg/png/gif/webp). Video max 2GB (mp4/mov). Reel video 3–90s, Story video 3–60s; a plain video post has no length limit.

**platformSpecific options:**
- `linkPreview.url`
- `shareToStory` — boolean, also post it as a story
- `thumbnailUrl` — string, cover image URL for a video or Reel. Facebook only
  accepts a cover once the video exists, so it is applied after the video
  publishes and lands a moment after the post; a cover that cannot be fetched or
  that Facebook rejects leaves the video published with Facebook's own chosen
  frame rather than failing the post. Omit to let Facebook choose

---

## Instagram

| Field | Value |
|---|---|
| Platform key | `instagram` |
| Char limit | 2,200 |
| Title required | No |
| Account type | Business or Creator (personal rejected) |

**Post types:**

| Type | Media | Notes |
|---|---|---|
| `feed_photo` (default) | 1 image required | Single photo post |
| `feed_video` | 1 video required | Single video post |
| `reel` | 1 video required | Short-form video, 9:16 recommended |
| `story` | 1 image OR 1 video required | Disappears after 24h |
| `carousel` | 2-10 images/videos required | Mixed media OK |

**Media specs:** Image max 8MB (jpg/jpeg only). Video max 1GB (mp4/mov). Reel and feed video 3s–15min, Story video 3–60s; carousel videos are not length-checked.

**platformSpecific options:**
- `collaborators` — string (comma-separated) or array of usernames, without a leading `@`. Tagged as co-authors. Post types `feed_photo`, `feed_video`, `reel` and `carousel`; ignored on `story`
- `trialReel` — boolean, trial reel shown to non-followers first. Only takes effect with `postTypeOverrides.instagram: "reel"`; ignored on `feed_video`
- `graduationStrategy` — `"manual"` (default) or `"auto"`; ignored unless `trialReel` is true
- `shareToStory` — boolean, also post it as a story
- `thumbnailTimestamp` — number (seconds into the video) for the cover frame. Applies to `reel` AND `feed_video`. Ignored when `coverUrl` is also set
- `coverUrl` — string, cover image URL for a video or Reel. Instagram accepts a cover image or a cover moment, never both, so this wins over `thumbnailTimestamp`

**IMPORTANT:** If you have video and don't set `postTypeOverrides.instagram`, it defaults to `feed_photo` and FAILS. Always set to `reel` or `feed_video` for video.

---

## X / Twitter

| Field | Value |
|---|---|
| Platform key | `x` |
| Char limit | 280 (25,000 for long posts) |
| Title required | No |

**Post types:**

| Type | Media | Notes |
|---|---|---|
| `tweet` (default) | 0-4 images OR 0-1 video | Text-only OK. No mixing images+video |
| `thread` | Per-part media | Use `postFormat: "thread"` + `threadParts` |

**Media specs:** Image max 5MB (jpg/png/gif/webp), max 4. Video max 512MB (mp4/mov), max 1, up to 140s (up to 4 hours with X Premium; X checks this, BulkPublish does not).

---

## YouTube

| Field | Value |
|---|---|
| Platform key | `youtube` |
| Char limit | 5,000 (description) |
| Title required | **YES** — `platformSpecific.youtube.title` (1-100 chars) |
| Video required | **YES** — always |

**Post types:**

| Type | Media | Notes |
|---|---|---|
| `video` (default) | 1 video required | Standard upload |
| `short` | 1 video required | Vertical, under 3 minutes |

**Media specs:** Video max 128GB (mp4/mov/avi/wmv/flv/webm), max 1.

**platformSpecific options:**
- `title` — **REQUIRED**, 1-100 chars (falls back to first line of content)
- `privacyStatus` — `public` (default), `private`, `unlisted`
- `categoryId` — YouTube category ID (default 22)
- `madeForKids` — boolean (default false)
- `tags` — string array
- `playlistId` — add to playlist after upload
- `thumbnailUrl` — custom thumbnail URL

**IMPORTANT:** YouTube ONLY accepts video. Never include YouTube channel for image-only posts.

---

## TikTok

| Field | Value |
|---|---|
| Platform key | `tiktok` |
| Char limit | 2,200 |
| Title required | No (uses content) |
| Video required | **YES** (or images for slideshow) |

**Post types:**

| Type | Media | Notes |
|---|---|---|
| `video` (default) | 1 video required | Standard video upload |
| `photo_slideshow` | 1-35 images required | Auto-creates slideshow with music |

**Media specs:** Video max 4GB (mp4/mov), max 1. Image max 20MB (jpg/jpeg/webp), max 35 for slideshow.

**platformSpecific options:**
- `privacyLevel` — `PUBLIC_TO_EVERYONE` (default when omitted), `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY`; any other value is rejected with 400, and TikTok accepts only the levels the connected account offers
- `disableDuet` — boolean
- `disableStitch` — boolean
- `disableComment` — boolean
- `isAigc` — boolean (AI-generated content disclosure)
- `thumbnailTimestamp` — number (seconds into the video) for the cover frame

**IMPORTANT:** TikTok ONLY accepts video (or images for slideshow). Omitted privacy publishes as `PUBLIC_TO_EVERYONE` — ask the user and set `privacyLevel` explicitly.

---

## LinkedIn

| Field | Value |
|---|---|
| Platform key | `linkedin` |
| Char limit | 3,000 |
| Title required | No (optional for articles/videos) |

**Post types:**

| Type | Media | Notes |
|---|---|---|
| `post` (default) | 0-1 image OR 0-1 video | Text-only OK |
| `multi_image` | 2-20 images required | Image gallery |
| `pdf_carousel` | 2-20 images required | Converted to PDF carousel |
| `article` | 0-1 image (thumbnail) | Link share, requires `platformSpecific.url` |

**Media specs:** Image max 10MB (jpg/png/gif), max 20. Video max 500MB (mp4 only), max 1, 3s-30min.

**Account types:** `personal` (member profile) or `organization` (company page). Both are connected in the dashboard and then used like any other channel — `list_channels` reports which via `accountType`.

The two run on separate LinkedIn apps (company pages use the Community Management API, which LinkedIn requires to be the only product on its application), so they are **gated separately**. `list_platforms` reports company pages under `variants.organization`; the platform-level state covers personal profiles. Pages can be paused — no new page connections — while personal-profile posting is fully live. When a variant is what blocks a write, the 403 `PLATFORM_DISABLED` error carries an `accountType` field naming it.

**platformSpecific options:**
- `title` — article/video title
- `description` — article description
- `url` — **REQUIRED for article type**, link URL
- `carouselTitle` — PDF carousel title

---

## Pinterest

| Field | Value |
|---|---|
| Platform key | `pinterest` |
| Char limit | 500 |
| Title required | **YES** — `platformSpecific.pinterest.title` (1-100 chars) |
| Board required | **YES** — `platformSpecific.pinterest.boardId` (auto-creates "BulkPublish" board if missing) |

**Post types:**

| Type | Media | Notes |
|---|---|---|
| `pin` (default) | 1 image required | Standard pin, 2:3 ratio recommended |
| `video_pin` | 1 video required | Video pin |
| `carousel` | 2-5 images required | Multi-image pin |

**Media specs:** Image max 20MB (jpg/png/webp), max 5. 1000x1500 recommended. Video mp4/mov, max 1, 4s to 5 min; Pinterest publishes no file size for ordinary video pins (2GB is its video-ads figure).

**platformSpecific options:**
- `title` — **REQUIRED**, 1-100 chars (falls back to first 100 chars of content)
- `description` — pin description, max 500 chars
- `link` — destination URL
- `boardId` — target board ID (get from `get_channel_options`)
- `dominantColor` — hex color
- `coverImageUrl` — video pin cover image. Optional: when omitted the server uses an attached image, then the video's auto-extracted poster frame

---

## Threads

| Field | Value |
|---|---|
| Platform key | `threads` |
| Char limit | 500 |
| Title required | No |

**Post types:**

| Type | Media | Notes |
|---|---|---|
| `text` (default) | None | Text-only post |
| `image` | 1 image required | Photo post |
| `video` | 1 video required | Video post |
| `carousel` | 2-20 images/videos | Mixed media OK |
| `thread` | Per-part | Use `postFormat: "thread"` + `threadParts` |

**Media specs:** Image max 8MB (jpg/png), max 20. Video max 500MB (mp4/mov), max 20, each up to 5 min.

**platformSpecific options:** `quotePostId` — quote another Threads post

---

## Bluesky

| Field | Value |
|---|---|
| Platform key | `bluesky` |
| Char limit | 300 |
| Title required | No |

**Post types:**

| Type | Media | Notes |
|---|---|---|
| `post` (default) | 0-4 images OR 0-1 video | Text-only OK. No mixing. |
| `thread` | Per-part | Use `postFormat: "thread"` + `threadParts` |

**Media specs:** Image max 10MB auto-resized to <976KB (jpg/png/webp), max 4. Video mp4 only, max 1; no size limit is published for this upload path (~19MB is proven).

---

## Google Business Profile

| Field | Value |
|---|---|
| Platform key | `gmb` |
| Char limit | 1,500 |
| Title required | Only for events (`eventTitle`) |

**Post types:**

| Type | Media | Notes |
|---|---|---|
| `standard` (default) | 0-1 image | Business update |
| `event` | 0-1 image | Requires dates/times |
| `offer` | 0-1 image | Promotional offer |

**Media specs:** Image max 5MB (jpg/png), max 1. No video support.

**platformSpecific options:**
- `ctaType` — `BOOK`, `ORDER`, `SHOP`, `LEARN_MORE`, `SIGN_UP`, `CALL`
- `ctaUrl` — CTA destination URL (not needed for CALL)
- `eventTitle` — event title (required for event type)
- `startDate` / `endDate` — `YYYY-MM-DD` format
- `startTime` / `endTime` — `HH:MM` format
- `couponCode` — offer coupon code
- `redeemOnlineUrl` — offer redemption URL
- `termsConditions` — offer terms text

---

## Mastodon

| Field | Value |
|---|---|
| Platform key | `mastodon` |
| Char limit | 500 |
| Title required | No |

**Post types:**

| Type | Media | Notes |
|---|---|---|
| `post` (default) | 0-4 images OR 0-1 video | Text-only OK. No mixing. |
| `thread` | Per-part | Use `postFormat: "thread"` + `threadParts` |

**Media specs:** Image max 16MB (jpg/png/webp/avif/gif), max 4. Video max 99MB (mp4 only), max 1 (Mastodon sets no length limit).

**platformSpecific options:**
- `visibility` — `public` (default), `unlisted`, `private`, `direct`
- `spoilerText` — content warning text
- `language` — ISO 639-1 language code

---


## Discord

| Field | Value |
|---|---|
| Platform key | `discord` |
| Char limit | 2,000 |
| Title required | No |
| Target channel required | **YES** — `channelId` |

**Post types:** message with optional attachments (images/video), sent to a text channel of the connected server.

**Media specs:** up to **10 attachments**, 25MB each (Discord's limit for a non-boosted server). Images and video may be mixed.

**platformSpecific** — keyed by **channel ID**. A connected Discord "channel" in BulkPublish is an entire **server** (guild), so the message still needs a destination channel inside it:

```json
{"platformSpecific": {"discord": {"12": {"channelId": "1090123456789012345"}}}}
```

| Option | Notes |
|---|---|
| `channelId` | **REQUIRED.** The target Discord *text channel* snowflake — **not** the BulkPublish channel id used as the outer key. List postable channels via `GET /api/channels/{id}/options`. |

**Gotchas:** publishing uses a **global bot token**, not the per-user OAuth token. A failure is therefore never a re-authentication problem — reconnecting will not fix it and the channel is never flagged `needs_reconnect`. The real causes are permissions: the bot lacks access to the channel, cannot send messages there, or the channel was deleted.

---

## Telegram

| Field | Value |
|---|---|
| Platform key | `telegram` |
| Char limit | 4,096 (text) / 1,024 (media caption) |
| Title required | No |

**Post types:** text message, photo, video, or media group (up to 10 items), sent to the chat fixed when the channel was connected.

**platformSpecific:** **none.** Telegram accepts no options — there is nothing to select per post. To publish to a second channel or group, connect it as a separate BulkPublish channel.

**Media specs:** media is handed to Telegram as a **URL** rather than uploaded, and the Bot API caps download-by-URL far below its upload limits: **5MB** images (jpg/png/webp) and **20MB** video (mp4).

**Gotchas:** content is sent as **plain text with no parse mode**, so `&`, `<` and `>` are safe but Markdown you write is **not rendered** (URLs still auto-link). When a post has media and text longer than 1,024 characters, the media is sent captionless and the full text follows as a **second message** — nothing is truncated, but it arrives as two messages.

---

## Tumblr

| Field | Value |
|---|---|
| Platform key | `tumblr` |
| Char limit | 32,768 |
| Title required | No |

**Post types:** `post` — text, photo, or video post to a Tumblr blog.

**Media specs:** up to 30 images (jpg/png/gif/webp, 20MB each), OR exactly one video (mp4/mov, 500MB). A video CANNOT be combined with images in the same post.

**platformSpecific** — keyed by **channel ID**, because one Tumblr account can own several blogs:

```json
{"platformSpecific": {"tumblr": {"12": {"blogName": "myblog", "title": "Heading", "tags": ["art"], "link": "https://example.com"}}}}
```

| Option | Notes |
|---|---|
| `blogName` | Target blog. Defaults to the blog the channel was connected as. List options via `GET /api/channels/{id}/options`. |
| `title` | Rendered as a heading above the body. |
| `tags` | Array of strings, no leading `#`. Tags drive discovery on Tumblr more than on other networks. |
| `link` | Appended as a link block. |
| `sourceUrl` | Attribution URL stored as the post's source. |

---

## Snapchat

| Field | Value |
|---|---|
| Platform key | `snapchat` |
| Char limit | 160 (Spotlight description only) |
| Title required | No |

**Post types:** `story` (default), `saved_story`, `spotlight`.

**Media specs:** every Snapchat post requires exactly ONE media file — a jpg/png image or an mp4 video. Spotlight is **video-only**, 6-60 seconds.

**Caption handling:** plain stories carry NO text — the caption is only used as the Spotlight description (160 chars) and as a saved-story title fallback.

**platformSpecific** — a flat object applies to every Snapchat channel, or key options by **channel ID** (like Tumblr):

```json
{"platformSpecific": {"snapchat": {"title": "My saved story", "locale": "en_US", "saveToProfile": true}}}
```

| Option | Notes |
|---|---|
| `title` | Saved-story title, max 45 chars. Falls back to the caption when omitted. |
| `locale` | Spotlight only. Defaults to `en_US`. |
| `saveToProfile` | Spotlight only. Defaults to `true`. |

**Gotchas:** no first comments (`_firstComment` is unsupported and recorded as failed; the main post still publishes) and no comment reading/engagement.
