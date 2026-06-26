---
name: free-ride-prefix-fix
description: Fixed fork of FreeRide: resolves OpenRouter model prefix routing bug for reliable fallbacks. Free AI via OpenRouter with automatic fallback switching.
---

# FreeRide (Prefix Fix) - Free AI for OpenClaw

> 📌 This is a **community fork** of the original [FreeRide](https://clawhub.ai/skills/free-ride) by Shaishav Pidadi.
>
> **What's fixed:** Model ID prefix routing in the `format_model_for_openclaw()` function. The original skill wrote fallback model IDs without the `openrouter/` routing prefix, causing OpenClaw to fail with "Unknown model" errors. This fork ensures all specific models are prefixed with `openrouter/` while preserving the `openrouter/free` smart router ID.

## What This Skill Does

Configures OpenClaw to use **free** AI models from OpenRouter. Sets the best free model as primary, adds ranked fallbacks so rate limits don't interrupt the user, and preserves existing config.

## Prerequisites

1. **OPENROUTER_API_KEY is set:**
   ```bash
   export OPENROUTER_API_KEY="sk-or-v1-..."
   # Or persist it:
   openclaw config set env.OPENROUTER_API_KEY "sk-or-v1-..."
   ```

2. **The `freeride-fix` CLI is installed:**
   ```bash
   cd ~/.openclaw/workspace/skills/free-ride-prefix-fix
   pip install -e .
   ```

## Primary Workflow

```bash
# Step 1: Configure best free model + fallbacks
freeride-fix auto

# Step 2: Restart gateway
openclaw gateway restart
```

## Commands Reference

| Command | When to use it |
|---------|----------------|
| `freeride-fix auto` | Auto-select best free model (most common) |
| `freeride-fix auto -f` | Add fallbacks only, keep current primary |
| `freeride-fix auto -c 10` | More fallbacks (default: 5) |
| `freeride-fix list` | List available free models |
| `freeride-fix list -n 30` | Show more models |
| `freeride-fix switch <model>` | Switch to a specific model |
| `freeride-fix switch <model> -f` | Add as fallback only |
| `freeride-fix status` | Check current config |
| `freeride-fix fallbacks` | Update fallback models |
| `freeride-fix refresh` | Refresh model cache |

**After any config change, run `openclaw gateway restart`.**

## The Bug That Was Fixed

**Before (broken):**
```json
{
  "primary": "openrouter/qwen/qwen3.6-plus-preview:free",  // ✅ had prefix
  "fallbacks": [
    "openrouter/free",                      // ✅ smart router (ID includes prefix)
    "nvidia/nemotron-3-super-120b-a12b:free"  // ❌ missing openrouter/ prefix!
  ]
}
```

**After (fixed):**
```json
{
  "primary": "openrouter/qwen/qwen3.6-plus-preview:free",  // ✅
  "fallbacks": [
    "openrouter/free",                      // ✅ preserved (no double-prefix)
    "openrouter/nvidia/nemotron-3-super-120b-a12b:free"  // ✅ correct routing prefix
  ]
}
```

### Code Change (main.py `format_model_for_openclaw`)

**Original (buggy):**
```python
if with_provider_prefix:
    return f"openrouter/{base_id}"
return base_id  # ❌ fallbacks get NO prefix → "Unknown model" error
```

**Fixed:**
```python
# openrouter/free is already a fully-qualified router ID, don't double-prefix
if model_id in ("openrouter/free", "openrouter/free:free"):
    return "openrouter/free"

# All other specific models need the routing prefix
# Remove existing prefix first, normalize, then add it back
if base_id.startswith("openrouter/"):
    base_id = base_id[len("openrouter/"):]
if append_free and ":free" not in base_id:
    base_id = f"{base_id}:free"

return f"openrouter/{base_id}"  # ✅ always prefixed (except smart router)
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `freeride-fix: command not found` | `cd skills/free-ride-prefix-fix && pip install -e .` |
| `OPENROUTER_API_KEY not set` | Get a free key at https://openrouter.ai/keys |
| Changes not taking effect | `openclaw gateway restart` then `/new` |

## Attribution

- **Original author:** Shaishav Pidadi ([FreeRide](https://github.com/Shaivpidadi/FreeRide))
- **License:** MIT (unchanged from original)
- **Fix by:** rongtianhua (2026-04-01)
