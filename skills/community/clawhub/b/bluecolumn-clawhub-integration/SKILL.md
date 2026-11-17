---
name: bluecolumn-clawhub-integration
description: Integrate ClawHub with BlueColumn AI for audio ingest, memory, and semantic retrieval. Use when wiring ClawHub to push calls, music, podcasts, and voice notes through BlueColumn's /v1/audio/ingest endpoint; when setting up audio pipeline from ClawHub to BlueColumn; or when configuring real-time audio streaming for live conversations with mid-call memory.
---

# BlueColumn ClawHub Audio Ingest Integration

BlueColumn (bluecolumn.ai) is a Memory Infrastructure API for AI agents. This skill documents how ClawHub integrates with BlueColumn for audio ingest, memory, and semantic retrieval.

## Primary Endpoint

```
POST https://api.bluecolumn.ai/v1/audio/ingest
```

This endpoint handles uploaded calls, music, podcasts, voice notes, and mixed audio.

## Request Format

```json
{
  "audio_url": "https://signed-storage-url.example.com/audio-file.mp3",
  "namespace": "clawhub_audio",
  "session_id": "clawhub_call_12345",
  "user_ref": "customer_6789",
  "mode": "auto",
  "tier": "pro",
  "options": {
    "transcribe": true,
    "diarize": true,
    "detect_language": true,
    "translate_to_english": true,
    "pii_redaction": true,
    "sentiment": true,
    "extract_entities": true,
    "generate_summary": true,
    "generate_action_items": true,
    "analyze_music": true,
    "detect_bpm": true,
    "detect_key": true,
    "detect_instruments": true,
    "detect_mood": true,
    "detect_genre": true,
    "detect_sections": true,
    "generate_audio_embeddings": true,
    "generate_text_embeddings": true,
    "speaker_aware_chunking": true,
    "store_original_audio": true
  }
}
```

## Required Fields

Every BlueColumn request must include:
- `namespace` — never rely on a default
- `session_id` — unique session identifier
- `user_ref` — user reference
- `metadata.source` = `"clawhub"`
- `metadata.channel` — channel identifier
- `metadata.agent` — agent identifier

## Mode Options

| Mode | Use Case |
|------|----------|
| `"auto"` | Default for recorded calls |
| `"music"` | For music files |
| `"hybrid"` | For calls containing both speech and music |

## Default Audio Configuration

```json
{
  "mode": "auto",
  "tier": "pro",
  "transcribe": true,
  "diarize": true,
  "pii_redaction": true,
  "generate_summary": true,
  "generate_action_items": true,
  "speaker_aware_chunking": true,
  "analyze_music": true,
  "store_original_audio": true
}
```

## Webhook & Status Check

- Receive completion through the provided `webhook_url`
- If a webhook is unavailable, check: `GET /v1/audio/:audio_id`

## Real-Time Streaming

For live conversations requiring mid-call memory:

```
WebSocket: wss://api.bluecolumn.ai/v1/audio/stream
```

## Existing Integrations (Do Not Remove)

The following BlueColumn endpoints are not part of this ingest integration but must continue to work:

- `POST /v1/converse`
- `POST /v1/remember`
- `POST /v1/recall` — semantic retrieval
- `POST /v1/note`
- `GET /v1/sessions`
- `GET /v1/health`

## Field Name Gotchas

- `/agent-remember` uses `text` not `content`
- `/agent-recall` uses `q` not `query`
- `/agent-note` uses `text` not `note`

## API Key Handling

Store the BlueColumn API key using the platform's secret store (preferred) or in `TOOLS.md`:

```
### BlueColumn
API Key: bc_live_XXXXXXXXXXXXXXXXXXXX
```

Keys are generated at bluecolumn.ai/dashboard. Never log or expose keys in output.
