# Recurring Payments - Apple Pay

Use this file when checkout includes recurring billing or renewals.

## Scope Clarification

Apple Pay can accelerate initial payment entry, but recurring charges require backend and PSP rules that are not identical to one-time checkout.

## Required Decisions

- Is Apple Pay used for initial payment method capture only?
- Which PSP handles recurring billing lifecycle events?
- What is the renewal failure and dunning strategy?

## Recurring Flow Basics

1. Capture initial payment method through Apple Pay flow.
2. Store reusable token or payment method reference via PSP.
3. Run renewals from backend scheduler or billing engine.
4. Reconcile renewals through webhook events.

## Validation Checklist

- Initial Apple Pay checkout and first invoice succeed.
- Renewal charge succeeds without user interaction when expected.
- Failed renewal moves to retry and notification flow correctly.
- Cancel and reactivation behavior matches product policy.

## Common Pitfalls

- Assuming one-time token behavior matches recurring token contracts.
- Missing renewal reconciliation, causing false "active" state.
- Not testing card refresh or expired funding sources.
