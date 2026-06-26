# Task Creator Module

Purpose: standardize the creation flow for new automation tasks.

This module ensures that every cron task is created through a consistent pipeline so that schedules, payloads, and delivery channels are correctly defined.

## Creation Flow

1. **Identify task objective**
   - What should be monitored or executed?
   - Examples: news monitoring, GitHub tracking, reminders, reports.

2. **Determine schedule**
   - Ask user if schedule is missing.
   - Supported:
     - daily
     - weekly
     - monthly
     - cron expression

3. **Select delivery channel**
   - Pass to delivery-router module.
   - If multiple channels available, request user preference.

4. **Recommend template (via template-recommender module)**
   - If the task matches a template in `templates/`, load it.
   - Otherwise generate a custom cron task.

5. **Generate cron job configuration**

Example structure:

```
cron.add
schedule: <generated schedule>
payload: <task description>
delivery: <selected delivery>
```

6. **Confirm with user before deployment**

## Behavior

- Prevent duplicate tasks.
- Validate schedule format.
- Ensure delivery channel is explicit when multiple channels exist.
