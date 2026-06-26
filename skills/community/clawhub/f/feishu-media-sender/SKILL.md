---
name: feishu-send-media
description: 飞书媒体发送器 — 上传图片或视频并以媒体消息发送到飞书聊天中。图片直接预览，视频支持播放。补齐飞书渠道缺失的媒体投递能力。| Feishu Media Sender — Upload & send images/videos via Feishu OpenAPI with in-chat preview/playback.
license: MIT
compatibility: openclaw
metadata:
  version: "1.0.0"
  tags: [feishu, image, video, media, upload, im, messaging, openapi]
  openclaw:
    emoji: "🎬"
    requires:
      bins: [python3]
      config:
        - ~/.openclaw/openclaw.json
---

# Feishu Media Sender | 飞书媒体发送器

Upload images or videos to Feishu and send as media messages with in-chat preview/playback.

将图片或视频上传至飞书并以媒体消息发送，聊天中可直接预览/播放。

## Quick Start

```bash
# Send image (auto-detect)
python3 scripts/feishu_send_media.py --file photo.jpg --receive-id ou_xxx

# Send video
python3 scripts/feishu_send_media.py --file video.mp4 --receive-id ou_xxx

# Explicit type override
python3 scripts/feishu_send_media.py --file clip.gif --receive-id ou_xxx --type video
```

## Arguments

| Param | Required | Description |
|-------|----------|-------------|
| `--file` | ✅ | Local file path (absolute) |
| `--receive-id` | optional | Target `chat_id` or `open_id`. Falls back to `OPENCLAW_CHAT_ID` env var |
| `--receive-id-type` | optional | Auto-detected from prefix: `oc_` → chat_id, `ou_` → open_id |
| `--type` | optional | `image` or `video`. Auto-detected from file extension if omitted |

### Supported Formats

**Image:** JPG, JPEG, PNG, WEBP, GIF, BMP, ICO, TIFF, HEIC (max 10 MB)

**Video:** MP4, MOV, AVI, MKV, WEBM (max 30 MB, uploaded as MP4)

## How It Works

**Images:**
1. Upload via `/im/v1/images` → get `image_key`
2. Send message with `msg_type=image`, content `{"image_key": "..."}`

**Videos:**
1. Upload via `/im/v1/files` (file_type=mp4) → get `file_key`
2. Send message with `msg_type=media`, content `{"file_key": "..."}`

Credentials are auto-read from `~/.openclaw/openclaw.json`.

## API Reference

- [Upload Image](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create)
- [Upload File](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create)
- [Send Message](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create)
