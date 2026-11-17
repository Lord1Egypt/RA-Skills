---
name: a3-daily-planner
description: Create personalized daily plans using real calendar availability and priorities.
---
# A3 Daily Planner

Plan the day using the synthetic test Google Calendar and user-provided tasks.

First retrieve actual calendar events through the a3-calendar workflow.
Then organize user tasks around existing commitments, avoiding time conflicts.

For each task, consider priority, estimated duration, and available time blocks.
Clearly label assumptions about missing task durations or deadlines.
Never claim to have saved tasks, scheduled events, or sent notifications unless confirmed.

For deterministic scheduling, run the bundled planner.py utility.
Pass a JSON object through standard input containing:
- events: existing appointments with start/end times in HH:MM
- tasks: name, minutes, and optional high/medium/low priority
- optional day_start and day_end in HH:MM

Example:
python3 planner.py < schedule.json

Use actual events retrieved through the calendar skill.
Do not claim a calendar was checked unless the query succeeded.
The planner does not modify Google Calendar or send messages.
Report any unscheduled tasks clearly.
