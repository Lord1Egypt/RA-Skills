# Task Discovery Module

Purpose: allow the cron-manager skill to inspect existing cron jobs and infer patterns so the system can understand current automation usage and recommend improvements or templates.

## Capabilities

1. Scan existing cron jobs using the cron tool.
2. Extract task attributes:
   - task name
   - schedule
   - delivery channel
   - payload purpose

3. Categorize tasks into common automation patterns such as:
   - news monitoring
   - repository monitoring
   - price alerts
   - reports
   - reminders

4. Suggest improvements:
   - merge duplicate tasks
   - distribute schedules to reduce bursts
   - convert repeated custom tasks into reusable templates

## Behavior

When user requests:

- "analyze my automation"
- "review my cron tasks"
- "optimize my scheduled tasks"

The module will:

1. retrieve existing cron jobs
2. group similar tasks
3. identify patterns
4. recommend template-based replacements when possible

## Output Example

Automation Overview

Detected Categories:

- AI monitoring (2 tasks)
- GitHub tracking (1 task)
- reports (1 task)

Suggestions:

- consolidate AI monitoring tasks
- shift GitHub job to 18:00 to avoid conflicts
- convert report tasks into weekly template
