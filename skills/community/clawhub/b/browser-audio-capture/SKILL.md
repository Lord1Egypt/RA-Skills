---
name: browser-audio-capture
description: Capture audio from any browser tab — meetings, YouTube, podcasts, courses, webinars — and stream to any AI agent. Zero API keys, works with any framework.
version: 1.1.0
---

# Browser Audio Capture

**Give any AI agent ears for the browser.** One Chrome extension captures audio from any tab — meetings, YouTube, podcasts, webinars, courses, earnings calls — and streams it to your AI pipeline.

## Why Use This

Your AI agent can't hear anything happening in your browser. This skill fixes that. Capture audio from any Chrome tab and stream it to your agent — no API keys, no OAuth, no per-platform integrations.

**Use cases:** meeting summaries, YouTube/podcast notes, competitive intel from earnings calls, auto-notes from online courses, customer call analysis — anything that plays audio in a browser tab.

**Works with any AI agent** — Claude, ChatGPT, OpenClaw, LangChain, CrewAI, or your own. If your agent can run shell commands or receive HTTP, it gets browser audio.

## Prerequisites

Chrome with remote debugging:

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --user-data-dir=$HOME/.chrome-debug-profile &
```

Python 3.9+ with aiohttp: `pip install aiohttp`

## Quick Start

### CLI (any agent that can exec)

```bash
# List tabs — meetings flagged with 🎙️
python3 -m browser_capture.cli tabs

# Auto-detect and capture meeting tab
python3 -m browser_capture.cli capture

# Continuous watch mode
python3 -m browser_capture.cli watch --interval 15

# Stop
python3 -m browser_capture.cli stop
```

### Chrome Extension (one-click, persistent)

1. `chrome://extensions/` → Developer mode → Load unpacked → `scripts/extension/`
2. Join a meeting → click Percept icon → Start Capturing
3. Close popup — capture continues in background

## Supported Platforms

Google Meet • Zoom (web) • Microsoft Teams • Webex • Whereby • Around • Cal.com • Riverside • StreamYard • Ping • Daily.co • Jitsi • Discord — plus any future platform that runs in a browser.

## Audio Output

Streams to `http://127.0.0.1:8900/audio/browser` as JSON:

```json
{
  "sessionId": "browser_1709234567890",
  "audio": "<base64 PCM16>",
  "sampleRate": 16000,
  "format": "pcm16",
  "tabUrl": "https://meet.google.com/...",
  "tabTitle": "Weekly Standup"
}
```

Configure endpoint in `scripts/extension/offscreen.js` (`PERCEPT_URL`). Point it at Whisper, Deepgram, NVIDIA Riva, or any transcription service.

## Troubleshooting

- **No tabs**: Chrome needs `--remote-debugging-port=9222`
- **Button won't click**: Remove + re-add extension (MV3 caches aggressively)
- **Audio not arriving**: Check receiver on port 8900. Extension sends to `/audio/browser`
