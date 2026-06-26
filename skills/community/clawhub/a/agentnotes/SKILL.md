---
name: agentnotes
description: Log OpenClaw tasks to AgentNotes for SparkNotes rollups (success, failures, what happened). Use after cron jobs, channel replies, or multi-step sessions. Requires AGENTNOTES_API_KEY and AGENTNOTES_AGENT_ID env vars.
metadata: {"openclaw":{"requires":{"bins":["node"]},"primaryEnv":"AGENTNOTES_API_KEY","envVars":[{"name":"AGENTNOTES_API_KEY","required":true,"description":"API key from AgentNotes dashboard (an_...)"},{"name":"AGENTNOTES_AGENT_ID","required":true,"description":"Agent slug from AgentNotes (same as dashboard)"},{"name":"AGENTNOTES_BASE_URL","required":false,"description":"AgentNotes app URL"}]}}
---

# AgentNotes for OpenClaw

Send **high-level job summaries** to AgentNotes. Raw logs are rolled up hourly/daily into SparkNotes; you do not need to store every line forever.

## Setup (once)

1. AgentNotes dashboard → create agent (note the **slug**) → copy **env vars** from **Connect**.
2. Install this skill (see dashboard Connect → OpenClaw tab, or run `install-skill.ps1` / `install-skill.sh` from the repo).
3. Add env to `~/.openclaw/openclaw.json`:

```json5
{
  skills: {
    entries: {
      agentnotes: {
        enabled: true,
        env: {
          AGENTNOTES_API_KEY: "an_...",
          AGENTNOTES_AGENT_ID: "your-slug",
          AGENTNOTES_BASE_URL: "https://your-app.vercel.app",
        },
      },
    },
  },
}
```

4. Restart OpenClaw / new session. Verify:

```bash
node {baseDir}/scripts/verify.mjs
```

## Recommended: one command per task

Always pass a **plain-English summary** (this becomes the CEO-facing SparkNote):

```bash
node {baseDir}/scripts/task.mjs --summary "Replied to 2 Telegram chats, scheduled 1 meeting"
```

With an extra step log:

```bash
node {baseDir}/scripts/task.mjs --summary "Inbox sweep done" --message "Processed 12 threads" --step inbox
```

On failure:

```bash
node {baseDir}/scripts/task.mjs --summary "Send failed" --failed --error "SMTP timeout"
```

## Manual multi-step flow

```bash
export AGENTNOTES_RUN_ID=$(node {baseDir}/scripts/start-run.mjs)
node {baseDir}/scripts/log.mjs "Tool: calendar" --step tools
node {baseDir}/scripts/complete-run.mjs --summary "Updated 3 events"
```

## When to log

- After handling a user message on any channel
- After a cron / heartbeat completes
- After a skill or tool chain finishes (success or failure)

## Dashboard

`$AGENTNOTES_BASE_URL/agents` — SparkNotes tab is the long-term record.
