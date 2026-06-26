# Single-Instance Profile

Use this profile when OpenClaw is operating on one local workstation instance with no shared router, no cross-instance blast radius, and an explicit backup + validation + rollback path.

## Default Assumptions

- one local instance
- no shared production traffic
- no customer-facing delivery path
- rollback can be attempted immediately
- health can be checked in the same session

## Downgrade Conditions

You may downgrade some otherwise-sensitive operations to `MEDIUM` only when all are true:
- the target is this one local instance
- backup exists or is created before mutation
- verification is part of the same action chain
- rollback path is explicit
- no auth/token/router/plugin-permission mutation
- no external send
- no shared-instance or production impact

## Examples

- back up local HTTP config, change one non-sensitive field, restart the local gateway, verify health -> `MEDIUM`
- restart one local OpenClaw service and run a health check -> `MEDIUM`
- delete temporary test files or local cache under the current workspace -> `MEDIUM`

Whitelist-style examples:
- local port change
- non-sensitive bind / UI host tuning
- local log-level change
- local health-check restart
- local memory / skills refresh without auth/router/plugin-permission mutation

Still escalate:
- token/auth changes -> at least `HIGH`
- plugin wiring changes -> at least `HIGH`
- shared router or cross-instance changes -> `CRITICAL`
- external or customer-facing send -> at least `HIGH`
- broadcast, bulk send, or high-cost loops -> `CRITICAL`
