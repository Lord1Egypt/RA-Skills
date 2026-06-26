# Query Operations and Change Windows

Use this file when planning query changes, bulk writes, and production maintenance operations.

## Preflight for Read and Write Changes

For every planned change, capture:
- target tables and estimated row counts
- predicates used for filtering
- expected lock behavior
- worst-case rollback duration

If row counts are unknown, block execution until baseline is measured.

## Safe Sequence for High-Risk Writes

1. Run read-only preview query for the exact predicate.
2. Verify expected row count with user confirmation.
3. Start transaction when supported and practical.
4. Execute write with conservative batch size.
5. Re-run verification queries before commit.

Skipping step 1 or 2 is the most common source of mass-update accidents.

## Lock and Latency Guardrails

Before production execution:
- evaluate lock scope and expected lock time
- estimate index usage and full-scan probability
- define timeout thresholds and abort criteria

Never run unknown lock behavior during peak traffic windows.

## Query Regression Check

After query or index changes, compare:
- p95 and p99 latency
- execution plan shape
- CPU and IO profile
- error rate changes

A successful deployment is not complete until post-change metrics are stable.

## Rollback Readiness

For every risky operation, define rollback mode:
- transactional rollback
- compensating update
- restore-from-backup path

If rollback mode is undefined, treat operation as unsafe.
