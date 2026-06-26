---
name: edge-tts-voice-system
description: Local voice system for OpenClaw using faster-whisper for inbound transcription and Edge TTS for outbound replies. Use when you need private voice workflows, offline transcription, cached reply audio, or voice message handling after OpenClaw updates.
---

# Edge TTS Voice System

A complete, privacy-focused voice system for OpenClaw that works entirely offline. No internet required, no data leaves your machine.

## Features

- **Outbound replies**: Edge TTS with cached audio output
- **Accurate STT**: faster-whisper base model for speech recognition
- **Fully offline**: No internet connection required
- **Privacy-focused**: All processing happens locally
- **Easy integration**: Ready-to-use Python and bash scripts
- **Voice conversations**: Natural back-and-forth voice interactions

## Quick Start

### Installation

```bash
# Install the skill
clawhub install lessac_offline_voice_system

# Or manually from this directory
./scripts/install.sh
```

### Basic Usage

```python
from scripts.voice_handler import VoiceHandler

handler = VoiceHandler()

# Transcribe audio to text
text = handler.audio_to_text("voice_message.ogg")
print(f"You said: {text}")

# Generate voice response
audio_file = handler.text_to_audio("Hello, this is a voice response.")
```

### Command Line

```bash
# Transcribe audio
./scripts/voice_integration.sh transcribe voice_message.ogg

# Generate TTS
./scripts/voice_integration.sh tts "Hello world" output.wav

# Full voice processing
./scripts/voice_integration.sh process voice_message.ogg
```

## Components

### 1. Text-to-Speech (TTS)
- **Voice**: Edge-supported voice (default `en-IE-ConnorNeural`)
- **Library**: Edge TTS (`edge-tts`)
- **Quality**: Natural speech with cached output
- **Sample rate**: provider-defined

### 2. Speech-to-Text (STT)
- **Model**: faster-whisper base
- **Accuracy**: High, comparable to cloud services
- **Languages**: Multi-language support (auto-detected)
- **Speed**: ~2 seconds for typical audio

### 3. Audio Processing
- **Formats**: OGG/Opus, WAV, MP3 (via ffmpeg)
- **Conversion**: Automatic format handling
- **Quality**: 16kHz mono for optimal recognition

## Performance

- **TTS Load time**: ~2 seconds (one-time)
- **TTS Generation**: ~3-4 seconds
- **STT Transcription**: ~2 seconds
- **Total response time**: 5-7 seconds

## Integration with OpenClaw

### Automatic Voice Processing

When installed, the skill can be configured to automatically:
1. Detect incoming voice messages
2. Transcribe them silently
3. Generate AI responses
4. Convert responses to voice
5. Send voice replies back

### OpenClaw reply TTS configuration

The built-in OpenClaw reply TTS path is **not** the local voice pipeline used by this skill.
This skill now uses a local **Edge TTS** reply path instead, with cached output
stored under `/root/.openclaw/tts/cache`.

Default outbound voice:
- `en-IE-ConnorNeural`

Relevant files:
- `tts_edge_wrapper.py`
- `voice_handler.py`
- `voice_integration.sh`
- `scripts/install.sh`

If you need to change the voice, set:

```bash
export OPENCLAW_EDGE_TTS_VOICE="en-IE-ConnorNeural"
```

or replace it with another Edge-supported voice.

### Reinstall after OpenClaw updates

After an OpenClaw system update, rerun the installer to restore the voice stack:

```bash
cd /root/.openclaw/workspace/skills/lessac_offline_voice_system
./scripts/install.sh
```

This refreshes:
- the Python venv dependencies (`faster-whisper`, `edge-tts`, `soundfile`)
- the runtime cache directory
- the local voice wrappers
- the config file under `/root/.openclaw/tts/config.json`

### Manual Integration

```python
# In your OpenClaw agent or custom script
import sys
sys.path.append("/path/to/skill/scripts")
from voice_handler import VoiceHandler

class YourAgent:
    def __init__(self):
        self.voice = VoiceHandler()
    
    def handle_voice_message(self, audio_file):
        # Transcribe
        text = self.voice.audio_to_text(audio_file)
        
        # Generate response (your AI logic here)
        response = self.generate_response(text)
        
        # Convert to voice
        voice_response = self.voice.text_to_audio(response)
        
        return voice_response
```

## Configuration

### Voice Model Selection

The skill uses Edge TTS by default. To use a different voice:

1. Set `OPENCLAW_EDGE_TTS_VOICE` to a supported Edge voice
2. Re-run the installer to refresh the cache and wrappers

### STT Model Selection

Change the faster-whisper model size in `scripts/voice_handler.py`:
- `"tiny"`: Fastest, lower accuracy
- `"base"`: Default, good balance
- `"small"`: Higher accuracy, slower
- `"medium"`: Best accuracy, slowest

## Troubleshooting

### Common Issues

1. **"No module named 'piper'"**
   ```bash
   pip install piper-tts
   ```

2. **"ffmpeg not found"**
   ```bash
   sudo apt-get install ffmpeg
   ```

3. **Out of memory with large models**
   - Use `"tiny"` or `"base"` STT model
   - Use a different Edge voice if needed

4. **Slow TTS generation**
   - First generation loads model (~2s)
   - Subsequent generations are faster (~0.3s per sentence)

### Debug Mode

Enable debug output:
```bash
export VOICE_DEBUG=1
./scripts/voice_integration.sh process audio.ogg
```

## Files

- `scripts/install.sh` - Installation script
- `scripts/voice_handler.py` - Main Python handler
- `scripts/piper_tts.py` - Edge TTS wrapper
- `scripts/voice_integration.sh` - Bash interface
- `references/voice_models.md` - Voice model information
- `assets/` - Voice model files (downloaded during install)

## Dependencies

- Python 3.8+
- ffmpeg
- Python packages (installed automatically):
  - faster-whisper
  - piper-tts
  - soundfile

## License

Open source. See included LICENSE file.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the references/ directory
3. Open an issue on the skill repository