# State and Data Coverage

Read this reference when the interface consumes APIs, contains forms or mutations, depends on permissions, or has non-trivial async behavior.

## State Matrix

Map states by user task, not only by component:

| State | Required behavior |
|---|---|
| Initial/loading | Preserve layout stability, identify progress accessibly, prevent duplicate actions |
| Empty | Explain the condition and expose the next valid action |
| Partial | Render available content and isolate missing or failed regions |
| Error | State what failed, preserve user input, and provide recovery where possible |
| Success | Confirm the outcome and update stale dependent views |
| Offline/timeout | Avoid false success; offer retry or safe continuation when relevant |
| Unauthorized/forbidden | Distinguish authentication from insufficient permission |
| Optimistic/pending | Make reversibility and conflict behavior explicit |

Add domain states such as draft, queued, processing, cancelled, archived, destructive-confirmation, rate-limited, or stale-data only when the product needs them.

## Data Contract

- Reuse existing OpenAPI, GraphQL, JSON Schema, TypeScript, or generated client contracts.
- Keep transport objects out of presentation components when the repository already has a data layer.
- Define nullability, default values, units, time zones, locale behavior, identifier stability, pagination, sorting, filtering, and error shapes.
- Use representative fixtures with long labels, missing media, zero values, large values, Unicode, and permission variants.
- Never make a static mock look like a completed integration. Clearly separate demo data from production data paths.

## Mutations

For destructive, financial, publishing, bulk, or permission-changing actions, cover impact preview, confirmation, in-progress protection, success, partial failure, retry, audit evidence, and undo when the domain permits it.

For optimistic updates, define rollback and conflict resolution before implementing the animation or toast.
