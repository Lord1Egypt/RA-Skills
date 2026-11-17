---
name: fuxux-social-manager
description: >-
  Turn OpenClaw into an autonomous social media manager for Fuxux. Schedule and publish
  to 14 platforms (Twitter/X, Instagram, LinkedIn, Facebook, TikTok, YouTube, Bluesky,
  Threads, Pinterest, Discord, Kick, Twitch, Telegram, Slack) via REST API
  and MCP — media, drafts, queue, editing, publishing analytics, and AI caption generation.
version: 1.1.6
metadata:
  openclaw:
    emoji: "📡"
    homepage: https://www.fuxux.com/openclaw
    primaryEnv: FUXUX_API_KEY
    requires:
      env:
        - FUXUX_API_KEY
      anyBins:
        - curl
        - npx
    envVars:
      - name: FUXUX_API_KEY
        required: true
        description: >-
          Fuxux personal API key from Settings → API keys (fx_live_ + 40 hex chars).
          Used as Authorization Bearer token for REST and MCP.
      - name: FUXUX_BASE_URL
        required: false
        description: >-
          API origin override (default https://www.fuxux.com).
    install:
      - kind: node
        package: mcp-remote
    mcp:
      url: https://www.fuxux.com/api/mcp
      tools:
        - whoami
        - list_connected_accounts
        - get_dashboard
        - list_posts
        - create_post
        - get_post
        - update_post
        - delete_post
---

# Social Media Assistant (via fuxux.com)

Turn your OpenClaw agent into an autonomous social media manager using the **Fuxux** API and MCP server. Use when scheduling, posting, or managing content across **Twitter/X, Instagram, LinkedIn, Facebook, TikTok, YouTube, Bluesky, Threads, Pinterest, Discord, Kick, Twitch, Telegram, or Slack**. Covers media upload, post creation, scheduling, draft mode, queue inspection, editing and deleting posts, publishing analytics, and AI caption generation (`POST /api/ai/generate`).

---

## Setup

1. Create a Fuxux account at **[fuxux.com](https://www.fuxux.com)** and connect at least one social account (**Settings → Accounts** or onboarding).
2. Create an **API key**: **Settings → API keys** → **Create key**. Keys look like `fx_live_` + 40 hex characters (48 chars total). The full secret is shown **once** — store it safely.
3. Store the key in the agent workspace `.env` (never commit real keys):

   ```bash
   FUXUX_API_KEY=fx_live_your_secret_here
   ```

4. Download API docs for offline reference:
   - **OpenAPI JSON:** `https://www.fuxux.com/openapi.json`
   - **Interactive reference:** `https://www.fuxux.com/reference`
   - **MCP setup guide:** `https://www.fuxux.com/mcp/docs`

5. **(Recommended for OpenClaw)** Connect MCP so the agent can call Fuxux tools directly (see *MCP* below).

---

## Auth

All authenticated HTTP requests use a Bearer token:

```http
Authorization: Bearer <FUXUX_API_KEY>
```

**Primary env var:** `FUXUX_API_KEY`

---

## Base URL

Routes below are rooted at `https://www.fuxux.com` (e.g. `GET https://www.fuxux.com/api/accounts`).

---

## MCP (recommended for OpenClaw)

Fuxux exposes a **Streamable HTTP** MCP server. Send the same Bearer header on every MCP request.

| Endpoint | Notes |
|----------|--------|
| `https://www.fuxux.com/api/mcp` | Primary public MCP endpoint |

**OpenClaw / Claude Desktop (stdio bridge):**

```json
{
  "mcpServers": {
    "fuxux": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://www.fuxux.com/api/mcp",
        "--header",
        "Authorization: Bearer YOUR_FUXUX_API_KEY"
      ]
    }
  }
}
```

**Cursor / HTTP clients:**

```json
{
  "mcpServers": {
    "fuxux": {
      "url": "https://www.fuxux.com/api/mcp",
      "headers": {
        "Authorization": "Bearer ${env:FUXUX_API_KEY}"
      }
    }
  }
}
```

### MCP tools

| Tool | Purpose |
|------|---------|
| `whoami` | Validate token; return the account email, name and plan |
| `list_connected_accounts` | Connected social accounts + `connected` / `expired` status |
| `get_dashboard` | Stats, upcoming scheduled posts, platform snapshot |
| `list_posts` | Queue / calendar — optional `month` (`YYYY-MM`), `status` (`scheduled` \| `published` \| `draft` \| `failed` \| `all`), `limit` (1–50, default 20), `offset`, `order` (`upcoming` \| `newest` \| `recently_published` \| `recently_updated`) |
| `create_post` | Publish, schedule (`scheduled_at`) or save a draft (`draft: true`); optional `targets` (`account_id`, `platform`, `format`, `board_id`) to pick accounts |
| `get_post` | One post with its per-platform variants (variant ids for `update_post`); also finds drafts |
| `update_post` | Reschedule, edit captions (`variant_updates`), or replace media on a draft/scheduled post |
| `delete_post` | Delete a post from Fuxux (published posts stay on the platform — only Fuxux's record goes) |

Prefer MCP when the host supports it; fall back to REST when you need raw control.

---

## Core workflow (REST)

### 1. Validate auth / profile

```http
GET /api/settings/profile
Authorization: Bearer $FUXUX_API_KEY
```

Returns user id, email, `full_name`, `plan` (`free` \| `creator` \| `growth` \| `pro`).

### 2. List connected social accounts

```http
GET /api/accounts
Authorization: Bearer $FUXUX_API_KEY
```

Returns `accounts[]` with `id`, `platform`, `platform_username`, `status` (`connected` \| `expired`), `scopes`, and `via_reminder` (this isn't a real OAuth connection — it's a manual "notify me" entry for a platform Fuxux can't auto-publish to; Fuxux will remind the user to post it themselves rather than publishing on their behalf).

**Important:** Fuxux posts by **platform id** in the `captions` map (e.g. `twitter`, `instagram`), not by account UUID. Only include platforms the user has **connected** and that are not **expired** — `status: "expired"` means the account must be reconnected in the Fuxux dashboard (**Settings → Accounts**) before it can publish again; publishing to it will fail otherwise.

### 3. Dashboard summary

```http
GET /api/dashboard
Authorization: Bearer $FUXUX_API_KEY
```

High-level stats (`postsThisMonth`, `totalPublished`, `upcomingThisWeek`), next scheduled posts, and per-platform connection info.

### 4. Upload media

**Option A — Fuxux upload (works with `fx_live_` API keys too, not just browser sessions):**

```http
POST /api/media/upload
Content-Type: multipart/form-data
```

Form field **`file`**. Allowed: JPEG, PNG, GIF, WebP, MP4, MOV, WebM. Fuxux itself allows up to **50 MB**, but the underlying hosting platform hard-caps any single request body at **~4.5 MB** — files above that will fail here regardless of the 50 MB limit. For anything larger, use Option B.

Response includes public **`url`** — pass it in `media_urls` on post create.

**Option B — API-only / agent workspace (recommended, and required for files over ~4 MB):**

Upload video or image to your own CDN or object storage, then pass public HTTPS URLs in `media_urls` (up to **4** URLs).

### 5. Create post — publish now, schedule, or save draft

```http
POST /api/posts
Authorization: Bearer $FUXUX_API_KEY
Content-Type: application/json
```

**Body:**

| Field | Required | Description |
|-------|----------|-------------|
| `captions` | Yes* | Object: platform id → caption string. Unknown keys are ignored. |
| `prompt` | No | Short idea stored on the post (max 500 chars). |
| `scheduled_at` | No | ISO 8601 **future** datetime. Omit to **publish immediately**. |
| `media_urls` | No | Up to 4 public URLs (images/video). |
| `draft` | No | If `true`, saves as draft — does not publish or schedule. Cannot combine with `scheduled_at`. |

\* Not required when `draft: true` if `prompt` is set.

**Publish now — X + LinkedIn:**

```json
{
  "prompt": "Shipped analytics timeframe picker",
  "captions": {
    "twitter": "You can now pick 7/14/30/90 days in Fuxux Analytics 📊",
    "linkedin": "We shipped a clearer analytics experience — pick your chart window and keep monthly summaries separate."
  }
}
```

**Schedule for later:**

```json
{
  "captions": { "instagram": "Tomorrow: AMA at 3pm ET" },
  "scheduled_at": "2026-05-20T19:00:00.000Z",
  "media_urls": ["https://cdn.example.com/promo.jpg"]
}
```

**Save draft (publish later from Fuxux UI or a follow-up API call):**

```json
{
  "prompt": "Thread idea: 5 lessons from our first 100 customers",
  "captions": {
    "twitter": "Draft hook — refine before posting",
    "linkedin": "Long-form draft for LinkedIn"
  },
  "draft": true
}
```

**Immediate publish response** includes per-platform `results[]` with `success`, `platform_post_id`, and `error` when applicable — plus two fields worth checking before treating a result as a hard failure:

- `still_processing`: true means `success` is `false` but the post was **accepted** and may still go live shortly (some networks confirm status asynchronously). Don't retry or tell the user it failed — check `GET /api/posts?status=published` again after **at least 60 seconds** instead (never in a tight loop).
- `inbox_pending`: true means the platform accepted the media into an inbox/draft flow (e.g. TikTok's upload inbox) rather than publishing directly — counts as success, but the user may need to finish posting from within that platform's own app.

**Rate limits:** ~30 creates per 5 minutes per user; 120 requests/min per API key and 300/min per account across all keys. Over the limit returns `429` with `Retry-After` (seconds): wait that long before retrying. Don't poll: post status settles on the order of minutes, so check at most once a minute.

### 6. List posts (queue / calendar)

```http
GET /api/posts?month=2026-05&status=scheduled
Authorization: Bearer $FUXUX_API_KEY
```

| Query | Meaning |
|-------|---------|
| `month` | `YYYY-MM` — filter scheduled posts in that calendar month |
| `status` | `scheduled` \| `published` \| `draft` \| `all` |
| `limit` | Optional, 1–50 |

Response: `posts[]` with `post_variants` (per-platform content + status) and `counts` (`scheduled`, `published`, `drafts`).

### 7. Check publish status

There is no separate `/post-results` endpoint. Inspect status via:

```http
GET /api/posts?status=published
GET /api/posts?status=scheduled
```

Each post / variant has `status`: `draft`, `scheduled`, `publishing`, `published`, or `failed`. Failed variants include `error_message`.

For **immediate** publishes, the `POST /api/posts` response already returns `results[]`.

### 8. Delete a scheduled post

```http
DELETE /api/posts/{post_id}
```

Works with your `fx_live_` API key. A draft or scheduled post is removed and will never publish. For an already-published post this deletes only Fuxux's record — it does **not** remove the post from the social platform. Returns `409` while the post is mid-publish; wait a moment and retry.

### 9. Publishing analytics

```http
GET /api/analytics?days=30
```

`days` ∈ `7` | `14` | `30` | `90` (default `30`).

Returns publishing stats: totals, success rate, daily post counts, platform breakdown (published vs failed), recent posts.

Also includes real third-party **engagement** where available — likes, comments, shares, views, impressions, reach:
- `engagement`: totals across the selected window, plus `postsWithInsights` (how many posts have synced data).
- `platformBreakdown[].engagement` / `.postsWithInsights`: the same, broken down per platform.
- `recentPosts[].post_variants[].insights`: per-post detail, including `engagement_rate` (not summed at the aggregate level since it's a percentage).

Engagement is only populated for posts published to a platform with native insights support, and syncs in on a delay (a few hours after publish, refreshed periodically) — expect `postsWithInsights: 0` / missing `insights` for brand-new posts or platforms without engagement support yet.

Works fine with `fx_live_` API keys — `get_dashboard` via MCP is also a good lighter-weight option for quick summaries.

---

## Platform IDs (`captions` keys)

Use these string ids (must match connected accounts):

| Platform | Id | Typical char limit |
|----------|-----|-------------------|
| Twitter / X | `twitter` | 280 |
| Instagram | `instagram` | 2200 |
| LinkedIn | `linkedin` | 3000 |
| Facebook | `facebook` | 63206 |
| TikTok | `tiktok` | 2200 |
| YouTube | `youtube` | 5000 |
| Bluesky | `bluesky` | 300 |
| Threads | `threads` | 500 |
| Pinterest | `pinterest` | 800 |
| Discord | `discord` | 2000 |
| Kick | `kick` | 140 (stream title) |
| Twitch | `twitch` | 140 (stream title) |
| Telegram | `telegram` | 4096 (1024 as a media caption; longer text follows as its own message) |
| Slack | `slack` | 4000 |

**Platforms that need more than a caption** (send them through `targets` on `POST /api/posts`; Twitch/Kick categories are REST-only):

- **Google Business Profile is coming soon.** It can't be connected or posted to yet, so don't offer it or send a `google-business` caption.
- **Reddit is not available to agents.** Reddit posts are written and approved by the user in the Fuxux web app; a `reddit` caption or target is refused with 403 `reddit_web_only`. Don't retry it; tell the user to post to Reddit from the app.
- **Twitch / Kick** don't have posts: the **first line** of the caption becomes the channel's stream title, and publishing updates the channel (at the scheduled time, if scheduled). Optional category: `{"account_id": "<uuid>", "platform": "twitch", "category": {"id": "509658", "name": "Just Chatting"}}` (numeric Twitch game id / Kick category id). No media on either.

### Per-platform captions (Fuxux model)

Unlike APIs that take one caption + platform config objects, Fuxux expects **one caption per platform** in the `captions` map. Tailor tone and length per network:

```json
{
  "captions": {
    "twitter": "Short hook + link 🚀",
    "linkedin": "Three-paragraph story with a clear takeaway for professionals.",
    "instagram": "Visual-first caption with 3–5 hashtags #buildinpublic"
  },
  "media_urls": ["https://cdn.example.com/launch.mp4"]
}
```

Only include keys for platforms that are **connected** (`GET /api/accounts`).

---

## Connecting new accounts (human-in-the-loop)

The agent should **not** handle OAuth secrets alone. Instruct the user to connect in the Fuxux UI:

- **OAuth:** Twitter/X, Instagram, LinkedIn, Facebook, TikTok, YouTube, Threads, Pinterest, Discord, Kick, Twitch — **Settings → Accounts**
- **Bluesky:** app password in Fuxux UI (**not** in chat)
- **Telegram:** the user adds the Fuxux bot (@Fuxux_post_bot) as an admin of the channel or group with permission to post, posts the one-time code Fuxux shows in that chat, and clicks Verify
- **Slack:** **Connect** next to Slack in Fuxux (or **Add to Slack**), then pick the workspace and channel on Slack's screen

---

## Recommended workflow for video content

1. Keep source videos in a workspace folder (e.g. `content/inbox/`).
2. Optional: extract a frame for caption context:

   ```bash
   ffmpeg -i video.mp4 -ss 00:00:04 -frames:v 1 frame.jpg -y
   ```

3. Write per-platform captions (short for X/Bluesky, longer for LinkedIn).
4. Upload media to public storage **or** use Fuxux upload from the web app → copy `url`.
5. `POST /api/posts` with `captions` + `media_urls` — publish now or set `scheduled_at`.
6. Move posted assets to `content/posted/` to avoid duplicates.
7. After scheduled time, `GET /api/posts?status=published` or `get_dashboard` to confirm delivery.
8. Review `GET /api/analytics?days=30` for volume and success rate trends.

---

## Tips

- **List accounts first** — intersect `captions` keys with connected platforms, and skip any account with `status: "expired"` (tell the user to reconnect it in Settings → Accounts instead of trying to publish to it).
- **Stagger schedules** across the day (e.g. 9:00 and 15:00 UTC) for better reach.
- **Batch schedule** with future `scheduled_at` values; Fuxux publishes automatically at the scheduled time.
- **Draft mode** (`draft: true`) for human review before going live.
- **MCP `create_post`** mirrors REST — use it from OpenClaw for fewer raw HTTP calls.
- **429 / rate limits:** respect `Retry-After`; avoid burst posting and never poll in a loop without sleeping (once a minute is plenty for status checks).
- **AI captions:** `POST /api/ai/generate` works with `fx_live_` API keys and enforces a monthly quota by plan — for unauthenticated one-off copy ideas outside a Fuxux account, the public tools (`/api/tools/tiktok-caption`, `/api/tools/youtube-tags`) are also an option.

---

## API key coverage (today)

| Route | `fx_live_` API key |
|-------|-------------------|
| `GET /api/settings/profile` | ✅ |
| `GET /api/accounts` | ✅ |
| `GET /api/dashboard` | ✅ |
| `GET /api/posts` | ✅ |
| `POST /api/posts` | ✅ |
| `GET /api/analytics` | ✅ |
| `POST /api/media/upload` | ✅ |
| `GET /api/posts/{id}` | ✅ |
| `PATCH /api/posts/{id}` | ✅ |
| `DELETE /api/posts/{id}` | ✅ |
| `POST /api/ai/generate` | ✅ |

When a route returns `401` with an API key, tell the user to complete the action in the Fuxux web app or use MCP tools that wrap supported routes.

---

## Safety

1. Treat **`FUXUX_API_KEY` like a password** — rotate from Settings if leaked.
2. **Confirm before** mass posting or irreversible actions; dry-run with `list_posts` + `list_connected_accounts` first.
3. Warn users that agents may read workspace files (including `.env`) when following these instructions.

---

## Install (ClawHub)

```bash
openclaw skills install @abogitoff/fuxux-openclaw-skill
```

---

## Version

- **Skill:** `1.1.6` (see frontmatter)
- **Compatible with:** Fuxux production — `https://www.fuxux.com`
- **MCP server:** `fuxux` v1.2.5 (8 tools)
