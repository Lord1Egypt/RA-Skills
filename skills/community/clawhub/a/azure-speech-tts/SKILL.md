---
name: azure-speech-tts
description: Azure Speech TTS skill for generating local audio files from text or SSML with Azure Speech. Use when the user asks to use Azure Speech / Azure TTS / Microsoft TTS / speech synthesis / text-to-speech / SSML, choose voices, control speaking rate/pitch/style, or export MP3/WAV/OGG/PCM audio.
---

# Azure Speech TTS

Use Azure Speech to turn text or SSML into a local audio file under `download/`.

## What this skill does

- Synthesize plain text into speech
- Synthesize full SSML payloads directly
- Choose voice, output format, rate, pitch, style, and role
- Save the result as a local audio file and print a JSON summary

## Configuration

This skill uses a small default config file plus environment variables.

### Default config file

File:
- `config.json`

Default values:
- `default_voice`: `zh-CN-Yunqi:DragonHDOmniLatestNeural`
- `default_format`: `mp3`
- `default_output_dir`: `download`
- `default_timeout_seconds`: `60`

### Secret values

Set these in the local shell environment:

- `AZURE_SPEECH_KEY`
- `AZURE_SPEECH_REGION`

### Optional environment overrides

- `AZURE_SPEECH_VOICE`
- `AZURE_SPEECH_FORMAT`

### Precedence

Use this order:

1. CLI flag
2. Environment variable
3. `config.json`
4. Built-in fallback

## Quick start

```bash
python3 scripts/azure_tts.py \
  --text "你好，这是一段测试语音。" \
  --voice zh-CN-Yunqi:DragonHDOmniLatestNeural \
  --format mp3 \
  --output download/test.mp3
```

For SSML:

```bash
python3 scripts/azure_tts.py \
  --ssml-file temp/input.ssml \
  --format wav \
  --output download/test.wav
```

## Workflow

1. Decide whether the input is plain text or full SSML.
2. Use `--text` / `--text-file` for normal narration.
3. Use `--ssml` / `--ssml-file` only when the payload already contains a complete `<speak>` document.
4. Pick the voice and output format, or let `config.json` supply the defaults.
5. Run `scripts/azure_tts.py`.
6. Return the generated audio path to the user.

## Rules

- Prefer plain text unless the user needs pauses, emphasis, multi-voice content, or expressive styling.
- `--ssml` input must include a full `<speak>` root element.
- Default voice is `zh-CN-Yunqi:DragonHDOmniLatestNeural` if nothing else is set.
- Default output folder is `download/`.
- If the user does not specify format, use the default MP3 output.
- Do not put secrets in `config.json`.

## Common formats

See `references/azure-speech-cheatsheet.md` for the format map and examples.

Short aliases supported by the script:

- `mp3`
- `wav`
- `pcm`
- `ogg`

## Useful options

- `--voice`: Azure voice name, for example `en-US-AriaNeural`
- `--language`: SSML `xml:lang` for plain-text mode
- `--rate`: speaking rate, for example `+10%`
- `--pitch`: pitch adjustment, for example `+2st`
- `--style`: expressive style such as `cheerful`, `sad`, `chat`
- `--style-degree`: strength of the expressive style
- `--role`: voice role when supported
- `--save-ssml`: write the generated SSML to a file for inspection
- `--dry-run`: print the generated SSML without calling Azure

## Output

The helper script writes the audio file and prints JSON like:

```json
{
  "ok": true,
  "output_path": "download/test.mp3",
  "format": "audio-24khz-48kbitrate-mono-mp3",
  "voice": "zh-CN-Yunqi:DragonHDOmniLatestNeural",
  "language": "zh-CN",
  "bytes": 123456
}
```

Use the printed `output_path` as the deliverable path.
