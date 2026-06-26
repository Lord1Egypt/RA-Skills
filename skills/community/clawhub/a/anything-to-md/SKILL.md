---
name: anything-to-md
description: "Convert any URL or file to Markdown. Supports webpage, WeChat, YouTube, Bilibili, Douyin, Xiaohongshu, PDF, and Office files."
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - ffmpeg
    install:
      - kind: brew
        formula: yt-dlp
        bins: [yt-dlp]
      - kind: brew
        formula: deno
        bins: [deno]
      - kind: brew
        formula: ffmpeg
        bins: [ffmpeg]
      - kind: brew
        formula: openai-whisper
        bins: [whisper]
      - kind: uv
        packages: [anything-to-md@git+https://github.com/haiwenai/anything-to-md.git]
    emoji: "📄"
    homepage: https://github.com/haiwenai/anything-to-md
---

# anything-to-md

Convert any URL or file to high-quality Markdown using the `tomd` command.

## Supported Inputs

- **Webpage URL** — any website article
- **WeChat article** — `mp.weixin.qq.com` links
- **YouTube video** — extracts subtitles or downloads audio for ASR transcription
- **Bilibili video** — downloads audio and transcribes via Whisper ASR
- **Douyin video** — extracts from iesdouyin (zero-dependency), transcribes audio
- **Xiaohongshu post** — image/video notes, supports share text with URL extraction
- **Local files** — PDF, DOCX, PPTX, XLSX, EPUB, CSV, JSON, etc.

## How to Use

When the user provides a URL or file path and asks to convert it to Markdown, run:

```bash
tomd "<input>" --stdout
```

Where `<input>` is:
- A URL: `https://example.com/article`
- A share text containing a URL (common for Douyin/Xiaohongshu): `"照着做！... http://xhslink.com/xxx ..."`
- A local file path: `~/Documents/paper.pdf`

### Options

- `--stdout` — output Markdown to stdout (default when used as a skill)
- `-o <path>` — save to a specific file
- `-d <dir>` — save to a specific directory
- `--type <type>` — force input type: `webpage`, `wechat`, `youtube`, `bilibili`, `douyin`, `xiaohongshu`, `file`
- `-v` — verbose output with progress logs

### Examples

```bash
# Convert a webpage
tomd "https://example.com/article" --stdout

# Convert a YouTube video (extracts subtitles or ASR)
tomd "https://www.youtube.com/watch?v=xxxxx" --stdout

# Convert a WeChat article
tomd "https://mp.weixin.qq.com/s/abc123" --stdout

# Convert a Bilibili video
tomd "https://www.bilibili.com/video/BVxxx" --stdout

# Convert from Douyin share text
tomd "https://v.douyin.com/xxx" --stdout

# Convert a Xiaohongshu post
tomd "https://www.xiaohongshu.com/explore/xxx" --stdout

# Convert a local PDF
tomd ~/Documents/paper.pdf --stdout
```

## Output Format

The output is Markdown with YAML frontmatter containing metadata:

```markdown
---
title: Article Title
author: Author Name
source_url: https://...
source_type: webpage
date: 2026-04-22
---

Article content in Markdown...
```

For video content, the output includes a `## Transcript` section with timestamped text.

## Error Handling

- If `tomd` is not found, install it: `uv pip install "anything-to-md[video] @ git+https://github.com/haiwenai/anything-to-md.git"`
- If `ffmpeg` is not found: `brew install ffmpeg`
- If `yt-dlp` is not found: `brew install yt-dlp`
- If YouTube returns "Sign in to confirm you're not a bot", `tomd` will automatically retry with browser cookies from Chrome
- Use `-v` flag for detailed error diagnosis
