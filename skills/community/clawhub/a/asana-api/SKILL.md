---
name: asana
description: |
  Asana API integration with managed OAuth. Access tasks, projects, workspaces, users, and manage webhooks. Use this skill when users want to manage work items, track projects, or integrate with Asana workflows. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Asana

Access the Asana API with managed OAuth authentication. Manage tasks, projects, workspaces, users, and webhooks for work management.

## Quick Start

**CLI:**

```bash
maton asana task list --project <project-gid>
```

```bash
maton api '/asana/api/1.0/tasks?project=PROJECT_GID'
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/asana/api/1.0/tasks?project=PROJECT_GID')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/asana/{native-api-path}
```

Maton proxies requests to `app.asana.com` and automatically injects your OAuth token.

## Installation

**NPM:**
```bash
npm install -g @maton-ai/cli
```

**Homebrew:**
```bash
brew install maton-ai/cli/maton
```

## Authentication

**CLI:**

```bash
maton login                          # Opens browser for API key
maton login --interactive            # Skip browser, paste API key directly
maton whoami                         # Show current auth state
```

**Manual:**

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key
4. Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

## Connection Management

Manage your Asana OAuth connections at `https://api.maton.ai`.

### List Connections

**CLI:**

```bash
maton connection list asana --status ACTIVE
```

```bash
maton api -X GET /connections -f app=asana -f status=ACTIVE
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=asana&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

**CLI:**

```bash
maton connection create asana
```

```bash
maton api /connections -f app=asana
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'asana'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

**CLI:**

```bash
maton connection view {connection_id}
```

```bash
maton api /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "asana",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

**CLI:**

```bash
maton connection delete {connection_id}
```

```bash
maton api -X DELETE /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Asana connections, specify which one to use:

**CLI:**

```bash
maton asana task list --project <project-gid> --connection {connection_id}
```

```bash
maton api /asana/api/1.0/tasks?project=PROJECT_GID --connection {connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/asana/api/1.0/tasks?project=PROJECT_GID')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always specify the connection to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to tasks, projects, workspaces, users, and manage webhooks within the connected Asana account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

### Tasks

#### Get Multiple Tasks

```bash
GET /asana/api/1.0/tasks
```

Query parameters:
- `project` - Project GID to filter tasks
- `assignee` - User GID or "me" for assigned tasks
- `workspace` - Workspace GID (required if no project specified)
- `completed_since` - ISO 8601 date to filter tasks completed after this date
- `opt_fields` - Comma-separated list of fields to include

Example:

```bash
maton asana task list --project 1234567890 --opt-fields name,completed,due_on
```

#### Get a Task

```bash
GET /asana/api/1.0/tasks/{task_gid}
```

Example:

```bash
maton asana task view 1234567890
```

#### Create a Task

```bash
POST /asana/api/1.0/tasks
Content-Type: application/json

{
  "data": {
    "name": "New task",
    "projects": ["PROJECT_GID"],
    "assignee": "USER_GID",
    "due_on": "2025-03-20",
    "notes": "Task description here"
  }
}
```

Example:

```bash
maton asana task create --name 'New task' --projects PROJECT_GID --assignee USER_GID --due-on 2025-03-20 --notes 'Task description here'
```

#### Update a Task

```bash
PUT /asana/api/1.0/tasks/{task_gid}
```

Example:

```bash
maton asana task update 1234567890 --completed
```

#### Delete a Task

```bash
DELETE /asana/api/1.0/tasks/{task_gid}
```

Example:

```bash
maton asana task delete 1234567890
```

#### Get Tasks from a Project

```bash
GET /asana/api/1.0/projects/{project_gid}/tasks
```

Example:

```bash
maton asana task list --project 1234567890
```

#### Get Subtasks

```bash
GET /asana/api/1.0/tasks/{task_gid}/subtasks
```

Example:

```bash
maton asana task list --parent 1234567890
```

#### Create Subtask

```bash
POST /asana/api/1.0/tasks/{task_gid}/subtasks
Content-Type: application/json

