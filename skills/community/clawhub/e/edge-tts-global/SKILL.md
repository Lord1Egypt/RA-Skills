---
name: edge-tts-global
description: Use the globally installed edge-tts command to generate Chinese or multilingual text-to-speech audio on this machine. Use when the user wants text converted to speech, wants a natural online voice quickly, wants Telegram voice-bubble style audio, or wants help choosing Edge TTS voices and commands.
---

# Edge TTS Global

Use this skill when the user wants fast text-to-speech with the globally installed `edge-tts` command.

## What is available

Global commands:
- `edge-tts`
- `edge-playback`

Bundled helper script:
- `scripts/tts_edge.py`

Preferred Chinese test voice:
- `zh-CN-XiaoxiaoNeural`

## Fast workflow

1. Put output files in the **current caller workspace** `temp/` directory.
2. Prefer the bundled Python script `scripts/tts_edge.py` for standard generation.
3. If needed, call `edge-tts` directly.
4. If sending back to Telegram and the user wants a voice bubble, send the audio with `message` and set `asVoice=true`.
5. If the user wants a normal file/audio attachment, send it normally.
6. **After successful sending, immediately delete the generated temporary file.**

## Preferred script usage

Generate audio to the current caller workspace `temp/` directory automatically:

```bash
python3 /data/claw/shared/skills/edge-tts-global/scripts/tts_edge.py -t "老板，你好，我是你的小助理。"
```

Generate audio with explicit relative path under the current caller workspace:

```bash
python3 /data/claw/shared/skills/edge-tts-global/scripts/tts_edge.py -t "老板，你好，我是你的小助理。" -o ./temp/out.mp3
```

Delete temporary file after successful sending:

```bash
python3 /data/claw/shared/skills/edge-tts-global/scripts/tts_edge.py cleanup ./temp/out.mp3
```

Delete both audio and subtitles:

```bash
python3 /data/claw/shared/skills/edge-tts-global/scripts/tts_edge.py cleanup ./temp/out.mp3 ./temp/out.vtt
```

Change voice explicitly:

```bash
python3 /data/claw/shared/skills/edge-tts-global/scripts/tts_edge.py -t "你好" -v zh-CN-XiaoxiaoNeural -o ./temp/out.mp3
```

Generate subtitles too:

```bash
python3 /data/claw/shared/skills/edge-tts-global/scripts/tts_edge.py -t "你好" -o ./temp/out.mp3 --subs ./temp/out.vtt
```

## Direct command patterns

### Generate MP3

```bash
mkdir -p ./temp
edge-tts --voice zh-CN-XiaoxiaoNeural --text "老板，你好，我是你的小助理。" --write-media ./temp/out.mp3
```

### List voices

```bash
edge-tts --list-voices
```

## Telegram sending rule

If the user asks for “气泡语音”, “语音条”, or a voice-message style result:
- generate the file first
- send with `message`
- set `asVoice=true`
- after successful sending, delete the temporary file immediately

If the user asks for a normal audio file:
- send as a regular attachment
- do not set `asVoice=true`
- after successful sending, delete the temporary file immediately

## Cleanup guidance

- Temporary outputs belong in the **current caller workspace** `temp/` directory
- Sending succeeds → delete the generated temporary files immediately
- Prefer `python3 scripts/tts_edge.py cleanup <file> [subtitle]` for deterministic cleanup
- Do not remove the global `edge-tts` install unless the user explicitly asks
