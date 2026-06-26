# 🛡️ Claw Secure Auditor

Security audit tool for ClawHub/OpenClaw skills with static analysis and reputation scoring.

---

## Quick Start

### 1. Configure (optional)

```bash
export VIRUSTOTAL_API_KEY="your-api-key-here"
```

### 2. Use

```bash
# Quick audit (static + reputation)
python3 scripts/auditor.py quick ./my-skill

# Full audit
python3 scripts/auditor.py full ./my-skill

# Pre-publish audit
python3 scripts/auditor.py before-publish ./my-new-skill
```

---

## Features

- ✅ Static analysis: 120+ dangerous keyword detection
- ✅ Self-whitelist: auto-mark self as safe
- ✅ Reputation score: 0-100
- ✅ JSON report export
- ✅ Read-only operation

---

## Full Documentation

Complete guide in `SKILL.md`.

---

## Security

Read-only only, no file modification, no external writes.

---

## License

MIT License

---

*Version: v1.1.1*
