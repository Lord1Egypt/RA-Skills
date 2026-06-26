# SenseASR notes for speaking mode

Required env var:
- `SENSEAUDIO_API_KEY`

Optional env var:
- `SENSEAUDIO_BASE_URL`

Endpoint:
- `POST /v1/audio/transcriptions`

Default choice for speaking mode:
- model: `sense-asr-pro`
- language: `en`
- response parsing: plain transcript text only

Why `sense-asr-pro` by default:
- better accuracy for short spoken english
- supports punctuation and ITN
- leaves room for timestamps or translation later if needed

Do not send raw ASR JSON back to Feishu.
Extract the transcript text and respond naturally.

Deepthink caveat:
- `sense-asr-deepthink` does not support `language`
- only use it deliberately

File guidance:
- keep single file <= 10 MB
- prefer lower-noise audio
- voice messages can be `.wav`, `.mp3`, `.m4a`, `.mp4`, and other supported formats
