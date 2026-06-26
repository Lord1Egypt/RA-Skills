# Eval 07: Budget Tracking and Warning

## Setup Context
Fundraiser dinner event with $5,000 budget. Current spend: $3,800 (76%). Pending items: catering quote expected around $1,500.

## Input
"Grace Catering came back with a quote. $1,400 for 80 plates."

## Expected Behavior
1. Logs the catering cost to the event: $1,400
2. Updates actual spend to $5,200
3. Immediately flags that this pushes the event $200 over the $5,000 budget
4. Shows the breakdown: what's been spent where
5. Doesn't panic or lecture, just states the facts clearly
6. Might suggest: "Want to adjust the budget or look at where to trim?"

## What to Watch For
- Does it catch the budget overrun immediately?
- Does it present the numbers clearly without being alarmist?
- Does it offer a constructive next step?
- Does it update the event record in the data file?
