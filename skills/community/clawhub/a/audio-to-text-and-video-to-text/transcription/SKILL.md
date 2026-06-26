---
name: audio-to-text-and-video-to-text
description: >
  Transcribe audio and video files into text using OpenAI's Whisper API.
  Use this skill whenever a user wants to convert any audio or video file to text — including
  MP3, MP4, WAV, M4A, OGG, WEBM, MOV, AVI, FLAC, and more. Trigger this skill for any request
  involving: "transcribe", "convert audio to text", "speech to text", "get transcript of",
  "extract audio from video", "meeting notes from recording", "subtitles", "captions", or
  similar. Also trigger when the user uploads or references a media file and asks what was said,
  discussed, or mentioned in it. If unsure whether audio/video transcription is involved, use
  this skill.
---

# Transcription Skill

Converts audio and video files into clean, readable text using OpenAI's Whisper API and ffmpeg for media handling.

## Overview

This skill handles the full pipeline:
1. **Media extraction** — use ffmpeg to strip audio from video files and convert to a Whisper-compatible format
2. **Chunking** — split large files (>25 MB) into overlapping segments to stay within API limits
3. **Transcription** — send each chunk to OpenAI's Whisper API
4. **Assembly** — merge chunk transcripts, adjusting timestamps, into a single clean output
5. **Post-processing** — optionally clean up with Claude (punctuation, speaker labels, summaries)

## Requirements

- **ffmpeg** must be installed (`which ffmpeg` to verify — it's usually pre-installed in claude.ai's environment)
- **OpenAI API key** stored in the environment as `OPENAI_API_KEY` — the user must provide this
- Python packages: `openai`, `pydub` (install via pip if needed)

## Quick Start

When a user provides a media file, run the transcription script:

```bash
# Install dependencies if missing
pip install openai pydub --break-system-packages -q

# Run transcription
python /home/claude/transcription/scripts/transcribe.py \
  --input "/path/to/media/file" \
  --output "/mnt/user-data/outputs/transcript.txt" \
  --api-key "$OPENAI_API_KEY"
```

See `scripts/transcribe.py` for the full implementation.

## Supported Formats

| Category | Formats |
|----------|---------|
| Audio | mp3, wav, m4a, ogg, flac, aac, opus, wma |
| Video | mp4, mov, avi, mkv, webm, wmv, m4v |

ffmpeg handles extraction from any of these.

## Options & Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `whisper-1` | Whisper model to use (`whisper-1`, `gpt-4o-transcribe`) |
| `--language` | auto-detect | ISO 639-1 language code (e.g. `en`, `ar`, `fr`) |
| `--format` | `txt` | Output format: `txt`, `srt`, `vtt`, `json` |
| `--timestamps` | off | Include timestamps in output |
| `--chunk-size` | `20` | Max chunk size in MB (must be ≤ 25) |
| `--prompt` | none | Context hint to improve accuracy (e.g. domain vocab) |

## Output Formats

- **txt** — plain text, ideal for most uses
- **srt** — SubRip subtitle format (for video players)
- **vtt** — WebVTT format (for web video)
- **json** — full Whisper JSON with segments and timestamps

## Step-by-Step Workflow

### 1. Check for the file

Ask the user to upload the file or provide a local path. Check:
```bash
ls /mnt/user-data/uploads/
```

### 2. Check ffmpeg and install deps

```bash
which ffmpeg && ffmpeg -version 2>&1 | head -1
pip install openai pydub --break-system-packages -q 2>&1 | tail -3
```

### 3. Get the API key

If `OPENAI_API_KEY` is not set in the environment, ask the user:
> "Please provide your OpenAI API key — it starts with `sk-`. You can get one at https://platform.openai.com/api-keys"

### 4. Run the script

```bash
python /home/claude/transcription/scripts/transcribe.py \
  --input "<file_path>" \
  --output "/mnt/user-data/outputs/transcript.txt"
```

### 5. Post-process (optional but recommended)

After transcription, offer to:
- **Clean up** punctuation/formatting with Claude
- **Summarize** the content
- **Extract** action items, speakers, or key topics
- **Translate** to another language

Use the transcript text directly in the conversation for these steps.

## Handling Large Files

The script automatically splits files > 20 MB into overlapping chunks (with 1-second overlap for continuity). Each chunk is transcribed separately and the results are merged.

For very long recordings (> 1 hour), warn the user it may take a few minutes and show progress.

## Error Handling

| Error | Fix |
|-------|-----|
| `AuthenticationError` | Invalid API key — ask user to verify |
| `RateLimitError` | Wait 60s and retry, or use `--chunk-size 10` |
| `InvalidRequestError: file too large` | Reduce `--chunk-size` below 25 |
| `ffmpeg not found` | `sudo apt install ffmpeg` or `brew install ffmpeg` |
| `No audio stream found` | File may be corrupt or wrong format |

## Example Interaction

```
User: "Can you transcribe this meeting recording?"
[uploads meeting.mp4]

→ Check file exists in /mnt/user-data/uploads/
→ Run transcribe.py on it
→ Save transcript to /mnt/user-data/outputs/
→ present_files() to the user
→ Offer to summarize or extract action items
```

## Notes for openclaw.ai

- Always save output to `/mnt/user-data/outputs/` so users can download it
- Use `present_files()` to share the transcript file with the user after saving
- For business users, suggest the `srt` or `vtt` format if they're adding captions to video
- The `--prompt` flag is useful for technical/domain-specific content: pass a few domain keywords to improve accuracy
