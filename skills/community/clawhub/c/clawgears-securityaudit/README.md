# ClawGears Security Audit Skill

[![Version](https://img.shields.io/badge/version-1.4.0-green)](https://github.com/JinHanAI/ClawGears)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey?logo=apple)](https://github.com/JinHanAI/ClawGears)

OpenClaw Security Audit Skill - Protect your Mac, guard your privacy.

## 🌟 What's New in v1.4.0

**Context-Aware Risk Explanations** - No more one-size-fits-all recommendations!

Each security check now provides:
- 📌 What this check protects
- ⚡ Real impact based on **your** scenario (risk table)
- 💡 Graded recommendations (🔴must/🟠recommended/🟡optional/⚪evaluate)
- Legitimate reasons to not fix
- Alternative compensating measures

## Installation

```bash
clawhub install clawgears-securityaudit
```

## Quick Start

After installation, ask your OpenClaw agent:

- "帮我检查一下 OpenClaw 的安全性"
- "Check if my OpenClaw is exposed"
- "Run a security audit"

## Features

- 🔒 Gateway exposure detection
- 🔑 Token strength validation
- 📷 Sensitive command blocking check
- 💾 TCC permission audit
- 🌐 IP leak detection (allegro.earth, Censys, Shodan)
- 🔧 Auto-fix capabilities
- **🆕 Context-aware risk explanations**

## Scripts Included

| Script | Purpose |
|--------|---------|
| `quick-check.sh` | 5-second security check with context-aware output |
| `ip-leak-check.sh` | IP exposure detection (3 databases) |
| `interactive-fix.sh` | Auto-fix security issues |
| `generate-report.sh` | Generate audit reports |
| `system-security-check.sh` | macOS system security (FileVault, SIP, Firewall) |

## Full Repository

For the complete CLI tool with TUI menu:

```bash
git clone https://github.com/JinHanAI/ClawGears.git
cd ClawGears
./clawgears.sh
```

## License

MIT-0 (ClawHub Platform License)

## Author

Victor.Chen ([@JinHanAI](https://github.com/JinHanAI))
