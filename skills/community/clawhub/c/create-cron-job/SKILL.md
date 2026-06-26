---
name: create-cron-job
description: Create and configure OpenClaw cron jobs with correct scheduling, execution modes, and delivery patterns. Use when asked to schedule a task, set up a recurring job, create a reminder, run something at a specific time, or automate a periodic operation.
verified-against: "2026.3.2"
---

# Create Cron Job

Set up a scheduled task per `conventions/cron.md`. Read the convention first.

**Need a periodic check instead?** Consider `HEARTBEAT.md` — see "Cron vs Heartbeat" in `conventions/cron.md`.

## Before You Start

Determine:
- Which agent handles the job
- Main session (needs conversation context) or isolated (standalone)
- Delivery mode (announce, webhook, none)

## Steps

### 1. Choose the execution mode

| Question | If yes | If no |
|---|---|---|
| Does the task need recent conversation context? | Main session | Isolated |
| Does the agent need its AGENTS.md/SOUL.md? | Isolated (normal) | Isolated + `lightContext` |
| Is this a one-shot reminder? | `--at` with `--delete-after-run` | Recurring schedule |

### 2. Choose a job name

Format: `<agent-id>-<purpose>` in kebab-case.

Examples: `auditor-daily-report`, `archivist-daily-backup`, `reminder-standup-meeting`

### 3. Choose a schedule

| Pattern | CLI flag | Example |
|---|---|---|
| Cron expression | `--cron` | `--cron "0 7 * * *"` (7 AM daily) |
| Fixed interval | `--every` | `--every "4h"` |
| One-shot (relative) | `--at` | `--at "20m"` |
| One-shot (absolute) | `--at` | `--at "2026-03-15T09:00:00Z"` |

Always set timezone for cron expressions: `--tz "America/Los_Angeles"`

### 4. Create the job

**Main session** (task needs conversational context):

```bash
openclaw cron add \
  --name "<agent-id>-<purpose>" \
  --every "<interval>" \
  --session main \
  --system-event "<instruction text>" \
  --wake now
```

**Isolated** (standalone task):

```bash
openclaw cron add \
  --name "<agent-id>-<purpose>" \
  --cron "<expr>" \
  --tz "<timezone>" \
  --session isolated \
  --message "<instruction text>" \
  --agent <agent-id> \
  --announce \
  --channel <channel> \
  --to "<target>"
```

**Isolated + lightweight context** (simple, self-contained chore):

```bash
openclaw cron add \
  --name "<agent-id>-<purpose>" \
  --every "<interval>" \
  --session isolated \
  --message "<self-contained instruction>" \
  --light-context \
  --announce
```

**One-shot reminder:**

```bash
openclaw cron add \
  --name "reminder-<purpose>" \
  --at "<time>" \
  --session isolated \
  --message "<reminder text>" \
  --announce \
  --delete-after-run
```

### 5. Bind to an agent

Always use `--agent <agent-id>` for agent-specific jobs.

### 6. Set delivery mode

- **Announce** (most jobs): `--announce --channel <ch> --to "<target>"`
- **Webhook**: `--webhook <url>`
- **None**: omit delivery flags

### 7. Document in the agent's AGENTS.md

```markdown
## Scheduled Tasks

| Job | Schedule | Message | Action |
|---|---|---|---|
| `<job-name>` | `<schedule>` | `<message>` | <what the agent does> |
```

### 8. Create a skill if the job uses scripts

If the cron job executes scripts (not just a self-contained message), create a skill using the `create-skill` skill:

- Scripts live in `workspace/skills/<skill-name>/scripts/`, not in ad-hoc workspace directories
- The skill makes the capability discoverable for on-demand use, not just cron
- Description should cover both automated (cron) and on-demand (user request) triggers
- See "Workspace File Placement" in `conventions/skills.md` for where files belong

Skip if the cron job's message is fully self-contained (no external scripts or supporting files).

### 9. Test the job

```bash
openclaw cron run <jobId>           # Force immediate execution
openclaw cron list                  # Verify job exists
openclaw cron runs --id <jobId>     # Check run history
```

## Post-Creation Checklist

- [ ] Job name follows `<agent-id>-<purpose>` kebab-case convention
- [ ] Timezone set for cron expressions (`--tz`)
- [ ] Explicit `--agent` binding for agent-specific jobs
- [ ] Delivery mode set (announce/webhook/none)
- [ ] Channel and target specified for announce delivery
- [ ] Agent's AGENTS.md updated with Scheduled Tasks entry
- [ ] Job tested with `openclaw cron run <jobId>`
- [ ] No duplicate: checked that no system crontab or existing job covers the same task
- [ ] One-shot reminders use `--delete-after-run`
- [ ] If job uses scripts: skill created in `workspace/skills/<name>/` with scripts in its `scripts/` subdir
- [ ] No ad-hoc files or directories created at workspace root (see `conventions/skills.md`)
