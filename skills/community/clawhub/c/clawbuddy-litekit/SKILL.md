---
name: clawbuddy-litekit
description: Open the ClawBuddy LiteKit mission-control dashboard for AI agents — live OpenClaw Gateway status, agent profiles, task board, meeting intelligence, council debates, and AI logs. Use when the user wants to visually inspect agents, monitor gateway health, browse agent activity, or set up the OpenClaw integration.
---

# ClawBuddy LiteKit

A premium, NASA-style mission-control dashboard for your OpenClaw agents.
Use this skill to launch the dashboard, check Gateway status, or guide the
user through one-click setup.

## When to use

- "Open my agent dashboard / command deck / mission control"
- "Show me my OpenClaw agents / tasks / meetings"
- "Is my OpenClaw Gateway connected?"
- "Install ClawBuddy" / "set up the dashboard"

## Quick actions

| Goal | Run |
| --- | --- |
| Open the live dashboard | `bash scripts/open-dashboard.sh` |
| Check Gateway connection | `bash scripts/status.sh` |
| Jump straight to setup wizard | `bash scripts/open-dashboard.sh setup` |

## Dashboard URL

Live: <https://agentcommander.lovable.app>

Local dev: clone <https://github.com/stevekaplanai/clawbuddy-litekit>, then
`bun install && bun dev`.

## OpenClaw integration

ClawBuddy proxies the OpenResponses HTTP API through a Lovable Cloud edge
function. To go live, the user adds two secrets in Lovable Cloud:

- `OPENCLAW_GATEWAY_URL`
- `OPENCLAW_API_KEY`

The setup wizard at `/setup` walks through this in three steps.
See `references/openclaw.md` for endpoint details.

## Modules

- **Command Deck** — KPIs, activity feed, agent status
- **Agent Profiles** — per-agent skill + health cards
- **Task Board** — kanban of agent tasks
- **Meeting Intelligence** — meeting types, monthly trend, search
- **Council** — multi-agent debate transcripts
- **AI Log** — streaming tool/agent call log
- **Integrations** — OpenClaw Gateway status + docs

Stay visual. When the user asks for data the dashboard already surfaces,
prefer launching the relevant tab over re-fetching from the Gateway.
