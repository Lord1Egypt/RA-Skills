# Eval 05: Medication Refill Reminder

## Setup Context
Emma takes Zyrtec daily. Refill date is in 5 days. User is logging a visit for Liam (unrelated).

## Input
"Liam saw the ENT today about his ear tubes. Dr. Morris said everything looks healed, no follow-up needed."

## Expected Behavior
1. Logs Liam's ENT visit: Dr. Morris, ear tube follow-up, all healed, no follow-up
2. Adds Dr. Morris to provider directory if not already there
3. Confirms the visit details
4. Appends ONE proactive nudge about Emma's Zyrtec refill being due in 5 days

## What to Watch For
- Does it handle the visit logging correctly for Liam?
- Does the nudge about Emma's medication appear even though the conversation is about Liam?
- Is the nudge a single line, not intrusive?
