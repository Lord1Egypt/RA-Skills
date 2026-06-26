---
name: claw-secure-auditor
description: Security audit tool for ClawHub/OpenClaw skills (static analysis + reputation scoring)
version: 1.1.1
homepage: https://github.com/YOURNAME/claw-secure-auditor
emoji: "🛡️"
metadata:
  openclaw: '{"requires":{"env":["VIRUSTOTAL_API_KEY"],"bins":["python3"]},"primaryEnv":"VIRUSTOTAL_API_KEY","install":[{"kind":"uv","package":"requests","bins":["python"]}],"os":["linux","darwin"]}'
---

# 🛡️ Claw Secure Auditor v1.1.1

Security audit tool for ClawHub/OpenClaw skills with static analysis and reputation scoring.

---

## 🚀 Quick Start

### 1. Configure (optional)

```bash
export VIRUSTOTAL_API_KEY="your-api-key-here"
```

### 2. Use

```bash
# Quick audit (static + reputation)
python3 scripts/auditor.py quick ./my-skill

# Full audit (static + sandbox + VirusTotal)
python3 scripts/auditor.py full ./my-skill

# Pre-publish audit
python3 scripts/auditor.py before-publish ./my-skill
```

---

## 📋 Features

- ✅ Static analysis: 120+ dangerous keyword detection
- ✅ Self-whitelist: auto-mark self as safe
- ✅ Reputation score: 0-100 with Safe/Caution/Dangerous levels
- ✅ JSON report export
- ✅ Read-only operation, no file modification

---

## 📊 Risk Levels

| Score | Level | Color |
|-------|-------|-------|
| 90-100 | Safe | 🟢 |
| 70-89 | Caution | 🟡 |
| 0-69 | Dangerous | 🔴 |

---

## 📌 Usage Examples

```
python3 scripts/auditor.py quick ./my-skill
python3 scripts/auditor.py full ./my-skill
python3 scripts/auditor.py before-publish ./my-new-skill
```

---

## ⚠️ Security Note

Read-only operation, no file modification, no external writes, API keys only for public data queries.

---

## 📝 Changelog

### v1.1.1 (2026-03)
- Simplified metadata for ClawHub compatibility
- Removed complex dependencies
- Kept core audit functionality

### v1.1.0 (2026-03)
- Self-whitelist: auto-mark self as safe
- Full English translation
- Improved scoring algorithm

### v1.0.0 (2026-03)
- Initial release with 120+ pattern detection
