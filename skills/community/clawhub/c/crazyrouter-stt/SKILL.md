---
name: crazyrouter-stt
description: Speech-to-text transcription via Crazyrouter API (OpenAI Whisper). Transcribe audio/video files to text. Supports mp3, mp4, wav, m4a, webm. Use when user asks to transcribe audio, extract text from video, or convert speech to text. Requires environment variable CRAZYROUTER_API_KEY (get at https://crazyrouter.com).
---

# Speech-to-Text via Crazyrouter

Transcribe audio files using OpenAI Whisper through [Crazyrouter](https://crazyrouter.com).

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
# Transcribe audio
node ${SKILL_DIR}/scripts/main.mjs --input audio.mp3

# Save to file
node ${SKILL_DIR}/scripts/main.mjs --input meeting.m4a --output transcript.txt

# Specify language hint
node ${SKILL_DIR}/scripts/main.mjs --input chinese.mp3 --language zh

# Translate to English
node ${SKILL_DIR}/scripts/main.mjs --input french.mp3 --translate
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--input <file>` | Audio file (required) | — |
| `--output <file>` | Save transcript to file | stdout |
| `--language <code>` | Language hint (ISO 639-1) | auto-detect |
| `--translate` | Translate to English | false |
| `--model <id>` | `whisper-1` | `whisper-1` |

### Supported Formats

mp3, mp4, mpeg, mpga, m4a, wav, webm
