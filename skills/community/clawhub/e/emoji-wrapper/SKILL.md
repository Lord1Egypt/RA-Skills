---
name: emoji-wrapper
description: Wrapper skill for local-auto-emoji - intercepts messages with [markers] and sends emoji images
version: 1.0.0
author: 阿狸
tags:
  - emoji
  - wrapper
  - local-auto-emoji
---

# Emoji Wrapper Skill

This skill wraps `local-auto-emoji` to automatically process emoji markers in messages.

## How it works

- Intercepts all incoming messages
- Detects `[标记]` patterns (e.g., `[可爱]`, `[眨眼]`)
- Replaces them with actual emoji images (MEDIA instructions)
- Sends both text and images back to user

## Configuration

Add to your OpenClaw config:

```yaml
skills:
  - "emoji-wrapper"
```

No other configuration needed.

## Dependencies

- `local-auto-emoji` skill must be installed and working
- User must have generated emoji pack (or will use fallback static emojis)
