# 🔐 Credential Vault

**Encrypted credential storage for OpenClaw agents.**

Stop storing API keys in plaintext. Use Credential Vault to encrypt, organize, and audit access to your secrets.

---

## Why?

**Before:**
```bash
# .env (plaintext, easily leaked)
OPENAI_API_KEY=sk-proj-abc123...
TAVILY_API_KEY=tvly-xyz789...
GITHUB_TOKEN=ghp_def456...
```

**After:**
```bash
# All credentials encrypted in ~/.openclaw/vault/
$ vault add OPENAI_API_KEY "sk-proj-abc123..." --tag openai
✅ Added credential: OPENAI_API_KEY

$ vault list
📋 Credentials (3):
  🔑 OPENAI_API_KEY
     Tags: openai
  🔑 TAVILY_API_KEY
     Tags: tavily
  🔑 GITHUB_TOKEN
     Tags: github
```

---

## Features

✅ **AES-256-GCM encryption** (PBKDF2 key derivation, 600k iterations)  
✅ **Tag-based organization** (by skill, project, environment)  
✅ **Expiry tracking** (get notified before keys expire)  
✅ **Audit logging** (know who accessed what, when)  
✅ **Environment injection** (`vault env --tag skill-name`)  
✅ **Zero network dependencies** (local-only, no phone-home)

---

## Installation

```bash
cd ~/ubik-collective/systems/ubik-pm/skills/credential-vault
uv sync
```

**Requirements:**
- Python 3.11+
- `uv` package manager

---

## Quick Start

### 1. Initialize the vault (one-time setup)

```bash
$ uv run vault init
Enter master password: ********
Confirm master password: ********
✅ Vault initialized at /Users/you/.openclaw/vault/vault.enc.json
```

### 2. Unlock the vault

```bash
$ uv run vault unlock
Enter master password: ********
🔓 Vault unlocked
```

### 3. Add credentials

```bash
# Interactive (password prompt)
$ uv run vault add OPENAI_API_KEY --tag openai
Enter value for OPENAI_API_KEY: ********
✅ Added credential: OPENAI_API_KEY

# Non-interactive
$ uv run vault add TAVILY_API_KEY "tvly-abc123" --tag tavily --expires 2026-12-31
✅ Added credential: TAVILY_API_KEY
```

### 4. Use credentials

```bash
# Get a single credential
$ uv run vault get OPENAI_API_KEY
sk-proj-abc123...

# Export all credentials for a skill
$ eval $(uv run vault env --tag openai)
$ echo $OPENAI_API_KEY
sk-proj-abc123...
```

### 5. Lock when done

```bash
$ uv run vault lock
🔒 Vault locked
```

---

## Common Workflows

### Add a new API key

```bash
uv run vault unlock
uv run vault add ANTHROPIC_API_KEY --tag anthropic --expires 2027-01-01
# Paste key when prompted
uv run vault lock
```

### Check expiring keys

```bash
uv run vault unlock
uv run vault expiring --days 30
⚠️  Credentials expiring within 30 days:
  ⚠️  15 days - TAVILY_API_KEY
     Expires: 2026-04-01
     Tags: tavily
```

### Rotate a key

```bash
uv run vault unlock
uv run vault rotate OPENAI_API_KEY
# Enter new key when prompted
🔄 Rotated credential: OPENAI_API_KEY
```

### Review who accessed what

```bash
uv run vault audit --last 10
📝 Audit Log (last 10 entries):
  [2026-03-17T14:32:15] get: OPENAI_API_KEY
  [2026-03-17T14:30:00] add: TAVILY_API_KEY
     Details: {'tags': ['tavily'], 'expires': '2026-12-31'}
```

### Export credentials for a script

```bash
# Export all Tavily-related keys
eval $(uv run vault env --tag tavily)

# Now run your script (keys available as env vars)
python scripts/search.py
```

---

## Security Model

### What's Protected

| Threat | Protected? |
|--------|-----------|
| Accidental git commit of `.env` | ✅ Yes |
| Malware reading plaintext files | ✅ Yes |
| Casual browsing of your filesystem | ✅ Yes |
| Logs containing API keys | ✅ Yes (if using vault) |

### What's NOT Protected

| Threat | Protected? |
|--------|-----------|
| Keylogger capturing master password | ❌ No |
| Root-level system compromise | ❌ No |
| Memory dump while vault unlocked | ❌ No |
| Physical access to unlocked machine | ❌ No |

**Takeaway:** Vault protects against _accidental leaks_ and _casual snooping_, not nation-state attackers or root malware.

