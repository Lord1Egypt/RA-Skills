---
name: daily-introspection
description: Autonomous daily self-introspection and self-improvement for OpenClaw agents. Automatically reviews daily conversation logs, identifies mistakes and improvement opportunities, and upgrades core rules automatically. Trigger for daily self-improvement tasks, weekly rule refinement, and autonomous agent evolution.
---

# Daily Introspection

## Overview

Enables autonomous self-improvement for OpenClaw agents: automatically reviews daily conversation logs, identifies mistakes, extracts actionable rules, promotes mature lessons to permanent system rules, and continuously evolves the agent's behavior without manual intervention.

## Data Storage

| Type | Location | Description |
|------|----------|-------------|
| Private runtime data + all archived records | `workspace/.daily-introspection/` | Private hidden directory (auto-created):
  - Temporary cache, run logs, intermediate analysis
  - Daily introspection records: `introspection-YYYY-MM-DD.md`
  - Weekly evolution reports: `evolution-YYWW.md` |

## Core Workflow

### 1. Daily Run (triggered by cron at 22:00 daily)
1. Run `scripts/daily-introspect.py` to collect all sources:
   - Read today's conversation log: `memory/YYYY-MM-DD.md`
   - Read today's learning/error/feature records: `.learnings/*.md`
   - Check proactive mechanism files: `SESSION-STATE.md`, `HEARTBEAT.md`, `working-buffer.md`
2. Call LLM to perform self-introspection:
   - Identify incorrect answers, rule violations, and bad patterns
   - Extract concrete improvement suggestions
   - Classify as: one-time mistake / repeat pattern / new rule
3. Write daily record to `workspace/.daily-introspection/introspection-YYYY-MM-DD.md` (private data directory)

### 2. Weekly Promotion (triggered by cron on Sunday 20:00)
1. Aggregate all daily introspections from the week (read from `workspace/.daily-introspection/`)
2. Identify repeated patterns and validated improvements
3. **First, perform all rule promotions immediately**:
   - Promote mature rules to target files: AGENTS.md / MEMORY.md / TOOLS.md
   - Verify each promotion by reading the file after writing to confirm successful写入
   - Only after all promotions are verified complete, proceed to next step
4. Generate a weekly evolution report (reflecting that promotions are already done)
5. Send report to user for review
6. Archive the report to `workspace/.daily-introspection/` (private data directory)

**Mandatory Order**: `Do promotions → Verify promotions → Generate report → Send report`
**Never**: `Generate report → Do promotions` (this causes missed writes when interrupted)

## Scripts

### `scripts/daily-introspect.py`
Main entry point for daily self-introspection.

Usage:
```bash
python3 scripts/daily-introspect.py [--date YYYY-MM-DD]
```

If no date specified, uses today.

### `scripts/weekly-promote.py`
Weekly promotion of lessons to permanent system files.

Usage:
```bash
python3 scripts/weekly-promote.py [--week WWYY]
```

## Configuration

### OpenClaw Cron Setup

Add these two cron entries via OpenClaw CLI:

```bash
# Daily introspection at 22:00
openclaw cron add --name "Daily Self-Introspection" --cron "0 22 * * *" --exact --tz "Asia/Shanghai" --session main --system-event "daily-introspection: Daily self-introspection is triggered. Follow the daily-introspection skill process:
1. Run the script $OPENCLAW_WORKSPACE/skills/daily-introspection/scripts/daily-introspect.py to collect all sources
2. Read the collected sources from the script output
3. Perform LLM introspection analysis following these rules:
   - For errors in .learnings/ERRORS.md: if only recorded with corrective action, mark as '✅ Recorded, Rule Added'; only mark as '✅ Corrected' when verified no recurrence for >1 week
   - Do not automatically assume recorded = corrected; reflect actual status accurately
   - Identify any new errors from today's activities, add them to .learnings/ERRORS.md with corrective rules
   - Write the final introspection result to ~/.openclaw/workspace/.daily-introspection/introspection-YYYY-MM-DD.md
4. Report completion status in this session when done"

# Weekly promotion at 20:00 every Sunday
openclaw cron add --name "Weekly Introspection Promotion" --cron "0 20 * * 0" --exact --tz "Asia/Shanghai" --session main --system-event "daily-introspection: Weekly promotion is triggered. Follow the weekly-promotion process:
1. Execute scripts/weekly-promote.py to collect all daily introspections from this week
2. Identify repeated patterns that have not recurred for >1 week
3. **MANDATORY EXECUTION ORDER**:
   - FIRST: Perform all rule promotions one by one → write each mature rule to its target file (AGENTS.md/MEMORY.md/TOOLS.md)
   - AFTER each write: Read the target file back to verify the rule is actually written successfully
   - ONLY after ALL promotions are done and verified: Write the weekly evolution report to ~/.openclaw/workspace/.daily-introspection/evolution-YYWW.md
   - Never reverse this order - do not write the report before promotions are complete
4. Report completion status in this session when done
Rules:
- Only promote rules that have been verified and no recurrence for 1+ week
- Keep new recorded errors/learnings in .learnings/ for further verification
- Do not promote immature rules prematurely
```

### Configuration Notes
- Daily schedule: 22:00 daily (adjust timezone as needed)
- Weekly schedule: 20:00 every Sunday
- Target: `main` session for interactive analysis and writing
- Timezone: Use your IANA timezone (e.g. `Asia/Shanghai`, `UTC`, `America/New_York`)
