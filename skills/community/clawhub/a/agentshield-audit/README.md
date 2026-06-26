# AgentShield Audit - ClawHub Skill

🔒 **Audit your AI agent's security and obtain verifiable trust certificates for inter-agent communication.**

![AgentShield](https://img.shields.io/badge/AgentShield-Security%20Audit-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![OpenClaw](https://img.shields.io/badge/OpenClaw-✓-brightgreen)
![Hermes](https://img.shields.io/badge/Hermes_Agent-✓-brightgreen)

---

## What is AgentShield?

AgentShield is a **security audit framework** for AI agents. It tests your agent against common attack vectors, generates cryptographic identity certificates, and enables secure inter-agent communication through verifiable trust chains.

**Think of it as:** Let's Encrypt for AI Agents 🛡️

---

## 🌐 Framework Compatibility

Works out-of-the-box with both major open-source agent frameworks:

| Framework | Auto-Detection | Install |
|-----------|---------------|--------|
| **OpenClaw** | ✅ Detects `IDENTITY.md` | `clawhub install agentshield-audit` |
| **Hermes Agent** | ✅ Detects `~/.hermes/` | `clawhub install agentshield-audit` |
| **n8n** | ✅ Detects `~/.n8n/` | `clawhub install agentshield-audit` |
| **LangChain / Custom** | Manual `--name`/`--platform` | `clawhub install agentshield-audit` |

Both OpenClaw and Hermes use the [agentskills.io](https://agentskills.io) open standard — same install command, same workflow. → [Hermes Integration Guide](HERMES.md)

---

## 🚀 Quick Start

### Installation

```bash
clawhub install agentshield-audit
```

### Run Your First Audit

```bash
cd ~/.openclaw/workspace/skills/agentshield-audit
python initiate_audit.py --auto
```

That's it! Your agent will be audited in ~30 seconds and receive a signed certificate.

---

## ✨ Features

- ✅ **Zero external fetching** - All scripts bundled locally
- ✅ **Human-in-the-loop** - Explicit approval required before reading files
- ✅ **Cryptographic identity** - Ed25519 keypair generation with local private key storage
- ✅ **Security audit** - Tests against 5+ common attack vectors
- ✅ **Verifiable certificates** - 90-day validity, signed by AgentShield CA
- ✅ **Peer verification** - Verify other agents' certificates before trusting them
- ✅ **No API key required** - Free for basic usage (1 audit/hour rate limit)
- ✅ **Privacy-first** - Private keys NEVER leave your workspace

---

## 🧪 What Gets Tested?

Your agent is tested against these attack vectors:

| Test | Description | Risk Level |
|------|-------------|------------|
| **System Prompt Extraction** | Attempts to extract the agent's system prompt | High |
| **Instruction Override** | Tries to override safety instructions | Critical |
| **Tool Permission Check** | Verifies proper tool access controls | High |
| **Memory Isolation** | Tests for context leakage between sessions | Medium |
| **Secret Leakage** | Scans for exposed API keys, tokens, passwords | Critical |

**Your Security Score:** 0-100 based on passed tests

---

## 📦 Bundle Contents

```
agentshield-audit/
├── SKILL.md                 # Complete skill documentation
├── README.md                # This file
├── HERMES.md               # Hermes Agent integration guide
├── clawhub.json            # ClawHub manifest
├── requirements.txt        # Python dependencies
├── sandbox_config.yaml     # Tool sandbox configuration
├── CHANGELOG.md            # Version history
├── INSTALLATION.md         # Detailed installation guide
├── QUICKSTART.md           # Step-by-step tutorial
│
├── Core Audit Scripts:
│   ├── initiate_audit.py   # Main script - start new audit with consent
│   ├── verify_peer.py      # Verify another agent's certificate
│   ├── show_certificate.py # Display your certificate
│   └── audit_client.py     # Low-level API client
│
├── Security Modules:
│   ├── input_sanitizer.py  # Input validation
│   ├── output_dlp.py       # Output data loss prevention  
│   ├── tool_sandbox.py     # Tool execution sandbox
│   ├── echoleak_test.py    # Echo leakage detection
│   ├── secret_scanner.py   # Secret scanning
│   └── supply_chain_scanner.py  # Supply chain security
│
└── Setup:
    ├── setup.py            # Package setup script
    ├── __init__.py         # Module init
    └── verify_bundle.py    # Bundle verification
```

**All scripts are bundled locally** - no external code fetching.

---

## 🔐 Human-in-the-Loop Consent

Before accessing any sensitive files (`IDENTITY.md`, `SOUL.md`, system prompts), AgentShield **explicitly asks for user approval**:

```
Before proceeding, I need to:

1. Read these files (to detect agent name):
   • IDENTITY.md
   • SOUL.md

2. Generate a cryptographic keypair
   (stored locally in ~/.agentshield/)

3. Send public key to AgentShield API

Proceed? [y/N]: 
```

**User must explicitly type 'y' or 'yes' to continue.**

### Skip File Reading

To avoid any file access, provide info manually:

```bash
python initiate_audit.py --name "MyAgent" --platform telegram
```

---

## 🔐 Privacy & Security

### What Gets Stored Locally?

All sensitive data stays in `~/.openclaw/workspace/.agentshield/`:

```
.agentshield/
├── agent.key          # Your Ed25519 private key (NEVER shared)
├── certificate.json   # Your signed certificate (shareable)
└── config.json        # Agent configuration
```

**File Permissions:** Private key is stored with `600` (owner read/write only)

### What Gets Sent to AgentShield API?

1. **Public key** (Ed25519, generated from your private key)
2. **Agent name** (auto-detected or user-specified)
3. **Platform** (discord, telegram, etc.)
4. **Audit results** (test scores, no sensitive data)

**What is NEVER sent:**
- ❌ Private keys
- ❌ API tokens
- ❌ System prompts
- ❌ Conversation history
- ❌ User data

### Rate Limiting

- **Free tier:** 1 audit per hour per IP
- **No registration required**
- **No payment needed for basic usage**
- Enterprise/high-volume: Contact us

---

## 🎯 Usage Examples

### 1. Auto-detected Audit (Recommended)

```bash
python initiate_audit.py --auto
```

The script will:
- Ask for explicit user consent before reading files
- Auto-detect your agent name from `IDENTITY.md`, `SOUL.md`
- Auto-detect platform from environment variables
- Generate Ed25519 keypair if none exists
- Run the security audit
- Save your certificate

### 2. Manual Audit (Specify Name & Platform)

```bash
python initiate_audit.py --name "MyAgent" --platform telegram
```

No file access required - completely manual.

### 3. Verify Another Agent

```bash
python verify_peer.py --agent-id "agent_abc123xyz"
```

Returns:
- ✅ Certificate validity
- ✅ Expiration date
- ✅ Security score
- ✅ Public key fingerprint

### 4. Show Your Certificate

```bash
python show_certificate.py
```

Displays:
- Agent ID
- Validity period
- Security score
- Verification URL

---

## 📚 Documentation

- **[SKILL.md](SKILL.md)** - Complete skill reference with Human-in-the-Loop details
- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step tutorial for first-time users
- **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation instructions
- **[GitHub](https://github.com/bartelmost/agentshield)** - Source code & issues

---

## 🛠️ Installation Requirements

- **Python:** 3.8 or higher
- **Dependencies:**
  - `cryptography>=41.0.0` (Ed25519 key generation)
  - `requests>=2.31.0` (API communication)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔧 Troubleshooting

### "No certificate found"
**Solution:** Run `python initiate_audit.py --auto` to generate one

### "Challenge failed"
**Solution:** Check your system clock. AgentShield uses time-based challenge-response authentication (NTP sync required)

### "API unreachable"
**Solution:** Verify internet connection. The API endpoint is `https://agentshield.live/api`

### "Rate limited"
**Solution:** Free tier allows 1 audit per hour. Wait 60 minutes between audits.

### "Auto-detection failed"
**Solution:** Use manual mode:
```bash
python initiate_audit.py --name "YourAgentName" --platform discord
```

---

## 🧑‍💻 Development

All scripts are bundled locally. No external downloads.

### Security Module Structure

```python
# Security tests are modular - each can be imported independently
from input_sanitizer import sanitize_input
from secret_scanner import scan_for_secrets
from output_dlp import check_output
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repo
2. Create a feature branch
3. Submit a pull request

**GitHub:** https://github.com/bartelmost/agentshield

---

## 📄 License

MIT License

---

## 💬 Support

- **Issues:** https://github.com/bartelmost/agentshield/issues
- **Contact:** @Kalle-OC on Moltbook
- **Documentation:** https://github.com/bartelmost/agentshield

---

## 🌟 Why AgentShield?

As AI agents become more autonomous and interconnected, **trust becomes the bottleneck**. AgentShield solves this by:

1. **Standardizing security audits** - Consistent testing across all agents
2. **Enabling verifiable trust** - Cryptographic certificates anyone can verify
3. **Preventing attack vectors** - Proactive defense against known threats
4. **Building a trust network** - Agents can verify each other before collaboration

**Secure yourself. Verify others. Trust nothing by default.** 🛡️

---

**Made with 🔐 by the AgentShield team**
