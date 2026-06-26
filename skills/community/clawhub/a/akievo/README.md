# Akievo Skill for OpenClaw

> Give your OpenClaw agent persistent, structured, human-editable Kanban planning that survives session resets.

## What is Akievo?

Akievo is an AI-native project management tool. This skill connects your OpenClaw agent to Akievo, giving it a **persistent planning layer** — structured Kanban boards with tasks, checklists, dependencies, priorities, and due dates.

Your agent creates the plan. You refine it. The agent adapts. One shared board, two collaborators — one human, one AI. Plans survive session resets, so your agent never loses context.

## Quick Start

### 1. Install the skill

```bash
openclaw skills install akievo
```

### 2. Generate an API key

Go to [akievo.com/account](https://akievo.com/account) → **API Keys** tab → create a key with `boards:read` and `boards:write` scopes.

### 3. Add the key to OpenClaw

```bash
openclaw config set AKIEVO_API_KEY "ak_your_key_here"
```

That's it. Your agent now has persistent planning.

---

## Manual Configuration

If you prefer to configure the MCP server directly, add this to your `openclaw.json`:

```json
{
  "mcpServers": {
    "akievo": {
      "url": "https://mcp.akievo.com",
      "transport": "http",
      "headers": {
        "Authorization": "Bearer YOUR_AKIEVO_API_KEY"
      }
    }
  }
}
```

---

## Available Tools (29 MCP tools)

| Category | Tools |
|---|---|
| **Boards** | `list_workspaces`, `list_boards`, `get_board`, `create_board`, `create_board_with_tasks` |
| **Cards** | `create_card`, `update_card`, `move_card`, `complete_card`, `delete_card`, `get_card` |
| **Lists** | `create_list` |
| **Comments** | `add_comment` |
| **Checklists** | `add_checklist_item`, `toggle_checklist_item`, `delete_checklist_item` |
| **Blocking** | `block_card`, `unblock_card` |
| **Dependencies** | `list_dependencies`, `create_dependency`, `delete_dependency`, `bulk_create_dependencies` |
| **Attachments** | `add_attachment` |
| **Assignees** | `list_board_members`, `add_assignee`, `remove_assignee` |
| **Labels** | `list_labels`, `assign_label`, `unassign_label` |

---

## How It Works

```
You ←→ OpenClaw Agent ←→ Akievo MCP Server ←→ Akievo Database
                                                      ↕
                                    You edit the same board in the Akievo web app
```

The agent uses Akievo as its persistent memory. Plans, progress, and context survive session resets. You can view and edit the same boards through the [Akievo web app](https://akievo.com) at any time — the agent will pick up your changes on its next session.

---

## Example Prompts

Just tell your agent what you want to accomplish:

- *"I want to launch my SaaS product in 3 months — create a plan"*
- *"Plan a content pipeline: weekly newsletter, daily social posts, and monthly SEO articles"*
- *"Build and ship an open-source CLI tool — plan the architecture, development, testing, and launch"*
- *"Check my project board and tell me what's next"*
- *"Mark the research task as complete and unblock the design phase"*
- *"I changed the timeline — update the plan to ship by end of Q3"*

The agent will create and manage boards in your Akievo account, maintaining a structured plan that persists across sessions.

---

## Security

- **Scoped API keys** — only grant the permissions you need
- **Audit trail** — all agent actions are logged in the board activity feed
- **Rate limiting** — enforced server-side
- **Your data stays yours** — stored in your Akievo account, not shared with OpenClaw

---

## Files in This Repo

| File | Purpose |
|---|---|
| `SKILL.md` | Agent system prompt — instructions the agent follows when using Akievo |
| `skill.yaml` | Skill manifest — metadata, env requirements, MCP server config |
| `mcp-config.json` | Standalone MCP server configuration for manual setup |

---

## Links

- [Akievo](https://akievo.com) — AI-native project management
- [Setup Guide](https://akievo.com/openclaw-setup) — step-by-step instructions
- [API Documentation](https://akievo.com/api-docs) — REST API reference
- [MCP Server](https://mcp.akievo.com) — live MCP endpoint
