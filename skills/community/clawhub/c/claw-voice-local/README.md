# claw-voice-local

> Local offline TTS → Telegram Voice Note for [OpenClaw](https://openclaw.ai) agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**claw-voice** lets your OpenClaw agent speak — using [piper TTS](https://github.com/rhasspy/piper) to convert any text into a Telegram voice message, fully offline with no cloud API calls.

---

## What it does

```
Agent text  →  piper TTS  →  OGG Opus  →  Telegram Voice Note
```

Your agent calls `say.py "Good morning, here's your briefing."` and you receive a voice message in Telegram.

---

## Requirements

- Linux (x86_64 or ARM64 / Raspberry Pi)
- Python 3.11+
- [piper TTS binary](https://github.com/rhasspy/piper/releases) v1.2+
- ffmpeg (`sudo apt install ffmpeg`)
- A piper voice model (`.onnx`)
- Telegram bot token

---

## Installation

### 1. Install ffmpeg

```bash
sudo apt install ffmpeg
```

### 2. Install piper binary

Download the latest release for your platform from [github.com/rhasspy/piper/releases](https://github.com/rhasspy/piper/releases):

```bash
# Example: Linux ARM64 (Raspberry Pi)
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_aarch64.tar.gz
tar -xzf piper_linux_aarch64.tar.gz
mkdir -p ~/.local/bin ~/.local/lib/piper
cp piper/piper ~/.local/bin/piper
cp piper/*.so* ~/.local/lib/piper/
chmod +x ~/.local/bin/piper

# Example: Linux x86_64
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_x86_64.tar.gz
tar -xzf piper_linux_x86_64.tar.gz
mkdir -p ~/.local/bin ~/.local/lib/piper
cp piper/piper ~/.local/bin/piper
cp piper/*.so* ~/.local/lib/piper/
chmod +x ~/.local/bin/piper
```

### 3. Download a voice model

Browse voices at [huggingface.co/rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices):

```bash
mkdir -p ~/.local/share/piper

# Example: German female (kerstin-low)
wget -P ~/.local/share/piper \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/kerstin/low/de_DE-kerstin-low.onnx
wget -P ~/.local/share/piper \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/kerstin/low/de_DE-kerstin-low.onnx.json

# Example: English female (amy-low)
wget -P ~/.local/share/piper \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/low/en_US-amy-low.onnx
wget -P ~/.local/share/piper \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/low/en_US-amy-low.onnx.json
```

### 4. Configure environment

Export as environment variables (e.g. in your shell profile or OpenClaw env config):

```bash
export TELEGRAM_BOT_TOKEN=your_bot_token_here
export TELEGRAM_CHAT_ID=your_chat_id_here  # optional default target
```

OpenClaw users: set these in your agent's environment via `openclaw.json` or the OpenClaw plugin config.

### 5. Test it

```bash
python3 say.py "Hello, your OpenClaw agent is speaking."
```

---

## Usage

```bash
# Basic
python3 say.py "Good morning!"

# With explicit chat ID
python3 say.py "Alert: disk usage above 90%" --chat-id 123456789

# From stdin (pipeline-friendly)
echo "Task completed." | python3 say.py

# Custom model
python3 say.py "Hello" --model ~/.local/share/piper/en_US-amy-low.onnx

# Speed control (0.85 = slightly slower, easier to understand)
python3 say.py "Hello" --speed 0.85
```

---

## Components

| File | Purpose |
|------|---------|
| `say.py` | Main entry point — combines TTS + Telegram send |
| `speak.py` | Text → OGG Opus via piper + ffmpeg |
| `send_voice.py` | OGG → Telegram Voice Note (stdlib only, no requests) |

You can use each component independently:

```bash
# Generate audio only
python3 speak.py --text "Hello" --output /tmp/hello.ogg

# Send existing audio
python3 send_voice.py /tmp/hello.ogg --chat-id 123456789
```

---

## Using with OpenClaw

Add to your agent's `SOUL.md` or `TOOLS.md`:

```
- **claw-voice** → `python3 /path/to/skills/claw-voice/say.py "<text>"`
  Send text as Telegram voice note via piper TTS (offline)
```

Add to your agent's exec allowlist (`exec-approvals.json`):

```json
{"pattern": "/path/to/skills/claw-voice/say.py", "id": "skill-claw-voice-01"}
```

---

## Built with

- [piper TTS](https://github.com/rhasspy/piper) — fast local TTS
- [OpenClaw](https://openclaw.ai) — self-hosted AI agent platform
- [openclaw-docker-installer](https://github.com/photon78/openclaw-docker-installer) — production-ready OpenClaw setup

---

## License

MIT — see [LICENSE](LICENSE)
