# Failure Handling - Apple Pay

Use this file to classify failures fast and choose the next action.

## Common Failure Classes

| Class | Typical Symptom | First Action |
|------|------------------|--------------|
| Merchant session failure | Session request rejected | Verify merchant ID, certificate, and domain association |
| Token processing failure | Authorization declined or invalid token format | Validate backend parsing and PSP mapping |
| Environment mismatch | Sandbox token sent to production endpoint | Confirm credential and endpoint separation |
| Timeout or network errors | Checkout stalls before confirmation | Add retry strategy and clear user fallback |
| Duplicate authorization | Repeated charges on retry | Verify idempotency key usage and retry policy |

## Incident Response Loop

1. Record failure signature and affected scope.
2. Check if issue is deterministic or intermittent.
3. Validate prerequisites before code-level changes.
4. Apply smallest fix and rerun validation checklist.
5. Log mitigation and preventive action in `incidents.md`.

## User-Facing Response Rules

- Explain whether the user can retry immediately.
- Offer fallback payment without losing cart context.
- Avoid exposing internal error identifiers in UI text.

## Hard Stop Conditions

Pause rollout when:
- Merchant validation fails in production.
- Decline rates exceed normal baseline without explanation.
- Fallback flow is broken for a significant segment.
- Duplicate authorizations are detected in live traffic.
