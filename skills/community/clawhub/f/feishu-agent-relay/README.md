# Feishu Agent Relay Skill

**Multi-Agent Collaboration System for Feishu (Lark)**

[![ClawHub](https://img.shields.io/badge/platform-clawhub-blue)](https://clawhub.com)
[![OpenClaw](https://img.shields.io/badge/openclaw-skill-green)](https://openclaw.ai)
[![Version](https://img.shields.io/badge/version-1.2-orange)](https://clawhub.com/skills/feishu-agent-relay)

---

## 🎯 What It Does

Enable **multiple Feishu Bots to work together** as a coordinated team:

- **Coordinator Bot** receives user messages
- **Specialist Bots** (tech/product experts) provide domain expertise
- **Automatic task relay** between Bots
- **Proactive messaging** from specialists to users

**Key innovation:** Solves Feishu open_id isolation problem - each Bot has different open_id for the same user.

---

## 🚀 Quick Start

### Single-User Mode (Personal Use - 5 minutes)

```bash
# 1. Install skill from ClawHub
# 2. Set environment variable
export DEPLOYMENT_MODE=single-user

# 3. Contact any Bot - auto-configures!
# That's it! No manual setup needed.
```

### Multi-User Mode (Teams - 30 minutes)

```bash
# 1. Install skill from ClawHub
# 2. Set environment variable
export DEPLOYMENT_MODE=multi-user

# 3. Create 3+ Feishu Bots (coordinator + specialists)
# 4. Each user registers their User ID
```

---

## 📋 Features

### ✅ Deployment Modes

| Mode | For | Setup | Security |
|------|-----|-------|----------|
| **Single-User** | Personal use | 5 min, zero-config | ✅ High |
| **Multi-User** | Teams | 30 min, manual | ⚠️ Internal only |

### ✅ Core Capabilities

- **User Identity Mapping** - Cross-Bot user resolution
- **Task Relay** - Coordinator → Specialist routing
- **Proactive Messaging** - Specialists can DM users
- **Auto-Registration** - Single-user mode (zero-config)
- **Manual Registration** - Multi-user mode (with warnings)

### ✅ Documentation

- **SKILL.md** - Complete usage guide (13KB)
- **single-user-setup.md** - Personal use guide (12KB)
- **feishu-bot-setup.md** - Team setup guide (13KB)
- **mapping-schema.md** - Technical schema (7KB)
- **relay-examples.md** - Code examples (11KB)

---

## 🏗️ Architecture

```
User → Coordinator Bot → sessions_send → Specialist Bot → User
                          (userid only)    queries mapping
```

**Components:**
- Coordinator Agent (orchestrator)
- Specialist Agents (tech/product experts)
- User Mapping Table (cross-Bot identity)
- Mapping API (unified access)

---

## 📦 What's Included

```
feishu-agent-relay/
├── SKILL.md                    # Main skill documentation
├── scripts/
│   └── mapping-api.js          # User mapping API
└── references/
    ├── single-user-setup.md    # Personal use guide
    ├── feishu-bot-setup.md     # Team setup guide
    ├── mapping-schema.md       # Technical schema
    └── relay-examples.md       # Code examples
```

**Total size:** 22KB (compressed)

---

## 🔧 Requirements

### Feishu

- Feishu Developer Account
- 3+ Feishu Bot applications (Coordinator + Specialists)
- Bot permissions: messaging, user info, proactive messages

### OpenClaw

- OpenClaw runtime with session support
- `sessions_send` capability
- `message` tool for Feishu
- File system access for mapping table

---

## 🎓 Use Cases

### Personal Productivity

- Multiple specialist Bots for different domains
- Unified coordination through single Bot
- Zero configuration setup

### Team Collaboration

- Shared expert Bots for entire team
- Automatic task routing based on expertise
- User tracking across Bots

### Customer Support

- Coordinator handles initial contact
- Routes to appropriate specialist
- Specialists proactively follow up

---

## ⚠️ Important Notes

### Security

- **Single-User Mode:** Secure for personal use (only you)
- **Multi-User Mode:** Internal use only (no identity verification)
- **Production:** Add SSO/LDAP integration for proper authentication

### Limitations

- Manual User ID entry in multi-user mode (no verification)
- Requires multiple Feishu Bot applications
- Internal/enterprise use only

---

## 📖 Documentation

### Getting Started

1. **Choose your mode:** Single-user (personal) or Multi-user (teams)
2. **Follow setup guide:** Based on chosen mode
3. **Test relay flow:** Verify coordinator → specialist works
4. **Deploy:** Start using your multi-Bot system

### Key Concepts

- **Feishu open_id Isolation** - Each Bot has different open_id per user
- **User ID as Universal Identity** - Cross-Bot user identifier
- **Mapping Table** - Resolves userid → Bot-specific open_id
- **Relay Pattern** - Coordinator sends userid only, specialists query own open_id

---

## 🤝 Contributing

Found issues or have improvements?

1. Test the skill in your environment
2. Report bugs or suggestions
3. Share your use cases

---

## 📄 License

This skill is shared via ClawHub for the OpenClaw community.

---

## 🆘 Support

- **Documentation:** See `references/` folder
- **Examples:** `relay-examples.md` has 6 real-world scenarios
- **Troubleshooting:** Each guide has troubleshooting section

---

**Version:** 1.2  
**Last Updated:** 2026-03-07  
**Tested:** Feishu multi-Bot coordination (3 Agents)  
**Status:** ✅ Production-ready for internal/personal use

---

## 🎯 Quick Decision Guide

**Choose Single-User Mode if:**
- ✅ Only you will use the Bots
- ✅ Want zero configuration
- ✅ Personal productivity system

**Choose Multi-User Mode if:**
- ✅ Team or organization
- ✅ Multiple users needed
- ✅ Will add verification later

**Recommendation:** Start with Single-User for testing, switch to Multi-User for teams.
