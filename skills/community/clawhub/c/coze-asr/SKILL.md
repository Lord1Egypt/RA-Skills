---
name: coze-asr
description: Automatic Speech Recognition (ASR) using Coze API. Use when you need to transcribe audio files to text. Supports Chinese audio transcription via Coze's speech-to-text API.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["jq"], "env": ["COZE_API_KEY"] },
      },
  }
---

# Coze Automatic Speech Recognition (ASR)

Transcribe audio files to text using Coze API.

## Setup

**1. Get your API Key:**
Get a key from [Coze Platform](https://www.coze.cn/)

**2. Set it in your environment:**
```bash
export COZE_API_KEY="your-key-here"
```

## Supported Audio Formats

- **MP3** - Recommended
- **WAV** - Supported
- **OGG** - Supported (包括 opus 编码)

> **Note:** Coze API 原生支持 mp3、wav、ogg 格式，无需转换。

## Usage

### Basic Transcription

Transcribe an audio file:

```bash
bash scripts/speech_to_text.sh recording.mp3
```

### Full Options

```bash
bash scripts/speech_to_text.sh <audio_file> [language]
```

**Parameters:**
- `audio_file` (required): Path to audio file
- `language` (optional): Language code (default: zh)

## Output Format

The script outputs JSON with transcribed text.

Example output:
```json
{
  "text": "你好，这是转录的文本内容"
}
```

## Troubleshooting

**File Size Issues:**
- Check Coze API documentation for file size limits
- Reduce sample rate or bit depth if needed

**Poor Accuracy:**
- Improve audio quality
- Ensure clear speech and minimal noise
- Use appropriate language code

**Format Issues:**
- Ensure file is not corrupted
- Verify audio can be played by standard players
