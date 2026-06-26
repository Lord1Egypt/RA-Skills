---
name: default-model
description: Set the default model persistently via /default_model command with Telegram interactive picker
metadata:
  openclaw:
    requires:
      bins: []
---

# Default Model Plugin

Set the default model persistently via `/default_model` command. Changes are written to the config file and survive gateway restarts.

## Features

- `/default_model` — Show current default model from config
- `/default_model <model>` — Set default model (e.g. `/default_model openrouter/xiaomi/mimo-v2-pro`)
- Telegram interactive picker — Tap provider → model → auto-persist

## How it works

- Writes to `agents.defaults.model.primary` in the OpenClaw config file
- New sessions will use the configured default model
- Current session model is unchanged (use `/model` for session-level override)

## Installation

```bash
openclaw plugins install clawhub:default-model
```

## Source

https://github.com/jkyotnfjfbjnknh/openclaw-default-model
