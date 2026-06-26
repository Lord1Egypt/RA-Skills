# Setup & Connection Guide

## MCP Connection Options

Team Operations Mode requires connecting to the MCP server. Two transport options:

### Option 1: CLI (stdio) — Recommended

Run the MCP server locally via npx. Simpler setup, lower latency, only one key needed.

```json
{
  "mcpServers": {
    "management-brain": {
      "command": "npx",
      "args": ["-y", "@tonykk/management-brain-mcp"],
      "env": {
        "MANAGEMENT_BRAIN_API_KEY": "mb_your_api_key_here",
        "MANAGEMENT_BRAIN_BASE_URL": "https://manageaibrain.com"
      }
    }
  }
}
```

- No `MCP_HTTP_API_KEY` needed — stdio mode bypasses HTTP auth
- Only requires `MANAGEMENT_BRAIN_API_KEY` (the `mb_` prefixed key)
- Works with Claude Code, Hermes Agent, and any MCP client that supports stdio transport
- Zero install: `npx -y` auto-downloads and runs

### Option 2: HTTP (Streamable HTTP)

Connect to the cloud-hosted MCP endpoint. Works with ChatGPT, Gemini, and web-based MCP clients.

- **URL**: `https://manageaibrain.com/mcp`
- **Auth**: `Authorization: Bearer <MCP_HTTP_API_KEY>`
- **Accept**: `application/json, text/event-stream`
- Requires `MCP_HTTP_API_KEY` (separate from `MANAGEMENT_BRAIN_API_KEY`)

### npm install (alternative for CLI)

```bash
npm install -g @tonykk/management-brain-mcp
```

Then use `"command": "management-brain-mcp"` instead of npx in your MCP config.

## OpenClaw Integration Architecture

Boss AI Agent is the **brain layer** on top of OpenClaw's MCP connector ecosystem. It connects to its own backend (`manageaibrain.com/mcp`) for team data processing, while third-party tool integrations are handled by OpenClaw's MCP connectors.

```
OpenClaw Runtime (user environment)
  |-- MCP Connectors (user self-installs via OpenClaw)
  |    |-- Storage: Notion / Google Sheets  <-- bidirectional sync targets
  |    |-- Development: GitHub / Linear / Calendar / Gmail
  |    +-- Communication: Telegram / Slack / Discord / Lark / Signal
  |
  +-- Boss AI Agent Skill (brain layer + sync orchestrator)
       +-- manageaibrain.com API
            |-- 33 MCP tools (daily ops + intelligence + sync)
            |-- Company Context Layer  <- foundation for all reasoning
            |-- Execution Intelligence <- signals, risks, working memory
            |-- Communication Parser   <- check-ins -> structured events
            |-- Incentive Engine       <- context-aware scoring
            |-- AI Recommendation Engine <- memory-driven proactive suggestions
            +-- Sync Service           <- Notion/Sheets bidirectional sync
```

### Company Context Layer

The Context Layer is the **foundation** — all intelligence engines depend on it. It aggregates:

- **Organization context**: strategic priorities, key risks, management style, countries of operation
- **Employee context**: execution scores, current workload, strengths, risk flags, work scope
- **Goal context**: OKRs, KPIs with baselines and targets, goal ownership and attribution
- **Project context**: active projects, task status, blockers, delivery timelines

When OpenClaw MCP connectors are installed, they enrich the context layer automatically:
- **Notion/Jira/Sheets** -> project updates, task status, documentation changes
- **GitHub/Linear** -> PR activity, commit patterns, CI status feed into execution signals
- **Telegram/Slack/Discord/Lark** -> employee messages parsed into structured management events

### Data Ingestion Pipeline

1. **OpenClaw connectors** deliver raw data (GitHub commits, Jira updates, Slack messages, check-in reports)
2. **Communication Parser** extracts structured management events (`blocker_reported`, `task_completed`, `commitment_made`, `delay_reported`, `escalation_needed`, `proactive_update`)
3. **State Engine** generates execution signals (overload risk, delivery risk, engagement drops, blocker cascades)
4. **Working Memory** maintains AI situational awareness — focus areas, momentum, pending decisions
5. **Recommendation Engine** synthesizes all context through mentor lens for prioritized suggestions

## Permissions & Data

### Advisor Mode (no cloud)

- **Config file**: writes `~/.openclaw/skills/boss-ai-agent/config.json` during first run. User can read, edit, or delete at any time.
- **No network access**: zero HTTP requests. All responses from embedded mentor frameworks.
- **No cron jobs**: no persistent behavior.

### Team Operations Mode (MCP connected)

All Advisor Mode permissions, plus:

- **MCP tools** (requires `MANAGEMENT_BRAIN_API_KEY`): 33 tools on `manageaibrain.com/mcp`. 21 read-only; 4 write (send messages); 2 recommendation; 3 brain context; 3 sync.
- **Cron jobs**: up to 6 recurring jobs. Solo founder mode (team=0) only registers 3.
- **Third-party tools**: via OpenClaw connectors — skill does NOT store/manage tokens.
- **Cloud API** (optional): `BOSS_AI_AGENT_API_KEY` enables read-only GET to `manageaibrain.com/api/v1/`.

### Data Flow Summary

**What goes to the cloud**: MCP tool parameters sent to `manageaibrain.com`. Server stores team data in PostgreSQL.

**What stays local**: `config.json`, chat history, memory files. Never transmitted.

**Persistent behavior warning**: Team Ops Mode registers up to 6 autonomous cron jobs + 4 write tools + 3 sync tools. Review cron schedules in `config.json` before activating.

## Cron Job Management

| Job | Default Schedule | Solo Mode |
|-----|-----------------|-----------|
| checkin | `0 9 * * 1-5` (9am weekdays) | Skipped |
| chase | `30 17 * * 1-5` (5:30pm weekdays) | Skipped |
| summary | `0 19 * * 1-5` (7pm weekdays) | Skipped |
| briefing | `0 8 * * 1-5` (8am weekdays) | Active |
| signalScan | `*/30 9-18 * * 1-5` (every 30min work hours) | Active |
| sync | `*/30 9-18 * * 1-5` (every 30min work hours) | Active |

**Commands**: `cron list` / `cron remove <job-id>` / `cron remove --skill boss-ai-agent`

**Uninstall cleanup**: `clawhub uninstall boss-ai-agent` removes all cron jobs and `config.json`.

**User-editable**: modify `schedule` in `config.json` and re-run `/boss-ai-agent` to update.