### Encryption Details

- **Algorithm:** AES-256-GCM (Galois/Counter Mode)
- **Key derivation:** PBKDF2-SHA256, 600,000 iterations
- **Nonce:** 96-bit random (unique per encryption)
- **Authentication:** 128-bit GCM tag (integrity verification)

**Storage format:**
```json
{
  "version": "1.0",
  "salt": "base64-encoded-salt",
  "password_hash": "sha256-hash-for-verification",
  "entries": {
    "KEY_NAME": {
      "nonce": "base64",
      "ciphertext": "base64",
      "tag": "base64",
      "metadata": {
        "created": "ISO-timestamp",
        "modified": "ISO-timestamp",
        "tags": ["skill-name"],
        "expires": "2026-12-31"
      }
    }
  }
}
```

**What's never stored:**
- ❌ Master password (only verification hash)
- ❌ Plaintext credentials (always encrypted)
- ❌ Decryption key (except during unlocked session)

---

## CLI Reference

| Command | Description |
|---------|-------------|
| `vault init` | Initialize a new vault |
| `vault unlock` | Unlock vault for current session |
| `vault lock` | Lock vault and clear session key |
| `vault status` | Show vault status |
| `vault add KEY [VALUE]` | Add/update a credential |
| `vault get KEY` | Retrieve a credential |
| `vault list [--tag T]` | List credentials (masked) |
| `vault remove KEY` | Delete a credential |
| `vault env [--tag T]` | Export as `KEY=VALUE` |
| `vault audit [--last N]` | View audit log |
| `vault expiring [--days N]` | Check expiring keys |
| `vault rotate KEY [VALUE]` | Replace a credential |

For detailed usage, see [EXAMPLE.md](./EXAMPLE.md).

---

## Best Practices

### 1. Tag everything
```bash
vault add OPENAI_API_KEY "..." --tag openai --tag production
vault add OPENAI_API_KEY_DEV "..." --tag openai --tag development
```

### 2. Set expiry dates
```bash
vault add TEMP_TOKEN "..." --expires 2026-04-01
vault expiring --days 7  # Weekly check
```

### 3. Lock when idle
```bash
# In your shell logout script
vault lock
```

### 4. Review audit logs
```bash
vault audit --last 50 | grep "suspicious_key"
```

### 5. Rotate regularly
```bash
vault expiring --days 30  # See what's coming up
vault rotate OLD_KEY "new-value"
```

---

## Troubleshooting

### "Vault is locked"
**Solution:** Run `vault unlock` and enter your master password.

### "Incorrect master password"
**Solution:** Double-check your password. If forgotten, you'll need to reinitialize (⚠️ loses all credentials).

### "Vault not initialized"
**Solution:** Run `vault init` to create a new vault.

### Session persists after reboot
**Solution:** Run `vault lock` before shutdown, or add to logout script.

### Forgot master password
**No recovery possible.** You'll need to:
1. Delete `~/.openclaw/vault/`
2. Run `vault init` with a new password
3. Re-add all credentials (⚠️ old ones are lost)

**Prevention:** Store master password in a secure password manager (1Password, Bitwarden, etc.).

---

## Development

### Run tests
```bash
uv run pytest
```

### Project structure
```
credential-vault/
├── lib/               # Core libraries
│   ├── crypto.py      # AES-256-GCM + PBKDF2
│   ├── store.py       # Encrypted CRUD
│   ├── audit.py       # Access logging
│   └── expiry.py      # Expiry tracking
├── scripts/
│   └── vault.py       # CLI entry point
└── tests/             # Unit tests
```

---

## FAQ

**Q: Can I sync the vault across machines?**  
A: Not recommended. Each machine should have its own vault. If you need shared credentials, use a proper secrets manager (1Password, HashiCorp Vault).

**Q: Is this production-ready?**  
A: For local development, yes. For production secrets (servers, CI/CD), use dedicated tools (AWS Secrets Manager, GCP Secret Manager, etc.).

**Q: What if I lose the master password?**  
A: No recovery. You'll need to reinitialize and lose all credentials. Store master password in a secure password manager.

**Q: Can multiple users share a vault?**  
A: No. One vault = one user. For teams, use proper secrets management platforms.

**Q: Does this phone home?**  
A: No. Zero network dependencies. Everything is local.

---

## License

MIT-0 (public domain equivalent)

---

## Credits

Built for [OpenClaw](https://openclaw.com) agent ecosystem.  
Inspired by `pass`, `age`, and HashiCorp Vault.
