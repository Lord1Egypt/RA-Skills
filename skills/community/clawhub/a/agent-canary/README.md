# 🐤 Agent Canary

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![Platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor-purple)

**English** | **[中文](README.zh-CN.md)**

Plant decoy credentials in your workspace. When a malicious skill touches them, you know instantly.

**Decoy tokens. Instant alerts. Zero false sense of security.**

**The problem:** You install skills from the community. Some might read your credentials, exfiltrate tokens, or scan your memory files. You'd never know. Agent Canary plants realistic-looking decoy credentials — fake API keys, fake tokens, fake passwords — scattered across your workspace. If any skill or agent reads them, you get an alert before real damage happens.

## Table of Contents

<details>
<summary>Click to expand</summary>

- [How It Works](#how-it-works)
- [Install](#install)
- [Quick Start](#quick-start)
- [Onboarding](#onboarding)
- [License](#license)

</details>

## How It Works

```
decoy API keys ──→ scattered in workspace
                       │
                 skill/agent reads one
                       │
                       ▼
              🚨 instant alert
              "which skill, which file, when"
```

The canary tokens look real (proper format, realistic names) but are completely fake. Only an agent actively scanning for credentials would find and touch them.

## Install

```bash
# ClawHub
clawhub install agent-canary

# Or from source
git clone https://github.com/Thomaszhou22/agent-canary.git
cp -r agent-canary ~/.openclaw/skills/
```

## Quick Start

Ask your agent: **"deploy canary"** — decoys planted. **"canary status"** — check if any have been touched. **"canary cleanup"** — remove all decoys.

## Onboarding

First use asks 2 quick questions: alert method (chat/email/silent) and decoy density (low/medium/high). After that, it just works. Say "reset settings" to reconfigure.

## License

MIT
