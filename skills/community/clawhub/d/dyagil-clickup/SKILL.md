---
name: dyagil-clickup
description: Track tasks in ClickUp from an AI agent — check open tasks before starting work, log completed work after, and capture future ideas. Use whenever the user asks for something non-trivial or your agent finishes a meaningful action and needs persistent task tracking outside its memory files.
version: 1.0.0
license: MIT
author: dyagil
---

# ClickUp Task Tracking for AI Agents

> This skill is tuned for a specific personal ClickUp workspace, but the patterns generalize. Fork it and edit the list IDs in the **Configuration** section below.

## Principle

ClickUp is the **persistent task store** that lives next to your agent's daily memory files. Use it for active work, completed work, and future ideas — anything the user might later want to ask "what's open?" or "what did you finish this week?" about.

## Iron Rules

### Before any meaningful request

Before starting non-trivial work, **check if a relevant task is already open**:

```bash
cu list todo      # open tasks
cu search "term"  # quick fuzzy search
```

**Do check when:**
- The user asks for a complex action (build a feature, fix a bug, add a capability).
- They say "remember this" / "write that down".
- An idea comes up that isn't urgent but worth keeping.

**Don't bother when:**
- Simple info questions ("what time is it", "what did we do yesterday").
- Quick chat-style replies.
- Single-turn requests that finish in the same response.

### After any meaningful request

When done, **log the result**:

```bash
# Add a new task
cu add "task description" --desc "full details" --priority 2

# Close one
cu done <task_id>
```

Priority scale:
- `1` = Urgent (emergency)
- `2` = High (important feature / critical bug)
- `3` = Normal (default)
- `4` = Low (nice-to-have / future idea)

## Lists

| List | Purpose |
|---|---|
| **todo** | Open — what needs doing / in progress |
| **done** | Completed work. On ClickUp Free, `cu done` flips status to `complete` instead of moving lists (free plan blocks cross-list moves). `cu list done` shows all completed items across lists. |
| **ideas** | Future ideas, "maybe one day" features |

## Commands

```bash
cu list                   # default: todo
cu list done              # completed
cu list ideas             # future ideas
cu list all               # everything

cu add "task name"                 # adds to todo
cu add "idea"      --list ideas
cu add "critical bug" --priority 1

cu done <id-or-name>      # close task
cu search "term"
cu spaces                 # debug: show workspace structure
```

## Recommended Patterns

### Pattern 1 — New request from the user

1. User: "Add feature X to project Y"
2. Agent: `cu search "X"` or `cu list todo` first — maybe already tracked?
3. If not: `cu add "X" --priority 2`
4. Do the work.
5. When done: `cu done <id>`

### Pattern 2 — An idea surfaces mid-conversation

User: "It would be nice if Y existed someday."
- Agent: `cu add "Y" --list ideas --priority 4`
- Continue the conversation without breaking flow.

### Pattern 3 — Bug fixed inline

While doing other work you discover and fix a bug:
- After the fix: `cu add "[FIXED] bug in sync flow" --list done`

## Configuration

Before using this skill, edit `~/.openclaw/credentials/clickup/config.json` (or `cu.cjs:DEFAULT_CONFIG`) with **your** workspace IDs:

```json
{
  "teamId":   "<your-team-id>",
  "spaceId":  "<your-space-id>",
  "folderId": "<your-folder-id>",
  "lists": {
    "todo":  "<list-id-for-active>",
    "done":  "<list-id-for-completed>",
    "ideas": "<list-id-for-ideas>"
  }
}
```

Get these by running `cu spaces` after setting your token — it prints the full structure.

## Credentials

- **Token:** store at `~/.openclaw/credentials/clickup/api_token` (`chmod 600`).
- **Config:** `~/.openclaw/credentials/clickup/config.json` (optional override).
- **CLI:** `~/bin/cu` symlinked to your local `cu.cjs` (Node.js, plain `https`, no dependencies).

Get an API token at: https://clickup.com/api → Apps → Generate.

## API Notes

- ClickUp returns `task.id` without prefix (e.g. `86exjx19r`). The web app adds `t/` in the URL: `https://app.clickup.com/t/86exjx19r`.
- Free tier blocks moving tasks between lists. Close-in-place by setting status to `complete` instead.

## ClickUp vs Daily Memory

These complement each other:

| | Daily memory (`memory/YYYY-MM-DD.md`) | ClickUp |
|---|---|---|
| What | Free-form journal, in-the-moment | Formal task list |
| Content | "Talked to X", "debated Y", moments | "Need to build X", "fixed bug Z" |
| Who reads it | Agent | Agent + user (in ClickUp app) |
| Frequency | Continuous during conversation | Only for meaningful actions |

**Rule of thumb:** if the user might ask "what did you finish this week?", it belongs in ClickUp.
