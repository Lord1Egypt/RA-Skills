---
name: env-loader
description: "Shell-agnostic .env file loader. Generates a POSIX-compatible script to safely load environment variables from .env files across bash, zsh, dash, and ash. Use when: deploying apps that rely on .env files, fixing environment variable issues caused by shell differences, or writing deployment scripts that need to work across multiple shell environments."
---

# Env Loader

Generates and validates POSIX-compatible `.env` loading scripts that work consistently across bash, zsh, dash, and ash.

## Problem It Solves

`source .env` behaves differently across shells:
- **zsh**: Strips quotes from values correctly
- **bash/dash**: Preserves quotes as part of the value (`"value"` → includes the quotes)
- **All shells**: `source` only assigns, does not `export` — child processes can't see the variables

This causes silent failures in deployment when `.env` files contain quoted values or special characters.

## Usage

### Generate the Loader Script

Run the bundled script or use the template:

```bash
bash ~/.openclaw/skills/env-loader/scripts/generate-loader.sh /path/to/project
```

This creates `load-env.sh` in the target directory.

### Use in Deployment Scripts

```bash
# Instead of: source .env
# Use:
. ./load-env.sh .env
```

### Validate an Existing .env File

```bash
bash ~/.openclaw/skills/env-loader/scripts/validate-env.sh /path/to/.env
```

Checks for common issues: unquoted special characters, inline comments, non-POSIX variable names.

## Key Design Principles

1. **POSIX-only syntax** — no bashisms, no zsh-isms, works in dash/ash
2. **Manual key=value parsing** — never `source` or `eval` the .env file directly
3. **Explicit quote stripping** — removes surrounding single or double quotes consistently
4. **Key validation** — only allows `[A-Za-z_][A-Za-z0-9_]*` as variable names
5. **Explicit export** — every parsed variable is exported for child processes

## References

See `references/env-pitfalls.md` for a detailed catalog of shell-specific .env parsing pitfalls.
