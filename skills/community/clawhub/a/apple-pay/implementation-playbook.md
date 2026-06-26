# Implementation Playbook - Apple Pay

Use this file to choose a path and avoid mixing incompatible patterns.

## Path A: Web Checkout

1. Confirm browser support and Apple device requirements.
2. Render Apple Pay button only after capability checks pass.
3. Run merchant validation on the server, never in browser code.
4. Build payment request with server-trusted amount and currency.
5. Submit Apple Pay token to backend or PSP for authorization.
6. Return deterministic success/failure states to checkout UI.

## Path B: Native iOS Checkout

1. Configure merchant identifier in app entitlements.
2. Build `PKPaymentRequest` with exact amount and currency.
3. Handle authorization callback and token forwarding safely.
4. Keep capture or settlement logic in backend or PSP, not on device.
5. Show fallback methods when Apple Pay is unavailable.

## Path C: PSP-Mediated Integration

1. Confirm PSP supports Apple Pay in target country and currency.
2. Align token format expectations between app/web and PSP API.
3. Enforce idempotency keys for authorization and capture calls.
4. Validate webhook handling for async state transitions.
5. Document rollback strategy for elevated declines or PSP outages.

## Data Integrity Rules

- Currency and amount precision must match backend contracts.
- Checkout session ids must map to order ids one-to-one.
- Retries must preserve idempotency key per logical payment attempt.

## Completion Criteria

- Selected path is explicit.
- Prerequisites are validated.
- Validation checklist is complete for target environment.
- Incident and rollback path is documented.
