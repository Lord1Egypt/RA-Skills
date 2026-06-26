---
name: axiomata-voice
description: "Axiomata Voice — Text-to-Speech skill for OpenClaw agents. Use when: (1) converting text messages to speech audio, (2) sending voice messages via Telegram, (3) processing long messages as audio, (4) using ElevenLabs API for TTS synthesis. Requires: ElevenLabs API key, Telegram bot token, ffmpeg. Provides voice generation, audio processing, and Telegram delivery."
version: "1.0.0"
---

# Axiomata Voice — Text-to-Speech

> Convert text to speech and send via Telegram
> Impersonal — works for any agent

---

## Description

Axiomata Voice converts text messages to speech audio using ElevenLabs TTS API and delivers via Telegram.

**Requires:**
- ElevenLabs API key
- Telegram bot token  
- ffmpeg for audio processing

**Use when:** Converting long messages to audio, voice messaging, accessibility features.

---

## Setup

### Environment Variables

| Variable | Description |
|----------|-------------|
| `ELEVENLABS_API_KEY` | ElevenLabs API key |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token |

---

## Usage

### Text to Speech

```bash
# Convert text to speech
python3 scripts/voice_tts.py --text "Hello world" --output audio.mp3

# Send voice via Telegram
python3 scripts/voice_send.py --text "Hello" --chat_id <chat_id>
```

### API Call Example

```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/<voice_id>" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "voice_settings": {"stability": 0.5}}'
```

---

## Architecture

```
axiomata-voice/
├── SKILL.md
├── scripts/
│   ├── voice_tts.py      # Text-to-Speech
│   └── voice_send.py     # Telegram delivery
└── references/
    └── elevenlabs-api.md
```

---

_In Altum Per Vocem._
Axiomata Voice v1.0.0