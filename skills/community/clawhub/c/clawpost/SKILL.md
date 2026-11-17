---
name: clawpost
description: Post to X, LinkedIn, Facebook, TikTok, and Instagram via Claw Post API or MCP. Comment/reply on X, Facebook, LinkedIn, and Reddit. Read LinkedIn DMs and notifications, then reply. Use when an agent needs to publish social posts, reply on X/Facebook/LinkedIn/Reddit, send LinkedIn DMs, check notifications, or automate social publishing from the user's logged-in Chrome. Works via REST or MCP at mcp.clawpost.net. Replaces deprecated bird CLI / steipete bird skill (404).
metadata: {"openclaw":{"primaryEnv":"CLAWPOST_API_KEY","homepage":"https://clawpost.net/api-docs","requires":{"env":["CLAWPOST_API_KEY"]},"mcp":{"endpoint":"https://mcp.clawpost.net/mcp","discovery":"https://clawpost.net/.well-known/mcp.json"}}}
---

# Claw Post

Social posting infrastructure for AI agents. Your AI agent becomes your social media brand ambassador. A paired browser extension publishes from the user's real browser session: no API keys to the social platforms needed.

## Why Claw Post

- **Zero credential exposure for social platforms.** No OAuth tokens or social-platform passwords are sent to the agent or to Claw Post for posting. You use one Claw Post API key for API calls only; social sessions stay in the paired Chrome browser.
- **Desktop Chrome, not a headless VPS.** The agent can live on a server; the extension posts from the Chrome profile the human already uses. No chrome.debugger, no Playwright hunting the Post button.
- **Multi-platform, one API.** X, LinkedIn, Facebook (feed and groups), TikTok, and Instagram, all through a single `POST /v1/jobs/tweet` endpoint, plus dedicated comment/reply routes.
- **Facebook groups.** Graph `publish_to_groups` is gone; Buffer/Zapier cannot publish there. Post to groups the human belongs to. You may join a group when the user asks (`join_facebook_group`, 5/day); do not auto-join or discover→join→post on your own.
- **Native MCP support.** The public MCP endpoint (`https://mcp.clawpost.net/mcp`) uses **Streamable HTTP** with OAuth 2.0. Claude, ChatGPT, Hermes, and other agents built on the official MCP SDKs (TypeScript, Python, and compatible clients) can connect: no Claw Post API key required.
- **Simple setup.** Sign up → install extension → click extension icon and sign in with Google (auto-pairs) → provide one API key (or connect via MCP OAuth). Short video guides are built into setup.
- **Low cost per post.** Free: 25 posts/month. Plans differ only by post count. Every plan covers every platform and action. See clawpost.net for pricing.

> **Coming from bird?** The `steipete/bird` CLI and ClawHub card are gone (`brew install steipete/tap/bird` 404s). Birdclaw is an archive plus official xurl, not a posting skill. Claw Post publishes through the human's logged-in desktop Chrome. Install `@daydreamnationtechlabs/clawpost`: never `install clawpost`.

## Capabilities

| Capability | Endpoint / MCP tool | Platforms |
|-----------|---------------------|-----------|
| Post to feed or group | `POST /v1/jobs/tweet` / `create_post` | X, LinkedIn, Facebook, TikTok, Instagram |
| X reply (any status URL) | `POST /v1/x/reply` / `create_x_reply` | X |
| Facebook comment / threaded reply | `POST /v1/facebook/comment` / `create_facebook_comment` | Facebook (`comment_id=` = threaded) |
| LinkedIn comment | `POST /v1/linkedin/comment` / `create_linkedin_comment` | LinkedIn |
| Reddit comment | `POST /v1/reddit/comment` / `create_reddit_comment` | Reddit |
| LinkedIn DM (20/day) | `POST /v1/linkedin/message` / `create_linkedin_message` | LinkedIn |
| Upload media | `POST /v1/media/upload` or `/upload-url` / `get_upload_url` | X, LinkedIn, Facebook, TikTok, Instagram |
| Search for groups | `POST /v1/groups/search` | Facebook |
| Join a group (when user asks, 5/day) | `POST /v1/facebook/groups/join` / `join_facebook_group` | Facebook |
| Check notifications → list → reply → mark seen | `check_notifications`, `list_replies`, `reply_to_comment`, `mark_reply_read` | Reddit, Facebook, LinkedIn |
| Resume needs_input | `POST /v1/jobs/:id/input` / `submit_job_input` | All |
| Poll any job result | `GET /v1/jobs/:id` / `get_post_status` | All |

