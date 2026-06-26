# BestYou MCP Setup Reference

## First-Run Detection

Check if mcporter is installed and the BestYou server is configured:

```bash
mcporter --config ~/.openclaw/workspace/config/mcporter.json list
```

If `mcporter` is not found, install it: `npm install -g mcporter`

If `bestyou` is not in the output, walk the user through setup below.

## Setup Steps

### 1. Get API Key

Tell the user:

> "Open BestYou on your iPhone. Go to More, then Connected Apps, then OpenClaw, then Generate Key. Paste the key here when you have it."

Key format: `by_mcp_live_...`

### 2. Create the mcporter config

Write the config file at `~/.openclaw/workspace/config/mcporter.json`:

```json
{
  "mcpServers": {
    "bestyou": {
      "baseUrl": "https://mcp.bestyou.ai/mcp",
      "headers": {
        "Authorization": "Bearer <paste-key-here>"
      }
    }
  },
  "imports": []
}
```

The API key MUST go in the `Authorization` header with the `Bearer` prefix. The BestYou MCP server authenticates via this header. Do not pass it as a query parameter or body field.

### 3. Verify Connection

```bash
mcporter --config ~/.openclaw/workspace/config/mcporter.json call bestyou.get_account_link_status
```

Should return `linked: true` with granted scopes. If it returns a VALIDATION_ERROR about auth, the header is wrong.

### 4. Restart Gateway

```bash
openclaw gateway restart
```

## Calling Tools

All tool calls use this pattern:

```bash
mcporter --config ~/.openclaw/workspace/config/mcporter.json call bestyou.<tool_name> [param=value ...]
```

If the agent's working directory is the workspace, the shorter form works:

```bash
mcporter --config config/mcporter.json call bestyou.<tool_name> [param=value ...]
```

## Available Tools

| Tool | Purpose | Parameters |
|------|---------|-----------|
| `get_account_link_status` | Verify connection and scopes | (none) |
| `get_daily_briefing` | Readiness, insights, priorities | `date` (YYYY-MM-DD) |
| `get_todays_action_plan` | Day's scheduled blocks | `date` (YYYY-MM-DD), `location` (optional) |
| `get_progress_snapshot` | Domain scores and recommendations | `date` (YYYY-MM-DD) |
| `get_weekly_summary` | Weekly trends and achievements | `weekEndDate` (YYYY-MM-DD) |
| `generate_workout` | Create a workout plan | `type`, `duration`, `equipment`, `experienceLevel`, `goal` |
| `analyze_meal_text` | Nutritional analysis from text | `description`, `timestamp` (ISO 8601) |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `mcporter: command not found` | Not installed | `npm install -g mcporter` |
| VALIDATION_ERROR: auth required | Missing or malformed Authorization header | Check `mcporter.json` has `"Authorization": "Bearer by_mcp_live_..."` in headers |
| 401 Unauthorized | API key expired/invalid | Regenerate in BestYou app, update config |
| ENOENT error | Config file path wrong | Use full path: `--config ~/.openclaw/workspace/config/mcporter.json` |
| No tools found | MCP server not in config | Verify `mcporter.json` has the `bestyou` entry |
| Empty responses | No data for requested date | Try today's date |
| Connection refused | Gateway not restarted | Run `openclaw gateway restart` |
