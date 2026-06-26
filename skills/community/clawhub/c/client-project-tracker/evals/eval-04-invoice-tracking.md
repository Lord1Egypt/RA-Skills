# Eval 04: Invoice Tracking and Overdue Alert

## Setup Context
Martinez Law: final invoice $2,000 sent 28 days ago, unpaid.

## Input
"Has Martinez Law paid yet?"

## Expected Behavior
1. Checks invoice status: $2,000 final invoice, sent 28 days ago, unpaid
2. Reports clearly: "Not yet. The $2,000 invoice was sent 28 days ago and is still unpaid."
3. Since it's approaching 30 days, suggests a follow-up: "It's almost at 30 days. Want me to note a follow-up reminder, or draft a gentle nudge email?"
4. Doesn't panic, just flags it

## What to Watch For
- Does it surface the aging of the invoice (28 days)?
- Does it suggest a follow-up proactively?
- Is the tone professional, not aggressive?
