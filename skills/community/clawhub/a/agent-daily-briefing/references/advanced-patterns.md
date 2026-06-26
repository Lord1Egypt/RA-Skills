# Daily Briefing — Advanced Patterns

## Multi-Channel Delivery

Deliver different briefing versions to different channels:

```markdown
## Delivery
- **Primary:** Telegram (full briefing)
- **Secondary:** Discord #general (calendar + tasks only)
```

The agent sends the full briefing to the primary channel, then a trimmed version (only the specified sections) to secondary channels.

## Briefing Chains

Trigger follow-up actions based on briefing content:

```markdown
## Post-Briefing Actions
- If any task is overdue by >2 days, flag it with ⚠️ and ask if it should be dropped or rescheduled
- If calendar has >3 meetings, add "Meeting-heavy day — protect deep work blocks" note
- If weather shows rain, add "Bring umbrella" to the closing line
```

## Weekly Recap (Friday Add-on)

On Fridays, append a weekly summary:

```markdown
## Friday Recap
- Summarize completed tasks this week (from daily memory files)
- List anything that rolled over 3+ days
- One "win of the week" highlight
```

Implementation: the agent reads `memory/YYYY-MM-DD.md` for Mon-Fri of the current week and compiles the recap.

## Travel Mode

When traveling, the briefing adapts:

```markdown
## Travel Mode
- Active: yes
- Destination: Austin, TX
- Return: March 5
- Show: destination weather, flight status, hotel confirmation
- Hide: home tasks, routine calendar items
```

## Briefing Analytics

Track briefing engagement over time by having the agent log to `memory/briefing-log.json`:

```json
{
  "2026-02-25": {
    "delivered": true,
    "sections": ["weather", "calendar", "tasks", "pending", "quote"],
    "items": { "calendar": 3, "tasks": 4, "pending": 1 },
    "overdue_tasks": 0
  }
}
```

Use this data to tune the briefing — if calendar is always empty on weekends, auto-skip it.

## Integration with Memory Architecture

The daily briefing works best alongside the [memory-os](https://clawhub.com/skills/memory-os) skill:

1. **Morning:** Briefing reads yesterday's memory file for carryover tasks
2. **Evening:** Agent writes today's memory file with completed/pending items
3. **Next morning:** Briefing picks up where yesterday left off

This creates a continuous task-tracking loop with zero manual input.

---

*Daily Briefing — Advanced Patterns — by The Agent Ledger*
*[theagentledger.com](https://www.theagentledger.com)*
