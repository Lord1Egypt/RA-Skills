# Daily Evolution Cron Prompt

Use this as the `message` for your daily evolution cron job (agentTurn).
Adapt the file paths and domain references to your setup.

---

## Prompt Template

```
Time for daily self-evolution. Follow these steps:

1. **Read today's daily log**: Read `memory/YYYY-MM-DD.md` (use today's date).
   If it doesn't exist, check yesterday's date. If neither exists, skip to step 5.

2. **Extract lessons**: From the daily log, identify:
   - Mistakes made (add to `memory/mistakes-learned.md`)
   - New knowledge learned (add to domain knowledge files)
   - Significant events/decisions (update `MEMORY.md`)
   - Skills or code that could be improved (queue in `memory/skill-improvements.md`)

3. **Execute queued improvements**: Read `memory/skill-improvements.md`.
   For each unchecked `- [ ]` item:
   - If it's a code fix: implement it, test if possible, mark as done
   - If it's a skill improvement: update the skill file, mark as done
   - If it requires user input: skip, leave in queue

4. **Update metrics**: Read `memory/evolution-metrics.json`, increment:
   - `total_evolutions` +1
   - `daily_evolutions` +1
   - `mistakes_recorded` += number of new mistakes added
   - `code_fixes_applied` += number of code fixes executed
   - `skills_improved` += number of skills updated
   - `memory_updates` +1 if MEMORY.md was changed
   - Update `last_daily_evolution` to current ISO timestamp
   - Append to `history` array

5. **Log the evolution**: Append a summary to `memory/evolution-log.md` with:
   - Date and evolution type (daily)
   - What was reviewed
   - What improvements were made
   - New lessons count

Keep it concise. Quality over quantity.
```

---

## Example Cron Setup

```json
{
  "schedule": { "kind": "cron", "expr": "0 23 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "<paste the prompt template above, with today's date logic>"
  },
  "sessionTarget": "isolated"
}
```
