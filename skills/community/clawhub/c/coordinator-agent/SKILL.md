---
name: coordinator-agent
description: "Agent fleet coordinator for OpenClaw. Silent mode — only messages when something changed. Priority-sorts errors and handoffs above routine output. Trend detection vs 7-day average. Self-healing retriggers missed crons. Multi-platform: Telegram, Discord, Slack. ~$0.02/day."
version: 1.1.0
author: Walt Spence
homepage: https://github.com/waltspence/coordinator-agent
tags: [openclaw, clawdbot, agent-fleet, coordination, telegram, discord, slack, briefing]
metadata:
  clawdbot:
    requires:
      bins: ["openclaw"]
      config: ["telegram.enabled"]
---

# Coordinator Agent

One briefing. Only when something changed.

Reads every agent workspace daily at 9am. Delivers a structured briefing to Telegram (and optionally Discord/Slack). If nothing changed across the entire fleet, it stays silent.

## Security Warning

This skill reads all configured agent workspaces, sends summaries to external messaging platforms, and can automatically retrigger cron jobs. Before installing:

- **Workspace access:** The coordinator scans every workspace you configure. Restrict the workspace list to only what needs monitoring. Exclude any workspace containing credentials, secrets, or sensitive data.
- **Outbound messaging:** Briefing content is sent to Telegram (always) and optionally Discord/Slack. Review what gets included in the output format before enabling delivery to external platforms.
- **Auth scoping:** Use dedicated, scoped API credentials for the coordinator agent. Do not reuse auth profiles from other agents. The coordinator only needs read access to workspaces and write access to configured messaging channels.
- **Self-healing:** Automatically retriggering missed cron jobs can cause duplicate execution. Only enable this if your cron jobs are idempotent (safe to run twice). Disable self-healing by removing the retrigger rule from your SOUL.md if jobs have side effects.

## How It Works

### Silent Mode
No new files, no errors, no handoffs, no trend anomalies → no message. Zero-cost days are silent days.

### Priority Sort
Briefings ordered by actionability:
1. Errors and missed crons
2. Handoff requests and decisions needed
3. Trend anomalies vs 7-day average
4. New files listed by agent
5. Fleet health summary

### Trend Detection
Tracks output volume per agent over 7 days. Flags deviations >50% from rolling average. Catches silent/broken agents before you notice.

### Self-Healing
⚠️ Only enable if cron jobs are idempotent. If a cron job hasn't run by 11am, retriggers once. Reports the attempt. If it fails again, that's a critical alert.

### Multi-Platform
Telegram by default. Set `DISCORD_WEBHOOK` or `SLACK_WEBHOOK` env vars for additional delivery.

## Install

```bash
clawdhub install coordinator-agent
```

Create the agent directory:

```bash
mkdir -p ~/.openclaw/agents/coordinator/agent
```

Create `SOUL.md` in that directory. Customize workspace paths, webhook URLs, and toggle self-healing:

```markdown
# Coordinator — Fleet Briefing Agent

Read every agent workspace. Deliver one briefing. If nothing changed, stay silent.

## Workspaces to scan (restrict to what needs monitoring)
- Content: ~/.openclaw/workspace-seo-content/
- Research: ~/.openclaw/workspace-market-research/
- Shared memory: ~/.openclaw/company-brain/

## Delivery
- Telegram: enabled
- Discord: $DISCORD_WEBHOOK
- Slack: $SLACK_WEBHOOK

## Schedule
Daily at 9am. See openclaw.json for cron config.

## Rules
- Silent mode: send nothing if no changes, no errors, no handoffs, no anomalies
- Priority: errors → handoffs → trends → output → status
- Trend: compare file counts vs 7-day rolling average, flag >50% deviation
- Self-healing: remove this section unless cron jobs are idempotent
```

Set up auth with scoped credentials:

```bash
# Option A: Generate dedicated API key with minimal scope
# Add it to ~/.openclaw/agents/coordinator/agent/auth-profiles.json

# Option B: Copy from existing agent (broader access — review first)
cp ~/.openclaw/agents/researcher/agent/auth-profiles.json \
   ~/.openclaw/agents/coordinator/agent/
```

Add to `openclaw.json` agent list, cron to daily 9am, restart gateway.

## Requirements

- OpenClaw/Clawdbot + Telegram configured
- 2+ other agents producing output
- DeepSeek or Claude API key

## Cost

~$0.02/day on DeepSeek V4 Flash. Silent days are free.

## Limits

Overkill for 1-2 agents. OpenClaw-specific.
