---
name: gemini-live-phone
version: 1.0.1
description: Bridge Twilio phone calls to Google Gemini Live API for real-time AI voice conversations. No STT/TTS middleware required. Includes VAD and echo suppression.
metadata:
  openclaw:
    emoji: "📞"
    requires:
      bins: ["python3", "uvicorn"]
      env: ["GOOGLE_API_KEY", "TWILIO_AUTH_TOKEN"]
    primaryEnv: "GOOGLE_API_KEY"
---

# Gemini Live Phone Bridge

Real-time voice AI over phone calls using Google Gemini's native audio capabilities.

## Architecture

```
Phone ↔ Twilio ↔ WebSocket (μ-law 8kHz) ↔ Bridge (PCM transcoding) ↔ Gemini Live API (24kHz PCM)
```

## Quick Start

```bash
# Set required env vars
export GOOGLE_API_KEY="your-key"
export TWILIO_AUTH_TOKEN="your-token"

# Run the bridge
python scripts/bridge.py --port 3335
```

## Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/gemini-live/status` | GET | Health check + active calls |
| `/gemini-live/incoming` | POST | TwiML for inbound calls (Twilio webhook) |
| `/gemini-live/stream` | WS | Twilio Media Stream WebSocket |
| `/gemini-live/call` | POST | Initiate outbound call |
| `/gemini-live/twiml` | POST | TwiML for outbound calls |
| `/gemini-live/call-status` | POST | Twilio call status webhook |

## Outbound Call API

```bash
curl -X POST https://your-domain/gemini-live/call \
  -H 'Content-Type: application/json' \
  -d '{"to": "+1234567890", "greeting": "Hello! This is Marcia."}'
```

## Configuration

All settings via CLI args or environment variables:

### Core
- `--model` — Gemini model (default: `gemini-2.5-flash-native-audio-latest`)
- `--voice` — Gemini voice: Puck, Charon, Kore, Fenrir, Aoede, Leda, Orus, Zephyr (default: Kore)
- `--from-number` — Twilio outbound number (default: env `TWILIO_FROM`)
- `--system-prompt` — AI persona system prompt
- `--max-duration` — Max call seconds (default: 300)

### VAD (Voice Activity Detection)
- `--vad-enabled` / `--no-vad` — Toggle server-side VAD (default: on)
- `--vad-silence-ms` — Silence duration to trigger activityEnd (default: 500)
- `--vad-energy-threshold` — RMS energy threshold (default: 0.01)
- `--vad-speech-min-ms` — Min speech duration before activityStart (default: 100)

### Echo Suppression
- `--echo-multiplier` — VAD threshold multiplier during agent speech (default: 3.0)
- `--echo-decay-ms` — Decay time after agent stops speaking (default: 300)

## Twilio Setup

1. Buy a phone number on Twilio
2. Set Voice webhook: `https://your-domain/gemini-live/incoming` (HTTP POST)
3. Set Call status URL: `https://your-domain/gemini-live/call-status` (HTTP POST)
4. Ensure geo-permissions are enabled for target countries

## Network Requirements

The bridge must be accessible from the internet (Twilio connects to it).
Recommended: Caddy reverse proxy with WebSocket support.

```
# Caddy config example
handle /gemini-live/* {
    reverse_proxy localhost:3335 {
        flush_interval -1
        transport http {
            read_timeout 0
            write_timeout 0
        }
    }
}
```

## Performance

Latency benchmarks (Gemini 2.5 Flash Native Audio):

| Config | Median | Min | Max |
|---|---|---|---|
| No VAD, 200ms buffer | 3,660ms | 2,360ms | 5,180ms |
| Server VAD, 50ms buffer | **2,500ms** | **2,080ms** | 6,980ms |

Server-side VAD reduces median latency by ~32%.
