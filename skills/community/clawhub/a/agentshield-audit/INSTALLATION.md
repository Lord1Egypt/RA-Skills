# AgentShield Audit - Installation Guide

> **Using n8n, LangChain, or another platform?** → See [PLATFORMS.md](PLATFORMS.md) for platform-specific guides.

## 📦 ClawHub Installation (Recommended)

### One-Command Install

```bash
clawhub install agentshield-audit
```

That's it! The skill will be installed to `~/.openclaw/workspace/skills/agentshield-audit/`

### First Run

After installation, run your first audit:

```bash
cd ~/.openclaw/workspace/skills/agentshield-audit
python scripts/initiate_audit.py --auto
```

The script will:
1. Auto-detect your agent name and platform
2. Generate an Ed25519 keypair (stored locally)
3. Run security audit (~30 seconds)
4. Save your signed certificate

---

## 🔧 Alternative Installation Methods

### Method 1: pip Install (Future)

Once published to PyPI:

```bash
pip install agentshield-audit
```

Then use the command-line tools:

```bash
agentshield-audit --auto
agentshield-verify --agent-id "agent_xyz"
agentshield-cert
```

### Method 2: Manual Bundle Install

1. Download the bundle:
   ```bash
   curl -L -o agentshield-audit.tar.gz https://github.com/bartelmost/agentshield/releases/latest/download/agentshield-audit-v1.0.0-clawhub.tar.gz
   ```

2. Extract:
   ```bash
   mkdir -p ~/.openclaw/workspace/skills
   tar -xzf agentshield-audit.tar.gz -C ~/.openclaw/workspace/skills/
   ```

3. Install dependencies:
   ```bash
   cd ~/.openclaw/workspace/skills/agentshield-audit
   pip install -r scripts/requirements.txt
   ```

4. Run:
   ```bash
   python scripts/initiate_audit.py --auto
   ```

### Method 3: Git Clone (Development)

For developers who want to contribute:

```bash
git clone https://github.com/bartelmost/agentshield.git
cd agentshield
pip install -e .
```

---

## 🔍 Verify Installation

Run the verification script to check everything is set up correctly:

```bash
cd ~/.openclaw/workspace/skills/agentshield-audit
python verify_bundle.py
```

Expected output:
```
✅ ALL CHECKS PASSED (5/5)
Bundle is ready for distribution!
```

---

## 📋 System Requirements

### Operating System
- ✅ Linux (tested on Ubuntu 20.04+)
- ✅ macOS (tested on 11+)
- ✅ Windows (WSL2 recommended)

### Python
- **Required:** Python 3.8 or higher
- **Recommended:** Python 3.10+

Check your version:
```bash
python3 --version
```

### Dependencies

The skill requires:
- `cryptography>=41.0.0` - For Ed25519 key generation
- `requests>=2.31.0` - For API communication

These are installed automatically during setup.

### Network
- **Internet connection required** - For AgentShield API communication
- **Firewall:** Allow HTTPS outbound to `agentshield.live/api`

---

## 🚀 Quick Start After Installation

### 1. Auto-Detected Audit (Easiest)

```bash
python scripts/initiate_audit.py --auto
```

Detects agent name and platform automatically from your environment.

### 2. Manual Audit

```bash
python scripts/initiate_audit.py --name "MyAgent" --platform discord
```

### 3. Show Your Certificate

```bash
python scripts/show_certificate.py
```

### 4. Verify Another Agent

```bash
python scripts/verify_peer.py --agent-id "agent_abc123"
```

---

## 🗂️ File Locations After Install

```
~/.openclaw/workspace/
├── skills/
│   └── agentshield-audit/          # Skill code
│       ├── scripts/
│       ├── src/
│       └── ...
│
└── .agentshield/                   # Your private data
    ├── agent.key                   # Ed25519 private key (600 permissions)
    ├── certificate.json            # Your signed certificate
    └── config.json                 # Configuration
```

**Important:** The `.agentshield/` directory contains sensitive cryptographic keys. **Never share `agent.key`**.

---

## 🛠️ Troubleshooting Installation

### "pip not found"

Install pip:
```bash
# Ubuntu/Debian
sudo apt-get install python3-pip

# macOS
brew install python3

# Windows
# Download from https://www.python.org/downloads/
```

### "Permission denied"

On Linux/macOS, you might need to install as user:
```bash
pip install --user -r scripts/requirements.txt
```

### "Module not found: cryptography"

Install dependencies manually:
```bash
pip install cryptography>=41.0.0 requests>=2.31.0
```

### "clawhub command not found"

Ensure OpenClaw is installed and in your PATH:
```bash
which openclaw
openclaw --version
```

If not installed, follow [OpenClaw installation guide](https://openclaw.dev/docs/installation).

---

## 🔄 Updating

### Via ClawHub

```bash
clawhub update agentshield-audit
```

### Manual Update

1. Backup your keys:
   ```bash
   cp -r ~/.openclaw/workspace/.agentshield ~/.agentshield-backup
   ```

2. Remove old version:
   ```bash
   rm -rf ~/.openclaw/workspace/skills/agentshield-audit
   ```

3. Install new version:
   ```bash
   clawhub install agentshield-audit
   ```

4. Restore keys (if needed):
   ```bash
   cp -r ~/.agentshield-backup ~/.openclaw/workspace/.agentshield
   ```

---

## 🧪 Testing Your Installation

### Quick Test

```bash
cd ~/.openclaw/workspace/skills/agentshield-audit
python -m pytest tests/test_quick.py -v
```

### Full Test Suite

```bash
python -m pytest tests/ -v
```

### Security Modules Test

```bash
python tests/test_security_modules.py
```

---

## 📞 Support

If you encounter issues during installation:

1. **Check logs:** `~/.openclaw/logs/`
2. **GitHub Issues:** https://github.com/bartelmost/agentshield/issues
3. **Contact:** @Kalle-OC on Moltbook

---

## ✅ Post-Installation Checklist

- [ ] Bundle verification script passes (`python verify_bundle.py`)
- [ ] Dependencies installed (`cryptography`, `requests`)
- [ ] Scripts are executable (`chmod +x scripts/*.py`)
- [ ] `.agentshield/` directory created
- [ ] First audit completed successfully
- [ ] Certificate received and saved

---

**Ready to secure your agent? Run your first audit now!** 🛡️

```bash
python scripts/initiate_audit.py --auto
```
