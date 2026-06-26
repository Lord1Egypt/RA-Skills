---
name: asr
description: This skill should be used when the user asks to "transcribe audio", "transcribe video", "convert speech to text", "generate subtitles", "create captions", "identify speakers in audio", or mentions audio/video transcription needs. Provides local ASR transcription with speaker diarization using FunASR.
---

# ASR Transcription Skill

Provide local audio/video transcription with speaker diarization, multiple output formats, and progress indication.

## Purpose

Enable users to transcribe audio and video files to text with automatic speaker identification, supporting multiple subtitle formats while preserving privacy through local processing.

## When to Use

This skill triggers when the user:
- Wants to transcribe an audio file (MP3, WAV, M4A, FLAC)
- Wants to transcribe a video file (MP4, AVI, MKV)
- Needs subtitles or captions generated from media
- Wants to identify different speakers in audio
- Needs timestamped transcription output

## Quick Start

### Basic Transcription

```bash
# Transcribe audio file (outputs TXT by default)
python3 skills/asr/scripts/transcribe.py path/to/audio.mp3

# Transcribe video file
python3 skills/asr/scripts/transcribe.py path/to/video.mp4
```

### Output Formats

```bash
python3 skills/asr/scripts/transcribe.py audio.mp3 -f json   # Structured JSON with metadata
python3 skills/asr/scripts/transcribe.py audio.mp3 -f srt    # SubRip subtitles
python3 skills/asr/scripts/transcribe.py audio.mp3 -f ass    # ASS/SSA subtitles with speaker styling
python3 skills/asr/scripts/transcribe.py audio.mp3 -f md     # Markdown with speaker sections
```

### Python API

```python
from asr_skill import transcribe

result = transcribe("meeting.mp4", format="srt")
print(f"Output: {result['output_path']}")
print(f"Speakers: {result.get('speakers', [])}")
```

### Asynchronous Execution (Recommended for Long Files)

Avoid timeouts by running transcription in the background:

```bash
# Start async task
python3 skills/asr/scripts/transcribe.py long_video.mp4 --async
# Output: {"task_id": "a1b2c3d4", "status": "queued", ...}

# Check status
python3 skills/asr/scripts/transcribe.py --status a1b2c3d4
# Output: {"task_id": "a1b2c3d4", "status": "processing", "progress": 45, ...}

# List recent tasks
python3 skills/asr/scripts/transcribe.py --list
```

## Core Features

### Speaker Diarization

Automatically identifies and labels different speakers:
- Speaker A, Speaker B, Speaker C, etc.
- Per-segment timestamps
- Overlap detection marked with [OVERLAP]

### Hardware Auto-Detection

Detects and uses the best available hardware:
- CUDA GPU (NVIDIA)
- Apple MPS (Apple Silicon)
- CPU fallback with notification

### Long Audio Support

Handles audio files longer than 1 hour:
- VAD-based intelligent segmentation
- Memory-efficient processing
- Progress indication during transcription

### Multiple Output Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| txt | .txt | Plain text with timestamps |
| json | .json | Structured data with word-level info |
| srt | .srt | Video subtitles |
| ass | .ass | Styled subtitles |
| md | .md | Documentation with speaker sections |

## Implementation Details

### Processing Pipeline

1. **Input validation** - Check file exists and format supported
2. **Hardware detection** - Auto-detect GPU/MPS/CPU
3. **Video extraction** - Extract audio from video files via FFmpeg
4. **Audio preprocessing** - Resample to 16kHz mono
5. **Model loading** - Load FunASR models (cached locally)
6. **Transcription** - Run ASR with speaker diarization
7. **Formatting** - Output in requested format
8. **Cleanup** - Remove temporary files

### Model Components

- **ASR Model**: Paraformer-large (Chinese optimized)
- **VAD Model**: FSMN-VAD (voice activity detection)
- **Punctuation**: CT-Transformer
- **Speaker**: CAM++ (speaker diarization)

### File Locations

- Models cached in: `./models/`
- Output defaults to: same directory as input
- Temp files: auto-cleaned after processing

## Troubleshooting

### Common Issues

**"FFmpeg not found"**
- FFmpeg auto-installed via imageio-ffmpeg
- Check internet connection for first run

**"CUDA out of memory"**
- System falls back to CPU automatically
- Try shorter audio segments

**"No speakers detected"**
- Speaker diarization requires multi-speaker audio
- Single speaker audio shows "Speaker A" only

## Additional Resources

### Reference Files

For detailed format specifications:
- **`references/output-formats.md`** - Complete format documentation

### Scripts

Utility scripts for batch processing:
- **`scripts/transcribe.py`** - Batch transcription script

### Examples

Working examples:
- **`examples/basic_usage.py`** - Python API examples
- **`examples/cli_examples.sh`** - CLI usage examples

## Requirements

- Python >= 3.10
- FunASR (auto-installed)
- FFmpeg (auto-installed via imageio-ffmpeg for video)

## Notes

- First run downloads models (~1GB total)
- All processing happens locally for privacy
- Chinese language optimized for v1