{
  "data": {
    "name": "Subtask name",
    "assignee": "USER_GID",
    "due_on": "2025-03-20"
  }
}
```

Example:

```bash
maton asana task create --name 'Subtask name' --parent 1234567890 --assignee USER_GID --due-on 2025-03-20
```

#### Search Tasks (Premium)

**Note:** This endpoint requires an Asana Premium subscription.

```bash
GET /asana/api/1.0/workspaces/{workspace_gid}/tasks/search
```

Query parameters:
- `text` - Text to search for
- `assignee.any` - Filter by assignees
- `projects.any` - Filter by projects
- `completed` - Filter by completion status

Example:

```bash
maton asana task search -w 1234567890 --text 'quarterly report' --completed=false
```

### Projects

#### Get Multiple Projects

```bash
GET /asana/api/1.0/projects
```

Query parameters:
- `workspace` - Workspace GID
- `team` - Team GID
- `opt_fields` - Comma-separated list of fields

Example:

```bash
maton asana project list --workspace <workspace-gid> --opt-fields name,owner,due_date
```

#### Get a Project

```bash
GET /asana/api/1.0/projects/{project_gid}
```

Example:

```bash
maton asana project view <project-gid>
```

#### Create a Project

```bash
POST /asana/api/1.0/projects
```

Example:

```bash
maton asana project create --workspace <workspace-gid> --name 'New Project' --notes 'Project description'
```

#### Update a Project

```bash
PUT /asana/api/1.0/projects/{project_gid}
```

Example:

```bash
maton asana project update PROJECT_GID --name 'Updated Name'
```

#### Delete a Project

```bash
DELETE /asana/api/1.0/projects/{project_gid}
```

Example:

```bash
maton asana project delete <project-gid>
```

### Workspaces

#### Get Multiple Workspaces

```bash
GET /asana/api/1.0/workspaces
```

Example:

```bash
maton asana workspace list
```

#### Get a Workspace

```bash
GET /asana/api/1.0/workspaces/{workspace_gid}
```

Example:

```bash
maton asana workspace view 1234567890
```

#### Update a Workspace

```bash
PUT /asana/api/1.0/workspaces/{workspace_gid}
```

#### Add User to Workspace

```bash
POST /asana/api/1.0/workspaces/{workspace_gid}/addUser
```

#### Remove User from Workspace

```bash
POST /asana/api/1.0/workspaces/{workspace_gid}/removeUser
```

### Users

#### Get Multiple Users

```bash
GET /asana/api/1.0/users
```

Query parameters:
- `workspace` - Workspace GID to filter users

#### Get Current User

```bash
GET /asana/api/1.0/users/me
```

Example:

```bash
maton asana whoami
```

#### Get a User

```bash
GET /asana/api/1.0/users/{user_gid}
```

#### Get Users in a Team

```bash
GET /asana/api/1.0/teams/{team_gid}/users
```

#### Get Users in a Workspace

```bash
GET /asana/api/1.0/workspaces/{workspace_gid}/users
```

### Webhooks

#### Get Multiple Webhooks

```bash
GET /asana/api/1.0/webhooks
```

Query parameters:
- `workspace` - Workspace GID (required)
- `resource` - Resource GID to filter by

#### Create Webhook

**Note:** Asana verifies the target URL is reachable and responds with a 200 status during webhook creation.

```bash
POST /asana/api/1.0/webhooks
Content-Type: application/json

{
  "data": {
    "resource": "PROJECT_OR_TASK_GID",
    "target": "https://example.com/webhook",
    "filters": [
      {
        "resource_type": "task",
        "action": "changed",
        "fields": ["completed", "due_on"]
      }
    ]
  }
}
```

#### Get a Webhook

```bash
GET /asana/api/1.0/webhooks/{webhook_gid}
```

#### Update a Webhook

```bash
PUT /asana/api/1.0/webhooks/{webhook_gid}
```

#### Delete a Webhook

```bash
DELETE /asana/api/1.0/webhooks/{webhook_gid}
```

Returns `200 OK` with empty data on success.

## Pagination

Asana uses cursor-based pagination. The CLI automatically paginates with '--paginate'.

Example:

```bash
maton asana task list --project <project-gid> --paginate
```

## Code Examples

### CLI

```bash
# Get tasks as JSON (default format); select fields with --opt-fields
maton asana task list --project 1234567890 --opt-fields name,completed,due_on

# Filter with jq — e.g., only incomplete tasks (responses are wrapped in {"data": [...]})
# Note: --jq requires --json
maton asana task list --project 1234567890 --opt-fields name,completed,due_on \
  --json --jq '.data | map(select(.completed == false))'

# Extract specific fields
maton asana project list --workspace 1234567890 --opt-fields name --json --jq '.data[].name'
```

### JavaScript

```javascript
const response = await fetch(
  'https://api.maton.ai/asana/api/1.0/tasks?project=1234567890',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://api.maton.ai/asana/api/1.0/tasks',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'project': '1234567890'}
)
data = response.json()
```

## Notes

- Resource IDs (GIDs) are strings
- Timestamps are in ISO 8601 format
- Use `opt_fields` to specify which fields to return
- Workspaces are the highest-level organizational unit
- Organizations are specialized workspaces representing companies
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`fields[]`, `sort[]`, `records[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Bad request or missing Asana connection |
| 401 | Invalid or missing Maton API key |
| 403 | Forbidden - insufficient permissions |
| 404 | Resource not found |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Asana API |

### Troubleshooting: API Key Issues

**CLI:**

1. Check your auth state:

```bash
maton whoami
```

2. Verify the API key is valid by listing connections:

```bash
maton connection list
```

**Manual:**

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `asana`. For example:

- Correct: `https://api.maton.ai/asana/api/1.0/tasks`
- Incorrect: `https://api.maton.ai/api/1.0/tasks`

## Resources

- [Asana API Documentation](https://developers.asana.com)
- [API Reference](https://developers.asana.com/reference)
- [LLM Reference](https://developers.asana.com/llms.txt)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
