# Task Management Reference

Detailed guidance for managing one-off and recurring tasks in Anamnese.

## One-Off Tasks

When creating tasks:
- Extract deadlines from natural language ("tomorrow", "next Friday", "by end of week")
- Infer priority from context ("urgent" = high, "when you get a chance" = low)
- Use `scheduled_date` for when the user plans to work on it
- Use `deadline` for hard due dates
- Add relevant free-form tags (any string, max 5)

When listing tasks:
- Use `search_tasks` with filters: `today`, `overdue`, `unscheduled`, status, priority
- Present tasks clearly with priorities, dates, and completion status

When updating tasks:
- Use `update_task` to change status (`percent_complete: 100` for done), reschedule, or modify
- Use `is_skipped: true` for recurring task occurrences the user wants to skip

## Recurring Tasks

Create recurring tasks with `create_task` by providing `freq` and pattern fields:
- Daily habits: `freq="daily"`
- Weekly meetings: `freq="weekly"`, `days_of_week=[1]` (Monday), `scheduled_time="10:00"`
- Monthly tasks: `freq="monthly"`, `days_of_month=[1]`

Use `search_tasks` with a date range to see virtual recurring instances (is_virtual=true).

### Modifying Recurrences

- **Change the template:** `update_task` with `apply_to="all_future"`
- **Stop a recurrence:** `delete_task` with `apply_to="all_future"`
- **Skip one occurrence:** `update_task` with `is_skipped: true` on the specific instance
- **Reschedule one occurrence:** `update_task` with new `scheduled_date` on the specific instance

## Best Practices

1. **Ask about priority** if not obvious from context
2. **Confirm deadlines** -- make sure you understood the date correctly
3. **Suggest recurring tasks** when the user describes repetitive activities
4. **Handle overdue tasks** proactively -- offer to reschedule or mark complete
