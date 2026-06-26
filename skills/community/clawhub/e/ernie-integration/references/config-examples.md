# Configuration Examples

Complete configuration examples for ERNIE integration scenarios.

## Minimal Configuration

```json5
{
  "models": {
    "mode": "merge",
    "providers": {
      "ernie": {
        "baseUrl": "https://qianfan.baidubce.com/v2",
        "apiKey": "${ERNIE_API_KEY}",
        "api": "openai-completions",
        "models": [
          { "id": "ernie-5.0-thinking-preview", "name": "ERNIE 5.0" }
        ]
      }
    }
  }
}
```

## Full Configuration with Details

```json5
{
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
            "maxTokens": 65536,
            "cost": {
              "input": 0.000006,
              "output": 0.000024,
              "cacheRead": 0,
              "cacheWrite": 0
            }
          }
        ]
      }
    }
  }
}
```

## Configuration with Alias

```json5
{
  "agents": {
    "defaults": {
      "models": {
        "ernie/ernie-5.0-thinking-preview": {
          "alias": "ernie-5.0",
          "description": "Baidu ERNIE 5.0 thinking model"
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

## Multi-Model Setup with Failover

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ernie/ernie-5.0-thinking-preview",
        "fallback": [
          "anthropic/claude-sonnet-4-5"
        ]
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
          { "id": "ernie-5.0-thinking-preview", "name": "ERNIE 5.0", "contextWindow": 128000 }
        ]
      }
    }
  }
}
```

## Environment Variables Setup

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export ERNIE_API_KEY="bce-v3/ALTAK-your-key-here"
```

Then reload:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

**Security note:** Never commit API keys to version control. Rotate keys regularly on the Qianfan console.

## Testing Configuration

### Verify config syntax

```bash
clawdbot gateway config.get
```

### List available models

```bash
clawdbot models list
```

### Test API connection

```bash
curl -X POST "https://qianfan.baidubce.com/v2/chat/completions" \
  -H "Authorization: Bearer $ERNIE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ernie-5.0-thinking-preview",
    "messages": [
      {"role": "user", "content": "Hello"}
    ],
    "max_tokens": 100
  }'
```

### Test with streaming

```bash
curl -X POST "https://qianfan.baidubce.com/v2/chat/completions" \
  -H "Authorization: Bearer $ERNIE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ernie-5.0-thinking-preview",
    "messages": [
      {"role": "user", "content": "Hello"}
    ],
    "stream": true,
    "max_tokens": 100
  }'
```

### Switch model in chat

```
/model ernie/ernie-5.0-thinking-preview
```

Or use alias:
```
/model ernie-5.0
```
