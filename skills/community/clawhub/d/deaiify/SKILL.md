---
name: deaiify
description: "Ban LLM em-dashes and en-dashes before delivery, rewrite via embedded LLM."
homepage: https://github.com/shawnpetros/deaiify
metadata:
  {
    "openclaw":
      {
        "emoji": "🚫",
        "plugin": true
      }
  }
---

# deAIify Plugin

Enforces the "no em dashes" rule across all output by intercepting messages, detecting U+2013 (en dash) and U+2014 (em dash), and forcing a rewrite turn via embedded LLM correction.

## What it does

- Detects U+2013 and U+2014 in outbound messages
- Calls embedded LLM to rewrite without dashes (preserves meaning, tone, style)
- Returns corrected output to user
- Never touches U+002D (hyphen-minus in code)
- Excludes content inside code blocks and inline code

## How it works

1. `before_agent_reply` intercepts the completed assistant text before delivery
2. Detects banned dash characters outside of code blocks
3. Calls `runEmbeddedPiAgent` with a restructuring prompt
4. Verifies the rewrite is sane (word count and length checks)
5. Returns the rewritten reply

## Installation

```bash
openclaw plugin install deaiify
```

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `rewriteTimeoutMs` | integer | `15000` | Timeout in ms for the embedded rewrite call |

The plugin uses the session's default model for rewrites. No model config needed.
