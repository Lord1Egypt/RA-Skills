---
name: boring-tiktok-publisher
description: "Publish videos and photo carousels to TikTok using Boring. Use when the user says 'post to TikTok', 'upload TikTok video', 'create TikTok post', 'publish TikTok carousel', or wants to upload videos or photo slideshows to TikTok with privacy settings and draft mode."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🎵"
    homepage: https://boring-doc.aiagent-me.com/getting-started/mcp.html
    requires:
      config:
        - MCP Connector link from boring.aiagent-me.com (contains embedded auth token)
---

# Boring TikTok Publisher

Publish videos and photo carousels to TikTok. Powered by [Boring](https://boring-doc.aiagent-me.com).

## Security & Data Handling

- **MCP link is a credential**: Your MCP Server URL contains an embedded authentication token. Treat it like a password — do not share it publicly. Regenerate anytime in Settings.
- **Media uploads**: Video files and photos are uploaded to Boring's Google Cloud Storage to make them accessible for TikTok's API. TikTok requires media for all posts.
- **Data flow**: Your content and media are sent from Boring's server to TikTok's API on your behalf via your connected OAuth token.
- **No local credentials**: No local API keys or environment variables needed. All auth is embedded in the MCP link.

## Prerequisites

1. **Sign up** at [boring.aiagent-me.com](https://boring.aiagent-me.com) with Google
2. **Connect TikTok** account via OAuth
3. **Get your MCP link**: Go to **Settings** → copy your MCP Server URL (contains your auth token — treat it like a password)
4. **Add to Claude**: Paste the MCP link as a Connector — no install, no API key needed

## Workflow

### Step 1: List Accounts

Call `boring_list_accounts` and filter for `tiktok` platform.

### Step 2: Determine Content Type

TikTok supports:

| Type | Media | Specs |
|------|-------|-------|
| Video | 1 video | MP4 recommended, max 4GB, max 10 minutes |
| Photo Carousel | 2-35 images | PNG auto-converts to JPEG |

- **Caption**: Optional, max 2,200 characters
- **Media is required** — TikTok does not support text-only posts

### Step 3: Prepare Media

Upload files to get public URLs:
- **Local files**: `boring_upload_file` with `file_path`
- **External URLs**: `boring_upload_from_url`
- **Google Drive**: Pass directly

### Step 4: Publish

Call `boring_publish_post`:

**Video post**:
```
boring_publish_post(
  account_id="<tiktok_account_id>",
  platform="tiktok",
  text="Caption for the video #fyp #trending",
  media_urls=["https://...video.mp4"]
)
```

**Photo carousel**:
```
boring_publish_post(
  account_id="<tiktok_account_id>",
  platform="tiktok",
  text="Swipe through these photos!",
  media_urls=["https://...1.jpg", "https://...2.jpg", "https://...3.jpg"]
)
```

### Draft Mode

Use `draft: true` to send the video to the creator's TikTok inbox instead of publishing directly. The creator must manually publish it in the TikTok app.

```
boring_publish_post(
  account_id="<tiktok_account_id>",
  platform="tiktok",
  text="Review this before posting",
  media_urls=["https://...video.mp4"],
  draft=true
)
```

This is useful when:
- The user wants to preview before going live
- Adding TikTok-specific effects or music in the app
- Content needs final approval

### Step 5: Report

Show:
- Post ID and success status
- If draft: inform user to check their TikTok inbox to finalize

## TikTok-Specific Notes

- **Media required**: TikTok needs either a video or photos
- **Privacy**: Default is `PUBLIC_TO_EVERYONE`. Other options: `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY`
- **Video limits**: Max 4GB, max 10 minutes
- **Photo carousel**: Up to 35 images (PNG auto-converts to JPEG)
- **Draft mode**: Sends to creator's inbox for manual publish
- **Token**: 24-hour access token with auto-refresh (refresh token lasts 1 year)
- **Permissions**: `video.upload`, `video.publish`

## Error Handling

| Error | Solution |
|-------|----------|
| `MediaRequired` | TikTok requires video or photos |
| `MediaTooLarge` | Video max 4GB |
| `VideoProcessingFailed` | Check video format — MP4 recommended |
| `TokenExpired` | Reconnect at boring.aiagent-me.com |
| `PublishingFailed` | Check TikTok account status and permissions |

## Documentation

Full API docs: [boring-doc.aiagent-me.com](https://boring-doc.aiagent-me.com)
