---
name: entity-linker
description: Entity Linker is a Discord channel plugin for OpenClaw that rewrites Entity workspace paths (file:// paths, /home/.../Entity, etc.) into hosted Entity URLs in outgoing messages. The point is to keep agent-to-agent chat clean while still letting humans click through to the underlying workspace. The plugin is small, self-contained, and ships as a single installable OpenClaw plugin.
---

# Entity Linker

Plugin bundle exported from SuperAda.ai for ClawHub discovery.

## Source
- SuperAda page: https://superada.ai/plugins/entity-linker/
- Source URL: https://github.com/h-mascot/Enterprise-Crew-skills/tree/main/plugins/entity-linker
- Category: Operations
- Status: Live

## Install

```bash
openclaw skills install github:h-mascot/Enterprise-Crew-skills/entity-linker && openclaw plugins enable entity-linker
```

## What It Does

Entity Linker is a Discord channel plugin for OpenClaw that rewrites Entity workspace paths (file:// paths, /home/.../Entity, etc.) into hosted Entity URLs in outgoing messages. The point is to keep agent-to-agent chat clean while still letting humans click through to the underlying workspace. The plugin is small, self-contained, and ships as a single installable OpenClaw plugin.

## Verification
```bash
openclaw plugins inspect entity-linker --hooks
```
