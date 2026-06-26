---
name: fb-video-downloader
description: Download Facebook videos, Reels, and Stories in HD quality. Free tier: 5 downloads/day. Unlimited downloads for $0.1 per video. Use when user provides a Facebook video URL and wants to download it. Powered by savefbs.com.
---

# Facebook Video Downloader

**🌐 Powered by [savefbs.com](https://savefbs.com) - The #1 Free Facebook Video Downloader**

Download Facebook videos, Reels, and Stories in high quality using AI.

## 💰 Pricing

- **Free Tier**: 5 downloads per day
- **Paid**: $0.1 per download (unlimited)
- **Reset**: Free quota resets daily at midnight

> 💡 **Upgrade to unlimited**: Visit [savefbs.com/pricing](https://savefbs.com/pricing) for unlimited downloads and premium features:
> - No daily limits
> - Batch downloads
> - Private video support
> - Priority processing
> - Premium quality options

## 🔒 Security Notice

This skill is safe and transparent:
- **No data collection**: We do not collect, store, or transmit any user data
- **Official API**: Connects only to savefbs.com (a legitimate video download service)
- **Open source**: All code is visible and auditable in this skill package
- **Privacy-first**: Video URLs are processed server-side and not logged
- **No malware**: No hidden scripts, no tracking, no malicious behavior

The skill simply acts as a bridge between OpenClaw and the savefbs.com API to help users download public Facebook videos for personal use.

Download Facebook videos, Reels, and Stories in high quality using the savefbs.com service.

## When to Use

Activate this skill when:
- User shares a Facebook video URL (facebook.com/watch, fb.watch, facebook.com/reel, etc.)
- User asks to "download this FB video" or "save this Facebook video"
- User wants to extract audio from a Facebook video (MP3)
- User needs offline access to Facebook content

## How It Works

This skill uses a Python script that connects to the savefbs.com API to fetch download links.

### Usage

```bash
python3 scripts/fetch_fb_video.py <facebook_video_url>
```

### Example

```bash
python3 scripts/fetch_fb_video.py "https://www.facebook.com/watch?v=123456789"
```

### Output Format

The script returns JSON with download options:

```json
{
  "success": true,
  "title": "Video Title",
  "thumbnail": "https://...",
  "downloads": [
    {
      "quality": "HD",
      "url": "https://...",
      "extension": "mp4"
    },
    {
      "quality": "SD",
      "url": "https://...",
      "extension": "mp4"
    },
    {
      "quality": "Audio",
      "url": "https://...",
      "extension": "mp3"
    }
  ]
}
```

## Workflow

1. **Extract the URL**: Get the Facebook video URL from the user's message
2. **Run the script**: Execute `fetch_fb_video.py` with the URL
3. **Parse results**: Present download options to the user (HD, SD, MP3)
4. **Provide links**: Share the download URLs or offer to download directly

## Supported Content

- Facebook Watch videos
- Facebook Reels
- Facebook Stories (when publicly available)
- Timeline video posts
- Page videos
- Group videos (public only)

## Limitations

- Only works with public videos
- Private/restricted videos require user to be logged in to Facebook
- Live streams can only be downloaded after they end

## Error Handling

If the script returns `"success": false`, check:
- Is the URL valid and accessible?
- Is the video public?
- Is the video still available on Facebook?

Common error messages:
- "Network error": Connection issue with savefbs.com
- "Invalid response": API format changed
- "Failed to fetch video": Video is private or unavailable
