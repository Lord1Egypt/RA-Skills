---
name: audio-transcribe-summarize
description: Transcribe audio/video files to text and generate structured summaries using SenseAudio ASR API. Use when the user asks to transcribe, summarize, or take notes from audio files, video files, recordings, meetings, lectures, podcasts, or interviews.
---

# Audio/Video Transcription & Summarization

Transcribe audio/video files using the SenseASR API (`api.senseaudio.cn`), then summarize the content into structured notes.

**`{baseDir}`** refers to this skill's directory.

## Prerequisites

- Environment variable `SENSEAUDIO_API_KEY` configured (get your key at https://senseaudio.cn/platform/api-key)
- Python 3.8+ with `requests` installed
- For large files (>10MB): `ffmpeg` installed for splitting（macOS: `brew install ffmpeg`，Windows: [ffmpeg.org](https://ffmpeg.org/download.html) 下载并加入 PATH，Linux: `apt install ffmpeg`）

## Quick Start

1. Run the transcription script:

```bash
python {baseDir}/scripts/transcribe.py <audio_file> [--model sense-asr-pro] [--language zh] [--speakers] [--sentiment] [--translate en]
```

2. The script outputs a transcript `.txt` file alongside the source file
3. Read the transcript and generate a summary (see Summary Format below)

## Workflow

### Step 1: Assess the Audio File

Check file size and format:
- Supported formats: wav, mp3, ogg, flac, aac, m4a, mp4
- Max file size per request: 10MB
- If file > 10MB, the script auto-splits using ffmpeg

### Step 2: Choose the Right Model

| Model | Use When |
|-------|----------|
| `sense-asr-lite` | Quick batch transcription, simple audio, cost-sensitive |
| `sense-asr` | General transcription, need speaker separation or timestamps |
| `sense-asr-pro` | High accuracy needed: meetings, interviews, complex audio |
| `sense-asr-deepthink` | Noisy audio, dialects, heavy jargon, speech-to-clean-text |

Default to `sense-asr-pro` for best quality.

### Step 3: Transcribe

Run the transcription script. Key options:

```bash
# Basic transcription
python {baseDir}/scripts/transcribe.py recording.mp3

# Meeting with multiple speakers + emotion
python {baseDir}/scripts/transcribe.py meeting.wav \
  --model sense-asr-pro \
  --speakers --max-speakers 4 \
  --sentiment \
  --timestamps segment

# Transcribe and translate to English
python {baseDir}/scripts/transcribe.py lecture.mp3 \
  --model sense-asr \
  --translate en
```

### Step 4: Summarize

After transcription, read the transcript file and produce a summary using the format below.

## Summary Format

Generate summaries in this structure:

```markdown
# [Title - inferred from content]

**Source**: filename.mp3
**Duration**: X min Y sec
**Date**: YYYY-MM-DD
**Speakers**: [if speaker diarization was used]

## Key Points
- Point 1
- Point 2
- ...

## Detailed Summary
[2-4 paragraph summary of the content organized by topic/chronology]

## Action Items
- [ ] Action item 1 (assigned to Speaker X, if applicable)
- [ ] Action item 2

## Notable Quotes
> "Direct quote from transcript" — Speaker X, [timestamp if available]

## Full Transcript
<details>
<summary>Click to expand full transcript</summary>

[Full transcript text here, with speaker labels and timestamps if available]

</details>
```

Adapt the template based on content type:
- **Meeting**: emphasize action items, decisions, speaker contributions
- **Lecture/Talk**: emphasize key concepts, learning points, structure
- **Interview**: emphasize Q&A pairs, key responses
- **Podcast**: emphasize topics discussed, interesting insights

## API Reference

For full SenseASR API parameters and response formats, see [api-reference.md](api-reference.md).
