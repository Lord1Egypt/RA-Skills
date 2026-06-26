# Implementation Playbook - Alipay

Use this file to choose a path and avoid mixing incompatible patterns.

## Path A: Web or H5 Checkout

1. Confirm browser, region, and wallet availability for Alipay users.
2. Build signed payment request with server-trusted totals.
3. Redirect or hand off to Alipay flow using approved gateway endpoint.
4. Handle synchronous return response and asynchronous notify callback.
5. Verify callback signature before updating order state.
6. Return deterministic success and failure states to checkout UI.

## Path B: In-App Checkout

1. Configure app integration and Alipay SDK handoff context.
2. Build request with exact amount and currency from backend state.
3. Trigger handoff and capture callback result safely.
4. Keep capture and settlement logic in backend or PSP.
5. Show fallback methods when wallet handoff fails or is unavailable.

## Path C: PSP-Mediated Integration

1. Confirm PSP supports Alipay in target country and currency.
2. Align signed payload and callback expectations between client and PSP API.
3. Enforce idempotency keys for authorization and capture calls.
4. Validate webhook handling for async state transitions.
5. Document rollback strategy for elevated declines or gateway outages.

## Data Integrity Rules

- Currency and amount precision must match backend contracts.
- Checkout session ids must map to order ids one-to-one.
- Retries must preserve idempotency key per logical payment attempt.

## Completion Criteria

- Selected path is explicit.
- Prerequisites are validated.
- Validation checklist is complete for target environment.
- Incident and rollback path is documented.
