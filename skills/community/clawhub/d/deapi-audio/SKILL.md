---
name: deapi-audio
description: Text-to-speech, voice cloning, voice design, and transcribe audio files via deAPI GPU network. Trigger on 'text to speech', 'TTS', 'generate voice', 'read aloud', 'voice clone', 'clone voice', 'voice design', 'design voice', 'custom voice', 'transcribe audio', 'STT'. For video/YouTube transcription use deapi-video instead.
version: 1.0.0
allowed-tools: Bash(bash ${CLAUDE_SKILL_DIR}/scripts/*), Read(${CLAUDE_SKILL_DIR}/**), Write(${CLAUDE_SKILL_DIR}/config.json)
metadata:
  author: deapi
  openclaw:
    requires:
      env:
        - DEAPI_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: DEAPI_API_KEY
    homepage: https://deapi.ai
---

# deAPI Audio

Text-to-speech, voice cloning, voice design, and audio transcription via deAPI decentralized GPU network.

## Scripts

| Script | Use when... |
|--------|-------------|
| `scripts/text-to-speech.sh` | User wants to convert text to spoken audio |
| `scripts/voice-clone.sh` | User wants to clone/replicate a voice from a sample audio file |
| `scripts/voice-design.sh` | User wants to generate speech with a voice described in natural language |
| `scripts/speech-to-text.sh` | User wants to transcribe an audio file (AAC, MP3, OGG, WAV, WebM, FLAC, max 10MB) |

## Your config
! cat ${CLAUDE_SKILL_DIR}/config.json 2>/dev/null || echo "NOT_CONFIGURED"

If the config above is NOT_CONFIGURED, ask the user:
- What is your deAPI API key? (get one at https://deapi.ai, free $5 credit)

Then write the answer to ${CLAUDE_SKILL_DIR}/config.json as `{ "api_key": "their_key" }`.

Alternatively, the user can set the `DEAPI_API_KEY` environment variable directly, which takes priority over config.json.

## Gotchas

- For YouTube/video transcription, use the `deapi-video` skill instead. This skill handles audio-only files (.mp3, .wav, .m4a, .flac, .ogg).
- Three TTS models: `Kokoro` (default), `Chatterbox`, `Qwen3`. Use `--model Chatterbox` or `--model Qwen3` to switch.
- Kokoro: Voice ID format is `{lang}{gender}_{name}`. Language is auto-detected from voice prefix if `--lang` is omitted.
- Chatterbox: voice is always `default`, speed is fixed at `1`, supports 22 languages. Text limit 10-2000 chars.
- Kokoro: text limit 3-10001 chars. Long text may timeout — split into segments and generate separately.
- TTS output format defaults to mp3. WAV files are much larger but lossless.
- Kokoro: `speed` range is 0.5-2.0. Values outside this range cause errors.
- Qwen3 Voice Clone (`voice-clone.sh`): ref audio must be 5-15 seconds. Too short or too long degrades quality. Formats: MP3, WAV, FLAC, OGG, M4A. URLs are downloaded automatically.
- Qwen3 Voice Design (`voice-design.sh`): quality depends on the `--instruct` description. Encourage specific details: gender, age, accent, speaking style, emotion.
- Qwen3 models use full language names (`English`, `French`, etc.) NOT language codes. 10 supported languages: English, Italian, Spanish, Portuguese, Russian, French, German, Korean, Japanese, Chinese.
- Qwen3 TTS (`--model Qwen3`): 9 voices available, default `Vivian`. Chinese language lacks `Ryan` voice.
- Qwen3 text limit is 10-5000 chars. Speed is fixed at 1. Voice Clone and Voice Design use voice=`default`.
- Audio transcription accepts a local file path or URL (`--audio`). Formats: AAC, MP3, OGG, WAV, WebM, FLAC. Max 10 MB.
- Result URLs expire in 24 hours. Download promptly.

## Quick examples

```bash
# Basic TTS
bash scripts/text-to-speech.sh --text "Hello world"

# British voice
bash scripts/text-to-speech.sh --text "Good morning" --voice bf_emma

# Chatterbox model (multilingual)
bash scripts/text-to-speech.sh --model Chatterbox --text "Bonjour le monde" --lang fr

# Qwen3 model
bash scripts/text-to-speech.sh --model Qwen3 --text "Hello world" --voice Serena --lang English

# Clone a voice from a sample
bash scripts/voice-clone.sh --text "Hello, this is my cloned voice" --ref-audio /path/to/sample.mp3

# Clone with reference transcript for better accuracy
bash scripts/voice-clone.sh --text "Welcome to the show" --ref-audio /path/to/sample.wav --ref-text "This is the original transcript"

# Design a custom voice from description
bash scripts/voice-design.sh --text "Good morning everyone" --instruct "A warm, deep male voice with a slight British accent"

# Voice design in another language
bash scripts/voice-design.sh --text "Bonjour tout le monde" --instruct "A cheerful young female voice" --lang French

# Transcribe audio file (local or URL)
bash scripts/speech-to-text.sh --audio /path/to/recording.mp3
bash scripts/speech-to-text.sh --audio "https://example.com/podcast.mp3"
```

For the full voice list and language codes, see [references/voices.md](references/voices.md).
