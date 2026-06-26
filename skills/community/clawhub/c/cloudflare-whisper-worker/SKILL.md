---
name: cloudflare-whisper-worker
description: Transcribe audio using a deployed Cloudflare Worker Whisper endpoint. Use when converting voice/audio files (wav, mp3, m4a, ogg, webm) to text through the custom /transcribe API, including bearer-token auth, plain-text extraction, and quick CLI transcription workflows.
---

# Cloudflare Whisper Worker

Use this skill to transcribe audio through the deployed Whisper Worker API.

## Endpoint

- Base URL: `https://lotfi-whisper-worker.medtouradmin.workers.dev`
- Route: `POST /transcribe`
- Auth: `Authorization: Bearer <API_TOKEN>`
- Body: raw audio bytes (`--data-binary @file`)

## Required environment variable

Set token once per shell:

```bash
export WHISPER_WORKER_TOKEN="<your_token>"
```

## Transcribe a file (JSON response)

```bash
curl -sS -X POST "https://lotfi-whisper-worker.medtouradmin.workers.dev/transcribe" \
  -H "content-type: audio/wav" \
  -H "authorization: Bearer $WHISPER_WORKER_TOKEN" \
  --data-binary "@audio.wav"
```

## Transcribe and return only text

```bash
curl -sS -X POST "https://lotfi-whisper-worker.medtouradmin.workers.dev/transcribe" \
  -H "content-type: audio/wav" \
  -H "authorization: Bearer $WHISPER_WORKER_TOKEN" \
  --data-binary "@audio.wav" \
| jq -r '.result.text // .text // .result.response // empty'
```

## Content-Type guide

- WAV: `audio/wav`
- MP3: `audio/mpeg`
- M4A: `audio/mp4`
- OGG/OPUS: `audio/ogg`
- WEBM: `audio/webm`

## Common errors

- `401 Unauthorized`: missing/invalid bearer token
- `400 Empty audio body`: file path wrong or empty file
- `400 Send raw audio...`: invalid content-type header
- `500`: worker/runtime/model error; retry and inspect full JSON
