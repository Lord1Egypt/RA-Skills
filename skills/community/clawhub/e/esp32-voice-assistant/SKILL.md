---
name: esp32-voice-assistant
description: Hands-free voice assistant for OpenClaw on an ESP32-S3-BOX-3 — on-device wake word, switchable xAI Grok / ElevenLabs / FishAudio STT+TTS, no Home Assistant required.
version: 1.1.0
metadata: {"openclaw":{"emoji":"🎙️","homepage":"https://github.com/darrenjrobinson/voice-esp32-openclaw","requires":{"env":["OPENCLAW_URL","ESP32_HOST","BRIDGE_ADVERTISE_HOST"],"bins":["docker","git"]},"primaryEnv":"XAI_API_KEY","envVars":[{"name":"XAI_API_KEY","required":false,"description":"xAI API key — required when STT_PROVIDER or TTS_PROVIDER is xai (the default)."},{"name":"ELEVENLABS_API_KEY","required":false,"description":"ElevenLabs API key — required when a provider is set to elevenlabs."},{"name":"FISHAUDIO_API_KEY","required":false,"description":"FishAudio API key — required when a provider is set to fishaudio."},{"name":"OPENCLAW_URL","required":true,"description":"OpenClaw OpenAI-compatible chat endpoint, e.g. http://host.docker.internal:18789 — the chat interface must be enabled in OpenClaw."},{"name":"OPENCLAW_API_KEY","required":false,"description":"Bearer token for the OpenClaw endpoint (most gateways return 401 without it)."},{"name":"ESP32_HOST","required":true,"description":"LAN IP or .local hostname of the ESP32-S3-BOX-3."},{"name":"ESP32_NOISE_PSK","required":false,"description":"ESPHome native API encryption key (base64), only if the device's api: block sets one."},{"name":"BRIDGE_ADVERTISE_HOST","required":true,"description":"LAN IP of the Docker host — the device fetches reply audio from here; container autodetection returns the wrong IP."},{"name":"STT_PROVIDER","required":false,"description":"Speech-to-text provider: xai (default), elevenlabs, or fishaudio."},{"name":"TTS_PROVIDER","required":false,"description":"Text-to-speech provider: xai (default), elevenlabs, or fishaudio."},{"name":"ELEVENLABS_VOICE_ID","required":false,"description":"ElevenLabs voice ID — required when TTS_PROVIDER=elevenlabs."},{"name":"ELEVENLABS_TTS_MODEL","required":false,"description":"ElevenLabs TTS model (default eleven_flash_v2_5)."},{"name":"ELEVENLABS_STT_MODEL","required":false,"description":"ElevenLabs STT model (default scribe_v1)."},{"name":"ELEVENLABS_OUTPUT_RATE","required":false,"description":"PCM rate requested from ElevenLabs (default 24000; free tier cap)."},{"name":"FISHAUDIO_VOICE_ID","required":false,"description":"FishAudio voice reference_id — required when TTS_PROVIDER=fishaudio."},{"name":"FISHAUDIO_TTS_MODEL","required":false,"description":"FishAudio TTS model (default s1)."},{"name":"FISHAUDIO_OUTPUT_RATE","required":false,"description":"PCM rate requested from FishAudio (default 44100)."},{"name":"OPENCLAW_SESSION_KEY","required":false,"description":"Session identity for voice turns (default agent:main:voice)."},{"name":"OPENCLAW_SESSION_MODE","required":false,"description":"How the session key is sent: user (OpenAI user field) or header (X-Session-Key)."},{"name":"OPENCLAW_MODEL","required":false,"description":"Model name in the chat completions body (default openclaw)."},{"name":"OPENCLAW_TIMEOUT_SECONDS","required":false,"description":"Max wait for the agent reply (default 240)."},{"name":"XAI_VOICE","required":false,"description":"xAI TTS voice (default eve) or a custom voice ID."},{"name":"XAI_TTS_LANGUAGE","required":false,"description":"Spoken language for STT/TTS (default en)."},{"name":"TTS_SAMPLE_RATE","required":false,"description":"Sample rate requested from TTS (default 24000)."},{"name":"TTS_STREAMING","required":false,"description":"Stream TTS synthesis (default true)."},{"name":"TTS_PORT","required":false,"description":"Wyoming TTS server port for the optional HA profile (default 10200)."},{"name":"WYOMING_HOST","required":false,"description":"Wyoming pipeline server bind host (default 127.0.0.1)."},{"name":"WYOMING_PORT","required":false,"description":"Wyoming pipeline server port (default 10300)."},{"name":"BRIDGE_HTTP_PORT","required":false,"description":"HTTP port the bridge serves reply audio on (default 10400)."},{"name":"BRIDGE_VOLUME","required":false,"description":"Device volume set before each reply, 0-1; 0 leaves it alone (default 1.0)."},{"name":"BRIDGE_ACK_PHRASE","required":false,"description":"Phrase spoken while the agent thinks; empty disables (default: On it.)."},{"name":"VAD_THRESHOLD","required":false,"description":"Mean-amplitude speech gate (default 500; ~60 suits the quiet BOX-3 mic)."},{"name":"VAD_SILENCE_SECONDS","required":false,"description":"End-of-utterance silence (default 0.8)."},{"name":"VAD_MAX_SECONDS","required":false,"description":"Capture cap in seconds (default 10)."},{"name":"LOG_LEVEL","required":false,"description":"Bridge log level (default INFO)."}]}}
---

