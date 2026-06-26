---
name: boring-social-media-publisher
description: "Publish social media posts to multiple platforms at once. Use when the user says 'post to social media', 'publish everywhere', 'cross-post', 'share on all platforms', 'publish to Facebook and Instagram', or wants to distribute content across Facebook, Instagram, Threads, YouTube, TikTok, or X simultaneously."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🚀"
    homepage: https://boring-doc.aiagent-me.com/getting-started/mcp.html
    requires:
      config:
        - MCP Connector link from boring.aiagent-me.com (contains embedded auth token)
---

# Boring Social Publisher

Publish content to multiple social media platforms with a single message. Powered by [Boring](https://boring-doc.aiagent-me.com) — a unified social media publishing API.

## Security & Data Handling

- **MCP link is a credential**: Your MCP Server URL (`https://boring.aiagent-me.com/mcp/t/xxxxx...`) contains an embedded authentication token. Treat it like a password — do not share it publicly.
- **Token scope**: The embedded token grants **publish access** to your connected social media accounts. It can create posts, upload media, and manage scheduled posts on the platforms you have connected. It cannot access your social media passwords or modify account settings.
- **Token storage**: The token is stored server-side in Boring's database (MongoDB on DigitalOcean). It is never written to your local filesystem. You can regenerate or revoke it anytime at [boring.aiagent-me.com/settings](https://boring.aiagent-me.com/settings).
- **Data flow**: Analytics queries are sent from Boring's server (Google Cloud, us-central1) to the platform's API on your behalf. Only performance metrics are retrieved — no content is uploaded or modified.
- **No local credentials**: No local API keys, environment variables, or secrets are needed. All auth is embedded in the MCP link.
- **Third-party service**: This skill relies on [Boring](https://boring.aiagent-me.com), an open-source social media management tool. Source code: [github.com/snoopyrain](https://github.com/snoopyrain).

## Prerequisites

1. **Sign up** at [boring.aiagent-me.com](https://boring.aiagent-me.com) with Google
2. **Connect your social accounts** — link Facebook Pages, Instagram Business, Threads, YouTube, TikTok, or X accounts via OAuth
3. **Get your MCP link**: Go to **Settings** → copy your MCP Server URL (contains your auth token — treat it like a password)
4. **Add to Claude**: Paste the MCP link into Claude settings as a Connector — no install, no API key needed

## Workflow

When the user wants to publish content across platforms, follow these steps:

### Step 1: Get Available Accounts

Call `boring_list_accounts` to see which platforms the user has connected. Show them a summary:
- Account name and platform
- Connection status

### Step 2: Confirm Content and Platforms

Ask the user:
- What content to post (text, images, videos)
- Which platforms to target (or "all")
- Whether to publish now or schedule for later

### Step 3: Prepare Media (if needed)

If the user provides local files or URLs:
- **Local files**: Use `boring_upload_file` with `file_path` to upload and get a public URL
- **External URLs**: Use `boring_upload_from_url` to re-host the media on Boring's cloud storage
- **Google Drive links**: Pass directly — Boring handles Google Drive URLs automatically

### Step 4: Adapt Content Per Platform

Automatically adjust content for each platform's requirements:

| Platform | Text Limit | Media Required | Notes |
|----------|-----------|----------------|-------|
| Facebook | No strict limit | No | Supports text, photo, album (2-10), video |
| Instagram | 2,200 chars | **Yes** | Photo, carousel (2-10), Reels (video 9:16) |
| Threads | 500 chars | No | Text, photo, carousel (2-20), video |
| YouTube | Title: 100, Desc: 5,000 | **Yes** (video) | Text format: `Title\n\nDescription` |
| TikTok | 2,200 chars | **Yes** (video or photos) | Video or photo carousel (up to 35) |
| X | 280 chars | No | Text, up to 4 images or 1 video |

**Important adaptations:**
- Truncate text to fit platform limits
- Skip Instagram if no media is available (media is mandatory)
- For YouTube: format text as `Video Title\n\nDescription text here`
- For Threads: split long content into a thread if over 500 chars using `boring_publish_thread`

### Step 5: Publish

For each selected platform, call `boring_publish_post` with:
- `account_id`: from the account list
- `platform`: the platform name
- `text`: adapted content
- `media_urls`: array of media URLs (if any)
- `scheduled_at`: ISO 8601 datetime if scheduling (e.g., `2025-12-25T10:00:00Z`)

### Step 6: Report Results

After publishing, summarize:
- Which platforms succeeded with post IDs
- Which platforms failed and why
- If scheduled, show the scheduled time and post IDs

## Scheduling

To schedule posts for later:
- Add `scheduled_at` parameter with ISO 8601 format: `2025-12-25T10:00:00Z`
- Use `boring_list_scheduled_posts` to view queued posts
- Use `boring_cancel_scheduled_post` to cancel before publish time

## Error Handling

| Error | Solution |
|-------|----------|
| `InvalidApiKey` | MCP link may be invalid — regenerate it at boring.aiagent-me.com Settings |
| `TokenExpired` | Ask user to reconnect the account at boring.aiagent-me.com |
| `MediaRequired` | Instagram/TikTok require media — skip or ask user for an image |
| `TextTooLong` | Truncate or split content for the platform |
| `RateLimitExceeded` | Wait and retry (check `retry_after` field) |
| `AccountDisabled` | Account was disconnected — reconnect at dashboard |

## Example Usage

**User**: "Post 'Just launched our new product!' with this image to all my accounts"

**Agent workflow**:
1. `boring_list_accounts` → finds Facebook, Instagram, Threads accounts
2. `boring_upload_from_url` (if image is a URL) → gets hosted URL
3. `boring_publish_post` to Facebook with text + image
4. `boring_publish_post` to Instagram with text + image
5. `boring_publish_post` to Threads with text + image
6. Report: "Published to 3 platforms successfully"

## Documentation

Full API docs: [boring-doc.aiagent-me.com](https://boring-doc.aiagent-me.com)
