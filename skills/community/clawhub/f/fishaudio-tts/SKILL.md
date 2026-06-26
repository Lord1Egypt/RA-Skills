---
name: fishaudio-tts
description: Text-to-Speech using FishAudio (fish.audio), generates natural human-like voice with great emotional expression.
---

# FishAudio TTS 🔊

High-quality text-to-speech using FishAudio (fish.audio), generates natural human-like voice with excellent emotional expression.

## Features
- More natural and realistic voice than default TTS
- Better emotional expression for news reading
- Supports multiple voices
- Outputs MP3 format directly

## Requirements
- Python 3.8+
- requests library
- FishAudio API key (get from https://fish.audio/)

## Installation
1. Get your API key from https://fish.audio/
2. Add API key to your `TOOLS.md` or environment variable `FISH_AUDIO_API_KEY`
3. `pip install requests` (usually already installed)

## Usage

### Basic Text to Speech
```python
python C:\path\to\skills\fishaudio-tts\fish_tts.py ^
--text "Your text here" ^
--output "output.mp3" ^
--voice "female"
```

### Available Voices
- `female` - Default female voice (good for news)
- `male` - Male voice
- `neutral` - Neutral voice

### Command Line Example
```powershell
python ~/.openclaw/workspace/skills/fishaudio-tts/fish_tts.py ^
--text "各位听众好，这里是2026年3月11日新闻简报。" ^
--output "C:\Users\hyzu\Documents\openclaw\news_audio.mp3" ^
--voice "female"
```

## Notes
- API key is required, get one for free at https://fish.audio/
- Free tier has rate limits, check FishAudio website for details
- For news video generation, female voice is recommended for better listening experience
- All generated audio files are saved locally on your machine
