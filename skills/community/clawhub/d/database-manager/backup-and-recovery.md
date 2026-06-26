# Backup and Recovery

Use this file to keep backup policy measurable and restoration confidence real.

## Backup Policy Baseline

Define for each critical database:
- backup method and frequency
- retention duration
- encryption and access policy
- storage location and redundancy

Policy without evidence is planning, not resilience.

## Recovery Targets

Record explicit recovery objectives:
- RTO: maximum tolerated restore time
- RPO: maximum tolerated data loss window

If RTO and RPO are unknown, incident decisions become inconsistent.

## Restore Drill Routine

Run drills on a predictable schedule and log:
- selected backup snapshot id
- start and finish times
- recovered row-count validation
- errors and mitigation actions

A passing drill is the strongest predictor of outage survivability.

## Failure Modes to Test

Include at least these scenarios:
- single-table accidental deletion
- corrupted index requiring rebuild
- full database restore to new instance
- point-in-time recovery to pre-incident timestamp

Testing only easy scenarios creates false confidence.

## Evidence and Audit Trail

For each drill or real recovery, capture:
- who executed
- what source was used
- what validation proved correctness
- what preventive actions were added

Recovery without evidence cannot be trusted in future incidents.
