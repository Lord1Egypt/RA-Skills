---
name: douyin-downloader
description: Download Douyin (抖音) short videos from URLs. Supports direct video links, search page links with modal_id, share links (v.douyin.com), and note links. Uses headless browser to bypass anti-scraping and extract video source. Use when asked to "download douyin video", "下载抖音视频", "save douyin clip", or given any douyin.com URL to download.
---

# Douyin Video Downloader

Downloads Douyin videos by opening the page in a headless browser, extracting the `<video>` source URL, and downloading via curl. This bypasses yt-dlp's cookie issues with Douyin's anti-scraping.

## Prerequisites

- `agent-browser` (`npm i -g agent-browser`)
- `curl`

## Usage

```bash
python3 scripts/douyin_download.py <URL> [--output-dir DIR] [--filename NAME]
```

## Supported URL Formats

- `https://www.douyin.com/video/<id>` — direct video page
- `https://www.douyin.com/search/...?modal_id=<id>` — search results with video modal
- `https://v.douyin.com/<code>` — share short links
- `https://www.douyin.com/note/<id>` — note/image posts with video

## Examples

```bash
# Basic download to ~/Downloads
python3 scripts/douyin_download.py 'https://www.douyin.com/video/7577715519366576522'

# Custom output directory and filename
python3 scripts/douyin_download.py 'https://www.douyin.com/video/7577715519366576522' \
  -o ~/Videos -f my_video

# From search page URL
python3 scripts/douyin_download.py 'https://www.douyin.com/search/关键词?modal_id=7577715519366576522'
```

## How It Works

1. Normalize URL → extract video ID, construct direct video page URL
2. Open page in `agent-browser` (headless Chromium)
3. Extract `<video>` element's `currentSrc` (CDN direct link)
4. Close browser
5. Download MP4 via `curl` with proper Referer header

## Notes

- No login required — fresh browser session is sufficient
- Video title auto-detected from page title for filename
- Large videos may take 30-60s to download depending on network
- CDN links are temporary (~2h validity); download promptly after extraction
