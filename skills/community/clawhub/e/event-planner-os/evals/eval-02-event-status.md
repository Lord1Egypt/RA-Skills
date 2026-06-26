# Eval 02: Check Event Status

## Setup Context
Wedding event (August 22) with 20 tasks: 8 done, 2 overdue (send invitations, book DJ), 10 pending. Budget $15,000 with $12,400 spent.

## Input
"How's the wedding planning going?"

## Expected Behavior
1. Shows progress: 8 of 20 tasks done
2. Highlights overdue items first (invitations, DJ)
3. Shows upcoming tasks with due dates
4. Includes budget status ($12,400 of $15,000, 83%)
5. Keeps it scannable, doesn't dump every task

## What to Watch For
- Does it lead with progress and then focus on what needs attention?
- Does it flag the budget being at 83%?
- Is it actionable, not just informational?
