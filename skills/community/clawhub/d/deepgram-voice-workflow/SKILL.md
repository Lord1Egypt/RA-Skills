---
name: deepgram-voice-workflow
description: End-to-end voice workflow with Deepgram STT and TTS. Use when transcribing voice messages, generating spoken replies, or building a shell-based audio pipeline that turns input audio into text and optionally returns an MP3 reply. Especially useful for Telegram/QQ/OneBot voice-message automation and Chinese speech workflows.
---

# Deepgram Voice Workflow

## Overview

Use this skill for a complete speech workflow:

1. transcribe audio to text with Deepgram STT
2. optionally synthesize a spoken reply with Deepgram TTS
3. return structured outputs that can feed chat or agent pipelines

This skill is the right choice when the task is broader than plain transcription and needs an input-audio to output-audio pipeline.

## Quick Start

### Transcribe only

```bash
{baseDir}/scripts/deepgram-transcribe.sh /path/to/audio.ogg
```

### Generate speech from text

```bash
{baseDir}/scripts/deepgram-tts.sh "你好，我是 Neko。"
```

### Run the full pipeline

```bash
{baseDir}/scripts/neko-voice-pipeline.sh /path/to/audio.ogg --reply "收到啦，这是语音回复测试。"
```

## Environment

Set `DEEPGRAM_API_KEY` before use.

The bundled scripts also fall back to reading it from:

- `/root/.openclaw/.env`

## Workflow Decision

### Use `deepgram-transcribe.sh` when

- only text transcription is needed
- the downstream system will generate its own reply
- the task is speech-to-text only

### Use `deepgram-tts.sh` when

- text already exists
- only an MP3 spoken response is needed
- the workflow is text-to-speech only

### Use `neko-voice-pipeline.sh` when

- the task begins with an audio file
- a transcript is needed
- an optional spoken reply should be generated in the same flow

## Outputs

### STT output

`deepgram-transcribe.sh` writes:

- transcript text file
- raw API JSON file next to it

### TTS output

`deepgram-tts.sh` writes:

- MP3 output file

### Pipeline output

`neko-voice-pipeline.sh` prints JSON with:

- `out_dir`
- `transcript_path`
- `transcript`
- `reply_audio_path`

This makes it easy to wire into scripts or adapters.

## Typical Uses

Prefer this skill for:

- transcribing Telegram/QQ/OneBot voice messages
- generating MP3 replies to short voice prompts
- building bot-side voice input/output automation
- testing speech pipelines from shell without introducing a full SDK

## Notes

- Defaults are tuned for lightweight practical use, not maximal configurability.
- `deepgram-transcribe.sh` defaults to `model=nova-2` and `language=zh`.
- `deepgram-tts.sh` defaults to `model=aura-2-luna-en`; override the model when a different voice is preferred.
- Inspect the raw JSON transcript response when debugging recognition quality or API errors.

## References

Read these files when needed:

- `references/stt-notes.md` for transcription details
- `references/tts-notes.md` for speech synthesis details
- `references/pipeline-notes.md` for end-to-end pipeline behavior
