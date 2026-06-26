---
name: asr-claw
version: 1.1.1
description: Speech recognition CLI for AI agent automation. Transcribe audio from stdin, files, or URLs.
metadata:
  openclaw:
    homepage: https://github.com/llm-net/asr-claw
    os: [darwin, linux]
    arch: [arm64, amd64]
    requires:
      bins: [asr-claw]
    install:
      kind: download
      url: https://github.com/llm-net/asr-claw/releases/latest/download/asr-claw-${os}-${arch}
      dest: bin/asr-claw
      executable: true
      checksum_url: https://github.com/llm-net/asr-claw/releases/latest/download/checksums.txt
    settings:
      - key: default_engine
        type: string
        default: qwen-asr
        description: Default ASR engine (qwen-asr, whisper, qwen3-asr, doubao, openai, deepgram)
      - key: default_lang
        type: string
        default: zh
        description: Default language code (zh, en, ja, ko, fr, de, es, ...)
      - key: model
        type: string
        default: Qwen/Qwen3-ASR-0.6B
        description: "HuggingFace model ID. Options: Qwen/Qwen3-ASR-0.6B (~1.9GB), Qwen/Qwen3-ASR-1.7B (~3.4GB)"
      - key: hf_mirror
        type: string
        default: ""
        description: "HuggingFace mirror URL for China users (e.g. https://hf-mirror.com)"
      - key: model_path
        type: string
        default: ""
        description: "Custom model directory path (overrides default ~/.asr-claw/models/)"
      - key: binary_path
        type: string
        default: ""
        description: "Custom qwen-asr binary path (overrides default ~/.asr-claw/bin/)"
---

# asr-claw

Speech recognition CLI for AI agent automation. Transcribe audio streams from stdin, files, or URLs with multiple ASR engines — local and cloud.

## Triggers

- User wants to transcribe audio, speech, or voice to text
- User needs speech recognition or ASR
- User wants to convert audio/voice recordings to text
- User wants to monitor live audio / livestream speech
- User asks about 语音识别、语音转文字、转写、直播语音
- adb-claw audio capture output needs to be transcribed
- User wants subtitles (SRT/VTT) generated from audio

## Binary

The `asr-claw` binary is located at `${CLAUDE_PLUGIN_ROOT}/bin/asr-claw`.

If it does not exist, the SessionStart hook will build or download it automatically.

## Setup

### Quick Start (Mac)

```bash
# Install the qwen-asr engine (builds C binary + downloads 0.6B model ~1.9GB)
asr-claw engines install qwen-asr

# Verify
asr-claw engines list
asr-claw doctor
```

### OpenClaw Setup

After installing the skill via ClawHub, configure settings:

```bash
# Set default language (default: zh)
claw config set asr-claw.default_lang en

# Use a larger model
claw config set asr-claw.model Qwen/Qwen3-ASR-1.7B

# For China users — set HuggingFace mirror
claw config set asr-claw.hf_mirror https://hf-mirror.com

# Custom model path (e.g., shared NAS)
claw config set asr-claw.model_path /mnt/models/Qwen3-ASR-0.6B

# Re-run install after changing model settings
asr-claw engines install qwen-asr
```

Settings are stored in `~/.asr-claw/config.yaml`:

```yaml
default:
  engine: qwen-asr
  lang: zh
  format: json

engines:
  qwen-asr:
    binary: ~/.asr-claw/bin/qwen-asr
    model_path: ~/.asr-claw/models/Qwen3-ASR-0.6B
```

### Cloud Engines (no local model needed)

```bash
# OpenAI Whisper API
export OPENAI_API_KEY=sk-...
asr-claw transcribe --file audio.wav --engine openai

# Volcengine Doubao (火山引擎)
export DOUBAO_API_KEY=...
asr-claw transcribe --file audio.wav --engine doubao

# Deepgram (native streaming)
export DEEPGRAM_API_KEY=...
asr-claw transcribe --file audio.wav --engine deepgram
```

## Commands

### transcribe — Core: audio to text

```bash
# File transcription
asr-claw transcribe --file meeting.wav --lang zh

# Pipe from stdin
cat audio.wav | asr-claw transcribe --lang zh

# Streaming (real-time, from adb-claw or ffmpeg)
adb-claw audio capture --stream --duration 60000 | asr-claw transcribe --stream --lang zh

# Subtitle output
asr-claw transcribe --file lecture.wav --format srt > lecture.srt
asr-claw transcribe --file lecture.wav --format vtt > lecture.vtt

# Specify engine
asr-claw transcribe --file audio.wav --engine whisper --lang en
```

**Flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `--file <path>` | stdin | Input audio file |
| `--stream` | false | Streaming mode (real-time) |
| `--lang <code>` | zh | Language code |
| `--engine <name>` | auto | ASR engine |
| `--format <fmt>` | json | Output: json, text, srt, vtt |
| `--chunk <sec>` | 0 | Fixed-time chunking (disables VAD) |
| `--rate <hz>` | 16000 | Sample rate for raw PCM input |

### engines — Manage ASR engines

```bash
asr-claw engines list                    # List all engines + status
asr-claw engines install qwen-asr       # Install local engine (Mac)
asr-claw engines info qwen-asr          # Engine details
asr-claw engines start qwen3-asr        # Start vLLM service engine
asr-claw engines stop qwen3-asr         # Stop service engine
asr-claw engines status                  # Running engines
```

### doctor — Environment check

```bash
asr-claw doctor    # Check platform, engines, dependencies
```

## Engine Matrix

| Engine | Type | Mac | GPU | Streaming | Install |
|--------|------|-----|-----|-----------|---------|
| **qwen-asr** | Local CLI | Yes | No (Accelerate) | VAD | `engines install qwen-asr` |
| **qwen3-asr** | vLLM Service | No | Yes (CUDA) | Native | `engines start qwen3-asr` |
| **whisper** | Local CLI | Yes | No | VAD | Manual |
| **doubao** | Cloud API | Yes | — | No | Set DOUBAO_API_KEY |
| **openai** | Cloud API | Yes | — | No | Set OPENAI_API_KEY |
| **deepgram** | Cloud API | Yes | — | Native | Set DEEPGRAM_API_KEY |

## Output Format

All commands output JSON envelope:

```json
{
  "ok": true,
  "command": "transcribe",
  "data": {
    "segments": [{"index": 0, "start": 0.0, "end": 2.5, "text": "..."}],
    "full_text": "...",
    "engine": "qwen-asr",
    "audio_duration_sec": 5.5
  },
  "duration_ms": 1230,
  "timestamp": "2026-03-13T10:00:00Z"
}
```

Use `-o text` for plain text, `-o quiet` for silent.

## With adb-claw

```bash
# Real-time transcription from Android device
adb-claw audio capture --stream --duration 60000 | asr-claw transcribe --stream --lang zh

# Record then transcribe
adb-claw audio capture --duration 30000 --file recording.wav
asr-claw transcribe --file recording.wav --lang zh

# Save audio + transcribe simultaneously
adb-claw audio capture --stream --duration 0 | tee backup.wav | asr-claw transcribe --stream
```
