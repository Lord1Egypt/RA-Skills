---
name: whisperkit-cli
description: On-device speech-to-text (Whisper) + text-to-speech (Qwen3-TTS) CLI. Runs on the Apple Neural Engine (ANE), Apple's low power, dedicated ML inference chip. Models download once on first run, then all inference is local.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - whisperkit-cli
    os:
      - macos
    install:
      - kind: brew
        formula: whisperkit-cli
        bins: [whisperkit-cli]
    homepage: https://github.com/argmaxinc/WhisperKit
    emoji: "\U0001F5E3"
---

# whisperkit-cli

**On-device Whisper transcription + Qwen3-TTS synthesis**  
Local file-based audio I/O -- models are downloaded from HuggingFace on first run, then all inference runs on-device with no network required. Perfect for agents that receive voice messages/attachments and reply with text or generated audio files.

The agent saves incoming audio attachments to a temp path, runs the CLI, and either returns the transcribed text in chat or attaches the generated `.wav`/`.m4a` reply.

## Why agents love this skill
- Runs on ANE -- no GPU contention, low power, always available
- No API keys, no per-request costs, no data leaves the machine after setup
- One-time model download on first run, then fully offline
- Handles audio files from user messages (m4a, wav, mp3, flac)
- Generates reply audio files the agent can attach/send
- 9 built-in voices + 10 languages
- Natural-language style instructions (1.7B model)

## Installation

```bash
brew install whisperkit-cli
```

**First run** automatically downloads models as needed.

## Core Commands

### Transcribe (Audio File -> Text)

```bash
whisperkit-cli transcribe --help
```

**Agent patterns**

```bash
# Transcribe user-uploaded audio attachment (recommended default)
whisperkit-cli transcribe --audio-path /tmp/user-message.m4a
```

**Important model notes**  
- By default, `whisperkit-cli transcribe` automatically selects the highest-quality model that fits on your Apple Silicon device (typically a large-v3 variant on M1+). This is great for accuracy but may be slower for real-time agent workflows.  
- `--model small` is the fastest option and works well across languages. For non-English audio, pass `--language` with the ISO code (e.g. `--language ja` for Japanese). Avoid `.en` model variants for non-English audio.

```bash
# Explicit small model (fast + good quality for most cases)
whisperkit-cli transcribe --model small --audio-path /tmp/voice-note.wav

# Non-English audio -- specify the language ISO code
whisperkit-cli transcribe --model small --language ja --audio-path /tmp/japanese-message.m4a

# Higher quality with auto language detection (no --language needed)
# --prompt provides context as if it were the previous transcript segment,
# helping the model spell proper nouns and domain terms correctly
whisperkit-cli transcribe --model large-v3-v20240930_626MB --audio-path /tmp/long-meeting.m4a \
  --word-timestamps --prompt "Argmax, WhisperKit, CoreML"
```

Output goes to stdout (clean text) -- agent copies it directly into the chat reply.

### TTS (Text -> Audio File)

```bash
whisperkit-cli tts --help
```

**Agent patterns**

```bash
# Generate reply audio file (agent will attach it)
whisperkit-cli tts --text "Got it, I'll handle the report by Friday" \
  --output-path /tmp/agent-reply

# With voice + language
whisperkit-cli tts --text "こんにちは、世界" \
  --speaker ono-anna --language japanese \
  --output-path /tmp/japanese-reply.m4a

# 1.7B model with expressive style instruction
whisperkit-cli tts --model 1.7b \
  --text "Once upon a time in a galaxy far, far away..." \
  --instruction "Read dramatically like a movie trailer narrator" \
  --output-path /tmp/story-reply.m4a

# From text file (great for long LLM summaries)
whisperkit-cli tts --text-file /tmp/llm-response.txt \
  --output-path /tmp/voice-reply.m4a
```

You can include the extension in `--output-path` (e.g. `/tmp/reply.m4a`) or omit it and the CLI will append it based on `--output-format` (default `.m4a`). Use `--output-format wav` for `.wav`. Default voice is `aiden` if `--speaker` is omitted.

## Voices (TTS)
`ryan`, `aiden`, `ono-anna`, `sohee`, `eric`, `dylan`, `serena`, `vivian`, `uncle-fu`

## Languages (TTS)
`english`, `chinese`, `japanese`, `korean`, `german`, `french`, `russian`, `portuguese`, `spanish`, `italian`

## Local OpenAI-Compatible API Server

```bash
whisperkit-cli serve --port 50060
```

Auto-selects the best model for your device. To specify a model explicitly:

```bash
whisperkit-cli serve --model small --port 50060
```

Exposes OpenAI-compatible endpoints at `http://127.0.0.1:50060`:
- `POST /v1/audio/transcriptions` -- transcribe audio to text
- `POST /v1/audio/translations` -- translate audio to English
- `GET /health` -- health check

## Agent Usage Patterns

```bash
# Typical voice message flow
# User sends audio -> agent saves to /tmp/user-audio.m4a
whisperkit-cli transcribe --model small --audio-path /tmp/user-audio.m4a

# Agent sends text to LLM, gets response, generates voice reply
whisperkit-cli tts --text "{{llm_response}}" --output-path /tmp/reply --speaker ryan

# Agent attaches /tmp/reply.m4a to the chat message
```

## Full docs & model list
https://github.com/argmaxinc/WhisperKit

**Whisper model sizes** (speed vs quality trade-off):
- `tiny` (~76MB), `base` (~146MB) -- fastest, lower accuracy
- `small` (~486MB) -- recommended for most agents, fastest. Works across languages when `--language` is specified. Avoid `.en` variants for non-English.
- `large-v3-v20240930_626MB` (~626MB) -- quantized large model, best balance of accuracy and size. Auto-detects language without needing `--language`.
- `large-v3-v20240930` (~1.6GB) -- auto-selected default on M1+, full-precision large model.

Model names use the short form after the `openai_whisper-` prefix (e.g. `--model small` resolves to `openai_whisper-small`). Append `.en` for English-only variants.

**TTS model sizes:**
- `0.6b` -- fast, works on all Apple Silicon devices
- `1.7b` -- best quality + style instructions, macOS 15+

Run `whisperkit-cli transcribe --help` or `whisperkit-cli tts --help` for the latest flags.
