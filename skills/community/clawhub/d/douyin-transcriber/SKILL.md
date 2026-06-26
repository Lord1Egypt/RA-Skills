---
name: douyin-transcriber
description: Audio/video transcription module using Docker Whisper ASR. Extract speech from audio or video files and convert to text. Use when: (1) Transcribing audio files (mp3, wav, m4a, etc.), (2) Transcribing video files (mp4, mkv, etc.), (3) Need speech-to-text for any media file, (4) Working with douyin/tiktok video transcription workflows. Supports automatic audio extraction, format conversion, and multiple Whisper models.
---

# Douyin Transcriber

Transcribe audio/video files to text using local Docker Whisper ASR.

## Quick Start

```bash
curl -X POST "http://localhost:PORT/asr" -F "audio_file=@/path/to/video.mp4"
```

The container has built-in ffmpeg for automatic audio extraction.

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| Docker | Whisper ASR | Docker Desktop |
| ffmpeg | Audio extraction | `winget install Gyan.FFmpeg` |

**Deploy Whisper ASR:**
```bash
docker run -d -p PORT:PORT -e ASR_MODEL=small -e ASR_ENGINE=faster_whisper --name whisper-asr onerahmet/openai-whisper-asr-webservice:latest
```

## Workflow

### Step 1: Extract Audio from Video

```bash
ffmpeg -i video.mp4 -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y
```

Parameters:
- `-ar 16000`: 16kHz sample rate
- `-ac 1`: Mono channel
- `-c:a pcm_s16le`: 16-bit PCM

### Step 2: Transcribe

```bash
curl -X POST "http://localhost:PORT/asr" -F "audio_file=@audio.wav"
```

Optional: specify language
```bash
curl -X POST "http://localhost:PORT/asr" -F "audio_file=@audio.wav" -F "language=zh"
```

### Step 3: Parse Result

Response format:
```json
{
  "text": "Transcribed content...",
  "segments": [
    {"start": 0.0, "end": 2.5, "text": "First sentence"},
    {"start": 2.5, "end": 5.0, "text": "Second sentence"}
  ],
  "language": "zh"
}
```

## Model Selection

| Model | Size | 5-min video | Accuracy |
|-------|------|-------------|----------|
| tiny | 75MB | ~30s | Fair |
| base | 142MB | ~1min | Good |
| small | 466MB | ~3min | Better (recommended) |
| medium | 1.5GB | ~8min | Best |

Change model via environment variable: `-e ASR_MODEL=medium`

## Supported Formats

**Video:** mp4, mkv, avi, mov, flv, wmv, webm, m4v

**Audio:** wav, m4a, mp3, aac, ogg, flac, wma, opus

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Docker not available | Install Docker Desktop |
| Container start fails | Check port availability |
| Transcription timeout | Use smaller model or split audio |
| ffmpeg not found | `winget install Gyan.FFmpeg` |

## Related Modules

- **douyin-fetcher** - Video download
- **douyin-analyzer** - Content analysis
- **douyin-orchestrator** - Workflow coordination
