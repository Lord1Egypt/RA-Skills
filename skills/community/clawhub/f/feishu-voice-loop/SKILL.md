---
name: feishu-voice-loop
description: A reusable Feishu voice loop: accept text or voice input, generate natural OpenAI speech, and deliver it to chat or web playback. Use when building or sharing a reusable Feishu voice workflow with text-or-voice in and audio out, including browser playback and Feishu voice replies.
---

# Feishu Voice Loop

Provide a reusable three-step voice loop for OpenClaw:
1. accept **text or voice** input
2. generate speech with **OpenAI TTS**
3. return the audio to **Feishu** or **a web player**

When the input is voice, transcribe it to text first, then continue through the same output pipeline.

## Quick start

Prerequisites:
- `OPENAI_API_KEY` is set for TTS
- Feishu app credentials exist in `~/.openclaw/openclaw.json` under `channels.feishu.appId/appSecret`, or are passed explicitly
- `ffmpeg` and `ffprobe` are installed and available
- local audio transcription is configured in `~/.openclaw/openclaw.json` under `tools.media.audio.models`

Main scripts:
- `scripts/openai_tts_feishu.py`
- `scripts/transcribe_audio.py`

## Tasks

### 1. Transcribe voice input

Use this when you have a local `.ogg`, `.opus`, `.wav`, or similar file and want text.

```bash
python3 scripts/transcribe_audio.py /path/to/input.ogg
```

This script reuses the existing Whisper CLI configuration from `~/.openclaw/openclaw.json`.

### 2. Generate and send voice output

Use this when you already have text and want to send a Feishu voice message.

```bash
python3 scripts/openai_tts_feishu.py \
  --to <feishu_open_id> \
  --text "这条是语音测试。" \
  --voice alloy \
  --model gpt-4o-mini-tts
```

The script will:
1. call OpenAI `audio/speech`
2. save WAV audio temporarily
3. convert to Feishu-friendly Opus via `ffmpeg`
4. upload the file to Feishu
5. send an `audio` message to the target `open_id`

### 3. Run the full voice loop

Use this skill when the goal is a reusable voice interaction pipeline:
1. transcribe input audio to text
2. decide or generate the reply text
3. synthesize reply audio with OpenAI TTS
4. send the reply back to Feishu

Read `references/input-output-workflow.md` when building or explaining the end-to-end loop.

## Default output style

Default preset is stored in `references/presets.md`.

Unless the user asks otherwise, use:
- model: `gpt-4o-mini-tts`
- voice: `alloy`
- default style: 年轻日系男声感、温柔里带一点撩、贴耳边私聊感、自然、不播音腔

When the user asks for a different flavor, either:
- pass a custom `--instructions`
- or adapt one of the presets in `references/presets.md`

## Handle failures

Common failure cases:
- `Missing OPENAI_API_KEY` → ask for API key / env setup
- HTTP 429 from OpenAI → billing or quota issue
- missing Feishu app credentials → configure `channels.feishu.appId/appSecret`
- missing `ffmpeg` or `ffprobe` → install locally before retrying
- missing transcription model config → configure `tools.media.audio.models`

When OpenAI billing is not enabled, say so directly instead of pretending the voice was generated.

## Packaging and sharing

Package with:

```bash
python3 /Users/zoepeng/.openclaw/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py \
  /Users/zoepeng/.openclaw/workspace/skills/openai-feishu-voice
```

The resulting `.skill` file can be shared or uploaded wherever the user distributes skills.

## Resources

### scripts/openai_tts_feishu.py

Use for deterministic TTS generation and Feishu delivery.

### scripts/transcribe_audio.py

Use for deterministic local audio transcription via the configured Whisper CLI.

### references/presets.md

Read when the user asks for a different voice direction or wants named presets.

### references/input-output-workflow.md

Read when packaging or explaining the complete voice-in / voice-out solution.
