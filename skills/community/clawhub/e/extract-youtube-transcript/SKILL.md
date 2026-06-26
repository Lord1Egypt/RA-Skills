---
name: extract-youtube-transcript
version: 2.1.0
description: Extract plain-text transcripts from YouTube videos using a local Python script. Use when the user wants to fetch, extract, or get a transcript from a YouTube video URL, analyze YouTube video content as text, or needs subtitles/captions from a video.
---

# Extract YouTube Transcript

Fetches plain-text transcripts from YouTube videos using `extract_youtube_transcript.py` in this skill folder.

## Dependency

```bash
pip show youtube-transcript-api &>/dev/null || pip install youtube-transcript-api
```

## Quick Start

```bash
python extract_youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Supported URL formats: `youtube.com/watch?v=`, `youtu.be/`, `/embed/`, `/live/`, `/shorts/`, or a raw 11-char video ID.

## Common Patterns

### Fetch with preferred language(s)

```bash
python extract_youtube_transcript.py "URL" --lang zh-Hant en
```

Pass languages in priority order. Falls back to any available transcript if none match.

### Save transcript to file

```bash
python extract_youtube_transcript.py "URL" --output transcript.txt
```

Text is printed to stdout and also written to the file.

### List available languages first

```bash
python extract_youtube_transcript.py "URL" --list-langs
```

Use this to discover what language codes are available before fetching.

## Language Codes

| Code | Language |
|------|----------|
| `en` | English |
| `zh-Hant` | Traditional Chinese |
| `zh-Hans` | Simplified Chinese |
| `ja` | Japanese |
| `ko` | Korean |
| `es` | Spanish |

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `TranscriptsDisabled` | Owner disabled captions | No transcript available |
| `NoTranscriptFound` | Requested lang not found | Run `--list-langs`, pick an available code |
| `VideoUnavailable` | Video is private/deleted | Verify the URL |
| `AgeRestricted` | Age-gated video | Auth not supported; no workaround |
| `InvalidVideoId` | Malformed URL or ID | Check the URL format |

## Workflow

1. Try a direct fetch first
2. If `NoTranscriptFound`, run `--list-langs` to see available codes, then re-fetch with `--lang <code>`
3. Save long transcripts to a file with `--output` for easier downstream processing
