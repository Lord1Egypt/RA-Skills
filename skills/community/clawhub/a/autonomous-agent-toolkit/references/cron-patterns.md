# Cron Patterns for Autonomous Agents

## Essential Cron Jobs

### 1. Heartbeat (Awareness Loop)
```bash
openclaw cron add --name "Heartbeat" \
  --cron "*/20 6-22 * * *" --tz "America/Denver" \
  --model "anthropic/claude-haiku-3.5" \
  --message "Read HEARTBEAT.md. Execute pending tasks. Reply HEARTBEAT_OK if nothing."
```
- Runs every 20 min during waking hours
- Use cheapest model — this is a simple check
- HEARTBEAT.md contains the checklist of periodic tasks

### 2. Memory Consolidation (Nightly)
```bash
openclaw cron add --name "Nightly Memory Review" \
  --cron "0 3 * * *" --tz "America/Denver" \
  --model "anthropic/claude-opus-4-6" \
  --message "Review memory/YYYY-MM-DD.md files from past 3 days. Update MEMORY.md with significant events, lessons, decisions. Remove outdated entries. Plan tomorrow's priorities."
```
- Use strongest model — this requires judgment
- Runs at 3 AM when no one is chatting

### 3. Daily Summary
```bash
openclaw cron add --name "Daily Summary" \
  --cron "0 21 * * *" --tz "America/Denver" \
  --message "Generate today's summary: what was done, key metrics, blockers, tomorrow's plan. Send to operator."
```

### 4. Monitoring / Sales Check
```bash
openclaw cron add --name "Sales Monitor" \
  --cron "0 0,6,12,18 * * *" --tz "America/Denver" \
  --model "anthropic/claude-haiku-3.5" \
  --message "Check sales API. If new sale found, alert operator immediately. Otherwise log silently and reply HEARTBEAT_OK."
```

### 5. Content Scheduling
```bash
openclaw cron add --name "Content Scheduler" \
  --cron "0 3 * * *" --tz "America/Denver" \
  --message "Read memory/x-trend-ideas.md and memory/x-analytics-log.md. Write and schedule tomorrow's posts using winning formats. Randomize times ±5-15 min off round numbers."
```

## Model Routing by Task

| Task Type | Model | Why |
|---|---|---|
| Heartbeat / monitoring | Haiku | Simple checks, high frequency |
| Content generation | Sonnet | Creative + fast |
| Strategy / memory review | Opus | Requires deep reasoning |
| Data parsing / alerts | Haiku | Structured, low complexity |

## Guardrail Patterns

### Pre-check Pattern
Every cron that takes action should validate first:
```
Before posting: read tracker file → check today's count → skip if over limit
Before sending alert: check last alert time → skip if < 1 hour ago
Before modifying files: verify file exists and is writable
```

### Idempotency Pattern
Crons may fire twice (restarts, overlaps). Design for it:
```
1. Read state file (e.g., last-run.json)
2. Check if this run's work is already done
3. If done, skip. If not, execute and update state file.
```

### Quiet Hours Pattern
Respect operator's schedule:
```
--cron "*/20 6-22 * * *"  ← Only 6 AM to 10 PM
```
For urgent alerts, use 24/7 but add severity check:
```
If severity < CRITICAL and hour is 23-7: log only, don't alert
If severity >= CRITICAL: alert immediately regardless of time
```

## Advanced: Chained Crons

For multi-step workflows, chain crons with time offsets:

```bash
# Step 1: Gather data (6 AM)
openclaw cron add --name "Gather Trends" --cron "0 6 * * *" \
  --message "Scan for trends. Save to memory/trends-today.md"

# Step 2: Generate content (6:30 AM, after data is ready)
openclaw cron add --name "Write Posts" --cron "30 6 * * *" \
  --message "Read memory/trends-today.md. Write and schedule today's posts."

# Step 3: Monitor performance (9 PM)
openclaw cron add --name "Analyze Performance" --cron "0 21 * * *" \
  --message "Pull analytics. Compare to yesterday. Log learnings."
```
