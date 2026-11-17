# GraphQL APIs — Consuming (GitHub v4, Shopify, Linear, monday)

## Errors

- HTTP 200 with an `errors` array is the normal failure mode (SKILL.md Core Rule 5). Check `errors` AND `data` on every response: partial success ships both — some fields resolved, others null with a matching error entry.
- The machine-readable cause is `errors[].extensions.code`; the message text is prose and changes without notice — never branch on it.
- Transport-level errors still occur (401 before the resolver runs, 5xx HTML from the edge) — handle both layers (→ `debug.md` Intermittent Failures).

## Pagination — Relay Connections

- The pattern: `first: N, after: $cursor` with `pageInfo { hasNextPage endCursor }`; loop while `hasNextPage` — the same termination law as `pagination.md` (the API's signal, never item count).
- Cursors are opaque and bound to the query's sort and filters — changing arguments mid-pagination invalidates them.
- Nested connections multiply pages: paginating a list inside every node of another list needs per-node cursors — restructure into a second query keyed by the parent IDs collected first.

## Rate Limits Are Cost-Based

- Cost is computed from what the query REQUESTS, not what exists: `first: 100` costs like 100 nodes even when 3 match — ask for realistic page sizes.
- GitHub's GraphQL budget is points per hour scored per query; Shopify runs a calculated-cost leaky bucket. One deep query can spend what hundreds of REST calls would — during development, select the API's rate-limit field alongside your data (GitHub: `rateLimit { cost remaining }`) to see each query's price.

## Query Hygiene

- Select only the fields you read: there is no `*`, and over-selection is the cost multiplier above.
- Variables, never string interpolation: `query($id: ID!)` plus a variables object — interpolation breaks on quotes and is the GraphQL injection vector.
- Need N objects of the same type? Alias them in one query (`a: node(id: "1") {...} b: node(id: "2") {...}`) — one round trip; the cost still sums per alias.
- Mutations return selectable fields: select what confirms the write (the new ID, updated timestamp) — an empty selection throws away the confirmation you need for idempotent retries.
- Introspection is often disabled in production — develop against the provider's published schema or docs, not runtime introspection.
