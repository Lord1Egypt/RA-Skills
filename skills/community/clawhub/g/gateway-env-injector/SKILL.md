---
name: gateway-env-injector
version: 1.0.0
description: Safely inject API keys from 1Password into macOS LaunchAgent plists using PlistBuddy. Use when running OpenClaw on macOS and storing secrets in 1Password — avoids plaintext keys on disk while keeping LaunchAgent env vars populated. Requires 1Password CLI (op).
metadata:
  {"openclaw": {"emoji": "🔐", "requires": {"bins": ["op", "bash"], "env": ["OP_SERVICE_ACCOUNT_TOKEN"]}, "primaryEnv": "OP_SERVICE_ACCOUNT_TOKEN", "network": {"outbound": true, "reason": "Reads secrets from 1Password via op CLI (1password.com). Writes locally to plist files only."}}}
---

# Gateway Environment Injector

Bake secrets from 1Password into macOS LaunchAgent plists without leaving plaintext keys on disk. Uses `op read` to fetch secrets and `/usr/libexec/PlistBuddy` to inject them directly into the plist's `EnvironmentVariables` block.

## Why This Exists

- `launchctl setenv` doesn't inject into a plist's own `EnvironmentVariables` block
- Environment variables in `.zshrc` aren't available to LaunchAgents
- Plaintext key files are a security risk
- 1Password service accounts provide read-only, rotatable access

## Usage

```bash
bash scripts/inject-gateway-env.sh
```

Reads each key from 1Password, injects into the gateway plist, then restarts the service.

## What It Injects

Configurable list of `op://Vault/Item/field` references mapped to environment variable names. Modify the script's `KEYS` array for your setup.

## Key Lesson

Changing the Node binary path (even to a symlink) can silently revoke macOS TCC permissions. Always keep the gateway plist locked to the Homebrew Cellar path, not an NVM symlink.

## Files

- `scripts/inject-gateway-env.sh` — Injection script with 1Password integration
