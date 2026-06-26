# 🚀 Quick Start Guide - Audio PT Auto-Reply

**From zero to voice-enabled in 3 minutes**

## Step 1: Install the Skill (30 seconds)

```bash
# Extract the skill
cd ~/.openclaw/skills
unzip audio-ptbr-autoreply.zip

# Enter the directory
cd audio-ptbr-autoreply
```

## Step 2: Run the Installer (2 minutes)

```bash
bash install.sh
```

You'll see something like:
```
🎙️  Audio PT Auto-Reply - Smart Installation
==============================================

[1/6] Detecting system...
  Architecture: aarch64
  OS: Linux
✓ ARM64 detected (Raspberry Pi, Apple Silicon)

[2/6] Creating directories...
✓ Directories created

[3/6] Installing Python dependencies...
✓ Python dependencies installed

[4/6] Downloading Piper TTS...
✓ Piper installed successfully

[5/6] Downloading voice models (this may take a while)...
  Downloading pt_BR-jeff-medium.onnx...
  Downloading pt_BR-cadu-medium.onnx...
  ...
✓ Voice models ready

[6/6] Finalizing setup...
✓ Setup complete!

============================================
✅ Installation successful!
============================================
```

**That's it!** Everything is installed and ready.

## Step 3: Restart OpenClaw (30 seconds)

```bash
openclaw gateway restart
```

Or:
```bash
openclaw restart
```

## Step 4: Start Using! 🎤

### First Time Setup
```
/voz listar    # See available voices
/voz jeff      # Choose Jeff voice
```

### Send Audio Message
1. Record a voice message in Portuguese
2. Send it to the bot
3. Get an intelligent audio reply in Portuguese

### Try Different Voices
```
/voz miro      # Switch to feminine voice
/voz cadu      # Switch to different masculine voice
```

### Get Text Responses
Say "**texto**" in your message and it will reply with text instead of audio.

## Optional: Enable Claude Integration (1 minute)

For **smarter AI responses**, set your Claude API key:

```bash
export ANTHROPIC_API_KEY="sk-proj-your-api-key-here"
```

Then restart OpenClaw:
```bash
openclaw gateway restart
```

Now your voice messages will be processed by Claude! 🤖

## Troubleshooting

### "Command not found: openclaw"
- Make sure OpenClaw is installed and in your PATH
- Try full path: `~/.openclaw/bin/openclaw restart`

### "No audio reply"
Run the health check:
```bash
python3 health_check.py
```

### "Piper not found"
The installer didn't complete properly. Try again:
```bash
bash install.sh
```

### "Voice models not downloaded"
This is normal if downloading is slow. The installer will complete the downloads automatically.

## What Gets Installed

| Component | Size | Where |
|-----------|------|-------|
| Piper TTS | ~25MB | `~/.openclaw/workspace/piper` |
| Voice Models | ~240MB | `~/.openclaw/workspace/piper` |
| Python Packages | ~500MB | Your Python environment |
| **Total** | **~765MB** | - |

## Next Steps

- 📖 Read the full README: `cat README.md`
- 🔧 Check installation status: `python3 health_check.py`
- 🎙️ Customize voice settings: `/voz` commands
- 🤖 Set up Claude for smarter responses (optional)

## Tips & Tricks

### Change Default Voice
The first voice you use becomes the default. To reset:
```bash
python3 scripts/voice_config.py set jeff
```

### Batch Voice Selection
Set the environment variable:
```bash
export AUDIO_VOICE="miro"
```

### Manual API Testing
```bash
# Test transcription
python3 scripts/transcribe.py /path/to/audio.wav

# Test voice synthesis
python3 scripts/synthesize.py "Olá, tudo bem?"

# Test Claude integration
ANTHROPIC_API_KEY="sk-..." python3 scripts/claude_adapter.py "Oi, como vai?"
```

---

**You're all set!** 🎉

Send your first voice message and enjoy intelligent Portuguese-language responses! 🎤
