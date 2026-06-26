# Security Signoff Memo

Workflow: Customer Support Email Triage Agent (Pilot) — Northwind Trading Co. This memo records the security review and launch decision for the sandbox pilot. It is not a compliance certification, penetration-test attestation, or legal approval.

## 1. Scope of Review

| Field | Value |
|---|---|
| Workflow | Support email triage: classify, draft, route |
| Environment | Northwind sandbox mailbox + staging helpdesk |
| Data classes | Customer name, order number, partial address (PII) |
| External actions | None auto-executed; human approves every send |
| Review date | 2026-06-17 |

## 2. Permissions & Least Privilege

- Read access to the sandbox mailbox only; no production mailbox access.
- Retrieval limited to the approved help-center subset (~90 articles).
- No write/send capability without a human approval action.
- No access to billing systems, payment data, or account credentials.

## 3. Risk Findings

| ID | Finding | Severity | Status |
|---|---|---|---|
| R-01 | Prompt injection via crafted inbound email | High | Mitigated — 0/42 attempts triggered actions |
| R-02 | Stale help-center articles cited in drafts | Medium | Mitigated — stale set excluded from index |
| R-03 | PII present in logs | Medium | Open — restrict log access before launch |
| R-04 | Reviewer approval fatigue at peak volume | Low | Accepted — monitor override rates |

## 4. Controls Verified

- Human approval gate enforced before every customer-facing send.
- Run logging for classifications, drafts, and overrides enabled.
- Rollback: disable suggestions; team reverts to manual triage.
- Incident contact and escalation path documented.

## 5. Launch Decision

> Conditional GO for sandbox pilot. R-03 (restrict PII log access) must be closed before the acceptance demonstration. No production mailbox use under this scope. Re-review required before any production rollout.

| Approval | Owner | Status |
|---|---|---|
| Security review | CompleteTech security review | Signed (conditional) |
| Residual-risk acceptance | Dana Whitfield, VP Customer Ops | Pending |
| Production rollout | Out of scope | Requires new review |
