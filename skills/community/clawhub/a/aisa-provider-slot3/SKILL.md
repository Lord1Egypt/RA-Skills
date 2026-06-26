---
name: aisa-provider
description: 'Configure AIsa as an OpenAI-compatible provider endpoint for OpenClaw and related runtimes. Use this skill when the user wants to set `AISA_API_KEY`, point a client at `https://api.aisa.one/v1`, inspect AIsa model IDs, compare routed model options such as Qwen, DeepSeek, Kimi, and Doubao, or troubleshoot provider configuration. Use when: the user needs model routing, provider setup, or Chinese LLM access guidance.'
author: AIsa
version: 1.0.4
license: Apache-2.0
homepage: https://aisa.one
source: https://github.com/baofeng-tech/agent-skills-io/tree/main/targetSkills/aisa-provider
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  env:
  - AISA_API_KEY
metadata:
  aisa:
    emoji: 🤖
    requires:
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  openclaw:
    emoji: 🤖
    requires:
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
---

# AIsa Provider for OpenClaw

> Release note: This package is published for this runtime. References to OpenClaw below describe the original source workflow, a companion runtime, or compatibility guidance unless the skill is explicitly about OpenClaw itself.

This skill is a setup guide for using `AISA_API_KEY` with the AIsa gateway at `https://api.aisa.one/v1`. It documents provider configuration, example model IDs, and verification steps for OpenClaw-compatible runtimes.

This package ships guidance and reference material only. It does not include local onboarding scripts or direct model-runtime code inside the skill bundle.

> ⚠️ All pricing listed below is for reference. Real-time pricing is subject to change — always check https://marketplace.aisa.one/pricing for the latest rates.

## Trust Boundaries

- You provide `AISA_API_KEY` to your local runtime, which then sends model requests to `https://api.aisa.one/v1`.
- Verify current model availability, pricing, partnership claims, and privacy terms with AIsa's official docs before routing sensitive traffic.
- Prefer interactive onboarding or environment-variable setup over pasting real secrets into shell history.

## Quick Setup

### Option 1: Environment Variable (recommended)

```bash
export AISA_API_KEY="your-key-here"
```

If your runtime supports provider auto-discovery, `AISA_API_KEY` may be enough. Otherwise use the explicit config examples below.

### Option 2: Interactive Onboarding (recommended when available)

```bash
openclaw onboard --auth-choice aisa-api-key
```

