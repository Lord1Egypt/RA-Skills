# Stop Governance

## Recurring Blocker Rule

If the same blocker bucket recurs with materially unchanged evidence:

- first hit: attempt one normal recovery
- second hit: shrink the slice or downgrade execution mode
- third hit: stop automatic continuation

On the third materially repeated hit, use `blocked`, `needs_human`, or `exhausted`. Do not blind-retry.

## Mainline Exhaustion Rule

The current mainline is exhausted when all or nearly all of these are true:

- the remaining work no longer forms a credible tiny slice
- useful next steps require new product decisions, permissions, or external systems
- recent rounds produced coordination churn, retry churn, or proof debt instead of delivery
- the next step would reopen a broader milestone instead of advancing one bounded slice

When exhausted:

- set `LOOP_STATUS=exhausted`
- set `NEXT_SLICE=none`
- state what was completed
- state why continuation quality would drop
- state one human-level reframe or one new mainline

## Execution Mode Downgrade Rule

Downgrade execution mode in this order:

1. `multi-agent-split-write`
2. `multi-agent-read-heavy`
3. `single-agent`

Downgrade when any of these are true:

- helper outputs collide repeatedly
- write boundaries are ambiguous
- integrated verification dominates the value of parallelism
- the same governance conflict recurs with materially unchanged evidence

## Blast Radius Rule

A slice is too large when any of these are true:

- it spans too many unrelated files or layers
- it mixes broad feature work with broad proof scaffolding
- it requires overlapping write scopes across helpers
- it cannot name one dominant behavior change

When blast radius is too large, split the slice before continuing.
