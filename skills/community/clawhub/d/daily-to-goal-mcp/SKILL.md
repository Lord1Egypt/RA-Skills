---
name: daily-to-goal-mcp
description: Connect to Daily-to-Goal (D2G) platform via MCP to manage goals, tasks, entities, and team performance. Use when the user wants to interact with their D2G platform — creating/updating/listing goals, managing tasks, tracking team performance, or querying entities. Requires a D2G account and API key. Triggers on phrases like "manage my goals", "create a task", "show team performance", "D2G", "daily to goal", "goal tracking".
metadata:
  openclaw:
    requires:
      env:
        - DTG_API_KEY
---

# Daily-to-Goal MCP Integration

Connect your AI assistant to [Daily-to-Goal](https://h5.dd-up.com/) via MCP to manage goals, tasks, and team performance.

## Setup

### 1. Get Your API Key

1. Visit [https://h5.dd-up.com/](https://h5.dd-up.com/) and sign up or log in
2. Go to Settings → API Keys
3. Generate a new API key (format: `dtg_live_...`)
4. Save the key — it is shown only once

### 2. Configure MCP Server

Add to your OpenClaw / Claude Desktop MCP config:

```json
{
  "mcpServers": {
    "daily-to-goal": {
      "command": "npx",
      "args": ["@daily-to-goal/mcp-server"],
      "env": {
        "DTG_API_KEY": "dtg_live_your_key_here"
      }
    }
  }
}
```

Replace `DTG_API_KEY` with your actual key.

> **Security:** Never commit your API key to version control. Use environment variables or a secrets manager.

## Available Tools (18)

### Goal Management (6)
| Tool | Description |
|------|-------------|
| `goals_list` | List goals with filters (status, date range, parent) |
| `goals_create` | Create a goal (supports hierarchy via parentId) |
| `goals_update` | Update goal details |
| `goals_delete` | Delete a goal |
| `goals_add_progress` | Add manual progress entry |
| `goals_get_hierarchy` | Get full goal tree from a root goal |

### Task Management (5)
| Tool | Description |
|------|-------------|
| `tasks_list` | List tasks with filters (status, assignee, goal) |
| `tasks_create` | Create a task (optionally linked to a goal) |
| `tasks_update` | Update task details |
| `tasks_complete` | Mark a task as completed |
| `tasks_approve` | Approve a task (manager/admin only) |

### Entity Management (4)
| Tool | Description |
|------|-------------|
| `entities_list` | List entities (assets) with filters |
| `entities_create` | Create a new entity |
| `entities_update` | Update entity details |
| `entities_delete` | Delete an entity |

### Team Insights (3)
| Tool | Description |
|------|-------------|
| `team_members` | List team members with stats |
| `team_performance` | Get team performance metrics |
| `team_leaderboard` | Get team rankings |

## Resources (read-only URI access)

- `dtg://goals/{goalId}` — Goal details
- `dtg://goals/{goalId}/hierarchy` — Full goal tree
- `dtg://tasks/{taskId}` — Task details
- `dtg://goals/{goalId}/tasks` — Tasks under a goal
- `dtg://team/members` — Team member list
- `dtg://team/performance` — Team performance metrics
- `dtg://entities/{entityId}` — Entity details

## Permissions (RBAC)

| Role | Read | Write own | Write team | Approve |
|------|------|-----------|------------|---------|
| Admin | All | All | All | Yes |
| Manager | All | Yes | Yes | Yes |
| Member | All | Yes | No | No |

## API Key Scopes

`goals:read`, `goals:write`, `tasks:read`, `tasks:write`, `entities:read`, `entities:write`, `team:read`, `datasets:read`

## Troubleshooting

- **Authentication failed**: Verify your API key is correct and not expired
- **Permission denied**: Check your user role and API key scopes
- **Resource not found**: Confirm the resource belongs to your tenant

For detailed API key management and security practices, see [references/security.md](references/security.md).
