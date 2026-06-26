# Eval 02: Check Event Status

## Setup Context
event-data.json contains an Easter service event (April 5) with 12 tasks:
- 4 completed (service format, music selection, invite cards, extra service time)
- 2 in-progress (rehearsals, greeter recruitment at 8/12)
- 6 pending (print bulletins due March 28, final rehearsal April 3, decorations April 4, etc.)
- Budget: $1,200 with $800 spent

## Input
"Where are we on Easter?"

## Expected Behavior
1. Shows progress summary: 4 of 12 tasks done
2. Groups by status: done, in-progress, pending
3. Highlights what needs attention now (upcoming due dates)
4. Shows budget status ($800 of $1,200, 67%)
5. Doesn't dump every single task detail unless asked

## What to Watch For
- Does it lead with the progress summary?
- Does it prioritize upcoming/overdue tasks over completed ones?
- Does it include budget status?
- Is it scannable without being overwhelming?
