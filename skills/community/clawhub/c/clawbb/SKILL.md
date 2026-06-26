---
name: clawbb
description: "ClawBB — Free macOS voice-to-text built for Vibe Coding. Hold Globe key, speak, text appears at your cursor. Powered by Google Gemini LLM. Apple Notarized."
version: 1.1.5
metadata:
  openclaw:
    requires:
      env:
        - GEMINI_API_KEY
      config:
        - ~/Tools/xiabb/.api-key
    primaryEnv: GEMINI_API_KEY
---

# ClawBB (虾BB)

**Hold Globe key. Speak. Text appears.** Free voice-to-text built for Vibe Coding.

- 🆓 **Free forever** — Google Gemini free tier, 250 transcriptions/day
- 🌏 **Bilingual** — Mixed Chinese + English, perfect punctuation for AI prompts
- 🔴 **Live streaming preview** — See text appear as you speak (Gemini Live API)
- ⚡ **341KB pure Swift** — Zero dependencies, macOS native
- 🧠 **LLM engine** — Not Whisper ASR. Gemini understands meaning, not just sound.
- 📖 **Open source** — MIT License, Apple Notarized

## Install

Download the Apple Notarized DMG (app release v1.1.3): from GitHub Releases:

```bash
curl -L -o /tmp/XiaBB.dmg "https://github.com/dyz2102/xiabb/releases/download/v1.1.3/XiaBB-v1.1.3-macOS-arm64.dmg"
```

**Verify checksum before opening:**

```bash
echo "ce53a5b0ccc3b0993b284686ab05716f3e616969f98395d1baf8aec083f8d784  /tmp/XiaBB.dmg" | shasum -a 256 -c
```

Then open the DMG and drag XiaBB.app to Applications:

```bash
open /tmp/XiaBB.dmg
```

The app is signed with Developer ID and Apple Notarized — no Gatekeeper warnings.

### Build from source (optional)

If you prefer to inspect and compile yourself:

```bash
git clone https://github.com/dyz2102/xiabb.git /tmp/xiabb-build
cd /tmp/xiabb-build
# Review install.sh and native/main.swift before running
cat install.sh
bash install.sh
```

Requires Xcode Command Line Tools (`xcode-select --install`).

## Setup

### Gemini API Key

Get a free key at https://aistudio.google.com/apikey, then configure:

```bash
# Recommended: environment variable
export GEMINI_API_KEY="your-key-here"
```

Or configure via the app's menu bar → "Configure Gemini API Key...".

The key is stored locally at `~/Tools/xiabb/.api-key` (chmod 600 recommended).

### Permissions

On first launch, macOS will prompt for:
- **Accessibility**: Required for Globe key detection (CGEventTap)
- **Microphone**: Required for voice recording

Both are standard macOS permissions for a voice input app. Grant them in System Settings → Privacy & Security.

## Usage

| Action | Result |
|--------|--------|
| Hold 🌐 Globe key | Start recording, HUD shows live preview |
| Release 🌐 Globe key | Transcription pastes at cursor |
| Click HUD 📋 | Copy last result |

## Security & Privacy

- **Open source**: Full source at https://github.com/dyz2102/xiabb — review before use
- **Apple Notarized**: Signed with Developer ID, verified by Apple
- **No account required**: No signup, no tracking, no telemetry
- **Audio processing**: Audio is sent to Google Gemini API for transcription. Review Google's privacy policy if this concerns you.
- **Local storage only**: API key and config stored locally, never transmitted except to Gemini API

## Links

- 🌐 Website: https://xiabb.lol
- 📦 GitHub: https://github.com/dyz2102/xiabb
- 📄 MIT License
