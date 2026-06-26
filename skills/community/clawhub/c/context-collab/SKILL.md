---
name: context
description: Multi-agent collaboration protocol engine — shared spaces with auto-injected context, viral propagation, and human annotation workflow. Creates a shared Space per group/channel, auto-injects SPACE.md + TEAM.md + TASK.md into every Agent conversation, and provides 14 tools for reading/writing shared files, managing tasks, members, and annotations.
metadata:
  openclaw:
    type: plugin
    minVersion: "0.9.0"
    config:
      serverUrl:
        type: string
        default: "https://context-server-mj6f.onrender.com"
        description: Context Server URL
      autoInject:
        type: boolean
        default: true
        description: Auto-inject protocol files into system prompt
---

# Context Plugin

Multi-agent collaboration protocol engine for OpenClaw.

## What it does

- **Auto-injects** SPACE.md + TEAM.md + TASK.md into every conversation in a linked group
- **14 Agent Tools** for reading/writing shared files, managing tasks, and annotations
- **5 Slash Commands** for space management (`/ctx_create`, `/ctx_info`, `/ctx_files`, `/ctx_tasks`, `/ctx_team`)
- **Viral propagation** via shareable `/ctx/` URLs
- **Annotation workflow** for human → AI feedback loop

## Installation

```bash
clawhub install context
```

Then add to your `openclaw.json`:

```json
{
  "plugins": {
    "allow": ["context"],
    "entries": {
      "context": {
        "enabled": true,
        "config": {
          "serverUrl": "https://context-server-mj6f.onrender.com"
        }
      }
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `context_create_space` | Create a shared Space for a group |
| `context_lookup_space` | Find the Space linked to a group |
| `context_read_file` | Read a file from the Space |
| `context_write_file` | Write/update a file in the Space |
| `context_list_files` | List all files |
| `context_delete_file` | Delete a file |
| `context_get_protocol` | Get SPACE.md + TEAM.md + TASK.md at once |
| `context_update_task` | Update TASK.md |
| `context_add_member` | Add a team member |
| `context_list_members` | List members |
| `context_get_annotations` | Get human annotations/feedback |
| `context_resolve_annotation` | Mark annotation as resolved |
| `context_search_files` | Full-text search across files |
| `context_notify_member` | Send notification to group |

## Web UI

Human users can browse, edit, and annotate files at:
`https://context-server-mj6f.onrender.com/s`

## Source

https://github.com/luojingwei123/context
