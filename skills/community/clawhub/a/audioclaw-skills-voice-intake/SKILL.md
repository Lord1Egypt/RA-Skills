---
name: audioclaw-skills-voice-intake
description: Use when AudioClaw Skills needs to understand a user voice message with AudioClaw ASR, including speech-to-text, model routing for deepthink or pro features, optional timestamps or sentiment, and packaging the result into a ready-to-use AudioClaw user turn payload.
---

# AudioClaw Skills Voice Intake

## When to use

Use this skill when the user sends a voice message and AudioClaw should understand the content before replying.

Common triggers:
- A Feishu or chat bot receives an audio message instead of text.
- AudioClaw needs a transcript plus a clean user message payload.
- The workflow wants richer ASR features such as timestamps, sentiment, or speaker separation.
- The team wants one stable AudioClaw intake entrypoint instead of hand-written ASR requests.
- The channel stores inbound voice files as `.ogg` or `.opus`, and AudioClaw still needs one stable ASR path.

Do not use this skill for speech output. Use `$audioclaw-skills-voice-reply` for TTS.

## Workflow

1. Save the incoming audio file locally.
2. Run `scripts/openclaw_voice_intake.py` with the audio path.
3. Let the script choose the best model when no model is forced:
   - `sense-asr-deepthink` for normal single-speaker voice understanding
   - `sense-asr` when a language hint is provided
   - `sense-asr-pro` when timestamps, sentiment, speaker diarization, or punctuation are requested
   - `sense-asr-lite` when hotwords are requested
4. Use the JSON manifest it returns as the AudioClaw handoff:
   - `transcript.normalized_text`
   - `openclaw.turn_payload`
   - `routing.selected_model`
5. If `understanding.clarification_needed` is `true`, ask the user to repeat or resend the audio.

## Runtime model

Official HTTP ASR API:
- Endpoint: `https://api.senseaudio.cn/v1/audio/transcriptions`
- Content type: `multipart/form-data`
- File size limit: `<=10MB`
- Practical local input suffixes accepted by this skill: `.wav`, `.mp3`, `.ogg`, `.opus`, `.flac`, `.aac`, `.m4a`, `.mp4`

Supported response goals:
- plain transcript
- richer raw response passthrough
- AudioClaw-ready turn payload

The skill keeps two layers separate:
- ASR output from AudioClaw ASR
- AudioClaw packaging and clarification heuristics

## API key lookup

This skill now treats `SENSEAUDIO_API_KEY` as the default API key source again.

Runtime rules:
- If the host app injects `SENSEAUDIO_API_KEY` as an AudioClaw login token such as `v2.public...`, the shared bootstrap will replace it with the real `sk-...` value from `~/.audioclaw/workspace/state/senseaudio_credentials.json` before ASR starts.
- `--api-key-env` still works, but the default runtime path is `SENSEAUDIO_API_KEY`.

## Commands

Basic voice intake:

```bash
python3 scripts/openclaw_voice_intake.py \
  --input /path/to/user_audio.mp3
```

Voice intake with richer AudioClaw structure:

```bash
python3 scripts/openclaw_voice_intake.py \
  --input /path/to/meeting_clip.m4a \
  --enable-punctuation \
  --timestamp-granularity segment \
  --enable-sentiment \
  --out-json /tmp/openclaw_voice_turn.json
```

Force a specific model:

```bash
python3 scripts/openclaw_voice_intake.py \
  --input /path/to/user_audio.mp3 \
  --model sense-asr-deepthink
```

## AudioClaw integration pattern

Recommended handoff:

1. Channel adapter stores the inbound audio.
2. AudioClaw calls `scripts/openclaw_voice_intake.py`.
3. AudioClaw reads:
   - `openclaw.turn_payload.role`
   - `openclaw.turn_payload.content`
   - `openclaw.turn_payload.metadata`
4. The normal dialogue pipeline continues as if the user typed the recognized text.

Operational rules:
- Keep the original audio path in metadata for debugging.
- Pass `language` only when you are confident; otherwise let ASR auto-detect.
- If you request timestamps, sentiment, or diarization, let the script choose `sense-asr-pro`.
- If transcript is empty, do not hallucinate a user intent. Ask for clarification.

## Resources

- `scripts/senseaudio_asr_client.py`
  - Multipart HTTP client for AudioClaw ASR
  - Handles model routing validation and JSON or text responses
- `scripts/openclaw_voice_intake.py`
  - Main runtime for AudioClaw
  - Builds transcript, normalized user text, and turn payload
- `references/openclaw_voice_intake.md`
  - Official ASR docs summary, model support notes, and AudioClaw payload examples
