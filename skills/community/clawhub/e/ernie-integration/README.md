# ERNIE Integration for Clawdbot

Complete integration guide for adding Baidu ERNIE 5.0 (Qianfan) models to Clawdbot.

## Overview

This skill provides step-by-step instructions for integrating Baidu's ERNIE 5.0 model:

- **ERNIE 5.0** - Baidu's latest thinking model with 128K context window

## Installation

```bash
clawdbot skills install ernie-integration.skill
```

Or manually install by placing the skill folder in your Clawdbot skills directory.

## Quick Start

### 1. Get API Key

- **Baidu Qianfan Platform**: https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application

### 2. Set Environment Variable

```bash
export ERNIE_API_KEY="bce-v3/ALTAK-your-key-here"
```

### 3. Configure Clawdbot

Add to your `clawdbot.json`:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ernie/ernie-5.0-thinking-preview"
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
          { "id": "ernie-5.0-thinking-preview", "name": "ERNIE 5.0", "contextWindow": 128000 }
        ]
      }
    }
  }
}
```

### 4. Restart and Verify

```bash
clawdbot gateway restart
clawdbot models list
```

## Features

- Complete configuration examples for ERNIE 5.0
- Model aliases for quick switching
- API connection test script
- Troubleshooting guide
- Context window and rate limit specifications

## Available Models

### ERNIE 5.0

| Model | Context Window | Max Input | Max Output | Use Case |
|-------|----------------|-----------|------------|----------|
| `ernie-5.0-thinking-preview` | 128K | 119K | 65536 | Deep thinking, complex reasoning |

### Rate Limits

| Model | RPM | TPM |
|-------|-----|-----|
| `ernie-5.0-thinking-preview` | 60 | 150,000 |

## Usage Examples

### Switch models in chat

```bash
/model ernie/ernie-5.0-thinking-preview
```

### Use model alias

```bash
/model ernie-5.0
```

### Set as default

```bash
clawdbot models set ernie/ernie-5.0-thinking-preview
```

## Testing

Run the connection test script:

```bash
bash scripts/test_ernie_connection.sh
```

This verifies:
- API key is set correctly
- Endpoint is accessible
- Authentication works

## Documentation

- **SKILL.md** - Complete integration guide with step-by-step instructions
- **references/config-examples.md** - Ready-to-use configuration snippets
- **scripts/test_ernie_connection.sh** - API connection tester

## Troubleshooting

### Model not showing in list

```bash
# Check config syntax
clawdbot gateway config.get | grep -A 20 ernie

# Verify API key
echo $ERNIE_API_KEY
```

### Authentication errors

- Ensure API key format is `bce-v3/ALTAK-...`
- Verify key is valid on Qianfan console
- Check correct base URL: `https://qianfan.baidubce.com/v2`

### Connection issues

Test endpoint directly:

```bash
curl -X POST "https://qianfan.baidubce.com/v2/chat/completions" \
  -H "Authorization: Bearer $ERNIE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "ernie-5.0-thinking-preview", "messages": [{"role": "user", "content": "test"}]}'
```

## Resources

- [Baidu Qianfan Documentation](https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html)
- [Qianfan API Reference](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Fm2vrveyu)
- [Clawdbot Model Providers](https://docs.openclaw.ai/concepts/model-providers)

## Contributing

Found an issue or have suggestions? Open an issue or submit a pull request!

## License

MIT
