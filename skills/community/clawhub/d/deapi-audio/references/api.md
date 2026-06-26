# Audio API Reference

Base URL: `https://api.deapi.ai/api/v1/client/`
Auth: `Authorization: Bearer $DEAPI_API_KEY`

## txt2audio

```
POST /txt2audio
Content-Type: application/json

{
  "text": "Hello, welcome to our service.",
  "voice": "af_bella",
  "model": "Kokoro",
  "lang": "en-us",
  "speed": 1.0,
  "format": "mp3",
  "sample_rate": 24000,
  "mode": "custom_voice"
}
```

> **Note:** `voice_clone` mode requires `multipart/form-data` (file upload). `custom_voice` and `voice_design` modes use `application/json`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | Yes | Text to convert |
| `model` | string | Yes | See model details below |
| `mode` | string | No | `custom_voice` (default), `voice_clone`, `voice_design` |
| `voice` | string | Yes | Voice ID (see [voices.md](voices.md)) |
| `lang` | string | Yes | Language code or name (see model details below) |
| `speed` | float | Yes | See model details below |
| `format` | string | Yes | `mp3`, `wav`, `flac` |
| `sample_rate` | int | Yes | `24000` |
| `instruct` | string | Conditional | Voice description (required for `voice_design` mode) |
| `ref_audio` | file | Conditional | Reference audio file (required for `voice_clone` mode) |
| `ref_text` | string | No | Transcript of ref_audio (optional, `voice_clone` only) |

### Model: Kokoro

- **Mode:** `custom_voice`
- **Voices:** 41 available (see [voices.md](voices.md#kokoro))
- **Languages:** `en-us`, `en-gb`, `es`, `fr-fr`, `hi`, `it`, `pt-br`
- **Speed:** 0.5-2.0
- **Text limit:** 3-10001 chars

### Model: Chatterbox

- **Mode:** `custom_voice`
- **Voice:** `default` (only option)
- **Languages:** `ar`, `da`, `de`, `en`, `es`, `fi`, `fr`, `he`, `hi`, `it`, `ja`, `ko`, `ms`, `nl`, `no`, `pl`, `pt`, `ru`, `sv`, `sw`, `tr`, `zh`
- **Speed:** fixed `1`
- **Text limit:** 10-2000 chars

### Model: Qwen3_TTS_12Hz_1_7B_CustomVoice

- **Mode:** `custom_voice`
- **Alias:** `--model Qwen3` in text-to-speech.sh
- **Voices:** `Vivian` (default), `Serena`, `Uncle_Fu`, `Dylan`, `Eric`, `Ryan`, `Aiden`, `Ono_Anna`, `Sohee`
- **Languages:** `English`, `Italian`, `Spanish`, `Portuguese`, `Russian`, `French`, `German`, `Korean`, `Japanese`, `Chinese`
- **Speed:** fixed `1`
- **Text limit:** 10-5000 chars
- **Note:** Chinese language does not have `Ryan` voice

### Model: Qwen3_TTS_12Hz_1_7B_Base (Voice Clone)

- **Mode:** `voice_clone`
- **Voice:** `default` (only option)
- **Languages:** `English`, `Italian`, `Spanish`, `Portuguese`, `Russian`, `French`, `German`, `Korean`, `Japanese`, `Chinese`
- **Speed:** fixed `1`
- **Text limit:** 10-5000 chars
- **Requires:** `ref_audio` (binary file, 5-15s, MP3/WAV/FLAC/OGG/M4A)
- **Optional:** `ref_text` (transcript of the reference audio)
- **Content-Type:** `multipart/form-data`

Example (multipart):
```
POST /txt2audio
Content-Type: multipart/form-data

text=Hello world
ref_audio=@sample.mp3
model=Qwen3_TTS_12Hz_1_7B_Base
mode=voice_clone
voice=default
lang=English
speed=1
format=mp3
sample_rate=24000
```

### Model: Qwen3_TTS_12Hz_1_7B_VoiceDesign (Voice Design)

- **Mode:** `voice_design`
- **Voice:** `default` (only option)
- **Languages:** `English`, `Italian`, `Spanish`, `Portuguese`, `Russian`, `French`, `German`, `Korean`, `Japanese`, `Chinese`
- **Speed:** fixed `1`
- **Text limit:** 10-5000 chars
- **Requires:** `instruct` (natural language voice description)

```json
{
  "text": "Hello, welcome to our service.",
  "instruct": "A warm female voice with a British accent",
  "model": "Qwen3_TTS_12Hz_1_7B_VoiceDesign",
  "mode": "voice_design",
  "voice": "default",
  "lang": "English",
  "speed": 1,
  "format": "mp3",
  "sample_rate": 24000
}
```

## audiofile2txt

```
POST /audiofile2txt
Content-Type: multipart/form-data

audio=@recording.mp3
include_ts=true
model=WhisperLargeV3
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audio` | file | Yes | Audio file (AAC, MP3, OGG, WAV, WebM, FLAC). Max 10 MB |
| `include_ts` | bool | Yes | Include timestamps in transcription |
| `model` | string | No | `WhisperLargeV3` |
| `return_result_in_response` | bool | No | Return result directly instead of polling |

### Model: WhisperLargeV3

- **Formats:** AAC, MP3, OGG, WAV, WebM, FLAC
- **Max file size:** 10 MB

## Polling

All endpoints return `{ "request_id": "..." }`. Poll:

```
GET /request-status/{request_id}
```

Status: `processing` (wait 10s), `done` (fetch `result_url`), `failed` (check `error`).
