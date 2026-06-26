# 📦 Integration Guide - Updating Your Skill

## How to Use These Files

You have **two options**:

### Option 1: Replace Entire Skill (Recommended)
```bash
# Backup current skill
mv ~/.openclaw/skills/audio-ptbr-autoreply ~/.openclaw/skills/audio-ptbr-autoreply.backup

# Create new skill structure
mkdir -p ~/.openclaw/skills/audio-ptbr-autoreply/scripts

# Copy these files to the skill directory:
cp install.sh ~/.openclaw/skills/audio-ptbr-autoreply/
cp health_check.py ~/.openclaw/skills/audio-ptbr-autoreply/
cp requirements.txt ~/.openclaw/skills/audio-ptbr-autoreply/
cp QUICKSTART.md ~/.openclaw/skills/audio-ptbr-autoreply/
cp README_IMPROVED.md ~/.openclaw/skills/audio-ptbr-autoreply/README.md
cp SKILL_IMPROVED.md ~/.openclaw/skills/audio-ptbr-autoreply/SKILL.md

# Copy script files
cp claude_adapter.py ~/.openclaw/skills/audio-ptbr-autoreply/scripts/
cp process.sh ~/.openclaw/skills/audio-ptbr-autoreply/scripts/

# Copy original scripts (from your uploads)
cp transcribe.py ~/.openclaw/skills/audio-ptbr-autoreply/scripts/
cp synthesize.py ~/.openclaw/skills/audio-ptbr-autoreply/scripts/
cp voice_config.py ~/.openclaw/skills/audio-ptbr-autoreply/scripts/
```

### Option 2: Merge with Existing Skill
```bash
# Just copy the new files
cp install.sh ~/.openclaw/skills/audio-ptbr-autoreply/
cp health_check.py ~/.openclaw/skills/audio-ptbr-autoreply/
cp claude_adapter.py ~/.openclaw/skills/audio-ptbr-autoreply/scripts/
cp process.sh ~/.openclaw/skills/audio-ptbr-autoreply/scripts/  # (overwrite)
cp requirements.txt ~/.openclaw/skills/audio-ptbr-autoreply/
```

## File Mapping

```
Your Downloaded Files → Skill Directory
─────────────────────────────────────────
install.sh                    → skills/audio-ptbr-autoreply/install.sh
health_check.py               → skills/audio-ptbr-autoreply/health_check.py
claude_adapter.py             → skills/audio-ptbr-autoreply/scripts/claude_adapter.py
process.sh                    → skills/audio-ptbr-autoreply/scripts/process.sh
requirements.txt              → skills/audio-ptbr-autoreply/requirements.txt
README_IMPROVED.md            → skills/audio-ptbr-autoreply/README.md
SKILL_IMPROVED.md             → skills/audio-ptbr-autoreply/SKILL.md
QUICKSTART.md                 → skills/audio-ptbr-autoreply/QUICKSTART.md

(Keep your existing scripts)
transcribe.py                 → skills/audio-ptbr-autoreply/scripts/transcribe.py
synthesize.py                 → skills/audio-ptbr-autoreply/scripts/synthesize.py
voice_config.py               → skills/audio-ptbr-autoreply/scripts/voice_config.py
agent_bridge.py               → skills/audio-ptbr-autoreply/scripts/agent_bridge.py (optional)
process_audio.sh              → skills/audio-ptbr-autoreply/scripts/process_audio.sh (optional)
```

## Installation Steps

### Step 1: Set Up Files
```bash
cd ~/.openclaw/skills/audio-ptbr-autoreply
chmod +x install.sh health_check.py
chmod +x scripts/*.py scripts/*.sh
```

### Step 2: Run the New Installer
```bash
bash install.sh
```

This will:
- ✅ Auto-detect your system
- ✅ Download Piper TTS
- ✅ Download voice models
- ✅ Install Python dependencies

### Step 3: Verify Installation
```bash
python3 health_check.py
```

### Step 4: Restart OpenClaw
```bash
openclaw gateway restart
```

## Configuration

### Optional: Claude API Integration
```bash
export ANTHROPIC_API_KEY="sk-your-api-key"
openclaw gateway restart
```

