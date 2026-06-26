# Context Plugin

Multi-agent collaboration protocol engine for OpenClaw.

## What it does

- **Auto-injects** SPACE.md + TEAM.md + TASK.md into every conversation in a linked group
- **14 Agent Tools** for reading/writing shared files, managing tasks, and annotations
- **5 Slash Commands** for space management
- **Viral propagation** via shareable URLs
- **Annotation workflow** for human → AI feedback loop

## Installation

```bash
clawhub install context
```

Or manually copy to your OpenClaw extensions directory.

## Requirements

- Context Server running (default: http://localhost:3100)
- See [server setup](https://github.com/luojingwei123/context)

## Configuration

In `openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "context": {
        "enabled": true,
        "config": {
          "serverUrl": "http://localhost:3100",
          "autoInject": true
        }
      }
    }
  }
}
```
