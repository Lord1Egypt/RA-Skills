# AIsa Provider Configuration Examples

## Minimal Setup

If your runtime supports provider auto-discovery, setting the environment variable may be enough:

```bash
export AISA_API_KEY="sk-aisa-xxxxx"
```

## Explicit Provider Block

Use an explicit provider config when you want the runtime to point at `https://api.aisa.one/v1` directly.

```json
{
  "models": {
    "providers": {
      "aisa": {
        "baseUrl": "https://api.aisa.one/v1",
        "apiKey": "${AISA_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "aisa/qwen3-max",
            "name": "Qwen3 Max",
            "reasoning": true,
            "input": ["text", "image"],
            "contextWindow": 256000,
            "maxTokens": 16384,
            "supportsDeveloperRole": false,
            "cost": { "input": 1.20, "output": 4.80 }
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "aisa/qwen3-max"
      }
    }
  }
}
```

## Lightweight Default

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "aisa/qwen-mt-flash"
      }
    }
  }
}
```

## Kimi-Focused Default

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "aisa/kimi-k2.5"
      }
    }
  }
}
```

> Note: if Kimi returns a temperature-related error, remove any custom temperature override or set that model to `1.0`.

## Multi-Provider Merge

If your runtime supports provider merge mode, you can keep another provider as the default while still registering AIsa:

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "aisa": {
        "baseUrl": "https://api.aisa.one/v1",
        "apiKey": "${AISA_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "aisa/qwen3-max",
            "name": "Qwen3 Max",
            "reasoning": true,
            "input": ["text", "image"],
            "contextWindow": 256000,
            "maxTokens": 16384,
            "supportsDeveloperRole": false,
            "cost": { "input": 1.20, "output": 4.80 }
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-5"
      }
    }
  }
}
```

## Optional Fallback Guidance

Persistent fallback chains can route later traffic through models you did not intend to use.

If you add fallbacks:

- keep the list short
- use only models you are comfortable routing sensitive work through
- re-check the final runtime config after setup

## Model ID Quick Reference

| Common Name | Example AIsa Model ID | Notes |
|-------------|-----------------------|-------|
| Qwen3 Max | `aisa/qwen3-max` | General flagship model |
| Qwen Plus | `aisa/qwen-plus-2025-12-01` | Versioned ID |
| Qwen MT Flash | `aisa/qwen-mt-flash` | Lightweight option |
| DeepSeek V3.1 | `aisa/deepseek-v3.1` | Cost-sensitive reasoning |
| Kimi K2.5 | `aisa/kimi-k2.5` | Verify availability and temperature handling |
