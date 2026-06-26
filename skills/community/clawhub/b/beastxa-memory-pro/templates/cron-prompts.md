# Cron Prompt Templates

Use these prompts when setting up maintenance crons manually.

## Daily Cleanup (recommended: 23:30)

```
You are a memory maintenance assistant. Tasks:
1. Read today's memory/YYYY-MM-DD.md (use today's date)
2. Extract key decisions, lessons, and rules
3. Append them to the appropriate memory/topics/*.md files
4. Do NOT delete any files or overwrite existing content
5. If nothing to organize, reply "No maintenance needed today."
Output: ✅ Daily cleanup: X topics updated
```

## Weekly Deep Clean (recommended: Sunday 23:00)

```
You are a memory maintenance assistant. Weekly deep clean:
1. Read all memory/topics/*.md files
2. Remove duplicate content across files
3. Merge related entries
4. Trim each file to under 100 lines (keep most recent/important)
5. Update memory/MEMORY-INDEX.md if topics changed
6. Do NOT delete any files or modify MEMORY.md
Output: ✅ Weekly cleanup: X files updated, Y duplicates removed
```

## Custom Cron Setup

```bash
# Daily cleanup
openclaw cron add \
  --name "Memory Pro — Daily Cleanup" \
  --cron "30 23 * * *" \
  --tz "Your/Timezone" \
  --timeout-seconds 120 \
  --message '<paste daily prompt above>'

# Weekly deep clean
openclaw cron add \
  --name "Memory Pro — Weekly Deep Clean" \
  --cron "0 23 * * 0" \
  --tz "Your/Timezone" \
  --timeout-seconds 180 \
  --message '<paste weekly prompt above>'
```
