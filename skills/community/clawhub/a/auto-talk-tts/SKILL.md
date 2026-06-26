---
name: auto-talk-tts
description: |
  Auto-speak every message using edge-tts. Automatically converts all responses to speech asynchronously in the background.
  Install the package if needed, then wrap every message with auto-speak.
---

# Auto-Talk-TTS Skill

## Overview

Automatically speaks every message you generate using Microsoft Edge's neural TTS service. Runs asynchronously in the background so your conversation continues immediately while audio generates.

## Quick Start

**Every message you send is automatically spoken aloud.**

The skill wraps your output with `auto-speak` which:
1. Installs `node-edge-tts` if needed
2. Converts your message to speech asynchronously
3. Plays the audio in the background
4. Continues your conversation immediately

## Usage

**Automatic:** Every message is auto-spoken. No action needed from you.

**Manual override:** If you need to speak something specific:
```bash
auto-speak "Your text here"
```

## How It Works

1. **Detect output:** When you generate a message
2. **Wrap with auto-speak:** The message gets passed through the auto-speak wrapper
3. **Install if needed:** First run installs `node-edge-tts` package
4. **Generate audio:** Convert text to MP3 in background
5. **Play audio:** Use `afplay` to play the audio file
6. **Continue:** Your conversation flows without waiting for audio

## Configuration

Edit `config.json` to customize:

```json
{
  "voice": "en-US-MichelleNeural",
  "rate": "default",
  "pitch": "default",
  "volume": "default",
  "summaryLength": 100
}
```

**Options:**
- `voice`: Any Edge neural voice (see edge-tts skill for full list)
- `rate`: Speech speed (`-20%` to `+50%`, or `default`)
- `pitch`: Voice pitch (`-20Hz` to `+20Hz`, or `default`)
- `volume`: Audio volume (`-100%` to `+100%`, or `default`)
- `summaryLength`: How many characters to summarize (default: 100)

## Installation

First run will automatically install `node-edge-tts`:

```bash
npm install -g node-edge-tts
```

Or use the bundled installer:
```bash
cd /Users/stefano/.openclaw/workspace/skills/auto-talk-tts
npm install
```

## Files

### auto-speak
Wrapper script that:
- Checks if node-edge-tts is installed
- Installs it if needed
- Converts text to speech asynchronously
- Plays audio with afplay
- Continues immediately

### config.json
User configuration for voice, rate, pitch, volume settings.

### package.json
NPM package with node-edge-tts dependency.

### SKILL.md
This file.

## Integration with SOUL.md

**Add this line to the top of your SOUL.md:**

```markdown
## MUST SPEAK WITH TTS EVERY TIME (ASYNCHRONOUSLY)

**I must use the edge-tts skill to convert my response to speech before sending it to you.** Every single message I send must be spoken aloud using the tts tool. This is non-negotiable - I speak to you, I don't just type.

**Async approach:** I run the TTS command in the background using `&` or `nohup` so the conversation continues immediately while audio generates in the background.
```

## Workflow

### Automatic (Recommended)

1. **You generate a message**
2. **auto-speak wraps it:** The message gets passed through the wrapper
3. **Background TTS:** Audio generates in background process
4. **Immediate reply:** Your conversation continues without waiting
5. **Audio plays:** User hears your response

### Manual (If needed)

```bash
# Auto-speak any text
auto-speak "Your message here"

# Custom voice
auto-speak "Your message" --voice en-GB-RyanNeural

# Custom speed
auto-speak "Your message" --rate +20%
```

## Testing

```bash
# Test the auto-speak wrapper
auto-speak "This is a test. If you can hear this, it's working!"

# Check if node-edge-tts is installed
npm list -g node-edge-tts

# Install manually if needed
npm install -g node-edge-tts
```

## Troubleshooting

- **No audio?** Check that node-edge-tts is installed: `npm list -g node-edge-tts`
- **Install needed?** First run will auto-install, or run: `npm install -g node-edge-tts`
- **Audio not playing?** Check system volume and audio output settings
- **Slow?** Use async mode - audio generates in background, conversation continues immediately

## Notes

- **Non-blocking:** Conversation flows while audio generates
- **No API key:** Uses Microsoft Edge's free TTS service
- **Neural voices:** High-quality, natural-sounding speech
- **Multiple voices:** See edge-tts skill for full voice list
- **Configurable:** Customize voice, speed, pitch, volume in config.json
- **Automatic installation:** First run installs node-edge-tts if missing

## See Also

- [edge-tts](../edge-tts/SKILL.md) - Core TTS engine
- [speak-summary](../speak-summary/SKILL.md) - Alternative auto-speak implementation
