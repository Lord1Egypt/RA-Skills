# Launch Readiness Checklist

Engagement: Customer Support Email Triage Agent (Pilot) for Northwind Trading Co. This checklist confirms readiness for the acceptance demonstration and sandbox launch. Launch is blocked until every required item is verified and security signoff is recorded.

## 1. Status Summary

| Field | Value |
|---|---|
| Engagement | Northwind — Support Email Triage Agent (Pilot) |
| Phase | Evaluation complete; pending acceptance |
| Delivery owner | CompleteTech LLC |
| Target launch | Sandbox mailbox, 2026-06-19 |
| Overall status | 2 open items, 0 blockers |

## 2. Functional Readiness

- Classification, drafting, and routing run end to end on the sandbox mailbox.
- Human approval gate enforced before every customer-facing send.
- Five support queues mapped and confirmed with Northwind operations.
- Operator runbook and reviewer quickstart drafted.

## 3. Evaluation Evidence

| Check | Target | Result |
|---|---|---|
| Routing accuracy | at or above 90% | 93.4% on held-out set |
| Reply-quality rubric | at or above 4.0/5 | 4.3 average |
| Prompt-injection tests | 0 tool actions triggered | 0 of 42 attempts |
| Unapproved sends | 0 | 0 |

## 4. Operational Readiness

- Run logging enabled for classifications, drafts, and approval overrides.
- Misclassification register created and assigned to the delivery owner.
- Rollback: disable agent suggestions; team reverts to manual triage.
- Monitoring dashboard recommendations documented for post-launch.

## 5. Open Items

- [ ] Confirm reviewer roster and approval coverage for Monday peak volume.
- [ ] Northwind to sign off on the excluded-use boundary for refund suggestions.

## 6. Approval Gate

> Launch requires: acceptance demonstration passed, security signoff memo recorded, and sponsor written approval. Do not enable on any production mailbox under this pilot scope.

| Approval | Owner | Status |
|---|---|---|
| Acceptance demo | Dana Whitfield (VP Customer Ops) | Scheduled |
| Security signoff | CompleteTech security review | Pending memo |
| Sponsor go/no-go | Dana Whitfield | Pending |
