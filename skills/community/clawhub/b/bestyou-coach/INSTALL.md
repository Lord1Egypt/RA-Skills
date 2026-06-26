# BestYou Coach Skill — Install Guide

## What This Is

An OpenClaw skill that renders BestYou health data (daily briefings, action plans, progress snapshots, weekly summaries, meal analysis, workouts) as Dark Glass themed visual widgets via canvas.

## Prerequisites

- OpenClaw instance running
- BestYou iOS app with an active account
- Node.js (comes with OpenClaw)

## Install Steps

### 1. Install the skill

```bash
clawhub install bestyou-coach
```

OpenClaw auto-discovers skills from the `skills/` directory. No config registration needed.

### 2. Install mcporter

mcporter is the CLI that talks to MCP servers. It's a separate package, not bundled with OpenClaw.

```bash
npm install -g mcporter
```

Verify it installed:

```bash
mcporter --version
```

### 3. Get your BestYou API key

In the BestYou iOS app:
1. Go to **More → Connected Apps → OpenClaw**
2. Tap **Generate Key**
3. Copy the key (it starts with `by_mcp_live_...`)

### 4. Create the mcporter config file

Create the file at `~/.openclaw/workspace/config/mcporter.json` with this exact content, replacing `YOUR_KEY_HERE` with the key from step 3:

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

**Important:** The API key goes in the `Authorization` header as a Bearer token. This is how the BestYou MCP server authenticates requests.

### 5. Verify the connection

```bash
mcporter --config ~/.openclaw/workspace/config/mcporter.json list
```

Should show `bestyou` with 7 tools. Then test it:

```bash
mcporter --config ~/.openclaw/workspace/config/mcporter.json call bestyou.get_account_link_status
```

Should return `"linked": true` with your granted scopes.

### 6. Restart the gateway

```bash
openclaw gateway restart
```

## Usage

Once connected, just talk naturally:

- "What's my day look like?" — daily briefing + action plan
- "How am I doing?" — progress snapshot
- "How was my week?" — weekly summary
- "I just had a chicken burrito bowl" — meal analysis
- "Give me a 20 minute bodyweight workout" — workout generator

The agent fetches live data from BestYou's API via MCP and renders it as visual widgets.

## Files

```
bestyou-coach/
├── SKILL.md              # Agent instructions (the brain)
├── INSTALL.md            # This file
├── references/
│   └── setup.md          # Detailed MCP setup reference
└── assets/
    ├── shared.css         # Dark Glass design system
    ├── daily-briefing.html
    ├── action-plan.html
    ├── progress-snapshot.html
    ├── weekly-summary.html
    ├── meal-analysis.html
    ├── workout.html
    └── account-status.html
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `mcporter: command not found` | Run `npm install -g mcporter` |
| `ENOENT` config errors | Make sure `config/mcporter.json` exists at the path above. Use `--config` flag to point to it explicitly. |
| `VALIDATION_ERROR: auth is required` | The API key is missing or wrong. Check `mcporter.json` has the `Authorization` header with `Bearer` prefix. |
| `401 Unauthorized` | API key expired. Regenerate in BestYou app, update `mcporter.json`. |
| `bestyou` not showing in `mcporter list` | Config file path is wrong. Run `mcporter --config <full-path> list` to verify. |
| Widgets render blank | Run `mcporter call bestyou.get_daily_briefing` to check if raw data comes back. |
| Gateway won't restart | Run `openclaw gateway status` to diagnose. |
