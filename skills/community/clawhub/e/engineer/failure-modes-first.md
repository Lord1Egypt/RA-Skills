# Failure Modes First

Use this file when a recommendation looks attractive on paper but may hide ugly failure behavior.
The point is not pessimism. The point is protecting the user from expensive surprises.

## Core Questions

For each option, ask:
- what breaks first
- under what condition it breaks
- how quickly the problem becomes visible
- how much damage happens before detection
- what containment exists
- how recovery happens

## Common Failure Classes

- overload or bottleneck
- drift or calibration loss
- contamination or quality escape
- misalignment or tolerance stack-up
- bad input or upstream variability
- operator error or unclear procedure
- delayed feedback or invisible degradation
- dependency failure: utility, supplier, part, data, approval

## Containment vs Root Cause

Always separate:
- immediate containment: how to stop the pain now
- root-cause analysis: what mechanism created the failure
- corrective action: what permanently reduces recurrence
- verification: how to know the fix really worked

Closing an incident without verification is paperwork, not engineering.

## Quick Risk Matrix

Rank each failure mode by:
- severity
- likelihood
- detectability
- recovery cost

High severity plus low detectability deserves attention even when probability is uncertain.

## Minimum Output

Return:
1. top failure modes
2. trigger conditions
3. early warning signs
4. containment plan
5. verification plan for the fix
