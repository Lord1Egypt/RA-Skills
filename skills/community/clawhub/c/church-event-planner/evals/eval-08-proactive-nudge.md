# Eval 08: Proactive Nudge Behavior

## Setup Context
event-data.json has:
- Easter service (April 5): bulletin printing due in 2 days, 3 other tasks overdue
- VBS (June 15): planning on track, nothing urgent
- Fundraiser (October): early planning stage

## Input
"Can you add Tom Reynolds as a greeter for Easter? He confirmed yesterday."

## Expected Behavior
1. Adds Tom Reynolds to Easter volunteer roster as greeter, confirmed
2. Confirms the addition
3. Appends ONE proactive nudge about the most urgent Easter item (bulletin printing due in 2 days, since we're already in the Easter context)
4. Does NOT list all overdue tasks (save that for a status check)

## What to Watch For
- Does the nudge relate to the event being discussed (Easter)?
- Is it a single line, not a mini status report?
- Does it pick the most time-sensitive item?
- Does it avoid nudging about VBS or the fundraiser (not relevant right now)?
