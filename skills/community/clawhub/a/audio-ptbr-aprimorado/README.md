# 🎙️ Audio PT Auto-Reply - Premium Voice Interface

**Brazilian Portuguese voice transcription + AI responses with Claude integration**

> Just install the skill once. Everything else is automatic.

## ✨ What's New

- ✅ **Zero-touch installation** - No manual downloads needed
- ✅ **Claude integration** - Intelligent AI responses (optional)
- ✅ **Auto-detection** - Works on ARM64, x86_64, Mac, Linux
- ✅ **Health check** - Validates everything is working
- ✅ **Production-ready** - Error handling, fallbacks, logging

## 🚀 Quick Start (Really Quick!)

### Step 1: Install the Skill
```bash
# Download from ClaWHub or your repository
cd ~/.openclaw/skills
unzip audio-ptbr-autoreply.zip
cd audio-ptbr-autoreply
```

### Step 2: Run the Installer (One Command!)
```bash
bash install.sh
```

That's it! The script will:
- ✓ Detect your system (ARM64, x86_64, etc.)
- ✓ Download Piper TTS automatically
- ✓ Download 4 Brazilian Portuguese voice models
- ✓ Install Python dependencies
- ✓ Validate everything works

### Step 3: Restart OpenClaw
```bash
openclaw gateway restart
```

### Step 4: Verify Installation (Optional)
```bash
python3 health_check.py
```

## 🎤 How to Use

### Voice Commands
```
/voz jeff          👨 Use Jeff (masculine, clear)
/voz cadu          👨 Use Cadu (masculine, warm)
/voz faber         👨 Use Faber (masculine, balanced)
/voz miro          👩 Use Miro (feminine, high quality)
/voz feminina      👩 Auto-select feminine voice
/voz masculina     👨 Auto-select masculine voice
/voz listar        📋 List all voices
```

### Usage Modes
| Action | What Happens |
|--------|--------------|
| Send audio message | Transcribes → Gets intelligent response → Sends audio reply |
| Say "texto" | Response comes as text instead of audio |
| Send text message | Works as normal (no audio processing) |

## 🤖 Claude Integration (Optional)

For **intelligent, natural responses**, set your Claude API key:

```bash
export ANTHROPIC_API_KEY="sk-your-api-key-here"
```

Without the API key, the skill still works using OpenClaw's agent for responses.

### What's Different with Claude?
- 🧠 More natural, context-aware responses
- ⚡ Faster response times
- 🎯 Better understanding of Portuguese slang & expressions
- 🔒 Responses stay private (processed locally or via Anthropic)

### Cost
- Free tier available (check Anthropic pricing)
- Each voice message = 1 API call

## 📋 What Gets Installed

```
~/.openclaw/workspace/
├── piper/                        # TTS Engine
│   ├── piper/piper              # Binary (auto-downloaded)
│   ├── pt_BR-jeff-medium.onnx   # Voice models (auto-downloaded)
│   ├── pt_BR-cadu-medium.onnx
│   ├── pt_BR-faber-medium.onnx
│   └── pt_BR-miro-high.onnx
└── .audio_pt_voice_config       # Your voice preference
```

**Total size:** ~240MB (voice models)

## 🛠️ Troubleshooting

### Audio reply doesn't work
```bash
# Check health
python3 health_check.py

# Test transcription
python3 scripts/transcribe.py /path/to/audio.wav

# Test synthesis
python3 scripts/synthesize.py "Teste"
```

### Piper not found
```bash
# Reinstall Piper
rm -rf ~/.openclaw/workspace/piper
bash install.sh
```

### Claude API issues
```bash
# Check your API key
echo $ANTHROPIC_API_KEY

# Or use OpenClaw agent only
export ANTHROPIC_API_KEY=""  # Unset to use OpenClaw
```

### Wrong voice being used
```bash
# Check current voice
python3 scripts/voice_config.py get

# Reset to default
python3 scripts/voice_config.py set jeff
```

## 📊 Technical Details

### Speech Recognition (ASR)
- **Model:** wav2vec2-large-xlsr-53-portuguese
- **License:** Apache 2.0 (Free)
- **Best at:** Brazilian Portuguese slang, informal speech
- **Also supports:** English
- **Provider:** jonatasgrosman (HuggingFace)

### Text-to-Speech (TTS)
- **Engine:** Piper (by Rhasspy)
- **Speed:** Real-time on ARM64 & x86_64
- **Voices:** 3 masculine + 1 feminine (community)
- **Quality:** Neural (not robotic)
- **Format:** Opus OGG (Telegram optimized)
- **License:** MIT (Free)

### AI Response Generation
- **Default:** OpenClaw Agent (included with your setup)
- **Optional:** Claude API (requires ANTHROPIC_API_KEY)
- **Both:** Fully compatible, easy to switch

## 📦 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8+ | 3.10+ |
| RAM | 2GB | 4GB+ |
| Storage | 300MB | 500MB |
| Internet | Required (download only) | Required (download only) |

**Supported OSes:**
- ✅ Linux (Ubuntu, Debian, Raspberry Pi OS, etc.)
- ✅ macOS (Intel & Apple Silicon)
- ✅ Windows (via WSL2)

## 🔄 Update & Uninstall

### Update to latest
```bash
cd ~/.openclaw/skills/audio-ptbr-autoreply
bash install.sh  # Re-runs, only installs missing pieces
```

### Uninstall completely
```bash
rm -rf ~/.openclaw/skills/audio-ptbr-autoreply
rm -rf ~/.openclaw/workspace/piper
rm ~/.openclaw/workspace/.audio_pt_voice_config
```

## 📝 File Structure

```
audio-ptbr-autoreply/
├── install.sh                  # ⭐ Run this once!
├── health_check.py             # Validate installation
├── scripts/
│   ├── transcribe.py           # ASR (audio → text)
│   ├── synthesize.py           # TTS (text → audio)
│   ├── voice_config.py         # Voice management
│   ├── claude_adapter.py        # Claude integration
│   └── process.sh              # Full workflow
├── SKILL.md                    # Skill manifest
└── README.md                   # This file
```

## 🙏 Credits

**Built with open source:**
- [wav2vec2-pt-br](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-portuguese) by jonatasgrosman
- [Piper TTS](https://github.com/rhasspy/piper) by Rhasspy
- [Claude API](https://www.anthropic.com/claude) by Anthropic (optional)

**Voices:**
- Jeff, Cadu, Faber: Piper Voices repository
- Miro: Community contribution by TarcisoAmorim

## 📞 Support

- **Issue with installation?** Run `python3 health_check.py`
- **Feature request?** Check the [repository](https://github.com)
- **Found a bug?** Report it with `health_check.py` output

## 📄 License

MIT - Free to use, modify, and redistribute. No attribution required.

---

**Ready to go?**
```bash
bash install.sh
openclaw gateway restart
/voz jeff  # Set a voice
# Send your first audio message! 🎤
```
