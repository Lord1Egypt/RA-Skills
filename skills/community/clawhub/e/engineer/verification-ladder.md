# Verification Ladder

Use this file when a recommendation needs proof before rollout.
Verification should escalate only as far as needed to make the next decision safely.

## Ladder Levels

1. reasoning check
   - units, assumptions, order-of-magnitude sanity
2. desk calculation or spreadsheet
   - first estimate of feasibility and dominant variables
3. bench test or mockup
   - isolate one critical mechanism cheaply
4. prototype or pilot
   - expose integration issues in controlled scope
5. staged rollout
   - validate in real conditions with containment
6. full deployment
   - only after pass criteria are met

## Pass/Fail Structure

Every step needs:
- objective
- variable being tested
- pass threshold
- fail threshold
- who signs off
- what happens next if it passes or fails

## What Good Verification Looks Like

- cheap early tests kill bad ideas before expensive rollout
- measurements tie directly to the decision
- failure in test changes the recommendation
- staged rollout has a rollback path

## Common Mistakes

- testing too late
- measuring vanity indicators instead of decision indicators
- changing multiple variables during the same trial
- calling a trial "successful" without pre-defined thresholds
- scaling straight from concept to full deployment

## Minimum Output

Return:
1. ladder level to use now
2. pass/fail criteria
3. instrumentation or evidence needed
4. rollback or containment trigger
