# Versioning and Deprecation — Staying on a Moving API

## Pin Styles

| Style | Example | Trap |
|---|---|---|
| URL path | `/v2/...` | Coarse: v1→v2 is a migration project, not a pin bump |
| Date header | `Stripe-Version`, `anthropic-version` | Unpinned requests float on the ACCOUNT default — someone changing the dashboard default changes prod behavior without a deploy. Pin in code. |
| Query param | `?api-version=...` (Azure style) | Easy to omit on one call and run mixed versions in one codebase |
| Media type | `Accept: application/vnd.github+json` | Invisible in the URL; forgetting it silently selects a default version |

- SDK major upgrades can move the pinned API version underneath you — read the changelog line about API version before bumping, and re-record test fixtures after (→ `testing.md`).

## Deprecation Signals — Log Them

- `Sunset` header (RFC 8594) = the date it dies; `Deprecation` header = it is on notice; `Warning: 299` = miscellaneous advisories. All arrive on SUCCESSFUL responses — nobody sees them unless you log and alert on their presence. One log line per unique endpoint+header per day is enough.
- Provider deprecation emails go to the account owner, not the developer on call — response headers are the signal you actually control.

## Tolerant Reader — What Breaks and What Must Not

- Additive changes arrive WITHOUT a version bump: new response fields, new enum values, new webhook event types, longer strings. Your parser must ignore unknown fields and route unknown event types or enum values to a logging default arm — a strict schema breaks on the provider's schedule, not yours (same law as `webhooks.md` Processing).
- Breaking changes (field removal, type change, semantic change) come with a version bump — which is exactly why floating unpinned is the risk.

## Migration Procedure

1. Read the provider's changelog between your current pin and the target.
2. Bump the pin in sandbox; run integration tests and replay recorded scenarios (→ `testing.md`).
3. Where feasible, diff old-pin vs new-pin responses on read-only endpoints.
4. Ship the prod pin bump as its own deploy — never bundled with feature work, so a regression bisects to it instantly.

## Reference Drift

Version-sensitive claims in this skill's service sections (current pricing, current rate limits, model names) lag reality — the Official Docs link at the end of each section is authoritative (`setup.md` Lookup Procedure, step 5).
