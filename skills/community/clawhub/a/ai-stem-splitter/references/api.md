# AI Stem Splitter API Reference

Load this file when executing audio splitting, writing integration code, or explaining API behavior.

## Product Facts

- Product name: AI Stem Splitter
- Core output: vocals, drums, bass, guitar, piano, other
- Common use cases: karaoke vocal removal, acapella extraction, DJ remix prep, guitar or piano practice loops, stem-level audio analysis
- Public API base: `https://api.aistemsplitter.org/v1`
- API key source: AI Stem Splitter Settings -> Developer
- Authentication: `Authorization: Bearer $AISTEMSPLITTER_API_KEY`
- Credits: one credit equals one second of source audio
- Statuses: `queued`, `processing`, `succeeded`, `failed`
- Main model choices mentioned in product docs: `htdemucs_ft`, `htdemucs`, `htdemucs_6s`; raw REST examples use `stemModel: "6s"` for six-stem output

## Endpoints

Check credits:

```bash
curl -sS "https://api.aistemsplitter.org/v1/credits" \
  -H "Authorization: Bearer $AISTEMSPLITTER_API_KEY"
```

Create a split from a direct audio URL:

```bash
curl -sS -X POST "https://api.aistemsplitter.org/v1/audio/splits" \
  -H "Authorization: Bearer $AISTEMSPLITTER_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: demo-001" \
  -d '{
    "input": {
      "type": "direct_url",
      "url": "https://example.com/song.mp3"
    },
    "stemModel": "6s",
    "webhookUrl": "https://example.com/webhooks/aistemsplitter"
  }'
```

Reserve an upload:

```bash
curl -sS -X POST "https://api.aistemsplitter.org/v1/audio/uploads" \
  -H "Authorization: Bearer $AISTEMSPLITTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "song.wav",
    "contentType": "audio/wav",
    "contentLength": 23812033
  }'
```

Then upload the file to the returned `uploadUrl` with the returned `uploadHeaders`, and create the split with `input.type` set to `uploaded_file`.

Poll status:

```bash
curl -sS "https://api.aistemsplitter.org/v1/audio/splits/$SPLIT_ID" \
  -H "Authorization: Bearer $AISTEMSPLITTER_API_KEY"
```

## SDKs

Node:

```bash
npm install @aistemsplitter/sdk
```

Python:

```bash
pip install aistemsplitter
```

Use SDKs for production code because they expose typed methods, upload helpers, wait helpers, typed errors, and webhook verification helpers.

## Webhooks

When `webhookUrl` is provided, AI Stem Splitter posts terminal events. Verify `AIStemSplitter-Signature` with the webhook signing secret.

Signature format:

```txt
AIStemSplitter-Signature: t=1760000000,v1=<hex-hmac>
```

HMAC input:

```txt
<timestamp>.<raw-json-body>
```

Use SHA-256 HMAC and reject stale timestamps.

## Errors

| Code | HTTP | Meaning |
| --- | ---: | --- |
| `UNAUTHORIZED` | 401 | Missing or invalid API key |
| `INSUFFICIENT_CREDITS` | 402 | Not enough credits |
| `VALIDATION_ERROR` | 422 | Invalid request body or audio source |
| `RATE_LIMITED` | 429 | API key exceeded its per-minute limit |
| `SERVER_ERROR` | 500 | Internal service error |
