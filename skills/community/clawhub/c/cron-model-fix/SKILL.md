---
name: cron-model-fix
description: Diagnose and fix OpenClaw cron job model override issues. Use when cron jobs show "not allowed, falling back to agent defaults" in logs, experience unexpected cloud token burn, have slow run times, or models aren't being applied correctly. Fixes agent model allowlist configuration.
---

# Cron Model Fix

Diagnose and fix OpenClaw cron job model override issues where configured models are rejected and fall back to agent defaults.

## When to Use This Skill

Use when:
- Cron jobs show `"not allowed, falling back to agent defaults"` in gateway logs
- Unexpected cloud token burn on cron jobs configured with local models
- Slow cron run times (60-180s) when local models should be used
- Model overrides in cron jobs aren't being applied
- Need to validate agent model allowlist configuration

## Quick Start

```bash
# Diagnose the issue
openclaw skill run cron-model-fix --diagnose

# Apply the fix (adds missing models to allowlist)
openclaw skill run cron-model-fix --fix --model ollama/qwen3.5:0.8b

# Validate configuration
openclaw skill run cron-model-fix --validate
```

## Root Cause

OpenClaw has **three model configuration layers**. ALL must include the model:

### Layer 1: Provider Model Definition
**Location:** `models.providers.<provider>.models[]`
**Purpose:** Defines model specs (context, costs, capabilities)

### Layer 2: Agent Default Model
**Location:** `agents.defaults.model.primary`
**Purpose:** Default model when none specified

### Layer 3: Agent Model Allowlist ← **COMMON ISSUE**
**Location:** `agents.defaults.models`
**Purpose:** **WHICH MODELS ARE PERMITTED** for agent/cron use

**Problem:** Model exists in Layer 1, but missing from Layer 3 (allowlist).

**Gateway logs show:**
```
{"subsystem":"cron"}
"payload.model 'ollama/qwen3.5:0.8b' not allowed, falling back to agent defaults"
```

## Diagnosis

### Step 1: Check Gateway Logs

```bash
tail -100 /tmp/openclaw/openclaw-*.log | grep -i "not allowed\|falling back"
```

**If you see:** `"payload.model '<model>' not allowed, falling back to agent defaults"`
→ Model is missing from agent allowlist

### Step 2: Check Agent Allowlist

```bash
cat ~/.openclaw/openclaw.json | python3 -c "
import json, sys
config = json.load(sys.stdin)
models = config.get('agents', {}).get('defaults', {}).get('models', {})
print('Allowed models:')
for model in models:
    print(f'  - {model}')
"
```

**Check if your cron model is in the list.** If not, it will be rejected.

### Step 3: Check Cron Job Configuration

```bash
openclaw cron list
```

**Verify:**
- Cron job has `model` specified in payload
- Model format matches allowlist (e.g., `ollama/qwen3.5:0.8b`)

## The Fix

Add the model to `agents.defaults.models` in `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/qwen3.5:cloud",
        "fallbacks": [...]
      },
      "models": {
        "ollama/glm-4.7-flash": {},
        "ollama/kimi-k2.5:cloud": {},
        "ollama/qwen2.5vl:7b": {},
        "ollama/qwen3.5:397b-cloud": {},
        "ollama/qwen3.5:4b-32K": {},
        "ollama/qwen3.5:4b-32k": {},
        "ollama/qwen3.5:9b-128k": {},
        "ollama/qwen3.5:cloud": {},
        "ollama/qwen3.5:0.8b": {},  ← ADD THIS
        "ollama/qwen3.5:2b": {}     ← Optional
      }
    }
  }
}
```

### Manual Fix Steps

1. **Edit config:**
   ```bash
   nano ~/.openclaw/openclaw.json
   ```

2. **Add to `agents.defaults.models`:**
   ```json
   "ollama/qwen3.5:0.8b": {},
   ```

3. **Restart gateway:**
   ```bash
   openclaw gateway restart
   ```

4. **Verify:**
   ```bash
   openclaw cron runs --id <job-id> --limit 3
   ```
   Look for `"model": "qwen3.5:0.8b"` instead of `qwen3.5:cloud`

### Automated Fix Script

Use the included script:

```bash
python3 ~/.npm-global/lib/node_modules/openclaw/skills/cron-model-fix/scripts/add-model-allowlist.py --model ollama/qwen3.5:0.8b
```

## Expected Results

### Before Fix
| Metric | Value |
|--------|-------|
| Model | Cloud fallback |
| Duration | 60-180 seconds |
| Input Tokens | 200K-600K per run |
| Cost | Cloud token burn |

### After Fix
| Metric | Value | Improvement |
|--------|-------|-------------|
| Model | Local (e.g., qwen3.5:0.8b) | ✅ Free |
| Duration | 1-13 seconds | 5-14x faster |
| Input Tokens | 5K-36K | 85-95% reduction |
| Cost | ZERO | 100% savings |

## Validation

After applying fix, verify:

```bash
# Check for model rejection warnings
tail -50 /tmp/openclaw/openclaw-*.log | grep -i "not allowed"

# Should be EMPTY (no warnings)
```

```bash
# Check cron run history
openclaw cron runs --id <job-id> --limit 1

# Should show:
# "model": "qwen3.5:0.8b" (not cloud)
# "durationMs": <15000 (fast)
# "input_tokens": <50000 (low)
```

## Common Issues

### Issue: Model still not working after fix

**Check:**
1. Gateway restarted after config change?
2. Model format matches exactly? (e.g., `ollama/qwen3.5:0.8b` vs `qwen3.5:0.8b`)
3. Model exists in provider config (Layer 1)?

### Issue: Invalid JSON after editing

**Fix:**
```bash
openclaw doctor --fix
```

Or restore from backup:
```bash
cp ~/.openclaw/openclaw.json.backup ~/.openclaw/openclaw.json
```

## Related Skills

- `inbox-optimizer` - Optimizes inbox scanning patterns (mesh-specific)
- `healthcheck` - General OpenClaw system health monitoring

## References

- See `references/model-config-layers.md` for detailed configuration structure
- See `references/troubleshooting-examples.md` for real-world case studies

## Version

1.0.0 - Initial release (2026-03-30)