### Option 3: Manual Config in `~/.openclaw/openclaw.json`

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
            "cost": {
              "input": 1.20,
              "output": 4.80,
              "cacheRead": 0,
              "cacheWrite": 0
            }
          },
          {
            "id": "aisa/qwen-plus-2025-12-01",
            "name": "Qwen Plus",
            "reasoning": true,
            "input": ["text", "image"],
            "contextWindow": 256000,
            "maxTokens": 16384,
            "supportsDeveloperRole": false,
            "cost": {
              "input": 0.30,
              "output": 0.90,
              "cacheRead": 0,
              "cacheWrite": 0
            }
          },
          {
            "id": "aisa/qwen-mt-flash",
            "name": "Qwen MT Flash",
            "reasoning": true,
            "input": ["text"],
            "contextWindow": 256000,
            "maxTokens": 8192,
            "supportsDeveloperRole": false,
            "cost": {
              "input": 0.05,
              "output": 0.30,
              "cacheRead": 0,
              "cacheWrite": 0
            }
          },
          {
            "id": "aisa/deepseek-v3.1",
            "name": "DeepSeek V3.1",
            "reasoning": true,
            "input": ["text"],
            "contextWindow": 131072,
            "maxTokens": 8192,
            "supportsDeveloperRole": false,
            "cost": {
              "input": 0.27,
              "output": 1.10,
              "cacheRead": 0.07,
              "cacheWrite": 0
            }
          },
          {
            "id": "aisa/kimi-k2.5",
            "name": "Kimi K2.5",
            "reasoning": true,
            "input": ["text"],
            "contextWindow": 131072,
            "maxTokens": 8192,
            "supportsDeveloperRole": false,
            "cost": {
              "input": 0.60,
              "output": 2.40,
              "cacheRead": 0,
              "cacheWrite": 0
            }
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

## Official References

- https://aisa.one
- https://aisa.one/docs/api-reference
- https://marketplace.aisa.one/pricing

## Available Models

### Default Models (pre-configured, API-verified ✅)

| Model | Model ID | Best For | Context | Reasoning | Verified |
|-------|----------|----------|---------|-----------|----------|
| Qwen3 Max | `aisa/qwen3-max` | Complex reasoning, flagship tasks | 256K | ✅ | ✅ |
| Qwen Plus | `aisa/qwen-plus-2025-12-01` | Main production model | 256K | ✅ | ✅ |
| Qwen MT Flash | `aisa/qwen-mt-flash` | High-frequency, lightweight tasks | 256K | ✅ | ✅ |
| DeepSeek V3.1 | `aisa/deepseek-v3.1` | Cost-effective reasoning | 128K | ✅ | ✅ |
| Kimi K2.5 | `aisa/kimi-k2.5` | Routed reasoning model, availability varies by catalog | 128K | ✅ | ✅ |

### Kimi K2.5 Notes

If AIsa currently exposes `aisa/kimi-k2.5`, treat it like any other routed model:

- confirm the model ID is still present in `GET /v1/models`
- verify current pricing and retention terms with the latest AIsa and vendor documentation
- prefer a dedicated, revocable API key for provider testing

One practical caveat observed in prior testing:

- some Kimi routes may reject temperatures other than `1.0`

If a request fails because of temperature handling, retry with the model default instead of assuming the model ID is unavailable.

### Additional Models Available via AIsa

Users can add any model supported by AIsa to their config. The full catalog includes **49+ models**:

**Qwen family (8 models):**
- `qwen3-max`, `qwen3-max-2026-01-23`, `qwen-plus-2025-12-01`
- `qwen-mt-flash`, `qwen-mt-lite`
- `qwen-vl-max`, `qwen3-vl-flash`, `qwen3-vl-plus` (vision models)

**DeepSeek (4 models):**
- `deepseek-v3.1`, `deepseek-v3`, `deepseek-v3-0324`, `deepseek-r1`

**Kimi / Moonshot (2 models):**
- `kimi-k2.5`, `kimi-k2-thinking`

**Also available:** Claude series (10), GPT series (9), Gemini series (5), Grok series (2), and more.

**List all available models:**
```bash
curl https://api.aisa.one/v1/models -H "Authorization: Bearer $AISA_API_KEY"
```

## Model ID Versioning

AIsa uses **versioned model IDs** for some models. If you encounter a `503 - No available channels` error, the model ID may need updating.

**Known model ID mappings:**

| Common Name | Correct AIsa Model ID | ❌ Does NOT work |
|-------------|----------------------|------------------|
| Qwen Plus | `qwen-plus-2025-12-01` | `qwen3-plus`, `qwen-plus`, `qwen-plus-latest` |
| Qwen Flash | `qwen-mt-flash` | `qwen3-flash`, `qwen-turbo`, `qwen-turbo-latest` |
| Qwen Max | `qwen3-max` | (works as-is) |
| DeepSeek V3.1 | `deepseek-v3.1` | (works as-is) |
| Kimi K2.5 | `kimi-k2.5` | (works as-is) |

To check the latest available model IDs:
```bash
curl https://api.aisa.one/v1/models -H "Authorization: Bearer $AISA_API_KEY"
```

## Switching Models

In chat (TUI):

```
/model aisa/qwen3-max
/model aisa/deepseek-v3.1
/model aisa/kimi-k2.5
```

Via CLI:

```bash
openclaw models set aisa/qwen3-max
```

## Operational Notes

- Treat pricing, regional routing, partner claims, and latency expectations as time-sensitive vendor information that must be rechecked in the official AIsa docs.
- For high-assurance or regulated use, confirm retention terms, provider contracts, and endpoint ownership directly with AIsa before routing sensitive traffic.

## Troubleshooting

### "503 - No available channels" error
The model ID may be incorrect or outdated. Check the **Model ID Versioning** section above for correct IDs. Common fixes:
- `qwen3-plus` → use `qwen-plus-2025-12-01`
- `qwen3-flash` → use `qwen-mt-flash`

### "Model not found" error
Ensure the model ID uses the `aisa/` prefix in OpenClaw config:
```
✅ aisa/qwen3-max
❌ qwen3-max
```

### Kimi K2.5 "invalid temperature" error
Kimi K2.5 only accepts `temperature=1.0`. If your config sets a different temperature, add a model-specific override or let OpenClaw use the default.

### Kimi K2.5 empty response
In rare cases Kimi K2.5 may return empty content while consuming output tokens. Retry the request — this is typically transient.

### API key not detected
1. Check whether the env var is set without printing the secret:
   `if [ -n "${AISA_API_KEY:-}" ]; then echo "AISA_API_KEY is set"; else echo "AISA_API_KEY is missing"; fi`
2. Or verify in config: `openclaw config get auth.profiles`
3. Re-run onboarding: `openclaw onboard --auth-choice aisa-api-key`

### Streaming not working
AIsa uses the OpenAI-compatible API (`openai-completions`). Ensure your config has:
```json
"api": "openai-completions"
```

### Rate limits or daily caps
Rate limits, quotas, and daily caps can change by provider agreement or account tier. Check the current AIsa documentation or account console instead of assuming a fixed policy.

## Get an API Key

1. Visit https://marketplace.aisa.one/
2. Sign up and create an API key
3. Set it as `AISA_API_KEY` or use the onboarding wizard

## Notes

- AIsa's endpoint is OpenAI-compatible (`https://api.aisa.one/v1`)
- All models support streaming and function calling
- `supportsDeveloperRole` is set to `false` for Qwen models
- Default context window: 256,000 tokens (Qwen) or 131,072 tokens (DeepSeek/Kimi)
- Reasoning (thinking) is enabled for all default models
- Kimi K2.5 requires `temperature=1.0` — other values cause API errors
- Image/Video generation models (WAN) are available but require separate configuration
- AIsa API supports 49+ models total — use the models endpoint to discover all available options