### Verify Everything Works
```bash
# Check voices
python3 scripts/voice_config.py list

# Test transcription with a real audio file
python3 scripts/transcribe.py /path/to/audio.wav

# Test synthesis
python3 scripts/synthesize.py "Olá, como vai?"

# Check Claude integration
ANTHROPIC_API_KEY="sk-..." python3 scripts/claude_adapter.py "Teste"
```

## Key Improvements in This Version

| Feature | Benefit |
|---------|---------|
| `install.sh` | One-command automatic setup |
| `health_check.py` | Validate everything works |
| `claude_adapter.py` | Optional intelligent responses |
| Updated `process.sh` | Better error handling |
| `requirements.txt` | Explicit dependencies |
| New documentation | Clear guides and troubleshooting |

## Directory Structure After Integration

```
~/.openclaw/skills/audio-ptbr-autoreply/
├── install.sh                    ⭐ NEW - Run this!
├── health_check.py               ⭐ NEW - Validate setup
├── requirements.txt              ⭐ NEW - Dependencies
├── README.md                      ✨ UPDATED
├── SKILL.md                       ✨ UPDATED
├── QUICKSTART.md                 ⭐ NEW - Quick guide
├── scripts/
│   ├── transcribe.py             (existing)
│   ├── synthesize.py             (existing)
│   ├── voice_config.py            (existing)
│   ├── claude_adapter.py          ⭐ NEW - Claude integration
│   ├── process.sh                 ✨ UPDATED
│   ├── process_audio.sh           (existing)
│   └── agent_bridge.py            (existing)
└── [any other files you have]
```

## Troubleshooting Integration

### "install.sh: command not found"
```bash
# Make sure it's executable
chmod +x install.sh
bash install.sh
```

### "Python imports failed"
```bash
# Install dependencies manually
pip install transformers torch torchaudio anthropic
```

### "Piper not found"
```bash
# Reinstall Piper specifically
bash install.sh
# Or manually:
cd ~/.openclaw/workspace
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
tar xzf piper_arm64.tar.gz
```

### "Path errors in scripts"
All scripts use relative paths that should work. If you have custom paths:
1. Edit the paths in the scripts
2. Check `/home/node/.openclaw/workspace` is correct for your setup
3. Or set `WORKSPACE` environment variable

## Testing After Integration

```bash
# Full workflow test
cd ~/.openclaw/skills/audio-ptbr-autoreply

# 1. Validate installation
python3 health_check.py

# 2. Test each component
python3 scripts/voice_config.py list
python3 scripts/transcribe.py test.wav
python3 scripts/synthesize.py "Teste"

# 3. Test with Claude (if API key set)
ANTHROPIC_API_KEY="sk-..." python3 scripts/claude_adapter.py "Olá"

# 4. Test full workflow (if you have a test audio file)
bash scripts/process.sh test.wav
```

## Upgrading from Previous Version

If you already have the skill installed:

1. **Backup current installation**
   ```bash
   cp -r ~/.openclaw/skills/audio-ptbr-autoreply \
         ~/.openclaw/skills/audio-ptbr-autoreply.backup
   ```

2. **Copy new files (don't overwrite everything)**
   ```bash
   cd ~/.openclaw/skills/audio-ptbr-autoreply
   cp /downloaded/install.sh .
   cp /downloaded/health_check.py .
   cp /downloaded/claude_adapter.py scripts/
   cp /downloaded/process.sh scripts/  # This one CAN overwrite
   cp /downloaded/requirements.txt .
   ```

3. **Run installer to complete setup**
   ```bash
   bash install.sh
   ```

4. **Your voice preferences are preserved!**
   ```bash
   # Voice config is saved in:
   ~/.openclaw/workspace/.audio_pt_voice_config
   ```

## Next Steps

1. ✅ Copy files to skill directory
2. ✅ Run `bash install.sh`
3. ✅ Run `python3 health_check.py`
4. ✅ Restart OpenClaw
5. ✅ Test with `/voz list` command
6. ✅ Send your first audio message! 🎤

## Questions?

- **Check:** `IMPROVEMENTS_SUMMARY.md` for what's changed
- **Quick setup:** `QUICKSTART.md` (3 minute guide)
- **Full docs:** `README.md`
- **Troubleshooting:** `health_check.py`

---

**You're all set!** The skill is now production-ready with automatic installation and Claude integration. 🚀
