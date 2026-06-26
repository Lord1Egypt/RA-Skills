---
name: text-to-speech
description: Convert text to speech audio files. Use when user needs to create audio from text, generate voiceovers, create podcasts, or convert articles to audio.
---

# Text to Speech

Convert text to speech audio files.

## Quick Start

```bash
# Convert text to speech
python scripts/tts.py "Hello world" --output hello.mp3
```

## Usage

```bash
python scripts/tts.py TEXT [OPTIONS]

Options:
  --output PATH      Output audio file
  --voice VOICE      Voice name (male, female, neutral)
  --speed RATE       Speaking speed (0.5-2.0)
  --lang LANG       Language code (en, zh, ja, etc.)
  --list-voices     List available voices
```

## Examples

```bash
# Basic conversion
python scripts/tts.py "Hello world" --output hello.mp3

# Chinese text
python scripts/tts.py "你好世界" --lang zh-CN --output chinese.mp3

# Different speed
python scripts/tts.py "Hello" --speed 1.5 --output fast.mp3
python scripts/tts.py "Hello" --speed 0.8 --output slow.mp3

# List voices
python scripts/tts.py --list-voices
```

## Features

- Multiple language support
- Adjustable speaking speed
- Voice selection
- Audio format output
- SSML support
