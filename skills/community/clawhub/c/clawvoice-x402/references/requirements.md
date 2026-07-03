# Requirements

## Current Scope

This package installs and checks TTS (text-to-speech): agent text becomes audio.

Current required runtime:

- Node.js 18+
- Python 3 for local Supertonic install
- Supertonic 3 via `supertonic==1.3.1`

## Whisper / Superwhisper

Do not install Superwhisper or Whisper by default.

- Superwhisper is a dictation/speech-to-text product.
- Whisper is speech-to-text.
- This package is currently text-to-speech.

If the product expands into "agent ears", add an explicit optional STT module. Prefer open local components such as Whisper.cpp or platform-native transcription libraries over installing a proprietary desktop dictation app silently.

Current implementation: STT is opt-in via `mic.enabled: true|false` in `~/.x402-agent-voice/config.json` (a checkbox in `init`). When enabled, `install-mic` asks before creating the local Python speech-to-text runtime, installs faster-whisper (open, local, CTranslate2), predownloads the configured model, and detects FFmpeg — printing an install instruction rather than running a system package manager. `install-mic --yes` is the noninteractive approval path for automation. `listen` (push-to-talk transcription) and `talk` (conversation loop) ship as of 0.3.0; wake word and always-on listening remain `coming_soon`. Recording uses FFmpeg (avfoundation on macOS, pulse/alsa on Linux) at 16kHz mono; transcription runs locally via `scripts/transcribe.py` in the voice venv.

## FFmpeg

FFmpeg is optional for the current package.

Not required:

- generating WAV from Supertonic
- using the hosted ForgeMesh Voice API
- creating the x402 wallet

Useful later:

- converting WAV to MP3/OGG/AAC
- trimming silence
- normalizing volume
- mixing notification tones or background audio
- preparing Discord attachments in a smaller format

If FFmpeg becomes required for a command, detect it first and return a clear install instruction instead of failing mid-run.
