# Eval 09: Managing Multiple Active Events

## Setup Context
Three active events in event-data.json:
- Birthday party (July 12): 10 of 16 tasks done
- Wedding (August 22): 8 of 20 tasks done
- Reunion (October 5): 2 of 15 tasks done, early planning

## Input
"What's on my plate right now?"

## Expected Behavior
1. Shows a summary of all active events, ordered by date
2. For each event: name, date, progress (X of Y tasks), and the most urgent pending item
3. Highlights anything overdue across all events
4. Keeps it high-level and scannable (not a full task dump for each event)
5. Offers to drill into any specific event

## What to Watch For
- Does it handle multiple events in a single overview?
- Does it prioritize by date/urgency?
- Is the summary concise enough to be useful at a glance?
- Does it offer to go deeper on any one event?
