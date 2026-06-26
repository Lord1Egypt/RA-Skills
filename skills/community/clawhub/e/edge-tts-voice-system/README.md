# Edge TTS Voice System

A complete, privacy-focused voice system for OpenClaw that works entirely offline.

## Quick Start

```bash
# Install the skill
./scripts/install.sh

# Test the installation
./scripts/test_skill.py

# Use the voice system
./scripts/voice_integration.sh tts "Hello world" output.wav
```

## What's Included

### Core Components
1. **Text-to-Speech**: Edge TTS with cached outbound replies
2. **Speech-to-Text**: faster-whisper base model
3. **Audio Processing**: ffmpeg integration for format conversion
4. **Integration Scripts**: Python and bash interfaces

### Key Features
- ✅ **Fully offline** - No internet required
- ✅ **Privacy-focused** - All processing happens locally
- ✅ **Configurable voice** - default `en-IE-ConnorNeural`
- ✅ **Easy to use** - Simple Python and command-line interfaces
- ✅ **OpenClaw ready** - Designed for seamless integration

## File Structure

```
edge_tts_voice_system/
├── SKILL.md              # Main skill documentation
├── README.md             # This file
├── scripts/
│   ├── install.sh        # Installation script
│   ├── voice_handler.py  # Main Python handler
│   ├── tts_edge_wrapper.py # Edge TTS wrapper
│   ├── voice_integration.sh # Bash interface
│   └── test_skill.py     # Installation test
├── references/
│   └── voice_models.md   # Voice model information
└── assets/               # Voice model files (downloaded during install)
```

## Installation Options

### 1. Quick Install (Recommended)
```bash
./scripts/install.sh
```

### 2. Custom Install Location
```bash
./scripts/install.sh --install-dir /path/to/custom/location
```

### 3. Manual Installation
```bash
# Install dependencies
sudo apt-get install ffmpeg python3-pip

# Create virtual environment
python3 -m venv ~/.openclaw/tts/venv
source ~/.openclaw/tts/venv/bin/activate

# Install Python packages
pip install faster-whisper edge-tts soundfile

# Download voice model
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/high/en_US-lessac-high.onnx -O ~/.openclaw/tts/piper_voice.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/high/en_US-lessac-high.onnx.json -O ~/.openclaw/tts/piper_voice.json

# Copy scripts
cp scripts/*.py scripts/*.sh ~/.openclaw/tts/
chmod +x ~/.openclaw/tts/voice_integration.sh
```

## Usage Examples

### Command Line
```bash
# Transcribe audio to text
./scripts/voice_integration.sh transcribe audio.ogg

# Generate TTS from text
./scripts/voice_integration.sh tts "Hello world" output.wav

# Full voice message processing
./scripts/voice_integration.sh process voice_message.ogg

# Test the system
./scripts/voice_integration.sh test
```

### Python
```python
from voice_handler import VoiceHandler

# Create handler
handler = VoiceHandler()

# Transcribe audio
text = handler.audio_to_text("voice_message.ogg")
print(f"You said: {text}")

# Generate voice response
audio_file = handler.text_to_audio("This is a voice response.")
```

### OpenClaw Integration
```python
import sys
sys.path.append("/path/to/tts")
from voice_handler import VoiceHandler

class YourAgent:
    def __init__(self):
        self.voice = VoiceHandler()
    
    def handle_voice_message(self, audio_file):
        # Transcribe
        text = self.voice.audio_to_text(audio_file)
        
        # Generate AI response
        response = self.generate_response(text)
        
        # Convert to voice
        voice_response = self.voice.text_to_audio(response)
        
        return voice_response
```

## Performance

- **TTS Load time**: ~2 seconds (one-time)
- **TTS Generation**: ~3-4 seconds per response
- **STT Transcription**: ~2 seconds for typical audio
- **Total response time**: 5-7 seconds end-to-end

## System Requirements

- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 500MB for models and dependencies
- **CPU**: Modern x86-64 or ARM
- **OS**: Linux (tested on Ubuntu/Debian)

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   ```bash
   # Reinstall Python packages
   pip install faster-whisper edge-tts soundfile
   ```

2. **"ffmpeg not found"**
   ```bash
   sudo apt-get install ffmpeg
   ```

3. **Out of memory**
   - Use smaller models (tiny/base instead of small/medium)
   - Close other applications
   - Consider medium quality TTS instead of high

4. **Slow performance**
   - First TTS generation loads model (~2s)
   - Subsequent generations are faster
   - Use tiny STT model for faster responses

### Debug Mode
```bash
export VOICE_DEBUG=1
./scripts/voice_integration.sh process audio.ogg
```

## Customization

### Changing the Voice
1. Choose a supported Edge TTS voice such as `en-IE-ConnorNeural`
2. Replace `piper_voice.onnx` and `piper_voice.json`
3. Update paths if needed

### Changing STT Model
Edit `voice_handler.py`:
```python
self.stt_model = "base"  # Change to "tiny", "small", or "medium"
```

## License

Open source. See included LICENSE file.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review `references/voice_models.md`
3. Run `./scripts/test_skill.py` for diagnostics
4. Open an issue on the skill repository