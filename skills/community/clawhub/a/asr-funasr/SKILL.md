---
name: asr-funasr
version: 1.2.0
description: "Automatic Speech Recognition using OpenAI Whisper (local GPU). Supports Chinese, English, and 90+ languages. Auto-detects language."
metadata: { "openclaw": { "emoji": "🎤", "requires": { "bins": ["python3"] } } }
tags: ["asr", "speech-to-text", "whisper", "funasr", "sensevoice", "transcription", "audio"]
---

# ASR — Speech-to-Text (FunASR + Whisper)

Two engines for different scenarios:

| Engine | Best For | Chinese Quality | Speed |
|--------|----------|-----------------|-------|
| **FunASR SenseVoice** (default) | Chinese, Japanese, Korean | ⭐⭐⭐ 简体 | Fast (0.03 RTF) |
| **OpenAI Whisper** | Multilingual, translation | ⭐⭐ (繁体) | Slower |

## Quick Start

```bash
# Default: FunASR SenseVoice (best Chinese)
{baseDir}/scripts/asr.py --input audio.mp3

# Whisper for multilingual / translation
{baseDir}/scripts/asr.py --input audio.mp3 --engine whisper
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--input` | (required) | Input audio file (mp3, wav, m4a, etc.) |
| `--engine` | funasr | ASR engine: `funasr` (SenseVoice) or `whisper` |
| `--language` | auto | Language code: zh, en, ja, ko, etc. (auto-detect if omitted) |
| `--model` | base | Whisper model size: tiny/base/small/medium/large (whisper only) |
| `--task` | transcribe | transcribe or translate (whisper only) |
| `--output` | | Write transcript to file (default: stdout) |

## Engine Details

### FunASR SenseVoice-Small (Default)

- **Model**: `iic/SenseVoiceSmall` (893MB, auto-downloaded from ModelScope)
- **Strengths**: 简体中文最佳、情感识别、语音事件检测、速度极快
- **Output**: 简体中文，自动去除特殊标记
- **Languages**: zh, en, ja, ko, yue (Cantonese)

### OpenAI Whisper

- **Model**: base (139MB, auto-downloaded)
- **Strengths**: 90+ languages、翻译模式、多语言场景
- **Output**: 中文输出繁体字（已知问题，换 small 模型可改善）
- **Whisper model sizes**:

| Model | VRAM | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | ~1GB | Fastest | Low |
| base | ~1GB | Fast | OK |
| small | ~2GB | Medium | Good |
| medium | ~5GB | Slow | Better |
| large | ~10GB | Slowest | Best |

## Examples

```bash
# Chinese audio → FunASR (default, best quality)
{baseDir}/scripts/asr.py --input meeting.mp3

# Force Chinese language
{baseDir}/scripts/asr.py --input podcast.wav --language zh

# Multilingual audio → Whisper
{baseDir}/scripts/asr.py --input mixed.wav --engine whisper

# Whisper with better model
{baseDir}/scripts/asr.py --input lecture.mp3 --engine whisper --model small

# Translate Chinese speech to English text
{baseDir}/scripts/asr.py --input speech.mp3 --engine whisper --language zh --task translate

# Save transcript to file
{baseDir}/scripts/asr.py --input audio.wav --output transcript.txt
```

## Dependencies

- `funasr` + `modelscope` (FunASR engine)
- `openai-whisper` (Whisper engine)
- `imageio-ffmpeg` (bundled ffmpeg binary)
- First run downloads model weights (auto-cached in `~/.cache/`)
