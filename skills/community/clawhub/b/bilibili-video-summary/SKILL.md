---
name: bili-summary
description: "Extract and summarize Bilibili videos. Fetches subtitles or GPU-transcribed audio, danmaku (scrolling comments), video comments, and description — outputs structured JSON for AI agents to summarize. Triggers: Bilibili video summary, summarize this video, what does this video say, bilibili video, B站视频总结, BV号, bilibili.com, video content, video summary, extract video text, video transcript."
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/gkd2323c/bili-summary
    requires:
      bins:
        - python3
        - yt-dlp
      anyBins:
        - whisper-cli
    emoji: "🎬"
---

# Bilibili Video Summary Tool

Extract full content from a Bilibili video — transcript/subtitles, danmaku, comments, and description — then use your own LLM capabilities to produce a deep summary. No external AI API required (no OpenAI / Gemini key needed).

## Capabilities

| Data Source | Method | Priority |
|-------------|--------|----------|
| **CC Subtitles** | Bilibili API | Fastest, used if available |
| **Audio Transcription** | whisper.cpp + Vulkan GPU | Automatic fallback when no subtitles |
| **Video Description** | yt-dlp | Always captured |
| **Danmaku** (scrolling comments) | yt-dlp | Parsed, analyzed for frequent content |
| **Comments** | Bilibili Comment API | Hot-sorted, deduplicated, top liked extracted |

## Workflow

When you receive a Bilibili video link and are asked to summarize it, follow these steps:

### Step 1: Extract all data

```bash
python bili-transcript.py "<video_url>"
```

The script automatically:
1. Gets video title, uploader, duration, description
2. Attempts Bilibili CC subtitles (fastest, used if available)
3. Falls back to GPU transcription: download audio → convert to wav → whisper.cpp with Vulkan
4. Downloads and analyzes danmaku (scrolling comments)
5. Fetches video comments, sorted by likes

Output files are saved to `./bili-output/`:
- `transcript.txt` — full transcript/subtitle text
- `danmaku.json` — danmaku data with statistics
- `comments.json` — comment data with top-liked

The JSON output includes preview text, danmaku summary, and top comments.

### Step 2: Read full transcript

The JSON preview truncates at 2000 characters. Read the full file:

```bash
cat ./bili-output/transcript.txt
```

### Step 3: Read danmaku and comments

Review community response data:

```bash
cat ./bili-output/danmaku.json
cat ./bili-output/comments.json
```

### Step 4: Compose your summary

Use your own LLM capabilities to produce a comprehensive summary. Suggested structure:

**Video Overview** — Title, uploader, duration, transcription source (subtitle / GPU). Key info from the description (project links, update notes, etc.).

**Core Content** — What the video is about. Fluent paragraph summary of the main narrative.

**Key Points** — Notable arguments, data points, or information worth highlighting.

**Community Response** (optional) — Reactions from danmaku and comments. Skip if content is insubstantial (spam, trolling, no valuable discussion).

- Danmaku analysis: look for frequently repeated phrases (community memes/reactions), informative questions, technical discussions, controversy points
- Comment analysis: look for top-liked opinions, creator interactions, user-reported issues, technical insights

**Assessment** (optional) — Content quality, information density, notable strengths or weaknesses.

## Available Actions

```bash
# Video metadata only
python bili-transcript.py "<URL>" --action info

# CC subtitles only (if available)
python bili-transcript.py "<URL>" --action subtitle

# Force GPU transcription (skip subtitle check)
python bili-transcript.py "<URL>" --action transcribe

# Danmaku only
python bili-transcript.py "<URL>" --action danmaku

# Comments only
python bili-transcript.py "<URL>" --action comments

# Custom output directory
python bili-transcript.py "<URL>" --output ./my-output
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `WHISPER_CPP_DIR` | Path to whisper.cpp directory (containing whisper-cli) |
| `WHISPER_MODEL` | Path to whisper model file (e.g., ggml-large-v3-turbo.bin) |
| `BILI_OUTPUT_DIR` | Default output directory (default: ./bili-output) |

## Performance Reference

| Video Length | Total Time | Notes |
|-------------|-----------|-------|
| 5 minutes | ~15s | GPU transcription is fast |
| 12 minutes | ~22s | Download + convert + transcribe |
| 1 hour | ~2-3 min | Depends on audio density |
| Danmaku/Comments | ~5-10s | Depends on comment volume |

## Dependencies

- **Python packages**: yt-dlp, av (PyAV)
- **Transcription engine**: whisper.cpp with Vulkan support (optional, only needed if no CC subtitles)
- **Model**: ggml-large-v3-turbo.bin (~1.6GB, download separately)
- **GPU**: Any Vulkan-compatible GPU (NVIDIA, AMD, Intel) — auto-detected
- No external AI API keys required

## Limitations

- Requires internet access to Bilibili
- Some content requires login (paid courses, restricted videos) — may fail
- Danmaku and comment APIs may be rate-limited
- whisper.cpp does not support m4a; script auto-converts via PyAV
- Very long videos (>2 hours) take significant transcription time; try `--action subtitle` first
- Comments are fetched from the first 3 pages (~60 comments); may not cover very hot videos fully
