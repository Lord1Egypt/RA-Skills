---
name: bilibili-watcher
description: Fetch and read transcripts from Bilibili (B 站) videos. Use when you need to summarize a B 站 video, answer questions about its content, or extract information from it.
author: Joshua
version: 1.0.0
triggers:
  - "watch bilibili"
  - "b 站总结"
  - "视频字幕"
  - "b 站 summary"
  - "analyze b 站 video"
metadata: {"clawdbot":{"emoji":"📺","requires":{"bins":["yt-dlp"]},"install":[{"id":"pip","kind":"pip","package":"yt-dlp","bins":["yt-dlp"],"label":"Install yt-dlp (pip)"}]}}
---

# Bilibili Watcher

Fetch transcripts from Bilibili (B 站) videos to enable summarization, QA, and content extraction.

## Usage

### Get Transcript

Retrieve the text transcript of a B 站 video.

```bash
python3 {baseDir}/scripts/get_transcript.py "https://www.bilibili.com/video/BV1xx411c7mD"
```

## Examples

**Summarize a video:**

1. Get the transcript:
   ```bash
   python3 {baseDir}/scripts/get_transcript.py "https://www.bilibili.com/video/BV1xx411c7mD"
   ```
2. Read the output and summarize it for the user.

**Find specific information:**

1. Get the transcript.
2. Search the text for keywords or answer the user's question based on the content.

## Notes

- Requires `yt-dlp` to be installed and available in the PATH.
- Works with videos that have closed captions (CC) or auto-generated subtitles.
- If a video has no subtitles, the script will fail with an error message.
- Supports B 站 video URLs in formats:
  - https://www.bilibili.com/video/BV1xx411c7mD
  - https://b23.tv/xxxxxx
  - https://www.bilibili.com/video/av12345678
