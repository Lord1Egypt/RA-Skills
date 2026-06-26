---
name: adaptlypost
description: Schedule and manage social media posts across Instagram, X (Twitter), Bluesky, TikTok, Threads, LinkedIn, Facebook, Pinterest, and YouTube using the AdaptlyPost API. Use when the user wants to schedule social media posts, manage social media content, upload media for social posting, list connected social accounts, check post status, cross-post content to multiple platforms, or automate their social media workflow. AdaptlyPost is a SaaS tool — no self-hosting required.
homepage: https://adaptlypost.com
version: 1.2.0
required_environment_variables:
  - name: ADAPTLYPOST_API_KEY
    prompt: AdaptlyPost API key
    help: Generate a dedicated, revocable token at https://adaptlypost.com → Settings → API Tokens
    required_for: all API calls
metadata:
  openclaw: { 'emoji': '📬', 'primaryEnv': 'ADAPTLYPOST_API_KEY', 'requires': { 'env': ['ADAPTLYPOST_API_KEY'] } }
  hermes:
    tags: [social-media, scheduling, marketing, api]
    category: productivity
---

# AdaptlyPost

Schedule social media posts across 9 platforms from one API. SaaS — no self-hosting needed.

## Setup

1. Sign up at https://adaptlypost.com/signup
2. Go to Settings → API Tokens → generate a **dedicated, revocable** API token for this agent — do not reuse a token that is also used by other tools or humans.
3. Connect only the social accounts the agent actually needs. The token has delegated access to every account in the group, so a smaller group = smaller blast radius.
4. Set the environment variable:
   ```bash
   export ADAPTLYPOST_API_KEY="adaptly_your-token-here"
   ```
   - **Hermes Agent**: the local CLI prompts for the key on first load. If you talk to Hermes through a messaging platform (Telegram, Discord, WhatsApp, etc.), it will **not** prompt for secrets there — set the key on the host via `hermes setup` or in `~/.hermes/.env` first.
   - **OpenClaw**: set it in your OpenClaw environment config as usual.

Base URL: `https://post.adaptlypost.com/post/api/v1`
Auth header: `Authorization: Bearer $ADAPTLYPOST_API_KEY`

## Safety rules — read before any write call

Posts are **public, attributable, and hard to fully retract**. Treat every `POST /social-posts` and `POST /upload-urls` as a high-impact action.

1. **Confirm before every post.** Before calling `POST /social-posts`, show the user a summary and get an explicit "yes" covering all four items:
   - **Content** — exact text (and per-platform overrides), media filenames
   - **Platforms** — which networks and which connected accounts (by `displayName`/`username`, not just ID)
   - **Timing** — "now", a specific scheduled time, or draft
   - **Visibility** — TikTok `privacyLevel`, YouTube `privacyStatus`, Instagram `postType`, etc.
     A previous "yes" does not authorize a new post. Re-confirm each one.
2. **Prefer drafts when uncertain.** If the user has not run this skill before, or the content is sensitive, default to `saveAsDraft: true` and let them review in the AdaptlyPost UI before publishing.
3. **Never batch without explicit batch consent.** If the user asks to schedule many posts in a row, ask them to confirm a **small first batch** (e.g. 1–3 posts) before scheduling the rest. A single typo or wrong connection ID will otherwise propagate to every queued post.
4. **Verify media before upload.** Files uploaded via `/upload-urls` are stored at a **public URL** that exists from the moment of upload — before the post goes live, and even if the post is never created. Before calling `/upload-urls`:
   - Confirm the exact file path with the user.
   - Refuse to upload files from directories that may contain unrelated content (`~/Downloads`, `~/Desktop`, screenshot folders, etc.) without an explicit per-file "yes".
   - Never upload a file the user did not name.
5. **Do not retry failed posts silently.** If a `POST /social-posts` returns an error or unexpected `skippedPlatforms`, surface it to the user and ask before retrying — do not loop.
6. **Scheduled / unattended runs default to drafts.** If you are running from a cron job, scheduled task, or any automation with no human in the loop, set `saveAsDraft: true` on every post — unless the user explicitly pre-authorized this exact recurring workflow (content source, platforms, accounts, timing, and visibility) when they set the schedule up. Never escalate a draft-only schedule to live posting on your own; that change requires a fresh human confirmation. If a required confirmation cannot be obtained because nobody is present, save a draft and report back instead of guessing.

