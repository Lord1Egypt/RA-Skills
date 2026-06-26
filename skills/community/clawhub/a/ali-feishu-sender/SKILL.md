---
name: ali-feishu-sender
description: |
  Send multimedia content to Feishu (Lark) via API. Use when: (1) sending images, audio, video, rich text, or cards to Feishu users/groups, (2) uploading media to Feishu, (3) user says "send to feishu/lark", (4) posting MiniMax generated content (images, TTS, music, video) to Feishu. Supports: inline images, native voice bubbles (opus+duration), inline video player (mp4+duration+cover), rich text with embedded media, interactive cards.
---

# Feishu Media Sender

Send multimedia messages to Feishu with proper formatting: inline images, voice bubbles, video players, rich text, and cards.

## Dependencies

- `ffmpeg` at `D:\ffmpeg\bin\ffmpeg.exe` (for audio conversion, video fix)
- `ffprobe` at `D:\ffmpeg\bin\ffprobe.exe` (for duration detection)
- Python 3.7+
- Feishu app credentials (pre-configured in script defaults)

## Quick Reference

Run the script at `scripts/feishu_media.py`:

```python
import sys; sys.path.insert(0, r'<skill_dir>/scripts'); from feishu_media import *
```

### Available Functions

| Function | Message Type | Key Features |
|----------|-------------|--------------|
| `send_text(text)` | text | Plain text |
| `send_image(filepath)` | image | Inline embed, auto-detect mime |
| `send_audio(filepath)` | audio | Voice bubble, auto→opus, auto duration |
| `send_video(filepath, cover_image=None)` | media | Inline player, faststart, auto duration |
| `send_rich_text(title, elements)` | post | Rich text with embedded media |
| `send_card(title, elements)` | interactive | Card with header color |

All functions accept optional: `open_id`, `token`, `app_id`, `app_secret`.

### Key Rules (learned from testing)

1. **Audio**: Must be opus format, must include `duration` (ms). Auto-converts non-opus via ffmpeg.
2. **Video**: Must upload as `file_type=mp4`, must include `duration` (ms). Script auto-applies `-movflags +faststart`.
3. **Video message type**: Use `msg_type=media` (not `video`), content uses `file_key` + optional `image_key` for cover.
4. **Image in video**: `image_key` is the cover thumbnail. Without it, video has no preview frame.
5. **Rich text media**: Use `{'tag': 'media', 'file_key': '...', 'image_key': '...'}` as an independent paragraph.
6. **File upload types**: `opus` (audio), `mp4` (video), `stream` (generic file), `pdf`, `doc`, `xls`, `ppt`.

### Example: Send MiniMax content to Feishu

```python
# Image
send_image('minimax-output/kitten.png')

# TTS voice bubble (auto converts mp3→opus)
send_audio('minimax-output/greeting.mp3')

# Video with cover (auto faststart + duration)
send_video('minimax-output/kitten_video.mp4', cover_image='minimax-output/kitten.png')

# Rich text with video
send_rich_text('阿离的报告', [
    [{'tag': 'text', 'text': '一舞剑气动四方~'}],
    [{'tag': 'media', 'file_key': 'file_xxx', 'image_key': 'img_xxx'}],
])
```

### CLI Usage

```bash
python scripts/feishu_media.py text "Hello"
python scripts/feishu_media.py image photo.png
python scripts/feishu_media.py audio greeting.mp3
python scripts/feishu_media.py video clip.mp4 --cover thumb.png
```
