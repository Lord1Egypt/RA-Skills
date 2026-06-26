---
name: asana-remote-mcp
description: Use Asana through mcporter-backed remote MCP tools. Use when working with tasks, projects, portfolios, goals, or team workspaces via the hosted mcp.asana.com server. Tokens are MCP-scoped and issued via Asana's MCP OAuth app.
---

# asana-remote-mcp

Use Asana through `mcporter` backed by the official hosted MCP at `https://mcp.asana.com/v2/mcp`.

## Credential Setup

The OAuth token is injected automatically via `$env:ASANA_MCP_OAUTH_TOKEN` when the user has connected their Asana account through Maverick. Tokens are issued by Asana's MCP app and are scoped to the MCP server only. Never ask the user for a token directly.

## Workflow

1. Verify the server is reachable:
   - `mcporter list asana --schema`
2. Get the user's workspace GID first — most Asana queries are scoped to a workspace.
3. Search or list projects before querying tasks — avoid guessing GIDs.
4. Fetch task details before updating to confirm field names and current values.
5. Confirm before creating, moving, or completing tasks.

## Key Tools

- `get_me` — fetch the authenticated user's profile, email, and workspace list. Always call this first to get the `workspace_gid`.
- `search_tasks` — search tasks across a workspace by keyword, assignee, project, or completion status. Requires `workspace_gid`.
- `get_task` — fetch full details of a single task by `task_gid`, including assignee, due date, notes, and custom fields.
- `create_task` — create a new task in a project or workspace. Requires `workspace_gid`, `name`, and optionally `projects`, `assignee`, `due_on`, `notes`.
- `update_task` — update task fields (name, notes, due date, assignee, completion). Requires `task_gid` and the fields to update.
- `get_tasks_for_project` — list all tasks in a specific project. Requires `project_gid`.
- `get_projects` — list projects in a workspace. Requires `workspace_gid`. Use to resolve a project name to its GID.
- `get_project` — fetch details of a single project by `project_gid`.
- `create_project` — create a new project in a workspace or team.
- `get_subtasks_for_task` — list subtasks of a task. Requires `task_gid`.
- `add_task_to_project` — add an existing task to a project. Requires `task_gid` and `project_gid`.
- `add_followers_to_task` — add followers (users) to a task. Requires `task_gid` and `followers` (array of user GIDs).
- `get_teams_for_workspace` — list teams in a workspace. Use to resolve a team name to its GID when creating projects.

## Tool Selection Guide

- User asks about their tasks or workspace → `get_me` for workspace GID, then `search_tasks`.
- User asks about a specific project → `get_projects` to find GID, then `get_tasks_for_project`.
- User asks to create a task → confirm project and assignee, then `create_task`.
- User asks to mark a task complete → `update_task` with `{"completed": true}`.
- User asks about subtasks → `get_subtasks_for_task`.
- User asks about teams → `get_teams_for_workspace`.

## opt_fields Usage

Most tools accept an `opt_fields` parameter to specify which fields to return (comma-separated). Use it to reduce response size and avoid hitting complexity limits:

- For task lists: `"gid,name,completed,due_on,assignee.name"`
- For task details: `"gid,name,notes,completed,due_on,assignee.name,projects.name,custom_fields"`
- For projects: `"gid,name,color,status,owner.name"`

## Operational Rules

- Always call `get_me` first in a new conversation to get the `workspace_gid` — it is required for most search and list operations.
- Resolve project or task names to GIDs via `get_projects` or `search_tasks` before calling detail endpoints. Never guess GIDs.
- When creating tasks, always specify at least one of `projects` or `workspace` — tasks without a project are in the user's "My Tasks" only.
- Treat `completed: true` on a task as a significant action — confirm with the user before marking tasks done.
- Asana MCP tokens are scoped to the MCP app and may not access all workspaces. If a workspace is missing, the user may need to reconnect.
- If a tool call returns a 401, the token has expired. Instruct the user to reconnect their Asana account in Maverick settings.
- Asana rate limit: 1500 requests per minute. Large list operations with many `opt_fields` count more against this limit.

## Common Errors

- `Not Found (404)` — the GID is wrong or the user lacks access to that resource.
- `Invalid Request (400)` — a required field is missing or a field value is invalid (e.g. bad date format — use `YYYY-MM-DD`).
- `Forbidden (403)` — the token doesn't have permission for this operation.
- `401 Unauthorized` — token expired; user must reconnect in Maverick.