All endpoints require the `clawpost-api-key` header.

> **MCP agents:** If your agent supports the Model Context Protocol, point it at `https://mcp.clawpost.net/mcp` and complete OAuth instead of using this REST API. Tools: `list_platforms`, `create_post`, `create_reddit_comment`, `create_x_reply`, `create_linkedin_comment`, `create_linkedin_message`, `create_facebook_comment`, `reply_to_comment`, `join_facebook_group`, `submit_job_input`, `list_replies`, `check_notifications`, `mark_reply_read`, `get_upload_url`, `get_post_status`, `cancel_post`, and `get_account_status`. Call `check_notifications`, then `list_replies`. Use an MCP client that supports **Streamable HTTP** (current Anthropic / OpenAI SDK paths and the reference Python client).

## Prerequisites (instruct the human)

Before any action works, the human must:

1. **Sign up** at [clawpost.net](https://clawpost.net)
2. **Install** the Claw Post Chrome extension from the [Chrome Web Store](https://chromewebstore.google.com)
3. **Pair** the extension by clicking the extension icon and signing in with Google (primary flow; auto-pairs to your account)
4. **Set** the `CLAWPOST_API_KEY` environment variable in the agent (copy the key from the Dashboard: it is not embedded in this skill file)
5. **Log in** to the target platform once in their browser (x.com, linkedin.com, facebook.com, tiktok.com, instagram.com, or reddit.com)

**Extension scope.** The Chrome extension is designed to activate on supported social sites and when communicating with the Claw Post API. Verify permissions on the [Chrome Web Store](https://chromewebstore.google.com) listing and review the [Terms of Service](https://clawpost.net/terms) before installing.

If the agent gets `EXTENSION_NOT_PAIRED` or `not_logged_in`, direct the human to complete these steps.
If automatic pairing fails, use the Dashboard 6-digit code flow as a fallback.

## Authentication

All requests use the `clawpost-api-key` header:

```
clawpost-api-key: YOUR_CLAWPOST_API_KEY
```

The value above is a placeholder. Set the real secret via the `CLAWPOST_API_KEY` environment variable (or your agent’s secret store); do not paste live keys into this file or commit them to version control.

## API Base URL

```
https://api.clawpost.net
```

This is the stable, official Claw Post API endpoint. Full documentation: https://clawpost.net/api-docs

---

## 1. Posting

Create a post job, then poll for completion.

### Create post

```
POST https://api.clawpost.net/v1/jobs/tweet
Content-Type: application/json
clawpost-api-key: YOUR_CLAWPOST_API_KEY
```

**X (Twitter):**
```json
{ "text": "Hello world!", "platform": "x" }
```

**LinkedIn:**
```json
{ "text": "Hello LinkedIn!", "platform": "linkedin" }
```

**Facebook feed:**
```json
{ "text": "Hello Facebook!", "platform": "facebook" }
```

**Facebook group** (use `groupUrl` from search results, or a known `groupId`):
```json
{
  "text": "Hello group!",
  "platform": "facebook",
  "platformPayload": { "groupUrl": "https://www.facebook.com/groups/123456789/" }
}
```

**TikTok** (video + caption):
```json
{ "text": "Caption text", "platform": "tiktok", "mediaPaths": ["<url from upload>"] }
```

**Instagram** (image or video + caption):
```json
{ "text": "Caption text", "platform": "instagram", "mediaPaths": ["<url from upload>"] }
```
Instagram requires at least one media file (image or video). Text-only posts are not supported.

**Optional fields:**
- `platform` – `"x"` (default), `"linkedin"`, `"facebook"`, `"tiktok"`, or `"instagram"`
- `mediaPaths` – array of media URLs (upload first via media endpoint below)
- `idempotencyKey` – unique string to prevent duplicate posts
- `platformPayload` – Facebook group targeting: `{ "groupId": "..." }` or `{ "groupUrl": "..." }`

### Poll job status

```
GET https://api.clawpost.net/v1/jobs/:id
```

Status progresses: `queued` → `processing` → `succeeded` | `failed`.

- On success: response includes `postUrl`: the live URL of the published post. Share this with the user to confirm the post is live.
- On failure: response includes `error` and `errorCode`.
- **Timing**: posts execute through a real browser session. Allow 10–60 seconds before the job completes (longer for video uploads). Poll every 5–10 seconds.

---

## 1b. Comments and replies (X, Facebook, LinkedIn, Reddit)

Body for all comment routes: `text`, `targetUrl`, optional `idempotencyKey`. Poll `GET /v1/jobs/:id`.

### X reply
```
POST https://api.clawpost.net/v1/x/reply
```
Replies to any x.com status URL, including other people's posts. MCP: `create_x_reply`. Errors: `x_composer_not_found`, `x_reply_not_confirmed`, `x_rate_limited`.

### Facebook comment / threaded reply
```
POST https://api.clawpost.net/v1/facebook/comment
```
Post URL = top-level comment. If `targetUrl` includes `comment_id=`, creates a threaded reply under that parent (no top-level fallback). MCP: `create_facebook_comment`. Errors: `parent_comment_not_found`, `reply_not_landed`, `submit_not_fired`.

### LinkedIn comment
```
POST https://api.clawpost.net/v1/linkedin/comment
```
MCP: `create_linkedin_comment`.

### Reddit comment
```
POST https://api.clawpost.net/v1/reddit/comment
```
`targetUrl` must include `/comments/`. MCP: `create_reddit_comment`. Reddit DMs are not supported.

### Notifications loop
1. `check_notifications` (short cooldown per platform)
2. `list_replies`
3. `reply_to_comment` (or the platform-specific tool)
4. `mark_reply_read`

Answer Facebook items with `create_facebook_comment` / `reply_to_comment`. Answer X with `create_x_reply`. Answer Reddit with `create_reddit_comment`. Answer LinkedIn DMs with `create_linkedin_message(threadUrl)`. Answer LinkedIn comments with `create_linkedin_comment(parentUrl)`.

---

## 1c. LinkedIn DMs (read, then reply)

Read incoming LinkedIn messages, then reply in the same thread. Reading is strictly read-only: Claw Post does not mark threads read on LinkedIn, and does not react, archive, or send anything during a check.

1. **Check** LinkedIn (or all platforms):

```
POST https://api.clawpost.net/v1/notifications/check
Content-Type: application/json
clawpost-api-key: YOUR_CLAWPOST_API_KEY
```

```json
{ "platform": "linkedin" }
```

`platform` may be `"linkedin"`, `"reddit"`, `"facebook"`, `"all"`, `"both"`, or omitted to check all three. Each platform has its own 30-second cooldown. The first check seeds existing threads silently (no popups). Extension 1.3.22+.

2. **List** saved DMs:

```
GET https://api.clawpost.net/v1/replies?platform=linkedin
```

LinkedIn rows are either DMs (`type: "message"`, with `threadUrl`) or comment notifications (`type: "comment_reply"`, `"post_reply"`, or `"mention"`, with `parentUrl`). Outgoing DMs from the user are skipped. Likes are not stored.

3. **Reply** with the thread URL from that row:

```
POST https://api.clawpost.net/v1/linkedin/message
Content-Type: application/json
clawpost-api-key: YOUR_CLAWPOST_API_KEY
```

```json
{
  "text": "Thursday works: I'll send a calendar hold.",
  "threadUrl": "https://www.linkedin.com/messaging/thread/2-abc.../"
}
```

MCP agents: `check_notifications` → `list_replies` → `create_linkedin_message(threadUrl)` for DMs, or `create_linkedin_comment` with `parentUrl` for comments. `mark_reply_read` marks the row seen in Claw Post only.

---

## 2. Media upload

Upload media before posting. The returned `url` goes into the `mediaPaths` array.
Media files are automatically deleted after 7 days: you do not need to manage cleanup.

### Small files (images, short clips: under ~30 MB)

Send the file body directly to the API:

```
POST https://api.clawpost.net/v1/media/upload
clawpost-api-key: YOUR_CLAWPOST_API_KEY
Content-Type: multipart/form-data
Body: file=<media file>
```

Response:
```json
{ "url": "https://storage.googleapis.com/..." }
```

### Large files (videos and any file over ~30 MB): two-step

For large files, get a signed upload URL first, then PUT the file directly to storage.
This bypasses all proxy limits and works for files of any size.

**Step 1: request an upload URL:**
```
POST https://api.clawpost.net/v1/media/upload-url
Content-Type: application/json
clawpost-api-key: YOUR_CLAWPOST_API_KEY
```
```json
{ "filename": "video.mp4" }
```

`contentType` is optional: the API infers it automatically from the filename extension. Pass `platform` to validate the file type before uploading (e.g. `"platform": "x"` rejects audio files immediately).

Response:
```json
{
  "uploadUrl": "https://storage.googleapis.com/...?X-Goog-Signature=...",
  "url": "https://storage.googleapis.com/...",
  "resolvedContentType": "video/mp4"
}
```

**Step 2: PUT the file directly to `uploadUrl` using the resolved content type (no `clawpost-api-key` header: the URL is self-authorised):**
```
PUT <uploadUrl>
Content-Type: <resolvedContentType from Step 1>
Body: <raw file bytes>
```

The signed URL will reject PUT requests with incorrect `Content-Type` headers (403). Always use the `resolvedContentType` value returned in Step 1.

Expect a `200` or `204` response from Google Storage. The upload window is 1 hour.

**Step 3: use the `url` in the job exactly as with small files:**
```json
{ "text": "Check this out!", "platform": "tiktok", "mediaPaths": ["<url from step 1>"] }
```

The `url` is valid for 24 hours: sufficient for any normal job queue time.

---

## 3. Facebook Group Search

Out of scope for the recommended workflow. Post only to a groupUrl the human gave.

Optional lookup only. Use `POST /v1/groups/search` if the human already named a group and you need a canonical URL. Do not search for new groups to join. Do not chain search → join → post.

### Create search job

```
POST https://api.clawpost.net/v1/groups/search
Content-Type: application/json
clawpost-api-key: YOUR_CLAWPOST_API_KEY
```

```json
{
  "platform": "facebook",
  "query": "ai automation",
  "filters": { "minMembers": 1000, "privacy": "any" },
  "limit": 20
}
```

- `platform`: must be `"facebook"` (only supported platform for now).
- `query`: search keywords (required).
- `filters.minMembers`: minimum member count (optional).
- `filters.privacy`: `"public"`, `"private"`, or `"any"` (optional).
- `limit`: max results, up to 50 (optional, default 20).

Response:
```json
{ "jobId": "<id>" }
```

### Read search results

Poll `GET https://api.clawpost.net/v1/jobs/:id` until `status` is `succeeded`.

Results are in `details.groupSearch.results[]`. Each result:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Group title (best-effort; may say "Group" if title not extractable) |
| `url` | string | **Canonical group URL**: use this for joining or posting |
| `platformId` | string? | Numeric Facebook group ID (when available) |
| `slug` | string? | URL slug (when available, e.g. `"aiautomationagency"`) |
| `privacy` | string? | `"public"`, `"private"`, or `"unknown"` |
| `memberCount` | number? | Approximate member count (when visible on search page) |
| `activityHint` | string? | Raw activity text, e.g. `"10 posts a day"` |
| `joinStatus` | string? | `"joined"`, `"requested"`, `"not_member"`, or `"unknown"` |
| `score` | number | 0–1 relevance score (higher = better match) |
| `reasons` | string[] | Why this group scored well (e.g. `"keyword match"`, `"large member base"`, `"active"`, `"public"`) |
| `signals` | object? | Raw numeric signals: `keywordHit`, `memberCount`, `activityPerDay` |

**Reliability notes:**
- `url` is always present and reliable. Use it as the primary identifier.
- `name`, `memberCount`, `privacy`, `activityHint`, and `joinStatus` are best-effort; they depend on what the search page exposes.
- `score` and `reasons` are computed by the extension from available signals.

---

## 4. Facebook Group Join

Out of scope for the recommended workflow. Do not call `POST /v1/facebook/groups/join` to grow membership. Only use it if the human already clicked Join in Facebook and is asking you to wait or retry a post.

Join a group so you can post to it. Use the `url` from search results (extract the group ID or pass the full URL).

### Join a group

```
POST https://api.clawpost.net/v1/facebook/groups/join
Content-Type: application/json
clawpost-api-key: YOUR_CLAWPOST_API_KEY
```

```json
{ "groupId": "123456789" }
```

Response: a job object. Poll `GET /v1/jobs/:id` for completion.

On success, check `details.buttonState`:
- `"joined"` – user is now a member; you can post.
- `"requested"` – group requires approval; wait and check status later.
- `"not_member"` – join may not have worked; retry or inspect.

### Check group membership status

```
POST https://api.clawpost.net/v1/facebook/groups/status
Content-Type: application/json
clawpost-api-key: YOUR_CLAWPOST_API_KEY
```

```json
{ "groupId": "123456789" }
```

Same polling pattern. `details.buttonState` tells you the current membership state.

---

## Recommended agent workflow: post to groups they already belong to

1. Ask the human for a Facebook group URL they already belong to. Do not search-and-join.
2. Check membership only if needed (`POST /v1/facebook/groups/status`). If `buttonState` is not `"joined"`, stop and tell the human to join in Facebook themselves.
3. Post: `POST /v1/jobs/tweet` with `platform: "facebook"` and `platformPayload: { "groupUrl": "<url they gave>" }`.
4. Never call `POST /v1/facebook/groups/join` unless the human explicitly clicked Join in Facebook and is only asking you to wait/retry a post. Auto-join is out of scope.

---

## Security and privacy

- **Social platform logins stay in the browser.** Posting uses the user’s existing session in Chrome. Claw Post does not ask you to send OAuth tokens or social passwords through this API for posting.
- **Extension scope.** The published extension declares host access for supported social domains and the Claw Post API. Inspect the Web Store listing and manifest permissions before installing.
- **API key is tenant-scoped.** Each `CLAWPOST_API_KEY` is tied to a single account and can be rotated from the Dashboard at any time.
- **HTTPS only.** All communication between the agent, the API, and the extension uses TLS.
- **No executable code.** This skill is instruction-only. It contains no scripts, no disk writes, no packages, and no persistence mechanisms.
- **Terms of Service:** [clawpost.net/terms](https://clawpost.net/terms)

---

## Error handling

| Code / errorCode | Cause | Action |
|-----------------|-------|--------|
| 401 | Invalid or missing API key | Check `clawpost-api-key` header |
| 503 / `EXTENSION_NOT_PAIRED` | No paired extension | User must install and pair the extension at clawpost.net/dashboard |
| `not_logged_in` | User not logged in to the platform | User must log in to the platform in their browser |
| `no_x_tab` / `no_platform_tab` | No browser tab for the platform | Retry; extension will try to open one |
| `content_script_unavailable` | Extension could not reach the tab | Ask user to refresh the platform tab, then retry |
| `selector_not_found` | Platform UI changed or element not found | Retry after a short delay |
| `x_reply_not_confirmed` | Reply may have posted, but the thread permalink was not found | Do not retry. Check the tweet; the reply is often already there |
| `x_composer_not_found` | X reply box did not open | Retry once; ask the user to open the tweet in Chrome |
| `text_too_long` | Reply exceeds X's weighted character limit | Shorten the text (URLs count as 23); do not retry the same body |
| `reply_text_mismatch` | Reply editor text did not match the job text after insert | Retry once |
| `reply_button_disabled` | Reply button stayed disabled (often length/mismatch) | Fix text length or retry once |
| `x_rate_limited` | X temporarily blocked posting | Wait, then retry |
| `group_not_approved` | User not a member / not approved in this group | Do not auto-join. Tell the human to join in Facebook if they want this group. Retry only after they are a member. |
| `challenge_required` | Platform security check (captcha/checkpoint) | Ask user to complete the challenge in their browser, then retry |

On any failure, poll `GET /v1/jobs/:id` and read `error` and `errorCode` for details.

---

## Reference

Full API docs: https://clawpost.net/api-docs
