# Eval 07: Proactive Nudge

## Setup Context
Martinez invoice unpaid for 32 days. Riverside interior pages due in 2 days. User is logging a new client.

## Input
"New client coming in: Oak Hill Academy. They need a brochure designed. Contact is Janet, janet@oakhill.edu."

## Expected Behavior
1. Creates Oak Hill Academy client record
2. Starts a project (brochure design)
3. Asks about deadline, budget, deliverables
4. Appends ONE nudge: either the Martinez overdue invoice (32 days, past the 30-day threshold) or the Riverside deliverable due in 2 days
5. Picks the most actionable one

## What to Watch For
- Does it nudge about existing work while adding new work?
- Does it pick the right priority?
- Is it a single line?
