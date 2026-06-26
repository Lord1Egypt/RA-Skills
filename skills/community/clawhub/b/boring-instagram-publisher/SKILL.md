---
name: boring-instagram-publisher
description: "Publish posts to Instagram using Boring. Use when the user says 'post to Instagram', 'publish on IG', 'schedule Instagram post', 'create Instagram carousel', 'post a Reel', or wants to publish photos, carousels, or Reels to their Instagram Business account."
version: 1.0.0
metadata:
  openclaw:
    emoji: "📸"
    homepage: https://boring-doc.aiagent-me.com/getting-started/mcp.html
    requires:
      config:
        - MCP Connector link from boring.aiagent-me.com (contains embedded auth token)
---

# Boring Instagram Publisher

Publish photos, carousels, and Reels to Instagram. Powered by [Boring](https://boring-doc.aiagent-me.com).

## Security & Data Handling

- **MCP link is a credential**: Your MCP Server URL contains an embedded authentication token. Treat it like a password — do not share it publicly. Regenerate anytime in Settings.
- **Media uploads**: Local files or URLs are uploaded to Boring's Google Cloud Storage to make them accessible for publishing. Social media APIs require publicly accessible media URLs. Instagram requires media for all posts.
- **Data flow**: Your content and media are sent from Boring's server to Instagram's API on your behalf via your connected OAuth token.
- **No local credentials**: No local API keys or environment variables needed. All auth is embedded in the MCP link.

## Prerequisites

1. **Sign up** at [boring.aiagent-me.com](https://boring.aiagent-me.com) with Google
2. **Connect Instagram** — requires an **Instagram Business or Creator** account (personal accounts not supported)
3. **Get your MCP link**: Go to **Settings** → copy your MCP Server URL (contains your auth token — treat it like a password)
4. **Add to Claude**: Paste the MCP link as a Connector — no install, no API key needed

## Workflow

### Step 1: List Accounts

Call `boring_list_accounts` and filter for `instagram` platform.

### Step 2: Confirm Content

**IMPORTANT: Instagram requires media. Text-only posts are NOT supported.**

| Type | Media | Specs |
|------|-------|-------|
| Photo | 1 image | JPG/PNG, 320x320 to 1440x1440 |
| Carousel | 2-10 images | All images must have matching aspect ratios |
| Reels | 1 video | MP4, 9:16 vertical, up to 90 seconds |

- **Caption**: Up to 2,200 characters
- If the user only provides text with no media, inform them that Instagram requires at least one image or video

### Step 3: Prepare Media

Media must be publicly accessible URLs:
- **Local files**: `boring_upload_file` with `file_path` → returns public URL
- **External URLs**: `boring_upload_from_url` → re-hosts to Boring cloud storage
- **Google Drive links**: Pass directly to `media_urls`

### Step 4: Publish or Schedule

Call `boring_publish_post`:
```
boring_publish_post(
  account_id="<instagram_account_id>",
  platform="instagram",
  text="Your caption here #hashtags",
  media_urls=["https://...image.jpg"]
)
```

**For carousel** (2-10 images):
```
boring_publish_post(
  account_id="<instagram_account_id>",
  platform="instagram",
  text="Swipe to see more!",
  media_urls=["https://...1.jpg", "https://...2.jpg", "https://...3.jpg"]
)
```

**For Reels** (video):
```
boring_publish_post(
  account_id="<instagram_account_id>",
  platform="instagram",
  text="Check out this Reel!",
  media_urls=["https://...video.mp4"]
)
```

**Schedule**: Add `scheduled_at` in ISO 8601 format:
```
boring_publish_post(..., scheduled_at="2025-12-25T10:00:00Z")
```

### Step 5: Report

Show the post ID and confirmation. If scheduled, show the scheduled time.

## Managing Scheduled Posts

- **View**: `boring_list_scheduled_posts` with `platform: "instagram"`
- **Cancel**: `boring_cancel_scheduled_post` with `scheduled_post_id`

## Instagram-Specific Notes

- **Media is mandatory** — always need at least 1 image or video
- **Carousel aspect ratios**: All images in a carousel must have the same aspect ratio
- **Reels**: Vertical video (9:16), up to 90 seconds
- **Token**: 60-day long-lived token with auto-refresh
- **Rate Limit**: 200 calls/hour per user, 4,800/hour per app
- **Permissions**: `instagram_business_content_publish`, `instagram_business_basic`

## Error Handling

| Error | Solution |
|-------|----------|
| `MediaRequired` | Instagram requires media — ask user for an image or video |
| `InvalidCarouselSize` | Carousel needs 2-10 images |
| `CarouselCreationFailed` | Check that all images have the same aspect ratio |
| `MediaTooLarge` | Images max 8MB |
| `TokenExpired` | Reconnect at boring.aiagent-me.com |

## Documentation

Full API docs: [boring-doc.aiagent-me.com](https://boring-doc.aiagent-me.com)
