---
name: ernie-integration
description: Step-by-step guide for integrating Baidu ERNIE 5.0 (Qianfan) models into Clawdbot. Use when someone asks how to add ERNIE models, configure Baidu Qianfan, or set up ERNIE 5.0 in Clawdbot.
---

# ERNIE Model Integration

Complete guide for adding Baidu ERNIE 5.0 (Qianfan) models to Clawdbot.

## Overview

ERNIE 5.0 is Baidu's latest large language model with deep thinking capabilities:

- **ERNIE 5.0** (`ernie-5.0-thinking-preview`) - Advanced reasoning model with 128K context window via OpenAI-compatible API

## Prerequisites

- Clawdbot installed and configured
- API key from Baidu Qianfan platform (see Getting API Key section)

## Getting API Key

### Baidu Qianfan Platform

1. Visit https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application
2. Register a Baidu Cloud account if you don't have one
3. Navigate to the API Keys section
4. Create a new API key
5. Copy the key (format: `bce-v3/ALTAK-...`)

**Note:** The API key uses Baidu's BCE authentication format.

## Integration Steps

### Step 1: Set environment variable

Add to `~/.bashrc` or `~/.zshrc` for persistence:

```bash
export ERNIE_API_KEY="bce-v3/ALTAK-your-key-here"
source ~/.zshrc  # or source ~/.bashrc
```

**Security note:** Never commit API keys to version control. Rotate keys regularly on the Qianfan console.

### Step 2: Add provider configuration

Edit your `clawdbot.json` config:

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ernie/ernie-5.0-thinking-preview"
      },
      "models": {
        "ernie/ernie-5.0-thinking-preview": {
          "alias": "ernie-5.0"
        }
      }
    }
  },
  "models": {
    "mode": "merge",
    "providers": {
      "ernie": {
        "baseUrl": "https://qianfan.baidubce.com/v2",
        "apiKey": "${ERNIE_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "ernie-5.0-thinking-preview",
            "name": "ERNIE 5.0",
            "contextWindow": 128000,
            "maxTokens": 65536
          }
        ]
      }
    }
  }
}
```

### Step 3: Restart Clawdbot

```bash
clawdbot gateway restart
```

### Step 4: Verify integration

```bash
clawdbot models list
```

You should see ERNIE models in the list.

### Step 5: Use the model

Set as default:
```bash
clawdbot models set ernie/ernie-5.0-thinking-preview
```

Or use model alias in chat:
```bash
/model ernie-5.0
```

## Model Parameters

### ERNIE 5.0 Specifications

| Parameter | Value |
|-----------|-------|
| Model ID | `ernie-5.0-thinking-preview` |
| Context Window | 128K tokens |
| Max Input | 119K tokens |
| Max Output | 1 - 65536 tokens |
| RPM (Rate Per Minute) | 60 |
| TPM (Tokens Per Minute) | 150,000 |

### Supported Request Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (required) |
| `messages` | array | Chat context messages (required) |
| `stream` | boolean | Enable streaming response |
| `temperature` | number | Output randomness (model-specific range) |
| `top_p` | number | Nucleus sampling parameter |
| `max_tokens` | integer | Maximum output tokens |
| `stop` | array | Stop sequences (up to 4 elements) |
| `frequency_penalty` | number | Frequency-based repetition penalty |
| `presence_penalty` | number | Presence-based repetition penalty |

### Thinking Mode Parameters

ERNIE 5.0 supports deep thinking mode:

| Parameter | Type | Description |
|-----------|------|-------------|
| `enable_thinking` | boolean | Enable thinking mode |
| `thinking_budget` | integer | Max thinking chain tokens (default: 16384) |
| `thinking_strategy` | string | `short_think` or `chain_of_draft` |
| `reasoning_effort` | string | `low`, `medium` (default), or `high` |

## Troubleshooting

### Model not appearing in list

Check config syntax:
```bash
clawdbot gateway config.get | grep -A 20 ernie
```

Verify API key is set:
```bash
echo $ERNIE_API_KEY
```

### Authentication errors

- Verify API key format is `bce-v3/ALTAK-...`
- Check key is valid on Qianfan console
- Ensure correct base URL: `https://qianfan.baidubce.com/v2`

### Connection issues

Test API endpoint directly:
```bash
curl -X POST "https://qianfan.baidubce.com/v2/chat/completions" \
  -H "Authorization: Bearer $ERNIE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "ernie-5.0-thinking-preview", "messages": [{"role": "user", "content": "test"}]}'
```

### Rate limit errors

ERNIE 5.0 has the following rate limits:
- RPM: 60 requests per minute
- TPM: 150,000 tokens per minute

If you hit rate limits, reduce request frequency or apply for higher quotas on Qianfan console.

## Model Recommendations

- **ERNIE 5.0** (`ernie/ernie-5.0-thinking-preview`) - Best for complex reasoning tasks, deep analysis, and tasks requiring extensive thinking

## References

- Baidu Qianfan Docs: https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html
- Qianfan API Reference: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Fm2vrveyu
- Clawdbot Model Providers: https://docs.openclaw.ai/concepts/model-providers
