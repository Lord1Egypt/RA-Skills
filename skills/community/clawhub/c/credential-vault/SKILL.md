---
name: credential-vault
description: "Encrypted credential storage for OpenClaw agents. Stop storing API keys in plaintext."
license: "MIT-0"
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      bins: ["uv"]
    primaryEnv: "VAULT_MASTER_PASSWORD"
---

# 🔐 Credential Vault

Encrypted credential storage for OpenClaw agents. Stop storing API keys in plaintext.

## Overview

Credential Vault provides AES-256-GCM encrypted local storage for API keys, tokens, and other secrets. Instead of scattering credentials across `.env` files, centralize them in an encrypted vault with audit logging and expiry tracking.

## Features

- **AES-256-GCM encryption** with PBKDF2 key derivation (600,000 iterations)
- **CRUD operations** for credentials
- **Tag-based organization** (by skill, project, etc.)
- **Environment variable injection** for easy integration
- **Expiry tracking** with notifications
- **Audit logging** (who accessed what, when)
- **Session-based unlocking** (no password re-entry)

## Installation

```bash
cd ~/ubik-collective/systems/ubik-pm/skills/credential-vault
uv sync
```

## Quick Start

```bash
# Initialize vault (one-time setup)
uv run vault init

# Unlock vault
uv run vault unlock

# Add credentials
uv run vault add OPENAI_API_KEY "sk-..." --tag openai
uv run vault add TAVILY_API_KEY "tvly-..." --tag tavily --expires 2026-12-31

# List credentials
uv run vault list

# Get a credential
uv run vault get OPENAI_API_KEY

# Export for a skill
eval $(uv run vault env --tag tavily)

# Lock when done
uv run vault lock
```

## Security Model

### Encryption
- Master password → PBKDF2-SHA256 (600,000 iterations) → 256-bit key
- Each secret encrypted with AES-256-GCM (unique nonce per entry)
- Authentication tags verify integrity
- Master password never stored (only verification hash)

### Storage
- Vault: `~/.openclaw/vault/vault.enc.json` (encrypted)
- Audit log: `~/.openclaw/vault/audit.log` (plaintext, no values)
- Session key: `~/.openclaw/vault/session` (temporary, cleared on lock)

### Permissions
- Vault file: `0600` (owner read/write only)
- Session key: deleted on `vault lock`

### Threat Model
**Protects against:**
- ✅ Accidental credential leaks (git commits, logs)
- ✅ Casual file browsing
- ✅ Malware reading `.env` files

**Does NOT protect against:**
- ❌ Keyloggers (can capture master password)
- ❌ Root-level system compromise
- ❌ Memory dumps while vault is unlocked

## Usage Examples

See [EXAMPLE.md](./EXAMPLE.md) for detailed usage patterns.

## Commands

### `vault init`
Initialize a new vault with a master password.

### `vault unlock`
Unlock the vault for the current session.

### `vault lock`
Lock the vault and clear session key.

### `vault status`
Show vault status (locked/unlocked, credential count).

### `vault add KEY_NAME [VALUE] [--tag TAG] [--expires DATE]`
Add or update a credential. If VALUE is omitted, prompts securely.

### `vault get KEY_NAME`
Retrieve and decrypt a credential.

### `vault list [--tag TAG]`
List all credentials (values masked). Optionally filter by tag.

### `vault remove KEY_NAME [-y]`
Remove a credential. Prompts for confirmation unless `-y` is passed.

### `vault env [--tag TAG]`
Export credentials as `KEY=VALUE` for environment injection.

**Example:**
```bash
eval $(uv run vault env --tag openai)
echo $OPENAI_API_KEY  # Now available
```

### `vault audit [--last N]`
View recent audit log entries.

### `vault expiring [--days N]`
Check for credentials expiring within N days (default: 7).

### `vault rotate KEY_NAME [NEW_VALUE]`
Replace a credential with a new value (preserves tags/metadata).

## Integration with Skills

### Pattern: Inject credentials before running a skill

```bash
# Tavily search skill
eval $(uv run vault env --tag tavily)
uv run scripts/search.py "OpenClaw release date"
```

### Pattern: Skill checks vault directly

```python
from lib.store import Store

store = Store()
# Assumes vault is unlocked by user beforehand
api_key = store.get("TAVILY_API_KEY")
```

### Pattern: Auto-unlock in HEARTBEAT.md

```markdown
# HEARTBEAT.md
Check if vault is locked. If so, prompt user to unlock before running daily checks.
```

## Best Practices

1. **Use tags consistently** — Tag credentials by skill name for easy filtering
2. **Set expiry dates** — Track when API keys need rotation
3. **Lock when idle** — Run `vault lock` when not actively using credentials
4. **One vault per machine** — Don't sync the vault file across machines
5. **Rotate regularly** — Use `vault expiring` to track upcoming expirations
6. **Review audit logs** — Check `vault audit` periodically

## Limitations

- **Local only** — No network sync (by design)
- **Single-user** — No multi-user access control
- **No backup** — User responsible for backing up `~/.openclaw/vault/`
- **Session key on disk** — `vault unlock` stores decryption key until `vault lock`

## Troubleshooting

### "Vault is locked"
Run `uv run vault unlock` and enter your master password.

### "Incorrect master password"
Double-check your password. If forgotten, you'll need to reinitialize (losing all credentials).

### "Vault not initialized"
Run `uv run vault init` to create a new vault.

### Session key persists after reboot
Session file is cleared on `vault lock`, but not automatically on reboot. Run `vault lock` explicitly.

## Development

### Run tests
```bash
uv run pytest
```

### Add a test
See `tests/test_roundtrip.py` for examples.

## License

MIT-0 (public domain equivalent)
