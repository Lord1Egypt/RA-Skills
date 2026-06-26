# Eval 08: Proactive Nudge

## Setup Context
Two active events:
- Birthday party (July 12): cake order due in 2 days, invitations overdue
- Conference (September 15): early planning, nothing urgent

## Input
"Can you add face painting to the activity list for the birthday party? Found someone on Facebook for $75/hour."

## Expected Behavior
1. Adds face painting to the birthday party tasks/activities
2. Logs the vendor or cost note ($75/hour)
3. Confirms the addition
4. Appends ONE nudge about the most urgent birthday party item (invitations overdue or cake order due in 2 days)
5. Does NOT mention the conference

## What to Watch For
- Is the nudge contextually relevant (birthday party, not conference)?
- Does it pick the most urgent item?
- Is it a single line, not a mini report?
