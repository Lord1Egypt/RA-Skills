# Requirements Brief — Proposal / SOW Handoff

This brief packages verified discovery facts for the Customer Support Email Triage Agent opportunity at Northwind Trading Co. It is the handoff into proposal/SOW scoping. It is not a proposal, contract, or launch approval.

## 1. Opportunity Summary

Northwind Trading Co. runs a shared support inbox that receives roughly 850 customer emails per day across order status, returns, billing, and product questions. Two senior agents triage and route every message by hand before specialists reply, creating a 6–9 hour first-response lag during peak weeks.

| Field | Verified Fact |
|---|---|
| Client | Northwind Trading Co. (wholesale distribution) |
| Sponsor | Dana Whitfield, VP Customer Operations |
| Workflow | Inbound support email triage, drafting, and routing |
| Daily volume | ~850 emails/day; ~1,400 on Monday peaks |
| Current owners | 2 senior agents rotate triage duty |
| Primary pain | 6–9 hour first-response lag; inconsistent routing |

## 2. Current-State Workflow

- Email lands in a shared Outlook inbox monitored during business hours.
- A senior agent reads each message, labels it, and forwards it to one of five queues.
- Specialists draft replies from memory or by searching an aging help-center wiki.
- No structured logging of categories, volumes, or reply time exists today.

## 3. Proposed Future-State (for proposal scoping)

- An agent classifies each inbound email, drafts a suggested reply grounded in approved help-center content, and recommends a routing queue.
- A human support agent reviews, edits, and approves every customer-facing reply before send.
- All classifications, drafts, and overrides are logged for evaluation and monitoring.

## 4. Systems & Data Readiness

| Item | Status | Notes |
|---|---|---|
| Mailbox access | Available | Sandbox mailbox can be provisioned for the pilot |
| Help-center content | Partial | ~120 articles; ~30 are stale and need exclusion |
| Historical labels | Missing | No labeled triage history; must build a test set |
| PII in emails | Present | Names, order numbers, partial addresses |

## 5. Human Approval Gates

- Required before any customer-facing reply is sent.
- Required before escalation to a named specialist or manager.
- Required before any refund, credit, or goodwill offer is suggested to a customer.

## 6. Risks & Excluded Uses

- Excluded: autonomous sending without human review.
- Excluded: handling of payment card data or full account credentials.
- Risk: prompt injection via crafted inbound email content — must be tested.
- Risk: stale help-center articles producing incorrect guidance.

## 7. Draft Success Criteria

- Routing accuracy at or above 90% on a held-out labeled test set.
- Median first-response preparation time reduced from hours to minutes.
- Zero customer-facing replies sent without human approval during the pilot.

## 8. Open Questions & Assumptions

> Open: Which five queues are in scope, and who owns each? Assumed the existing Outlook routing taxonomy until confirmed.

- Assumption: a non-production sandbox mailbox is acceptable for the pilot.
- Assumption: legal will approve use of de-identified historical emails to build the test set.
- Open: who is the approver for excluded-use and data-boundary decisions?

## 9. Downstream Handoff

A proposal can scope an 8-week bounded pilot only after queue ownership, the approved help-center subset, data boundaries, and excluded uses are confirmed. Route data-sensitivity and prompt-injection concerns to the security-review skill before launch.
