---
name: clawmind
description: "Cloud workflow cache for OpenClaw. Reduces token usage by reusing verified automation patterns."
metadata:
  openclaw:
    emoji: "🧠"
---

# ClawMind

Cloud workflow registry for OpenClaw agents.

## What It Does

Caches successful automation workflows so agents can reuse them instead of regenerating from scratch.

**Benefits:**
- Lower token usage (up to 80% reduction)
- Faster execution (cached workflows run instantly)
- Auto-updating (workflows refresh when websites change)

## How It Works

1. Intercepts user intent before LLM processing
2. Queries cloud for matching cached workflow
3. If found: executes directly
4. If not found: normal LLM flow, then contributes successful result

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `cloud_endpoint` | string | `https://api.clawmind.dev` | Cloud API endpoint |
| `enabled` | boolean | `true` | Enable/disable interception |
| `auto_contribute` | boolean | `true` | Auto-contribute successful workflows |
| `timeout_ms` | number | `300` | API timeout (ms) |

## Installation

```bash
npx clawhub install ainclaw-cloudmind
```

## Privacy

- All PII stays local
- Only workflow patterns are shared
- Full sanitization before upload

## License

MIT-0