## Core Workflow

### 1. List connected accounts

```bash
curl -s -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  https://post.adaptlypost.com/post/api/v1/social-accounts
```

Returns `{ "accounts": [{ "id", "platform", "displayName", "username", "avatarUrl" }] }`. Save the `id` — you'll use it as a connection ID when creating posts. **This applies to Facebook too**: the `id` is what goes into `pageIds`. Facebook page accounts also show a `pageId` field (the page's public ID on facebook.com, shown since pages have no `username`) — it is informational, do NOT use it as an identifier in API calls.

### 2. Publish a post immediately (no scheduling)

⚠️ **Immediate publish is irreversible from the agent's side** — once `POST /social-posts` returns, the content is live on the user's connected accounts. Only call this after the four-item confirmation in [Safety rules](#safety-rules--read-before-any-write-call).

To publish right away, simply **omit `scheduledAt` entirely** and do NOT set `saveAsDraft`:

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["TWITTER"],
    "contentType": "TEXT",
    "text": "This goes live right now!",
    "timezone": "America/New_York",
    "twitterConnectionIds": ["CONNECTION_ID_HERE"]
  }'
```

**IMPORTANT**: Do NOT set `scheduledAt` to a time in the near future as a workaround. Omitting `scheduledAt` is the correct way to publish immediately.

Returns `{ "postId", "queuedPlatforms", "skippedPlatforms", "isScheduled", "scheduledAt" }`.

**Important**: You must include the correct `*ConnectionIds` array for each platform in `platforms`. For example, if posting to Instagram and Twitter, include both `instagramConnectionIds` and `twitterConnectionIds`. There is no `facebookConnectionIds` — Facebook posts target a *page*, so it uses `pageIds`, filled with the Facebook account's `id` from `/social-accounts` (NOT its `pageId` field):

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["FACEBOOK"],
    "contentType": "TEXT",
    "text": "This goes live on my Facebook page right now!",
    "timezone": "America/New_York",
    "pageIds": ["FACEBOOK_ACCOUNT_ID_HERE"]
  }'
```

If you omit `pageIds` (or use a wrong id) the post will not reach Facebook — never guess the id, always take it from `/social-accounts`.

### 3. Schedule a text post for later

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["TWITTER"],
    "contentType": "TEXT",
    "text": "Your post text here",
    "timezone": "America/New_York",
    "scheduledAt": "2026-06-15T10:00:00.000Z",
    "twitterConnectionIds": ["CONNECTION_ID_HERE"]
  }'
```

### 4. Save a post as draft (no scheduling)

Same as scheduling, but set `saveAsDraft: true` and omit `scheduledAt`:

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["INSTAGRAM"],
    "contentType": "TEXT",
    "text": "Draft post to review later",
    "timezone": "Europe/London",
    "saveAsDraft": true,
    "instagramConnectionIds": ["CONNECTION_ID_HERE"]
  }'
```

### 5. Schedule a post with media (3-step flow)

⚠️ **The `publicUrl` returned in Step A is publicly reachable as soon as Step B completes** — even if you never create the post in Step C. Confirm the exact file path with the user before Step A, and never upload a file the user has not explicitly named.

**Step A** — Get presigned upload URLs:

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/upload-urls \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "files": [{ "fileName": "photo.jpg", "mimeType": "image/jpeg" }] }'
```

Returns `{ "urls": [{ "fileName", "uploadUrl", "publicUrl", "key", "expiresAt" }] }`.

**Step B** — Upload file to storage (this is required — Step A only mints a URL, it does not store anything):

```bash
curl -X PUT "UPLOAD_URL_HERE" \
  -H "Content-Type: image/jpeg" \
  --data-binary @/path/to/photo.jpg
```

Confirm this PUT returns a `2xx` status before continuing. If you skip it, fail it, or let the upload URL expire (1 hour), Step C will reject the post with `400 Bad Request` and `Media file(s) not found in storage: <url>` — the server verifies every `publicUrl` exists in storage before creating the post. On that error, re-run Step B and confirm `2xx`, then retry Step C.

**Step C** — Create post with the public URL:

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["INSTAGRAM"],
    "contentType": "IMAGE",
    "text": "Post with image!",
    "mediaUrls": ["PUBLIC_URL_FROM_STEP_A"],
    "timezone": "America/New_York",
    "scheduledAt": "2026-06-15T10:00:00.000Z",
    "instagramConnectionIds": ["CONNECTION_ID_HERE"]
  }'
```

