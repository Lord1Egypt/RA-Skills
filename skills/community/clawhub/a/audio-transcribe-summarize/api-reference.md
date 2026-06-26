# SenseASR API Reference

## Endpoint

```
POST https://api.senseaudio.cn/v1/audio/transcriptions
Content-Type: multipart/form-data
Authorization: Bearer $API_KEY
```

## Models

| Model | Positioning | Best For |
|-------|------------|----------|
| `sense-asr-lite` | Ultra-fast | Batch transcription, 30+ languages, hotword boost |
| `sense-asr` | Standard | General use, subtitles, speaker diarization |
| `sense-asr-pro` | Professional | Meetings, interviews, high-accuracy scenarios |
| `sense-asr-deepthink` | Deep understanding | Dialect/jargon, speech cleanup, intelligent correction |

## Feature Matrix

| Feature | lite | asr | asr-pro | deepthink |
|---------|------|-----|---------|-----------|
| Basic recognition | Y | Y | Y | Y |
| Streaming | - | Y | Y | Y |
| Speaker diarization | - | Y | Y | - |
| Sentiment analysis | - | Y | Y | - |
| Word timestamps | - | Y | Y | - |
| Segment timestamps | - | Y | Y | - |
| Translation | - | Y | Y | Y |
| Hotword boost | Y | - | - | - |
| ITN | Y | Y | Y | - |
| Smart editing | - | - | - | Y |

## Required Parameters

| Param | Type | Description |
|-------|------|-------------|
| `file` | file | Audio file (wav/mp3/ogg/flac/aac/m4a/mp4), max 10MB |
| `model` | string | Model name (see above) |

## Optional Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `language` | string | auto-detect | ISO-639 code: `zh`, `en`, `ja`, etc. |
| `response_format` | string | `json` | `json` / `text` / `verbose_json` |
| `stream` | boolean | false | Enable SSE streaming (not lite) |
| `enable_itn` | boolean | true | Inverse text normalization (not deepthink) |
| `enable_punctuation` | boolean | false | Auto punctuation (asr/pro only) |
| `enable_speaker_diarization` | boolean | false | Speaker separation (asr/pro only) |
| `max_speakers` | integer | - | Max speakers 1-20 (asr-pro only) |
| `enable_sentiment` | boolean | false | Emotion detection (asr/pro only) |
| `timestamp_granularities[]` | array | - | `word` and/or `segment` (asr/pro only) |
| `target_language` | string | - | Translation target language (not lite) |
| `hotwords` | string | - | Comma-separated hotwords (lite only) |

## Response Formats

### JSON (default)
```json
{ "text": "recognized text" }
```

### Verbose JSON
```json
{
  "text": "full text",
  "duration": 4.153,
  "audio_info": { "duration": 4153, "format": "wav" },
  "segments": [
    {
      "id": 0, "start": 0.0, "end": 2.0,
      "text": "segment text",
      "speaker": "speaker_0",
      "sentiment": "Happy",
      "translation": "translated text"
    }
  ],
  "words": [
    { "word": "字", "start": 0.27, "end": 0.51 }
  ]
}
```

### Streaming (SSE)
```
data: {"delta": {"text": "incremental"}, "finish_reason": null}
data: {"delta": {"text": "."}, "finish_reason": "stop", "audio_info": {...}}
data: [DONE]
```

## Language Codes

Common codes: `zh` (Chinese), `en` (English), `ja` (Japanese), `ko` (Korean), `yue` (Cantonese), `fr` (French), `de` (German), `es` (Spanish), `ru` (Russian), `ar` (Arabic), `vi` (Vietnamese), `th` (Thai), `id` (Indonesian), `pt` (Portuguese), `it` (Italian).

## Error Codes

| HTTP | Code | Description |
|------|------|-------------|
| 400 | `invalid` | Bad parameters |
| 429 | `rate_limit_error` | Rate limited |
| 500 | `internal_error` | Server error |

## Constraints

- Max file size: 10MB per request
- Recommended: 16kHz sample rate, mono channel
- For files >10MB, split with ffmpeg before uploading
