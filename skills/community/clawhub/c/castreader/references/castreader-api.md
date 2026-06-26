# Castreader API Reference

## TTS API

### Endpoint
`POST {baseUrl}/api/captioned_speech_partly`

Default baseUrl: `https://api.castreader.ai`

### Request Body
```json
{
  "model": "kokoro",
  "input": "Text to convert to speech",
  "voice": "af_heart",
  "response_format": "mp3",
  "return_timestamps": true,
  "speed": 1.5,
  "stream": false,
  "language": "en"
}
```

### Response
```json
{
  "audio": "<base64 encoded MP3>",
  "timestamps": [
    { "word": "Hello", "start_time": 0.0, "end_time": 0.3 },
    { "word": "world", "start_time": 0.35, "end_time": 0.7 }
  ],
  "duration": 5.2,
  "processed_text": "Text that was processed",
  "unprocessed_text": "Remaining text for next call"
}
```

### Key Behavior
- **Partly processing**: Each call only processes a portion of the input text
- `unprocessed_text` contains the remaining text — loop until empty
- Timestamps may use `start/end` or `start_time/end_time` format
- Audio is base64-encoded MP3

### Retry Logic
- Retry on HTTP 502/503/504 (up to 3 times)
- Exponential backoff: 2s × attempt number

## Chrome Extension Messages

### Content Script → Background
| Message Type | Payload | Response |
|---|---|---|
| `TTS_GENERATE` | `{ input, voice?, speed?, language? }` | `{ audioUrl, timestamps, duration }` |
| `GET_SETTINGS` | — | `{ apiBaseUrl, voice, speed, language }` |

### Popup/Background → Content Script
| Message Type | Payload | Effect |
|---|---|---|
| `START_READING` | — | Start extraction + TTS playback |
| `STOP_READING` | — | Stop playback, hide player |
| `TOGGLE_READING` | — | Toggle play/pause/restart |
| `GET_STATUS` | — | Returns current status + playback state |

## Extraction Pipeline

3-layer extraction:
1. **Special extractors** — Site-specific (WeRead, Kindle, Notion, Google Docs, etc.)
2. **Site rules** — CSS selector rules from `site-rules.json`
3. **Visible-Text-Block** — Generic algorithm (text density + link density + context-sensitive classification)

### Bundle API
After injecting `extractor-bundle.js`:
```javascript
const result = await window.__castreaderExtract();
// result: { success, title, paragraphs: [{text, tagName, className}], language, method }
```
