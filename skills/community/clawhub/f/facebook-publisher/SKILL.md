---
name: facebook-publisher
description: "Publish posts to Facebook Pages. Use when the user says 'post to Facebook', 'publish on FB', 'schedule Facebook post', 'manage Facebook scheduled posts', or wants to create text, photo, album, or video posts on their Facebook Page."
version: 1.0.0
metadata:
  openclaw:
    emoji: "📘"
    homepage: https://boring-doc.aiagent-me.com/getting-started/mcp.html
    requires:
      config:
        - MCP Connector link from boring.aiagent-me.com (contains embedded auth token)
---

# Boring Facebook Publisher

Publish and schedule posts to Facebook Pages. Powered by [Boring](https://boring-doc.aiagent-me.com).

## Security & Data Handling

- **MCP link is a credential**: Your MCP Server URL (`https://boring.aiagent-me.com/mcp/t/xxxxx...`) contains an embedded authentication token. Treat it like a password — do not share it publicly.
- **Token scope**: The embedded token grants **publish access** to your connected social media accounts. It can create posts, upload media, and manage scheduled posts on the platforms you have connected. It cannot access your social media passwords or modify account settings.
- **Token storage**: The token is stored server-side in Boring's database (MongoDB on DigitalOcean). It is never written to your local filesystem. You can regenerate or revoke it anytime at [boring.aiagent-me.com/settings](https://boring.aiagent-me.com/settings).
- **Data flow**: Analytics queries are sent from Boring's server (Google Cloud, us-central1) to the platform's API on your behalf. Only performance metrics are retrieved — no content is uploaded or modified.
- **No local credentials**: No local API keys, environment variables, or secrets are needed. All auth is embedded in the MCP link.
- **Third-party service**: This skill relies on [Boring](https://boring.aiagent-me.com), an open-source social media management tool. Source code: [github.com/snoopyrain](https://github.com/snoopyrain).

## Prerequisites

1. **Sign up** at [boring.aiagent-me.com](https://boring.aiagent-me.com) with Google
2. **Connect Facebook** — requires admin access to a Facebook Page
3. **Get your MCP link**: Go to **Settings** → copy your MCP Server URL (contains your auth token — treat it like a password)
4. **Add to Claude**: Paste the MCP link as a Connector — no install, no API key needed

## Workflow

### Step 1: List Facebook Accounts

Call `boring_list_accounts` and filter for `facebook` platform accounts. Show the user their connected Pages.

### Step 2: Confirm Content

Ask the user what to post. Facebook supports:

| Type | Description | Media |
|------|-------------|-------|
| Text | Caption-only post | None |
| Photo | Single image post | 1 image (JPG/PNG, max 4MB) |
| Album | Multi-image post | 2-10 images |
| Video | Video post | 1 video (MP4/MOV, max 1GB, max 240 min) |

### Step 3: Prepare Media

If the user provides media:
- **Local file**: `boring_upload_file` with `file_path`
- **URL**: `boring_upload_from_url` with the URL
- **Google Drive link**: Pass directly to `media_urls`

### Step 4: Publish or Schedule

Call `boring_publish_post` with:
```
account_id: "<facebook_account_id>"
platform: "facebook"
text: "Your post content here"
media_urls: ["https://...image.jpg"]  (optional)
scheduled_at: "2025-12-25T10:00:00Z"  (optional, for scheduling)
```

**For immediate publish**: omit `scheduled_at`
**For scheduling**: include `scheduled_at` in ISO 8601 format

### Step 5: Report

Show the user:
- Post ID and success confirmation
- If scheduled: the scheduled time and post ID

## Managing Scheduled Posts

- **View scheduled**: `boring_list_scheduled_posts` with `platform: "facebook"`
- **Cancel**: `boring_cancel_scheduled_post` with the `scheduled_post_id`

## Facebook-Specific Notes

- **Token**: Facebook Page tokens never expire — no re-authentication needed
- **Data Access**: Valid for 90 days (auto-managed by Boring)
- **Rate Limit**: 200 API calls/hour per Page
- **Permissions**: `pages_manage_posts`, `pages_read_engagement`
- **Aspect Ratio**: 16:9 or 9:16 recommended for videos

## Error Handling

| Error | Solution |
|-------|----------|
| `InvalidApiKey` | MCP link may be invalid — regenerate it at boring.aiagent-me.com Settings |
| `InvalidAccountId` | Run `boring_list_accounts` to get valid account IDs |
| `MediaTooLarge` | Images max 4MB, videos max 1GB |
| `PublishingFailed` | Check if Page permissions are correct at boring.aiagent-me.com |
| `RateLimitExceeded` | Wait and retry — 200 calls/hour limit |

## Examples

**Text post**:
```
boring_publish_post(account_id="abc", platform="facebook", text="Hello from Boring!")
```

**Photo post**:
```
boring_publish_post(account_id="abc", platform="facebook", text="Check this out!", media_urls=["https://example.com/photo.jpg"])
```

**Schedule for tomorrow 9 AM UTC**:
```
boring_publish_post(account_id="abc", platform="facebook", text="Scheduled post!", scheduled_at="2025-12-26T09:00:00Z")
```

## Documentation

Full API docs: [boring-doc.aiagent-me.com](https://boring-doc.aiagent-me.com)
