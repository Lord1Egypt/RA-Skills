---
name: faster-whisper-local-service
description: Local speech-to-text (STT) transcription service for OpenClaw using faster-whisper. Runs as HTTP microservice on localhost for voice input, microphone transcription, and speech recognition. No recurring API costs — after initial model download, runs fully local. Supports WebChat voice input, Telegram voice messages, and any OpenClaw voice workflow. Keywords: STT, speech to text, voice transcription, local transcription, whisper, faster-whisper, offline, microphone, speech recognition, voice input.
---

# Faster Whisper Local Service

Provision a local STT backend used by voice skills.

## What this sets up

- Python venv for faster-whisper
- `transcribe-server.py` HTTP endpoint at `http://127.0.0.1:18790/transcribe`
- systemd user service: `openclaw-transcribe.service`

## Important: Model download on first run

On first startup, faster-whisper downloads model weights from Hugging Face (~1.5 GB for `medium`). This requires internet access and disk space. After the initial download, models are cached locally and the service runs **fully offline**.

| Model | Download size | RAM usage |
|---|---|---|
| tiny | ~75 MB | ~400 MB |
| base | ~150 MB | ~500 MB |
| small | ~500 MB | ~800 MB |
| medium | ~1.5 GB | ~1.4 GB |
| large-v3 | ~3.0 GB | ~3.5 GB |

To pre-download models in an air-gapped environment, see [faster-whisper docs](https://github.com/SYSTRAN/faster-whisper#model-download).

## Security notes

### Network isolation
- Binds to `127.0.0.1` only — **not reachable from the network**.
- CORS restricted to a single origin (`https://127.0.0.1:8443` by default).
- No credentials, API keys, or secrets are used or stored.

### Input validation
- **Upload size limit**: Requests exceeding the configured limit are rejected before processing (HTTP 413). Default: 50 MB, configurable via `MAX_UPLOAD_MB`.
- **Magic-byte check**: Only files with recognized audio signatures (WAV, OGG, FLAC, MP3, WebM, M4A) are accepted. Unrecognized formats are rejected (HTTP 415) before reaching GStreamer.
- **Subprocess safety**: All arguments to `gst-launch-1.0` are passed as a list — no shell expansion or injection is possible.

### GStreamer dependency
The service uses GStreamer's `decodebin` for audio format conversion. Like any media library, GStreamer's parsers process binary data and should be kept up to date. **Mitigation**: install `gst-launch-1.0` from your OS vendor's trusted packages and apply security updates regularly. The magic-byte pre-filter above reduces the attack surface by rejecting non-audio payloads before they reach GStreamer.

### No data exfiltration
- No outbound network calls (after initial model download).
- No telemetry, analytics, or phone-home behavior.
- Temporary files are created in a per-request `TemporaryDirectory` and cleaned up immediately.

## Reproducibility defaults

- Pinned package: `faster-whisper==1.1.1` (override via env)
- Explicit dependency check for `gst-launch-1.0`
- CORS restricted to one origin by default
- Configurable workspace/service paths (no hardcoded user path)

## Deploy

```bash
bash scripts/deploy.sh
```

With custom settings:

```bash
WORKSPACE=~/.openclaw/workspace \
TRANSCRIBE_PORT=18790 \
WHISPER_MODEL_SIZE=medium \
WHISPER_LANGUAGE=auto \
TRANSCRIBE_ALLOWED_ORIGIN=https://10.0.0.42:8443 \
bash scripts/deploy.sh
```

### Language setting

Default: `auto` (auto-detect language). Set `WHISPER_LANGUAGE=de` for German-only, `en` for English-only, etc. Fixed language is faster and more accurate if you only use one language.

Idempotent: safe to run repeatedly.

## What this skill modifies

| What | Path | Action |
|---|---|---|
| Python venv | `$WORKSPACE/.venv-faster-whisper/` | Creates venv, installs faster-whisper via pip |
| Transcribe server | `$WORKSPACE/voice-input/transcribe-server.py` | Writes server script |
| Systemd service | `~/.config/systemd/user/openclaw-transcribe.service` | Creates + enables persistent service |
| Model cache | `~/.cache/huggingface/` | Downloads model weights on first run |

## Uninstall

```bash
systemctl --user stop openclaw-transcribe.service
systemctl --user disable openclaw-transcribe.service
rm -f ~/.config/systemd/user/openclaw-transcribe.service
systemctl --user daemon-reload
```

Optional full cleanup:

```bash
rm -rf ~/.openclaw/workspace/.venv-faster-whisper
rm -f ~/.openclaw/workspace/voice-input/transcribe-server.py
```

## Verify

```bash
bash scripts/status.sh
```

Expected:
- service `active`
- endpoint responds (HTTP 200/500 acceptable for invalid sample payload)

## Notes

- This skill provides backend transcription only.
- Pair with `webchat-voice-proxy` for browser mic + HTTPS/WSS integration.
- For one-step install, use `webchat-voice-full-stack` (deploys backend + proxy in order).
