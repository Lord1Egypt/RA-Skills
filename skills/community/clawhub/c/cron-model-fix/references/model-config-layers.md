# OpenClaw Model Configuration Layers

OpenClaw uses a three-layer model configuration system. Understanding all three is critical for troubleshooting model override issues.

## Layer 1: Provider Model Definition

**Location:** `models.providers.<provider>.models[]`

**Purpose:** Defines what models exist in the system and their technical specifications.

**Structure:**
```json
{
  "models": {
    "providers": {
      "ollama": {
        "models": [
          {
            "id": "qwen3.5:0.8b",
            "name": "qwen3.5:0.8b",
            "reasoning": false,
            "input": ["text"],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 16384
          },
          {
            "id": "qwen3.5:cloud",
            "name": "qwen3.5:cloud",
            "reasoning": true,
            "input": ["text", "image"],
            "cost": {
              "input": 0.003,
              "output": 0.015,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 256000
          }
        ]
      }
    }
  }
}
```

**What it controls:**
- Model capabilities (text, image, reasoning)
- Context window size
- Token costs
- Provider association

**If missing:** Model cannot be used at all - doesn't exist in system.

---

## Layer 2: Agent Default Model

**Location:** `agents.defaults.model`

**Purpose:** Specifies which model to use by default and the fallback chain.

**Structure:**
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/qwen3.5:cloud",
        "fallbacks": [
          "ollama/qwen3.5:397b-cloud",
          "ollama/qwen3.5:4b-32K",
          "ollama/qwen3.5:cloud",
          "ollama/kimi-k2.5:cloud",
          "ollama/qwen3.5:9b-128k",
          "ollama/qwen2.5vl:7b"
        ]
      }
    }
  }
}
```

**What it controls:**
- Default model when none specified
- Fallback order if primary unavailable
- Agent-level model preference

**If missing:** Uses system default (usually cloud model).

---

## Layer 3: Agent Model Allowlist ← **CRITICAL**

**Location:** `agents.defaults.models`

**Purpose:** **WHICH MODELS ARE PERMITTED** for agent and cron job usage.

**Structure:**
```json
{
  "agents": {
    "defaults": {
      "models": {
        "ollama/glm-4.7-flash": {},
        "ollama/kimi-k2.5:cloud": {},
        "ollama/qwen2.5vl:7b": {},
        "ollama/qwen3.5:397b-cloud": {},
        "ollama/qwen3.5:4b-32K": {},
        "ollama/qwen3.5:4b-32k": {},
        "ollama/qwen3.5:9b-128k": {},
        "ollama/qwen3.5:cloud": {},
        "ollama/qwen3.5:0.8b": {},  ← MUST BE HERE
        "ollama/qwen3.5:2b": {}
      }
    }
  }
}
```

**What it controls:**
- **Model permissions** for agents and cron jobs
- Which models can be explicitly selected
- Security/policy enforcement

**If missing:** Model is **REJECTED** with:
```
{"subsystem":"cron"}
"payload.model '<model>' not allowed, falling back to agent defaults"
```

**Silent fallback:** Cron jobs fall back to agent default (usually cloud) WITHOUT explicit error in cron config.

---

## Validation Flow

When a cron job specifies a model:

1. **Check Layer 1:** Does model exist in provider config?
   - ❌ No → Error: "Model not found"
   - ✅ Yes → Continue

2. **Check Layer 3:** Is model in agent allowlist?
   - ❌ No → **Silent fallback** to agent default + log warning
   - ✅ Yes → Use specified model

3. **Check Layer 2:** If fallback needed, what's the default?
   - Use `agents.defaults.model.primary`

---

## Common Mistakes

### Mistake 1: Only Adding to Layer 1

```json
// ✅ Model exists in provider config
"models": {
  "providers": {
    "ollama": {
      "models": [
        { "id": "qwen3.5:0.8b", ... }
      ]
    }
  }
}

// ❌ But missing from agent allowlist
"agents": {
  "defaults": {
    "models": {
      "ollama/qwen3.5:cloud": {}
      // qwen3.5:0.8b NOT HERE → REJECTED
    }
  }
}
```

**Result:** Model rejected, falls back to cloud.

### Mistake 2: Wrong Format

```json
// Config has:
"agents": {
  "defaults": {
    "models": {
      "qwen3.5:0.8b": {}  // No provider prefix
    }
  }
}

// Cron job uses:
"model": "ollama/qwen3.5:0.8b"  // With provider prefix
```

**Result:** Format mismatch → rejection.

**Fix:** Use consistent format (with or without provider prefix).

### Mistake 3: Not Restarting Gateway

After editing config, gateway must restart to reload configuration.

**Symptom:** Config updated but cron still using old model.

**Fix:**
```bash
openclaw gateway restart
```

---

## Troubleshooting Checklist

1. **Check logs for rejection warnings:**
   ```bash
   tail -100 /tmp/openclaw/openclaw-*.log | grep -i "not allowed"
   ```

2. **Verify model in all 3 layers:**
   ```bash
   cat ~/.openclaw/openclaw.json | python3 -c "
   import json, sys
   config = json.load(sys.stdin)
   
   # Layer 1
   models = [m['id'] for m in config['models']['providers']['ollama']['models']]
   print('Layer 1 (Provider):', 'qwen3.5:0.8b' in models)
   
   # Layer 3
   allowlist = config['agents']['defaults']['models'].keys()
   print('Layer 3 (Allowlist):', 'ollama/qwen3.5:0.8b' in allowlist)
   "
   ```

3. **Check cron run history:**
   ```bash
   openclaw cron runs --id <job-id> --limit 3
   ```
   Look for actual model used vs. configured model.

4. **Restart gateway:**
   ```bash
   openclaw gateway restart
   ```

---

## Case Study: 180x Speedup

**Problem:** Inbox processor cron job burning 600K tokens, 180s timeouts.

**Config showed:**
```json
"payload": {
  "model": "ollama/qwen3.5:0.8b"
}
```

**Logs showed:**
```
"payload.model 'ollama/qwen3.5:0.8b' not allowed, falling back to agent defaults"
```

**Root cause:** Model missing from Layer 3 (allowlist).

**Fix:** Added `"ollama/qwen3.5:0.8b": {}` to `agents.defaults.models`

**Result:**
- Model: Cloud → Local (qwen3.5:0.8b)
- Duration: 180s → <1s (180x faster)
- Tokens: 600K → ~500 (99.9% reduction)
- Cost: Cloud burn → FREE

---

## Best Practices

1. **Always add to Layer 3** when configuring new models for cron jobs
2. **Use consistent format** (provider prefix or not) across all layers
3. **Restart gateway** after config changes
4. **Check logs** for silent fallback warnings
5. **Validate with `openclaw cron runs`** to confirm actual model usage

---

**Version:** 1.0.0 (2026-03-30)
**Author:** Pixie + Kluebot collaboration