# ESP32 Voice Assistant for OpenClaw

Give OpenClaw a hardware voice: an **ESP32-S3-BOX-3** running **stock ESPHome firmware** talks directly to a Docker bridge — on-device wake word, VAD, STT, OpenClaw as the agent brain, then streamed sentence-chunked TTS back to the speaker. **No Home Assistant in the voice path**, and zero firmware changes: the bridge impersonates the Home Assistant voice client over the ESPHome native API (TCP 6053), so you never reflash or edit device YAML.

```
wake word (on-device) → ESP32-S3-BOX-3 → bridge (Docker): VAD → STT (xAI|ElevenLabs|FishAudio)
  → spoken ack → OpenClaw /v1/chat/completions → TTS (xAI|ElevenLabs|FishAudio, streamed)
  → device fetches reply audio (HTTP :10400, FLAC)
```

> The author's device answers to **"Yo Marvin" — a custom-trained wake word**. Yours can use any standard ESPHome wake word (e.g. "Hey Jarvis") or a custom one you train yourself; the process is covered in [Hardware Voice Assistant for OpenClaw](https://blog.darrenjrobinson.com/hardware-voice-assistant-for-openclaw/).

STT and TTS providers are **independently switchable** between xAI Grok Voice, ElevenLabs, and FishAudio — mix and match (e.g. cheap xAI STT + a FishAudio custom voice for TTS).

## Hardware & prerequisites

