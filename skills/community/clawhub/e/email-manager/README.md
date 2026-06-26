# 📧 Email Manager Skill for OpenClaw

A complete, non-interactive email management skill for [OpenClaw](https://github.com/openclaw/openclaw) agents, built for Postfix (MTA) and Dovecot (MDA) infrastructure. Zero external dependencies, pure Python standard library.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

- ✅ **Complete email management** - Read, send, drafts, folders, flags, spam
- ✅ **Zero dependencies** - Uses only Python standard library
- ✅ **Non-interactive** - Perfect for AI automation
- ✅ **Human-readable output** - Clean formatting with emojis
- ✅ **JSON output** - Machine-parsable for agents
- ✅ **Postfix/Dovecot ready** - Works with your existing infrastructure

## 📚 Documentation

For complete usage instructions, commands, and examples, see the **[SKILL.md](SKILL.md)** file.

## ⚙️ Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/openclaw-email-manager.git
cd openclaw-email-manager

# Configure your email settings
cp config.example.json config.json
# Edit config.json with your credentials

# Make scripts executable
chmod +x scripts/*.py

# Test connection
python3 scripts/imap_utils.py list-folders
```

## 📦 Installation for OpenClaw

```bash
# Create skill directory
mkdir -p ~/OpenClaw-Workspace/skills/email-manager

# Copy files
cp -r * ~/OpenClaw-Workspace/skills/email-manager/

# Check skill is loaded
openclaw skills list | grep email-manager
```

## 🤝 Support the Project

If you find this skill useful, consider a donation!

[![PayPal](https://img.shields.io/badge/PayPal-donate-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/soderholmm)
## 📄 License

MIT License

Copyright (c) Mattias Söderholm

## 🙏 Acknowledgements

- [OpenClaw](https://github.com/openclaw/openclaw) - The AI agent framework
- Postfix and Dovecot - The excellent MTA and MDA

