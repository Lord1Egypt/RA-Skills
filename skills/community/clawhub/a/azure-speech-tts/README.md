# azure-speech-tts

Azure Speech TTS skill for generating local audio files from text or SSML.

## What it does

- Turn plain text into speech
- Turn SSML into speech
- Choose voice, format, rate, pitch, style, and role
- Save audio to a local file under `download/`

## Requirements

Set these environment variables before using the skill:

- `AZURE_SPEECH_KEY`
- `AZURE_SPEECH_REGION`

## Default settings

- Voice: `zh-CN-Yunqi:DragonHDOmniLatestNeural`
- Format: `mp3`
- Output directory: `download/`
- Timeout: `60` seconds

## Quick start

```bash
python3 scripts/azure_tts.py \
  --text "你好，这是一段测试语音。" \
  --output download/test.mp3
```

SSML example:

```bash
python3 scripts/azure_tts.py \
  --ssml-file temp/input.ssml \
  --format wav \
  --output download/test.wav
```

## Notes

- Use SSML only when you already have a complete `<speak>` document.
- Prefer plain text for normal narration.
- See `SKILL.md` for the full workflow and options.
