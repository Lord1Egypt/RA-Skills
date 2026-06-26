# Migration and Release Control

Use this file to design rollout and rollback plans for schema and data migrations.

## Migration Packet Requirements

Every migration packet should include:
- migration id and owner
- objective and affected entities
- forward steps with order
- rollback steps with order
- validation query set
- communication and escalation plan

Incomplete packets should not be approved for production.

## Rollout Strategies

Choose one strategy explicitly:
- expand and contract for zero-downtime schema shifts
- dual-write transition with bounded duration
- offline migration with maintenance window

Defaulting to direct in-place change often causes compatibility outages.

## Compatibility Guardrails

When application and schema evolve together:
- ensure old and new app versions both function during rollout
- keep backward-compatible reads during transition
- remove deprecated columns only after proven zero usage

Dropping compatibility too early is a common rollback blocker.

## Deployment Checklist

Before production migration:
- backup freshness verified
- restore test evidence available
- replication health confirmed
- feature flags prepared if needed
- on-call owner active during window

## Post-Deploy Verification

After deployment, verify:
- data shape and row counts
- critical query latency
- write error rates
- downstream consumer compatibility

Close the migration only when all checks pass.
