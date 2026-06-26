---
name: env-secrets-rotator
description: Rotate and update secrets in environment files, generate Vault commands, and manage secret rotation workflows.
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Environment Secrets Rotator

## What This Does

A CLI tool to help rotate secrets in environment files and generate commands for secret managers like HashiCorp Vault. Securely generates new random values for secrets, updates .env files, and provides rotation workflows for development and production environments.

Key features:
- **Rotate secrets in .env files** - Generate new random values for specified keys
- **Multiple generation algorithms** - Hex, base64, UUID, custom length
- **Backup original files** - Create backups before modification
- **Dry-run mode** - Preview changes without modifying files
- **Generate Vault commands** - Output HashiCorp Vault CLI commands for secret rotation
- **Batch processing** - Rotate multiple keys across multiple files
- **Validation** - Check .env file format and key existence
- **Rotation history** - Track previous values (optional)

## How To Use

### Basic rotation:
```bash
./scripts/main.py rotate --file .env --keys API_KEY,DB_PASSWORD
```

### With custom generation:
```bash
./scripts/main.py rotate --file .env --keys API_KEY --algorithm base64 --length 32
```

### Dry run (preview):
```bash
./scripts/main.py rotate --file .env --keys "*" --dry-run
```

### Generate Vault commands:
```bash
./scripts/main.py vault --keys API_KEY,DB_PASSWORD --path secret/data/myapp
```

### Full command reference:
```bash
./scripts/main.py help
```

## Commands

- `rotate`: Rotate secrets in environment files
  - `--file`: Path to .env file (required)
  - `--keys`: Comma-separated keys to rotate, or "*" for all (default: "*")
  - `--algorithm`: Random generation algorithm: hex, base64, uuid, alphanumeric (default: hex)
  - `--length`: Length of generated secret (default: 32)
  - `--backup`: Create backup before modifying (default: true)
  - `--dry-run`: Preview changes without modifying files
  - `--output`: Write to new file instead of modifying original
  
- `vault`: Generate HashiCorp Vault commands
  - `--keys`: Comma-separated keys to generate commands for
  - `--path`: Vault secret path (e.g., "secret/data/myapp")
  - `--engine`: Vault secrets engine (default: "kv")
  - `--method`: Vault method: patch, put (default: "patch")
  
- `validate`: Validate .env file
  - `--file`: Path to .env file
  - `--strict`: Require all values to be non-empty
  
- `history`: Show rotation history (if enabled)
  - `--file`: Path to .env file
  - `--key`: Specific key to show history for

## Output

### Rotation output:
```json
{
  "file": ".env",
  "rotated": ["API_KEY", "DB_PASSWORD"],
  "new_values": {
    "API_KEY": "a1b2c3d4e5f6...",
    "DB_PASSWORD": "x9y8z7w6v5u4..."
  },
  "backup": ".env.backup.20260311",
  "vault_commands": [
    "vault kv patch secret/data/myapp API_KEY=a1b2c3d4e5f6...",
    "vault kv patch secret/data/myapp DB_PASSWORD=x9y8z7w6v5u4..."
  ]
}
```

### Vault commands output:
```bash
# Generated Vault commands for secret rotation:
vault kv patch secret/data/myapp API_KEY=a1b2c3d4e5f6...
vault kv patch secret/data/myapp DB_PASSWORD=x9y8z7w6v5u4...
```

## Limitations

- **No actual Vault integration** - Only generates commands; you must run them manually
- **Local files only** - Cannot rotate secrets in remote secret managers
- **No key distribution** - Does not distribute new secrets to services
- **Basic .env format** - Supports simple KEY=VALUE format; no multiline or complex parsing
- **No encryption** - Generated secrets are shown in plaintext in output
- **History tracking optional** - Requires enabling and may store sensitive data

## Security Considerations

- Always review generated values before use
- Use `--dry-run` to preview changes
- Backups are created by default
- Generated secrets are cryptographically random (using Python's secrets module)
- Consider using a real secret manager for production secrets

## Examples

Rotate all secrets in .env file:
```bash
./scripts/main.py rotate --file .env --keys "*" --backup true
```

Generate Vault commands for specific keys:
```bash
./scripts/main.py vault --keys API_KEY,DB_PASSWORD --path secret/data/production
```

Validate .env file before rotation:
```bash
./scripts/main.py validate --file .env --strict
```

Rotate with custom base64 secrets:
```bash
./scripts/main.py rotate --file .env --keys JWT_SECRET --algorithm base64 --length 64
```

## Installation Notes

Uses Python's built-in `secrets` module for cryptographically secure random generation. No external dependencies required.