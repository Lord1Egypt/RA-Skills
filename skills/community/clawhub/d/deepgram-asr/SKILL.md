---
name: deepgram-asr
description: "Transcribe audio via Deepgram Nova-3 API. Fast, accurate, and cost-effective speech-to-text for 50+ languages. Transcripción de audio rápida y precisa con Deepgram Nova-3. Use when the user needs transcription via Deepgram, or wants fast/cheap cloud transcription."
homepage: https://developers.deepgram.com/docs/getting-started-with-pre-recorded-audio
metadata:
  {
    "openclaw":
      {
        "emoji": "🔊",
        "requires": { "bins": ["curl", "python3"], "env": ["DEEPGRAM_API_KEY"] },
        "primaryEnv": "DEEPGRAM_API_KEY",
      },
  }
---

# Deepgram ASR (Nova-3)

Transcribe audio files via Deepgram's Nova-3 model. Sub-300ms latency, 50+ languages, $0.0043/min. Free $200 credit on signup.

Transcriba archivos de audio con el modelo Nova-3 de Deepgram. Latencia inferior a 300ms, más de 50 idiomas, $0.0043/min. $200 de crédito gratis al registrarse.

## Sending audio to OpenClaw

Currently, audio files can be sent to OpenClaw via **Discord** or **WhatsApp**. Send the audio file in a chat message and ask the bot to transcribe it.

Actualmente, los archivos de audio se pueden enviar a OpenClaw a través de **Discord** o **WhatsApp**.

> **Note**: Direct voice recording in the OpenClaw web UI is not yet supported. Use a messaging app to send pre-recorded audio files.
>
> **Nota**: La grabación de voz directa en la interfaz web de OpenClaw aún no está disponible. Use una aplicación de mensajería para enviar archivos de audio pregrabados.

## Quick start

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a
```

Defaults:

- Model: `nova-3`
- Output: `<input>.txt`

## Useful flags

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --out /tmp/transcript.txt
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --language es  # Spanish / Español
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --json --out /tmp/result.json
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --speakers  # speaker diarization / separación de hablantes
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --paragraphs  # smart paragraphs / párrafos inteligentes
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --summarize  # AI summary / resumen con IA
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --detect-language  # auto-detect language / detección automática de idioma
```

## How it works

The script sends audio directly to **Deepgram's API** (`api.deepgram.com`) via HTTPS. No third-party services are involved — audio goes only to Deepgram.

1. Reads the local audio file
2. POSTs it to `https://api.deepgram.com/v1/listen` with your API key
3. Parses the JSON response and extracts transcript text
4. Saves to output file

> **Privacy**: Audio is sent directly to Deepgram's servers over HTTPS. No data is stored by this skill; Deepgram's data retention policy applies.

## Dependencies

- `curl` — for API calls
- `python3` — for JSON response parsing (stdlib only, no pip packages needed)

## Credentials

1. Sign up at https://console.deepgram.com
2. Create an API key at https://console.deepgram.com/project/api-keys
3. Free tier: $200 credit on signup

Set the environment variable:

```bash
export DEEPGRAM_API_KEY="your_api_key"
```

## Supported languages

Nova-3 supports 45+ languages. Common language codes:

| Language | Code | Language | Code |
|----------|------|----------|------|
| English | `en` | Spanish / Español | `es` |
| French / Français | `fr` | German / Deutsch | `de` |
| Portuguese / Português | `pt` | Japanese / 日本語 | `ja` |
| Chinese / 中文 | `zh` | Korean / 한국어 | `ko` |
| Hindi / हिन्दी | `hi` | Russian / Русский | `ru` |
| Italian / Italiano | `it` | Dutch / Nederlands | `nl` |
| Arabic / العربية | `ar` | Turkish / Türkçe | `tr` |

Use `--detect-language` to auto-detect, or `--language <code>` to specify.

Full list: https://developers.deepgram.com/docs/models-languages-overview

## Supported formats

WAV, MP3, MP4, M4A, OGG, FLAC, WebM, and more.
