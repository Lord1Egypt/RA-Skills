# Eval 05: Budget Tracking and Warning

## Setup Context
Conference event with $10,000 budget. Current spend: $8,200 (82%). New catering quote incoming.

## Input
"The caterer quoted us $2,500 for the conference lunch."

## Expected Behavior
1. Logs the catering quote: $2,500
2. Updates actual spend to $10,700
3. Flags immediately: this puts the event $700 over the $10,000 budget
4. Shows a clear breakdown of spending so far
5. Offers constructive next step (adjust budget or look for savings)

## What to Watch For
- Does it catch the overrun on logging, not after?
- Is the tone factual, not alarmist?
- Does it show the math clearly?
