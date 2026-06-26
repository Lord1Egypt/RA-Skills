---
name: eo-expert
description: "EO Expert coordination hook - triggers multi-expert workflow when EO tools are called"
homepage: https://github.com/467718584/everything-openclaw
metadata:
  openclaw:
    emoji: "🤖"
    events: ["before_tool_call"]
    requires:
      bins: ["node"]
---

# EO Expert Hook

This hook coordinates the multi-expert collaboration workflow when EO tools are called.

## What It Does

1. Intercepts EO tool calls (tools starting with `eo_`)
2. Logs the tool call for debugging
3. Coordinates with Team Manager if multi-agent mode is enabled
4. Returns control to the tool handler

## Configuration

No configuration required - uses default EO settings.

## Requirements

- Node.js must be installed
- OpenClaw version >= 2026.3.0

## Events

Listens for: `before_tool_call`

## See Also

- [Everything Openclaw](https://github.com/467718584/everything-openclaw)
- [EO Documentation](https://github.com/467718584/everything-openclaw#readme)
