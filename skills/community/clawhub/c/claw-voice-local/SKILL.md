---
name: claw-voice-local
description: Convert text to offline Telegram voice messages using piper TTS. Use when the agent should speak a response, send audio, or deliver voice notes via Telegram without internet connectivity.
license: MIT
compatibility: Requires piper TTS binary (Linux ARM64 or x86_64), ffmpeg, and a Telegram bot token. Python 3.11+.
metadata:
  author: photon78
  version: "1.0.0"
  env_required: TELEGRAM_BOT_TOKEN
  env_optional: TELEGRAM_CHAT_ID
---

# claw-voice-local

**Local offline TTS → Telegram Voice Note**

Convert any text to a Telegram voice message using [piper TTS](https://github.com/rhasspy/piper) — fully offline, no cloud API required. Runs on Linux (including Raspberry Pi / ARM64).

## When to use
- Send spoken responses instead of text messages
- Read out summaries, alerts, or reports
- Any task where audio feedback is more natural than text

## Usage

```bash
python3 say.py "Your agent is ready."
python3 say.py "Good morning!" --chat-id 123456789
echo "Task complete." | python3 say.py
```

## Configuration

Set these environment variables (or add to `~/.openclaw/.env`):

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | Optional | Default chat ID (can be passed as `--chat-id`) |

## Environment Variables

```
TELEGRAM_BOT_TOKEN=required   # Telegram bot token — get one from @BotFather
TELEGRAM_CHAT_ID=optional     # Default target chat ID
```

## Config File

This skill reads `~/.openclaw/.env` as a fallback for credentials.
Ensure the file has restricted permissions: `chmod 600 ~/.openclaw/.env`

## Installation

See [README.md](README.md) for step-by-step piper installation.

## Files

| File | Description |
|------|-------------|
| `say.py` | Main entry point: text → Telegram voice note |
| `speak.py` | Core TTS: text → OGG Opus via piper + ffmpeg |
| `send_voice.py` | Telegram sender: OGG → voice message (no dependencies) |

## Requirements

- Python 3.11+
- piper binary (see README)
- ffmpeg
- A piper voice model (`.onnx`)
- Telegram bot token
