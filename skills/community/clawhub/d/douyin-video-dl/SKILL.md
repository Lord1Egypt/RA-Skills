---
name: douyin-dl
description: |
  Download Douyin (抖音) videos via the TikHub API — no login required.

  USE THIS SKILL whenever the user:
  - Shares a Douyin link (v.douyin.com, douyin.com, or any URL containing "douyin")
  - Pastes a modal_id or aweme_id (16–19 digit number)
  - Says "下载视频", "帮我下载", "save this video", "download this douyin"
  - Shares a short-link like "复制链接" text containing v.douyin.com
  - Asks to save, grab, or fetch a Douyin clip

  Always use this skill when you detect a Douyin URL or a numeric video ID — even if
  the user doesn't explicitly say "download". Just seeing a v.douyin.com link is enough.

  DO NOT USE FOR:
  - YouTube, Bilibili, Instagram, or other platforms (use their respective tools)
  - Douyin live streams (not supported by the API)
  - Douyin image carousels / 图集 (video-only)
---

# Douyin Downloader

Download Douyin videos using the TikHub API. Handles short links, full URLs, and bare video IDs.

## Configuration

Requires a TikHub API token in `~/.openclaw/config.json`:

```json
{ "tikhub_api_token": "your-token-here" }
```

Free tokens: https://user.tikhub.io/register

## Workflow

1. **Detect input** — identify a Douyin link or modal_id from the user's message
2. **Run the script** — call `python3 {baseDir}/scripts/douyin_download.py`
3. **Show result** — report the modal_id and either the video URL or the saved file path

## Commands

### Get video info (no download)
```bash
python3 {baseDir}/scripts/douyin_download.py "https://v.douyin.com/xxxxx/"
```

### Download to default location (~/Downloads/douyin/)
```bash
python3 {baseDir}/scripts/douyin_download.py "https://v.douyin.com/xxxxx/" --download
```

### Download to a custom directory
```bash
python3 {baseDir}/scripts/douyin_download.py "https://v.douyin.com/xxxxx/" --download --output-dir /path/to/dir
```

### Use a bare modal_id
```bash
python3 {baseDir}/scripts/douyin_download.py "7615599455526585067" --download
```

## Accepted Input Formats

| Format | Example |
|--------|---------|
| Short link | `https://v.douyin.com/iABCxyz/` |
| Full URL with modal_id | `https://www.douyin.com/video/7615599455526585067` |
| URL query param | `https://www.douyin.com/jingxuan?modal_id=7615599455526585067` |
| Bare modal_id | `7615599455526585067` |

## Output

- **Without `--download`**: prints modal_id + direct video URL
- **With `--download`**: downloads to `~/Downloads/douyin/douyin_<modal_id>.mp4` (or custom dir)
