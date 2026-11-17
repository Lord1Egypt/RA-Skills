# Scheduling the daily plan

Deliver the plan once per day at the user's chosen local time using OpenClaw automations (agent `automations` tool, legacy alias `cron`, or the `openclaw automations` CLI). The Gateway must be running for schedules to fire.

## Confirm before creating

- Delivery time in the user's local clock (e.g. 07:00)
- IANA timezone (e.g. `Asia/Shanghai`, `America/New_York`) — never abbreviations like CST/PST; ask for city/country if unknown
- Language (one of the 8)
- Delivery channel: this conversation or a specific channel

## In-chat (agent tool)

Use the `automations` tool (its exact parameter names come from the tool's schema; older versions accept the `cron` name):

```json
{
  "action": "create",
  "name": "Daily fitness plan",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "current",
  "payload": {
    "kind": "agentTurn",
    "message": "<self-contained prompt from the template below>"
  }
}
```

Cron expression: 5 fields `minute hour day month weekday`; `0 7 * * *` = every day at 07:00 in the given timezone. When both day-of-month and day-of-week are set, croner uses OR logic — avoid combining both fields when you mean AND.

## CLI equivalent

```bash
openclaw automations create "0 7 * * *" "<self-contained prompt>" \
  --name "Daily fitness plan" \
  --tz "Asia/Shanghai" \
  --session current
```

`--session current` binds to the active chat; `main` binds the main session; `isolated` starts a fresh session per run and needs `--announce` (plus channel/to flags) to post results.

## Self-contained payload prompt (replace placeholders)

```text
Daily fitness assistant run (skill: fitness-assistant): generate today's meal plan and workout for {name} using the saved profile — age {age}, sex {sex}, height {height}, weight {weight}, activity {activity}, goal {goal}, conditions/restrictions {conditions or none}, routine {routine}, language {language}, units {metric/imperial}, ingredient preferences {preferences or "use defaults"}, daily food budget {budget and currency or none}. Build meals from the saved ingredient choices when present, otherwise use the meal-planning defaults. Output the full daily plan in {language} with sections: Today's plan / Breakfast / Lunch / Dinner / Snack / Water / Workout / Estimated cost / Budget, including calories and macros, and match the workout to {experience} with {equipment}. When a budget is set, price only what still has to be bought and keep the day within it. If it has been 3+ days since the user last confirmed their menu/training plan, append the three-day review question and ask which ingredients the user has on hand today. Post it in this chat.
```

## Weekly summary job

Default: every Sunday at 21:00 in the user's timezone — cron `0 21 * * 0` (weekday 0 = Sunday).

```bash
openclaw automations create "0 21 * * 0" "<weekly summary prompt>" \
  --name "Weekly fitness summary" \
  --tz "Asia/Shanghai" \
  --session current
```

Weekly payload prompt (replace placeholders):

```text
Weekly fitness summary (skill: fitness-assistant): summarize the week for {name} using the saved profile — language {language}, units {metric/imperial}, training log {log or none}, menu changes {changes or none}, budget {budget and currency or none}. Cover Training this week, Nutrition this week, Spending this week (only when a budget is set), and Next week with 1-3 concrete suggestions. Use the fixed weekly-summary dialogue in references/dialogues.md and the fixed labels in languages.md. Report only recorded data; if a section has no data, say so and ask once. Keep it short and post it in this chat.
```

Content rules: [references/weekly-summary.md](weekly-summary.md). Keep one job — update the existing one instead of creating a duplicate.

## Manage

- Verify: `openclaw automations list` (check `nextRunAtMs`)
- Update time/timezone: `openclaw automations edit <job-id>` with the new schedule/tz flags (see `openclaw automations edit --help`)
- Remove: `openclaw automations remove <job-id>`
- Test manually: `openclaw automations run <job-id>`

## Notes

- If the user later changes timezone or wake time, update the existing job instead of creating a duplicate.
- `--at` one-shot timestamps without `--tz` are treated as UTC — always pass `--tz` for wall-clock times.
- When the automation runs in a chat session, the agent sends the message directly with its `message` tool; `--announce` is only the fallback delivery of the final reply.
