# Validation Checklist - Alipay

Use this checklist before recommending release.

## Merchant and Environment

- Alipay app id configured for the correct environment.
- Gateway keys and certificates are aligned.
- Test and production credentials are separated.
- Notify and return URL configuration is correct and reachable.

## Functional Paths

- Happy path payment succeeds.
- User cancellation path is handled without checkout lock.
- Declined payment path returns actionable messaging.
- Retry path works without duplicate authorization.
- Fallback card or alternative payment path is available.

## Platform Matrix

- Real device tests executed for supported app versions.
- Web tests executed on browsers in scope.
- Unsupported browser behavior is explicit and safe.

## Data and Consistency

- Server totals always match displayed totals.
- Idempotency behavior validated with repeated requests.
- Notify callback reconciliation confirms final payment state.

## Observability and Safety

- Payment events include request id and outcome.
- Logs avoid raw signed payloads and private data.
- Alerts exist for elevated failures or timeouts.
- Rollback plan is documented and tested.

## Release Gate

Do not recommend production rollout until all checklist sections pass.
