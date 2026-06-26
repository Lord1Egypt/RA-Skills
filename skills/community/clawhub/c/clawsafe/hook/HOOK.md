---
name: clawsafe-input-hook
description: "Intercepts all user input and blocks malicious content before it reaches the AI agent"
homepage: https://github.com/openclaw/clawSafe
metadata:
  openclaw:
    emoji: "🛡️"
    events: ["message:received", "message:preprocessed", "agent:input"]
    requires:
      bins: ["node"]
---

# clawSafe Input Hook

Security middleware that intercepts all user input before it reaches the AI agent.

## Features

- **Multi-layer Detection**: LLM, Web, API, Supply Chain, Deploy
- **Bilingual Support**: English and Chinese
- **Auto Language Detection**: Returns localized block messages
- **Configurable**: Confidence threshold, enabled layers

## Supported Events

- `message:received` - When message is received
- `message:preprocessed` - After media/link processing
- `agent:input` - Before agent processes input

## What It Does

1. Scans all incoming messages for malicious content
2. Blocks prompt injection, jailbreak attempts, XSS, SQL injection
3. Returns localized block messages (EN/CN)
4. Logs all blocked attempts

## Configuration

Edit `config.json` in the skill directory:

```json
{
  "enabled": true,
  "confidenceThreshold": 0.6,
  "layers": {
    "llm": { "enabled": true },
    "web": { "enabled": true },
    "api": { "enabled": true },
    "supply_chain": { "enabled": true },
    "deploy": { "enabled": true }
  }
}
```

## Detection Layers

| Layer | Threats |
|-------|---------|
| LLM | Prompt Injection, Jailbreak, Prompt Leaking, Encoding |
| Web | SQL Injection, XSS, CSRF, SSRF |
| API | Key Exposure, Rate Limiting, Auth Issues |
| Supply Chain | Dangerous Dependencies |
| Deploy | Environment Leaks, Debug Info |

## Response

If threat detected, returns block message in user's language:

**English:**
```
🛡️ Input blocked by clawSafe

Threats: Prompt Injection, Jailbreak
Confidence: 76%
```

**Chinese:**
```
🛡️ 输入已被 clawSafe 拦截

威胁类型: 提示注入, 越狱攻击
置信度: 76%
```
