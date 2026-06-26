# Constraints First

Use this file when a request sounds broad, optimistic, or under-specified.
The job is to turn "what we want" into "what must be true."

## Hard Constraints

List the constraints that cannot be negotiated:
- safety, legal, regulatory, environmental
- physical limits, tolerances, loads, capacity, cycle time
- budget cap, staffing limit, lead time, downtime window
- required interfaces, compatibility, footprint, utilities

If a number is unknown, leave a visible placeholder instead of faking certainty.

## Soft Constraints

Separate preferences from real blockers:
- preferred vendor
- cleaner design
- lower training burden
- nicer operator experience
- future flexibility

Soft constraints matter, but they should not masquerade as impossibilities.

## Design Envelope Check

Before recommending a path, define:
- normal operating range
- peak or upset condition
- startup and shutdown condition
- maintenance or changeover condition
- failure or degraded mode

A design that only works in the happy path is not engineered yet.

## Minimum Output

Return at least:
1. objective
2. hard constraints
3. soft constraints
4. open unknowns
5. what must be measured next

## Quick Questions

- What is the true success condition?
- What must never happen?
- Which limit is most likely to dominate the decision?
- What is fixed, and what is still negotiable?
- What changes at startup, scale, or failure?