- **ESP32-S3-BOX-3** running an ESPHome voice-assistant firmware with on-device wake word (the stock [wake-word-voice-assistants](https://github.com/esphome/wake-word-voice-assistants) config or a derivative — standard or custom-trained wake word). Other ESPHome voice devices should work; the bridge adapts to the advertised media format.
- **Docker host on the same LAN** — the device must be able to reach the bridge's HTTP port (default 10400).
- **OpenClaw** with the **chat interface enabled** — the bridge talks to OpenClaw's OpenAI-compatible `/v1/chat/completions` endpoint, which is only served when the chat interface is turned on in your OpenClaw configuration. It must be reachable from the bridge (default compose config expects it on the Docker host, port 18789).
- **xAI, ElevenLabs, and/or FishAudio API key** — at least one, matching your `STT_PROVIDER`/`TTS_PROVIDER` selection. `ELEVENLABS_VOICE_ID`/`FISHAUDIO_VOICE_ID` is also required when TTS is that provider.

## Setup

1. Clone the repo and create the config:

   ```bash
   git clone https://github.com/darrenjrobinson/voice-esp32-openclaw.git
   cd voice-esp32-openclaw
   cp .env.example .env
   ```

2. In OpenClaw, make sure the **chat interface is enabled** so `/v1/chat/completions` is being served, and note its URL and API key.

3. Edit `.env` — at minimum: `STT_PROVIDER`/`TTS_PROVIDER`, the matching API key(s), `OPENCLAW_URL`, `OPENCLAW_API_KEY`, `ESP32_HOST` (and `ESP32_NOISE_PSK` if the device API is encrypted), and `BRIDGE_ADVERTISE_HOST` (the Docker host's LAN IP — required inside Docker). A commented reference copy ships with this skill as [example.env](example.env).

4. **Disconnect Home Assistant's voice subscription** for the device (disable the ESPHome integration entry or its *assist satellite* entity). The protocol allows only one voice-assistant subscriber — with two, the wake word silently does nothing.

5. Start the bridge and verify:

   ```bash
   docker compose --profile bridge up -d --build
   docker compose logs -f voice-bridge
   # expect: "Connected to <device> (…)" and "device announcement format: flac @ 48000 Hz"
   ```

6. Say the wake word. Done.

## Configuration reference (all in `.env`)

| Variable | Default | Purpose |
|---|---|---|
| `STT_PROVIDER` / `TTS_PROVIDER` | `xai` | `xai`, `elevenlabs`, or `fishaudio`, independently — any mix works |
| `XAI_VOICE` | `eve` | Any of the 26 built-in xAI voices or a custom voice ID |
| `ELEVENLABS_VOICE_ID` | — | Required for ElevenLabs TTS; list yours with `python scripts/elevenlabs_voices.py` |
| `ELEVENLABS_TTS_MODEL` | `eleven_flash_v2_5` | Lowest-latency, half-price model |
| `FISHAUDIO_VOICE_ID` | — | Required for FishAudio TTS; this is the voice's `reference_id` — list yours with `python scripts/fishaudio_voices.py` |
| `FISHAUDIO_TTS_MODEL` | `s1` | Or `s2-pro`, `s2.1-pro`, or the free `s2.1-pro-free` |
| `OPENCLAW_SESSION_KEY` | `agent:main:voice` | Session identity sent to OpenClaw (`OPENCLAW_SESSION_MODE=user` sends it as the OpenAI `user` field, `header` as `X-Session-Key`) |
| `OPENCLAW_TIMEOUT_SECONDS` | `240` | Max wait for the agent's reply — tool-heavy turns can run minutes |
| `BRIDGE_ACK_PHRASE` | `On it.` | Spoken while the agent thinks; synthesized once and cached; empty disables |
| `BRIDGE_VOLUME` | `1.0` | Device volume set before each reply (`0` = leave alone) |
| `VAD_THRESHOLD` | `500` | Speech gate — the BOX-3 mic runs quiet, values near `60` work well; per-turn level stats are logged for tuning |
| `VAD_SILENCE_SECONDS` / `VAD_MAX_SECONDS` | `0.8` / `10` | End-of-utterance silence and capture cap |
| `TTS_STREAMING` | `true` | Stream synthesis for fastest time-to-first-audio |

Per-turn cost metrics (USD + ElevenLabs credits) are appended to `out/metrics.jsonl`. A typical turn costs ~$0.005 (all-xAI or all-FishAudio) to ~$0.015 (ElevenLabs TTS).

## Troubleshooting

- **`.env` changes don't apply**: containers read `.env` only at creation. From the repo directory run `docker compose --profile bridge up -d` (add `--force-recreate` if it reports nothing changed). `restart` is not enough.
- **401 or connection refused from OpenClaw**: confirm the chat interface is enabled in OpenClaw (it serves `/v1/chat/completions`), `OPENCLAW_URL` is reachable from inside the container, and `OPENCLAW_API_KEY` matches.
- **Wake word does nothing**: something else (usually Home Assistant) still holds the voice-assistant subscription — only one subscriber is allowed.
- **No reply audio**: check `BRIDGE_ADVERTISE_HOST` is the Docker *host's* LAN IP and port 10400 is reachable from the device.
- **Device quirks** (chunked-transfer rejection, FLAC-only decoding, wedged announcements, volume handling) are already handled by the bridge — see the README's "Device quirks" table before suspecting the device.
- **Rollback**: `docker compose --profile bridge down`, then re-enable the ESPHome integration in Home Assistant — the device reverts to the HA Assist pipeline immediately; nothing on the device was ever modified.

## Further reading

- [Going Direct — ESP32 Voice for OpenClaw](https://blog.darrenjrobinson.com/going-direct-esp32-voice-for-openclaw/) — the write-up of this integration.
- [Hardware Voice Assistant for OpenClaw](https://blog.darrenjrobinson.com/hardware-voice-assistant-for-openclaw/) — device setup and training custom wake words (like "Yo Marvin").
- [GitHub: darrenjrobinson/voice-esp32-openclaw](https://github.com/darrenjrobinson/voice-esp32-openclaw) — source, full README, cost analysis, and utility scripts.
