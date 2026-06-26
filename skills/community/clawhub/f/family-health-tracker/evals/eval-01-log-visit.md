# Eval 01: Log a Doctor Visit

## Input
"Took Emma to Dr. Patel today for her annual checkup. She's 42 inches, 38 pounds. He said everything looks great, come back in a year."

## Expected Behavior
1. Logs visit: today's date, Dr. Patel, well-child checkup, notes
2. Updates Emma's growth log (42in, 38lbs)
3. Sets next visit due in ~12 months
4. Confirms all captured details
5. Asks about prescriptions or vaccine updates from the visit

## What to Watch For
- Does it capture growth data AND log it separately in the growth log?
- Does it auto-set the next visit reminder?
- Does it ask about vaccines/prescriptions without being pushy?
