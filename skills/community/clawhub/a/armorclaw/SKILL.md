---
name: armorclaw
description: >
  AES-256 encrypted secrets manager for OpenClaw agents. Store API keys,
  tokens, and credentials in a secure local vault instead of plain-text .env
  files. Features master password with machine/IP binding, one-command .env
  migration, cross-skill secret sharing, and per-skill access logging.
  Use when: securing API keys, migrating from .env files, or auditing which
  skills access which credentials.
metadata:
  openclaw:
    emoji: "🔐"
    version: "1.0.0"
    author: "PHRAIMWORK LLC"
    url: "https://phraimwork.com"
    requires:
      python: ">=3.10"
---

# ArmorClaw — Encrypted Secrets Manager for OpenClaw

Stop storing API keys in plain-text `.env` files.
ArmorClaw encrypts everything with AES-256 and unlocks only on your machine.

## Install

```bash
npx clawhub@latest install armorclaw
pip install ./skills/armorclaw
```

## Quick Start

```bash
# Initialize vault
armorclaw init

# Store your first key
armorclaw set OPENAI_KEY

# Or import your whole .env at once
armorclaw import ~/.openclaw/openclaw.env

# List stored secrets
armorclaw list
```

## Use in OpenClaw Agent

```python
from armorclaw.openclaw import inject_vault_env

# Inject all vault secrets into environment at startup
inject_vault_env(password="your-master-password")

# Or use ARMORCLAW_PASSWORD env var for bot auto-unlock
# export ARMORCLAW_PASSWORD="your-master-password"
# inject_vault_env()
```

## Cross-Skill Sharing

One key, all your skills:

```python
from armorclaw.openclaw import get_vault_key

# Any skill can pull keys from the vault
api_key = get_vault_key("OPENAI_KEY", skill="senticlaw")
```

## CLI Reference

```
armorclaw init              Initialize vault + set master password
armorclaw set KEY [value]   Store a secret
armorclaw get KEY           Retrieve a secret
armorclaw list              List all stored keys (no values shown)
armorclaw delete KEY        Delete a secret
armorclaw import [path]     Import .env file into vault
armorclaw log [KEY]         View access log
armorclaw report            Skill usage report
```

## Lock Modes

| Mode | Security | Description |
|------|----------|-------------|
| `password` | Medium | Type master password each time |
| `machine` | Good | Locked to registered machine (MAC address) |
| `static-ip` | Good | Locked to your static external IP only |
| `machine+static-ip` | Strongest | Machine AND static external IP must match |
| `bot` | Convenient | Bot auto-unlocks using stored password |

> ⚠️ **IP restriction requires a STATIC external IP.** Dynamic/rotating IPs (most home internet) will lock you out when your IP changes. ArmorClaw will warn you and confirm before registering.

## Security

- **AES-256-CBC** encryption with PBKDF2-HMAC-SHA256 key derivation (600k iterations)
- **HMAC integrity** — detects tampering
- **Machine binding** — vault won't open on another machine
- **IP restriction** — vault won't open from a different network
- **Zero plaintext storage** — keys never written unencrypted anywhere
- **Access audit log** — every read/write tracked with skill name + timestamp

---

Built by [PHRAIMWORK LLC](https://phraimwork.com) · MIT License
Part of the PHRAIMWORK Security Suite: SentiClaw + ArmorClaw