For video: use `mimeType: "video/mp4"`, `contentType: "VIDEO"`.
For carousel: upload multiple files, include all public URLs in `mediaUrls`, use `contentType: "CAROUSEL"`.

### 6. List posts

```bash
curl -s -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  "https://post.adaptlypost.com/post/api/v1/social-posts?limit=20&offset=0"
```

Returns `{ "posts": [...], "total": 25, "hasMore": true }`. Use `limit` (1-100, default 20) and `offset` (default 0) for pagination.

### 7. Get post details

```bash
curl -s -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  https://post.adaptlypost.com/post/api/v1/social-posts/POST_ID
```

Returns full post object with platform-specific status for each target platform.

### 8. Cross-post to multiple platforms

Include multiple platforms and their connection IDs in a single request:

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["TWITTER", "BLUESKY", "LINKEDIN"],
    "contentType": "TEXT",
    "text": "Same post across 3 platforms!",
    "timezone": "America/New_York",
    "scheduledAt": "2026-06-15T10:00:00.000Z",
    "twitterConnectionIds": ["TWITTER_ID"],
    "blueskyConnectionIds": ["BLUESKY_ID"],
    "linkedinConnectionIds": ["LINKEDIN_ID"]
  }'
```

### 9. Use per-platform text

Override the default text for specific platforms:

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["TWITTER", "LINKEDIN"],
    "contentType": "TEXT",
    "text": "Default text for all platforms",
    "platformTexts": [
      { "platform": "TWITTER", "text": "Short version for X #shortform" },
      { "platform": "LINKEDIN", "text": "Longer professional version with more detail for LinkedIn audience." }
    ],
    "timezone": "America/New_York",
    "scheduledAt": "2026-06-15T10:00:00.000Z",
    "twitterConnectionIds": ["TWITTER_ID"],
    "linkedinConnectionIds": ["LINKEDIN_ID"]
  }'
```

## Platform-Specific Configs

Pass these as config arrays in the request body. See [references/platform-configs.md](references/platform-configs.md) for full details.

| Platform        | Config Field       | Key Options                                                                                                             |
| --------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| **TikTok**      | `tiktokConfigs`    | `privacyLevel` (required), `allowComments`, `allowDuet`, `allowStitch`, `sendAsDraft`, `brandedContent`, `autoAddMusic` |
| **Instagram**   | `instagramConfigs` | `postType` (FEED/REEL/STORY)                                                                                            |
| **Facebook**    | `facebookConfigs`  | `postType` (FEED/REEL/STORY), `videoTitle`                                                                              |
| **YouTube**     | `youtubeConfigs`   | `postType` (VIDEO/SHORTS), `videoTitle`, `tags`, `privacyStatus`, `madeForKids`, `playlistId`                           |
| **Pinterest**   | `pinterestConfigs` | `boardId` (required), `title`, `link`                                                                                   |
| **X (Twitter)** | —                  | No config object, uses `twitterConnectionIds` only                                                                      |
| **Bluesky**     | —                  | No config object, uses `blueskyConnectionIds` only                                                                      |
| **Threads**     | —                  | No config object, uses `threadsConnectionIds` only                                                                      |
| **LinkedIn**    | —                  | No config object, uses `linkedinConnectionIds` only                                                                     |

**Example with TikTok config:**

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["TIKTOK"],
    "contentType": "VIDEO",
    "text": "Check out this clip!",
    "mediaUrls": ["https://cdn.adaptlypost.com/social-media-posts/uuid/video.mp4"],
    "timezone": "America/New_York",
    "scheduledAt": "2026-06-15T18:00:00.000Z",
    "tiktokConnectionIds": ["TIKTOK_ID"],
    "tiktokConfigs": [{
      "connectionId": "TIKTOK_ID",
      "privacyLevel": "PUBLIC_TO_EVERYONE",
      "allowComments": true,
      "allowDuet": false,
      "allowStitch": true
    }]
  }'
