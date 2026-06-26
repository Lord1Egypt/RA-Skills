---
name: audio-ptbr-autoreply
version: 2.0.1
description: |
  Premium Portuguese-Brazilian voice interface with neural TTS and Claude AI integration. 
  Features wav2vec2-large-xlsr-53-ptBR for excellent PT-BR understanding (slang, expressions, accents) + 
  optional Claude API for intelligent responses. Multiple neural voices (3 masculine, 1 feminine). 
  Silent audio-in/audio-out by default with one-command installation.

category: voice
tags:
  - voice
  - audio
  - speech-to-text
  - text-to-speech
  - portuguese
  - accessibility
hooks:
  - event: "message.audio.receive"
    action: "bash process.sh \"{{MediaPath}}\" \"{{Target}}\" \"{{MessageID}}\""
triggers:
  - command: "/voz"
    description: "Configurar voz ou processar áudio manualmente"
    action: "bash process.sh \"{{args}}\""
config:
  tools:
    media:
      audio:
        scope:
          default: "allow"
---

# Audio PT Auto-Reply v2.0.1 - Premium Voice Interface

**Complete voice interface with superior Brazilian Portuguese understanding and automatic setup.**

## 🌟 Key Features

### Superior PT-BR Understanding
- **Model:** wav2vec2-large-xlsr-53-portuguese (jonatasgrosman)
- **Excellence in:** Brazilian Portuguese with slang, expressions, accents
- **Also supports:** English (multilingual)
- **Quality:** State-of-the-art for PT-BR ASR

### 🤖 Optional Claude Integration
- **Intelligent responses** using Claude API
- **Falls back** to OpenClaw agent automatically
- **Optional:** No API key required, still works with OpenClaw agent
- **Smart:** Better understanding of context and Portuguese nuances

### Neural Voice Options (Piper TTS)

| Voice | Gender | Quality | Character |
|-------|--------|---------|-----------|
| **jeff** | Masculina | Medium | Clear, professional |
| **cadu** | Masculina | Medium | Warm, natural |
| **faber** | Masculina | Medium | Balanced |
| **miro** | Feminina | High | Community voice |

### Voice Commands

Change voice anytime with:
- `/voz jeff` - Voice: Jeff
- `/voz cadu` - Voice: Cadu  
- `/voz faber` - Voice: Faber
- `/voz miro` - Voice: Miro (feminina)
- `/voz feminina` - Automatic: miro
- `/voz masculina` - Automatic: jeff
- `/voz listar` - Show all voices

## ⚡ Installation (NEW!)

### One-Command Installation
```bash
bash install.sh
```

The installer automatically:
- ✅ Detects your system architecture (ARM64, x86_64)
- ✅ Downloads Piper TTS
- ✅ Downloads 4 Brazilian Portuguese voice models (~240MB)
- ✅ Installs Python dependencies
- ✅ Validates everything works

**No manual downloads. No configuration. Just one command!**

## 🔄 Critical Rules

**DEFAULT: AUDIO ONLY - NO TEXT**

When user sends audio:
- ❌ NO transcription shown
- ❌ NO "Pesquisando...", "Gerando..."
- ❌ NO confirmations or explanations
- ✅ ONLY audio reply

**TEXT MODE:** Say "texto" or "responda em texto" explicitly

## 📊 Workflow

```
🎤 Audio Received (PT-BR/EN)
    ↓
🔤 Transcribe (wav2vec2 PT-BR - silent)
    ↓
🤖 AI Response (Claude API or OpenClaw Agent - silent)
    ↓
🗣️ Synthesize (Piper neural - silent)
    ↓
📤 Send Audio Reply (silent)
```

## 📁 Scripts

### Installation & Setup
- `install.sh` - Automatic installation (run once!)
- `health_check.py` - Validate the installation

### Core Processing
- `transcribe.py` - wav2vec2 PT-BR speech recognition
- `synthesize.py` - Piper TTS with voice selection
- `voice_config.py` - Voice preference management
- `process.sh` - Full workflow orchestration

### AI Integration
- `claude_adapter.py` - Claude API bridge (intelligent responses)

## 🔧 Configuration

### Optional: Enable Claude Integration

For intelligent AI responses, set your API key:
```bash
export ANTHROPIC_API_KEY="sk-your-api-key"
```

Without this, the skill uses OpenClaw's agent (still great responses!).

### Voice Configuration

Current voice is saved automatically in:
```
~/.openclaw/workspace/.audio_pt_voice_config
```

## 📊 Technical Details

### ASR Model
- **Name:** jonatasgrosman/wav2vec2-large-xlsr-53-portuguese
- **Training:** Fine-tuned on PT-BR Common Voice + other datasets
- **Strengths:** Brazilian slang, regional expressions, informal speech
- **License:** Apache 2.0

### TTS Engine
- **Engine:** Piper (fast, local neural TTS)
- **Voices:** 4 PT-BR options
- **Speed:** Real-time on ARM64/x64
- **Format:** Opus OGG (Telegram optimized)
- **License:** MIT

### AI Response (Optional)
- **Primary:** Claude API (when API key provided)
- **Fallback:** OpenClaw Agent (always available)
- **License:** Claude API is proprietary; OpenClaw Agent is included

## 🚀 Getting Started

1. **Install skill** from ClaWHub
2. **Run:** `bash install.sh`
3. **Restart:** `openclaw gateway restart`
4. **Use:** Send audio messages, use `/voz` commands

## 📋 Requirements

- OpenClaw 2026.4.10+
- Python 3.8+
- 300MB free disk space (for voice models)
- Internet connection (for initial downloads)
- Optional: ANTHROPIC_API_KEY for Claude integration

## 🔒 Privacy & Security

- ✅ Audio transcription happens locally (wav2vec2 runs on your machine)
- ✅ Voice synthesis happens locally (Piper runs on your machine)
- ⚠️ AI responses:
  - Without API key: Processed by OpenClaw Agent (check OpenClaw privacy)
  - With API key: Sent to Anthropic (Claude respects prompt privacy per TOS)

## 📜 License

MIT - Free to use, modify, and redistribute

## 🙏 Credits

- ASR: [jonatasgrosman/wav2vec2-large-xlsr-53-portuguese](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-portuguese)
- TTS: [Piper](https://github.com/rhasspy/piper) by Rhasspy
- AI: [Claude API](https://www.anthropic.com) by Anthropic (optional)
- Voices: Piper Voices repository + TarcisoAmorim community contribution
