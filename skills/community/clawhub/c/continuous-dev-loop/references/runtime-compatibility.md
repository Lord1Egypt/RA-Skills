# Runtime Compatibility

## Core-Compatible Runtime

A runtime is core-compatible only when it supports all of these behaviors:

- durable round state on disk or supervisor-owned state
- exact footer parsing
- exact `LOOP_STATUS` handling
- exact `NEXT_SLICE` handling
- repo-state stop or warning behavior
- execution mode recording
- coordinator role recording
- agent count recording
- contract-staleness detection

## Not Required For Core Compatibility

These are not part of core compatibility:

- scoring
- metrics dashboards
- review scoring
- heuristic architecture checks
- heuristic security checks
- auto-routing by score
- automatic push

## Precision Layer

If a runtime implements optional precision features, it MUST document their schema and routing semantics explicitly. Precision behavior MUST NOT be implied by core behavior.
