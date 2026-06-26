---
name: douyin-video-processor
description: "Extract speech-to-text from Douyin (TikTok China) videos, get watermark-free download links, and download videos. Use when user shares a Douyin link, asks to transcribe a Douyin video, wants to download a Douyin video without watermark, or needs to extract text from Chinese short videos."
homepage: "https://github.com/yzfly/douyin-mcp-server"
metadata:
  clawdbot:
    emoji: "🎬"
    requires:
      env: ["DASHSCOPE_API_KEY"]
      anyBins: ["python3"]
    primaryEnv: "DASHSCOPE_API_KEY"
    files: ["scripts/*"]
    os: ["linux", "darwin", "win32"]
---

# Douyin Video Processor

Process Douyin (TikTok China) share links: extract video speech to text, get watermark-free download URLs, and download videos locally.

## First-Time Setup

Before using any script, install the Python dependencies:

```bash
bash scripts/install_deps.sh
```

This installs `requests` and `dashscope`. Only needed once.

## Environment Variable

The text extraction feature requires `DASHSCOPE_API_KEY` from Alibaba Cloud Bailian.

The user must set this before you can call `douyin_extract_text.py`. If it is not set, tell the user:

> To use text extraction, you need an Alibaba Cloud Bailian API key.
> 1. Go to https://help.aliyun.com/zh/model-studio/get-api-key
> 2. Create an API key (starts with `sk-`)
> 3. Set it: `/secrets set DASHSCOPE_API_KEY sk-your-key`

The other two scripts (parse and download) do **not** need any API key.

## Available Scripts

### 1. Parse Video Info (no API key needed)

Extract video metadata (ID, title, watermark-free URL) from a Douyin share link.

```bash
python3 scripts/douyin_parse.py "SHARE_LINK"
```

**Input:** A Douyin share link or text containing one (e.g. `https://v.douyin.com/xxxxx/` or a full share text like `"7.29 复制打开抖音... https://v.douyin.com/xxxxx/"`)

**Output:** JSON to stdout:
```json
{
  "status": "success",
  "video_id": "7345678901234567890",
  "title": "Video title here",
  "download_url": "https://..."
}
```

**When to use:** User wants to see video info, or you need the download URL without downloading the file.

---

### 2. Download Video (no API key needed)

Download a watermark-free video file to local disk.

```bash
python3 scripts/douyin_download.py "SHARE_LINK" [output_directory]
```

**Input:**
- Arg 1: Douyin share link or text containing one
- Arg 2 (optional): Output directory, defaults to current directory

**Output:** JSON to stdout:
```json
{
  "status": "success",
  "video_id": "7345678901234567890",
  "title": "Video title here",
  "file_path": "/absolute/path/to/video.mp4",
  "size_bytes": 12345678
}
```

**When to use:** User asks to download a Douyin video, save a video, or get the actual video file.

---

### 3. Extract Text from Video (requires DASHSCOPE_API_KEY)

Parse a Douyin share link, then transcribe the video speech to text using Alibaba Cloud ASR.

```bash
DASHSCOPE_API_KEY="$DASHSCOPE_API_KEY" python3 scripts/douyin_extract_text.py "SHARE_LINK" [model]
```

**Input:**
- Arg 1: Douyin share link or text containing one
- Arg 2 (optional): ASR model name, defaults to `paraformer-v2`

**Output:** JSON to stdout:
```json
{
  "status": "success",
  "video_id": "7345678901234567890",
  "title": "Video title here",
  "text": "The full transcribed text content from the video..."
}
```

**When to use:** User wants to know what's said in a Douyin video, asks to transcribe, extract text, get subtitles, or summarize video content.

**Important:** Always pass `DASHSCOPE_API_KEY` as an environment variable in the command. If the key is not set, the script will return an error with setup instructions.

## Error Handling

All scripts return JSON even on failure:
```json
{
  "status": "error",
  "error": "Human-readable error message"
}
```

Common errors and what to tell the user:

| Error message contains | User-facing guidance |
|---|---|
| `No valid share link` | The input doesn't contain a valid Douyin URL. Ask the user to paste the full share link. |
| `Failed to parse video info` | The video may be deleted, private, or region-locked. Ask the user to verify the link opens in a browser. |
| `DASHSCOPE_API_KEY.*not set` | The API key is missing. Guide the user through setup (see Environment Variable section above). |
| `Transcription failed` | ASR API error — the key may be invalid or quota exhausted. Ask the user to check their Alibaba Cloud console. |
| `dashscope package not installed` | Run `bash scripts/install_deps.sh` to install dependencies. |

## Batch Processing

When the user provides multiple Douyin links, process them sequentially. For each link:

1. Call the appropriate script
2. Parse the JSON output
3. Collect results
4. Present a summary table to the user

For batch text extraction, **first parse all links** with `douyin_parse.py` to validate them, then extract text only from the valid ones with `douyin_extract_text.py`. This avoids wasting API calls on broken links.

## Cost Awareness

| Script | API Cost | Speed |
|--------|----------|-------|
| `douyin_parse.py` | Free | ~1-2s |
| `douyin_download.py` | Free | depends on video size |
| `douyin_extract_text.py` | Alibaba Cloud ASR (very low cost) | ~10-30s |

Always prefer `douyin_parse.py` first when you just need to verify a link or get the download URL.

## External Endpoints

| Endpoint | Purpose | Data Sent |
|----------|---------|-----------|
| `https://v.douyin.com/*` | Resolve Douyin share link redirects | Share URL |
| `https://www.iesdouyin.com/share/video/*` | Fetch video page to extract metadata | Video ID |
| Douyin CDN | Download video file (douyin_download.py only) | None (GET request) |
| `https://dashscope.aliyuncs.com/api/*` | Alibaba Cloud ASR (douyin_extract_text.py only) | Video URL + API key |

## Security & Privacy

- `DASHSCOPE_API_KEY` is only sent to Alibaba Cloud's official API endpoint (`dashscope.aliyuncs.com`)
- No data is collected, stored, or transmitted by this skill beyond the API calls listed above
- Downloaded video files are saved only where the user specifies
- No persistent background processes

## Trust Statement

By using this skill, Douyin share links are sent to **Douyin/ByteDance** servers for URL resolution, and video URLs may be sent to **Alibaba Cloud (Aliyun)** for speech-to-text transcription. Only install this skill if you trust these services.
