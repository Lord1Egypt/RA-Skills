# Validation Checklist - Apple Pay

Use this checklist before recommending release.

## Merchant and Environment

- Merchant ID configured for the correct team and environment.
- Payment processing certificate is valid and unexpired.
- Sandbox and production credentials are separated.
- Web domain association is present and reachable.

## Functional Paths

- Happy path payment succeeds.
- User cancellation path is handled without checkout lock.
- Declined payment path returns actionable messaging.
- Retry path works without duplicate authorization.
- Fallback card or alternative payment path is available.

## Platform Matrix

- Real device tests executed for supported iOS versions.
- Web tests executed on Safari versions in scope.
- Unsupported browser behavior is explicit and safe.

## Data and Consistency

- Server totals always match displayed totals.
- Idempotency behavior validated with repeated requests.
- Webhook or callback reconciliation confirms final state.

## Observability and Safety

- Payment events include request id and outcome.
- Logs avoid raw payment tokens and private data.
- Alerts exist for elevated failures or timeouts.
- Rollback plan is documented and tested.

## Release Gate

Do not recommend production rollout until all checklist sections pass.
