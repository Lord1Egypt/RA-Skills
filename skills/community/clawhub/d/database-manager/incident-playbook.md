# Incident Playbook

Use this file when production data integrity or database availability is at risk.

## Severity Triggers

Escalate to incident mode when any occurs:
- sustained error-rate increase tied to database operations
- replication lag breaching service threshold
- data corruption or accidental destructive write
- migration causing user-visible outage

## First 15 Minutes

1. Declare incident owner and communication channel.
2. Freeze non-essential database changes.
3. Capture current blast radius and impacted services.
4. Decide containment action (throttle, rollback, failover, or read-only mode).

Speed and role clarity are more important than perfect diagnosis early.

## Containment Patterns

Use the least risky path that reduces user impact:
- pause write-heavy jobs
- disable problematic feature flags
- revert to known-safe query path
- rollback migration if blast radius grows

Do not introduce multiple speculative fixes simultaneously.

## Data Integrity Verification

After containment, verify:
- row counts for impacted entities
- referential integrity checks
- application-level correctness for critical flows

A recovered service is not done until data correctness is confirmed.

## Closure and Follow-up

Before closing the incident:
- document root cause and contributing factors
- list timeline with exact decisions
- define one guardrail per failure mode
- schedule follow-up validation date

Incident closure without guardrails invites repeat failures.