```

## Supported File Types for Upload

| MIME Type         | Extension   | Use For |
| ----------------- | ----------- | ------- |
| `image/jpeg`      | .jpg, .jpeg | Images  |
| `image/png`       | .png        | Images  |
| `image/webp`      | .webp       | Images  |
| `video/mp4`       | .mp4        | Videos  |
| `video/quicktime` | .mov        | Videos  |

Upload 1-20 files per request.

## Media Specs Quick Reference

| Platform    | Images          | Video                     | Carousel        |
| ----------- | --------------- | ------------------------- | --------------- |
| TikTok      | Carousels only  | MP4/MOV, ≤250MB, 3s-10min | 2-35 images     |
| Instagram   | JPEG/PNG        | ≤1GB, 3-90s (Reels)       | Up to 10        |
| Facebook    | ≤30MB, JPG/PNG  | 1 per post                | Up to 10 images |
| YouTube     | —               | Shorts ≤3min, H.264       | —               |
| LinkedIn    | Up to 9         | ≤10min                    | Up to 9         |
| X (Twitter) | Up to 4         | —                         | —               |
| Pinterest   | 2:3 ratio ideal | Supported                 | 2-5 images      |
| Bluesky     | Up to 4         | Not supported             | —               |
| Threads     | Supported       | Supported                 | Up to 10        |

## Tips for the Agent

### CRITICAL — Always ask before posting

- **NEVER assume** whether the user wants to post now, schedule for later, or save as draft. **ALWAYS ask** the user: "Do you want to post this now, schedule it for a specific time, or save it as a draft?" Wait for their answer before making the API call.
- **No human present?** (cron job, scheduled task, unattended automation) → `saveAsDraft: true`, per Safety rule 6. Asking is only skippable when the user pre-authorized the exact recurring workflow.
- Before calling `POST /social-posts`, show a final summary covering **content, platforms (named, not just IDs), timing, and visibility**, and wait for an explicit "yes". Re-confirm for every post — prior approval does not carry over.
- When in doubt, **prefer `saveAsDraft: true`** so the user can review in the AdaptlyPost UI before anything goes live.
- For multi-post sessions, schedule a **small first batch (1–3)** and confirm before queuing the rest. A single mistake otherwise propagates across every queued post.
- If the user says "post now", "publish now", or "right away": **completely omit `scheduledAt` from the request body** — do NOT set it to a time in the near future. The API publishes immediately when `scheduledAt` is absent.
- If the user says "schedule": ask for the date and time, then set `scheduledAt` to an ISO 8601 timestamp.
- If the user says "draft": set `saveAsDraft: true` and omit `scheduledAt`.

### Timezone handling

- The `timezone` field is **required** on every post creation request.
- **On the first interaction**, ask the user: "What timezone are you in? (e.g., Europe/Berlin, America/New_York)". Once they answer, **remember it for all future posts** in this conversation — do not ask again.
- If the user has previously told you their timezone in this conversation, reuse it silently.
- Common timezones: `Europe/London`, `Europe/Berlin`, `Europe/Paris`, `America/New_York`, `America/Chicago`, `America/Los_Angeles`, `Asia/Tokyo`, `Australia/Sydney`.

### API workflow

- Always call `/social-accounts` first to get valid connection IDs for each platform.
- For media posts, complete the full 3-step upload flow (get upload URL → PUT file → create post with `mediaUrls`).
- `scheduledAt` must be ISO 8601 and in the future. Omit it when using `saveAsDraft: true`.
- Each platform needs its connection IDs: `twitterConnectionIds`, `instagramConnectionIds`, `blueskyConnectionIds`, `linkedinConnectionIds`, `tiktokConnectionIds`, `threadsConnectionIds`, `pinterestConnectionIds`, `youtubeConnectionIds`. Facebook uses `pageIds`, filled with the Facebook account's `id` from `/social-accounts`.
- TikTok configs **require** `privacyLevel` — always set it (e.g., `PUBLIC_TO_EVERYONE`).
- Pinterest configs **require** `boardId` — there is no way to fetch boards via this API currently, so ask the user which board to use.
- For carousels, upload multiple files and include all public URLs in `mediaUrls`.
- Use `platformTexts` to customize text per platform when cross-posting.
- Content types: `TEXT` (no media), `IMAGE` (single image), `VIDEO` (single video), `CAROUSEL` (multiple images/videos).
- Check `skippedPlatforms` in the response — it tells you if any platform was skipped and why.
