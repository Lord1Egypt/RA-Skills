# Official ASR summary

Sources:
- `https://senseaudio.cn/docs/speech_recognition/http_api`

Confirmed HTTP API contract:
- endpoint: `https://api.senseaudio.cn/v1/audio/transcriptions`
- method: `POST`
- content type: `multipart/form-data`
- auth: `Bearer API_KEY`
- required fields:
  - `file`
  - `model`

Official model list:
- `sense-asr-lite`
- `sense-asr`
- `sense-asr-pro`
- `sense-asr-deepthink`

Important public limits and recommendations:
- single file `<=10MB`
- long audio should be chunked
- recommended preprocessing: `16kHz`, mono, reduced background noise
- in Feishu or AudioClaw integrations, incoming voice messages may already be stored as `.ogg` or `.opus`

# Model routing notes

Use `sense-asr-deepthink` for ordinary user voice messages when you want the best text understanding.

Use `sense-asr` when a language hint is provided but no richer structure is required.

Use `sense-asr-pro` when you need:
- sentiment
- speaker diarization
- timestamps
- punctuation

Use `sense-asr-lite` when hotwords matter more than deeper understanding.

# Feature support boundaries from the docs

- `sense-asr-lite`
  - supports hotwords
  - does not support translation
  - does not support stream
  - does not support sentiment or diarization

- `sense-asr`
  - supports translation
  - supports stream
  - supports sentiment, diarization, timestamps
  - does not support hotwords

- `sense-asr-pro`
  - supports all of the richer structure options above
  - `max_speakers` is specifically documented for pro

- `sense-asr-deepthink`
  - good for intelligent correction and voice-input style understanding
  - does not support `language`
  - does not support `enable_itn`
  - does not support punctuation, sentiment, diarization, or timestamps
  - supports `target_language`

# AudioClaw handoff pattern

The main script returns:
- `transcript.raw_text`
- `transcript.normalized_text`
- `understanding.clarification_needed`
- `openclaw.turn_payload`

AudioClaw should treat `turn_payload.content` as the user message text for the next reasoning step.
