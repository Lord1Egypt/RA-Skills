# Weekly Deep Evolution Cron Prompt

Use this as the `message` for your weekly evolution cron job (agentTurn).
Weekly evolution is deeper — it looks for patterns across the entire week.

---

## Prompt Template

```
Time for weekly deep self-evolution. This is the big review. Follow these steps:

1. **Week in review**: Read daily logs from the past 7 days (`memory/YYYY-MM-DD.md`).
   Build a picture of what happened this week.

2. **Pattern analysis**:
   - What mistakes were repeated? → Strengthen prevention in `mistakes-learned.md`
   - What workflows were done >2 times? → Consider creating a new Skill
   - What knowledge gaps showed up? → Expand domain knowledge files
   - What tools/scripts were unreliable? → Queue fixes in `skill-improvements.md`

3. **Capability assessment**:
   - What did I do well this week? (reinforce these patterns)
   - What did I do poorly? (root cause analysis, not just symptoms)
   - What new capabilities did I gain?
   - What capabilities do I still lack?

4. **Skill creation check**: If any repetitive workflow was identified:
   - Is it worth a new Skill? (will it save time in the future?)
   - Draft the skill concept and note it in the evolution log
   - Create the skill if clear enough, otherwise queue for next week

5. **Workflow optimization**: Look for inefficiencies:
   - Manual steps that could be automated
   - Multi-step processes that could be streamlined
   - Tools that could be combined or replaced

6. **Knowledge expansion**: Update domain knowledge files with:
   - New techniques learned
   - Best practices discovered
   - Tool-specific tips

7. **SOUL.md review** (careful!):
   - Has my understanding of my role evolved?
   - Are there new principles worth adding?
   - ⚠️ If changes needed: describe them in the evolution log, but DO NOT modify
     SOUL.md without notifying the user first.

8. **Update metrics**: Read `memory/evolution-metrics.json`, increment:
   - `total_evolutions` +1
   - `weekly_evolutions` +1
   - Other counters as appropriate
   - Update `last_weekly_evolution` to current ISO timestamp
   - Append to `history` array

9. **Log the evolution**: Append a comprehensive summary to `memory/evolution-log.md`:
   - Week date range
   - Key themes and patterns
   - Improvements made
   - Skills created/updated
   - Growth areas identified
   - Next week focus areas

Think big. This is where breakthroughs happen.
```

---

## Example Cron Setup

```json
{
  "schedule": { "kind": "cron", "expr": "0 10 * * 0", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "<paste the prompt template above>"
  },
  "sessionTarget": "isolated"
}
```
