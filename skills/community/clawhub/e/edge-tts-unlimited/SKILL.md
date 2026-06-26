---
name: edge-tts-unlimited
description: Free, unlimited text-to-speech using Microsoft Edge neural voices via Python edge-tts. Use when generating long-form audio, podcasts, voice notes, spoken briefs, or headless/server-side TTS without API keys, credits, or character limits.
---

# Edge TTS Unlimited

Free, unlimited neural TTS. No API key. No credits. No character limits.

## Use this skill for

- long-form audio generation
- spoken briefs and voice notes
- server-side or headless TTS on Fly.io, VPS, or Docker
- cases where paid TTS quotas are unnecessary

Prefer this skill over premium TTS when cost and length matter more than voice cloning or premium voice acting.

## Quick start

Generate from text:
```bash
scripts/speak.sh "Hello world" -o output.mp3
```

Generate from file:
```bash
scripts/speak.sh --file /tmp/my-script.txt -o output.mp3
```

With voice and speed:
```bash
scripts/speak.sh --file script.txt -v en-US-GuyNeural -r "+5%" -o brief.mp3
```

## Requirements

- Python 3.8+
- `uv` preferred, or `pip`

The script auto-detects `uv`, falls back to `pip`, and runs `edge-tts` without requiring a dedicated venv.

## Voice presets

- `news-us` → `en-US-GuyNeural` +5%
- `news-bbc` → `en-GB-RyanNeural`
- `calm` → `en-US-AndrewNeural` -10%
- `fast` → `en-US-ChristopherNeural` +20%

Example:
```bash
scripts/speak.sh --file brief.txt --preset news-us -o brief.mp3
```

## Options

```bash
scripts/speak.sh [TEXT] [OPTIONS]
  TEXT              Text to speak (or use --file)
  --file, -f FILE   Read text from file
  --voice, -v NAME  Voice name (default: en-US-GuyNeural)
  --rate, -r RATE   Speed adjustment like "+5%" or "-10%"
  --preset, -p NAME Use a preset voice profile
  --output, -o FILE Output path (default: /tmp/tts-{timestamp}.mp3)
  --list            List available voices
  --list-filter STR Filter voice list
```

## Useful voices

- `en-US-GuyNeural` — strong default for briefs
- `en-US-ChristopherNeural` — authoritative US male
- `en-US-AriaNeural` — confident US female
- `en-GB-RyanNeural` — steady British male
- `en-GB-SoniaNeural` — British female

List voices:
```bash
scripts/speak.sh --list
scripts/speak.sh --list-filter british
scripts/speak.sh --list-filter female
```

## Notes

- Use `--file` for anything longer than a short sentence.
- `+5%` sounds natural for news and summaries.
- Output is compact MP3 suitable for voice content.
- This is not for real-time streaming, voice cloning, or premium character acting.
