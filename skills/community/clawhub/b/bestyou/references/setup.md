# BestYou MCP Setup Guide

## Prerequisites

- OpenClaw instance running
- BestYou iOS app with an active account
- Node.js (comes with OpenClaw)

## Step 1: Get Your API Key

In the BestYou iOS app:
1. Go to **More → Connected Apps → OpenClaw**
2. Tap **Generate Key**
3. Copy the key (format: `by_mcp_live_...`)

Full walkthrough with screenshots: [bestyou.ai/openclaw-setup](https://bestyou.ai/openclaw-setup)

## Step 2: Set the Environment Variable

Add your API key to your shell environment:

```bash
export BESTYOU_API_KEY="YOUR_KEY_HERE"
```

To persist across sessions, add the export to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.).

## Step 3: Install mcporter

mcporter is OpenClaw's MCP client. If you don't have it installed:

```bash
npm install -g mcporter
```

Verify:

```bash
mcporter --version
```

## Step 4: Add BestYou as an MCP Server

```bash
mcporter config add bestyou \
  --url https://mcp.bestyou.ai/mcp \
  --header "Authorization: Bearer $BESTYOU_API_KEY"
```

Alternatively, create or edit your mcporter config file at `~/.openclaw/workspace/config/mcporter.json`:

```json
{
  "mcpServers": {
    "bestyou": {
      "baseUrl": "https://mcp.bestyou.ai/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_KEY_HERE"
      }
    }
  },
  "imports": []
}
```

**Important:** The API key goes in the `Authorization` header as a Bearer token. Do not pass it as a query parameter or body field.

## Step 5: Verify the Connection

```bash
mcporter call bestyou.get_account_link_status
```

Expected output: `linked: true` with your granted scopes (read:brief, read:action_plan, write:workout, write:nutrition).

If using a custom config path:

```bash
mcporter --config ~/.openclaw/workspace/config/mcporter.json call bestyou.get_account_link_status
```

## Step 6: Restart the Gateway

```bash
openclaw gateway restart
```

## Available Tools (7)

| Tool | Purpose | Required Parameters |
|------|---------|---------------------|
| `get_account_link_status` | Verify connection and scopes | (none) |
| `get_daily_briefing` | Readiness score, insights, priorities | `date` (YYYY-MM-DD) |
| `get_todays_action_plan` | Day's scheduled blocks (workouts, meals, recovery) | `date` (optional) |
| `get_progress_snapshot` | Domain-level scores and recommendations | `date` (YYYY-MM-DD) |
| `get_weekly_summary` | Weekly trends and achievements | `weekEndDate` (optional) |
| `generate_workout` | Create a workout plan | `type`, `duration`, `equipment`, `experienceLevel` |
| `analyze_meal_text` | Nutritional analysis from text description | `description` |

### generate_workout optional parameters

`bodyParts`, `targetAreas`, `goal`, `injuries`, `includeWarmup`, `warmupStyle` (dynamic/activation), `warmupDuration`, `includeCooldown`, `cooldownStyle` (static/foam_rolling/combined), `cooldownDuration`

### analyze_meal_text optional parameters

`timestamp` (ISO 8601 format)

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `mcporter: command not found` | Run `npm install -g mcporter` |
| `VALIDATION_ERROR: auth required` | Check that `Authorization: Bearer ...` header is set correctly |
| `401 Unauthorized` | API key expired. Regenerate in BestYou app. |
| `ENOENT` config errors | Verify mcporter config file path |
| No tools found | Verify `bestyou` entry exists in mcporter config |
| Empty responses | Try today's date. Data availability depends on BestYou app usage. |

## Test in the Playground

Before wiring into your agent, test your connection at [mcp.bestyou.ai/openclaw](https://mcp.bestyou.ai/openclaw).
