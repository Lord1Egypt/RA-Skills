---
name: crazyrouter-tts
description: Text-to-speech via Crazyrouter API. OpenAI TTS voices (alloy, echo, fable, onyx, nova, shimmer). Convert text to natural speech audio files. Use when user asks to read aloud, generate audio, or convert text to speech. Requires environment variable CRAZYROUTER_API_KEY (get at https://crazyrouter.com).
---

# Text-to-Speech via Crazyrouter

Generate natural speech from text using [Crazyrouter](https://crazyrouter.com) — OpenAI-compatible TTS API.

## Voices

| Voice | Style |
|-------|-------|
| `alloy` | Neutral, balanced |
| `echo` | Warm, conversational |
| `fable` | Expressive, storytelling |
| `onyx` | Deep, authoritative |
| `nova` | Friendly, upbeat |
| `shimmer` | Soft, gentle |

## Script Directory

**Agent Execution**:
1. `SKILL_DIR` = this SKILL.md file's directory
2. Script path = `${SKILL_DIR}/scripts/main.mjs`

## Step 0: Check API Key ⛔ BLOCKING

```bash
[ -n "${CRAZYROUTER_API_KEY}" ] && echo "key_present" || echo "not_set"
```

| Result | Action |
|--------|--------|
| `key_present` | Continue |
| `not_set` | Ask user to set `CRAZYROUTER_API_KEY`. Get key at https://crazyrouter.com |

## Usage

```bash
# Basic TTS
node ${SKILL_DIR}/scripts/main.mjs --text "Hello world" --output hello.mp3

# Choose voice
node ${SKILL_DIR}/scripts/main.mjs --text "Welcome to Crazyrouter" --output welcome.mp3 --voice nova

# HD quality
node ${SKILL_DIR}/scripts/main.mjs --text "Premium audio" --output hd.mp3 --model tts-1-hd

# Read from file
node ${SKILL_DIR}/scripts/main.mjs --input article.txt --output article.mp3

# Adjust speed
node ${SKILL_DIR}/scripts/main.mjs --text "Slow and clear" --output slow.mp3 --speed 0.8
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--text <text>` | Text to speak | — |
| `--input <file>` | Read text from file | — |
| `--output <path>` | Output audio file (required) | — |
| `--voice <name>` | Voice selection | `alloy` |
| `--model <id>` | `tts-1` or `tts-1-hd` | `tts-1` |
| `--speed <num>` | Speed (0.25-4.0) | `1.0` |
| `--format <fmt>` | `mp3`, `opus`, `aac`, `flac` | `mp3` |
