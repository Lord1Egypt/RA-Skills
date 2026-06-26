---
name: download-video
description: Use when the user wants to download a YouTube or Bilibili video by URL or title, saving to local Videos folder
---

# Download Video (YouTube / Bilibili)

## Overview

Use `yt-dlp` to download videos from YouTube or Bilibili. Downloads go to the user's `Videos` folder (`~/Videos`).

## Prerequisites

**yt-dlp** must be installed:
```
yt-dlp --version

# Install if missing
pip install yt-dlp        # cross-platform
winget install yt-dlp      # Windows
brew install yt-dlp        # macOS
sudo apt install yt-dlp    # Debian/Ubuntu
```

**ffmpeg** is recommended for merging video+audio streams.

## Download by URL

```
yt-dlp -o "<videos-dir>/%(title)s.%(ext)s" "<url>"
```

Replace `<videos-dir>` with the user's Videos folder path, and `<url>` with the video URL.

Supported URLs:
- YouTube: `https://www.youtube.com/watch?v=...` or `https://youtu.be/...`
- Bilibili: `https://www.bilibili.com/video/BV...`

## Download by Title (search)

```
# YouTube
yt-dlp -o "<videos-dir>/%(title)s.%(ext)s" "ytsearch1:<title>"

# Bilibili
yt-dlp -o "<videos-dir>/%(title)s.%(ext)s" "bilisearch1:<title>"
```

## Quick Reference

| Goal | Flag |
|------|------|
| Best quality (default) | `-f bestvideo+bestaudio/best` |
| Audio only (mp3) | `-x --audio-format mp3` |
| Specific resolution | `-f "bestvideo[height<=720]+bestaudio"` |
| Subtitles | `--write-subs --sub-langs zh-Hans,en` |
| Playlist (all videos) | just pass the playlist URL |
| Limit speed | `--rate-limit 2M` |

## Common Mistakes

- **"ffmpeg not found"** — merge of best video+audio fails. Install ffmpeg or use `-f best` (single stream).
- **Bilibili login-required content** — add cookies with `--cookies-from-browser chrome`.
- **Videos folder missing** — create it first.

## Workflow

1. **URL given** → download directly
2. **Title given** → use `ytsearch1:` or `bilisearch1:` prefix
3. **yt-dlp missing** → install, then retry
4. **Error** → read error message, check Common Mistakes above
