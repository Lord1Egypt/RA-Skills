# Case Study — Customer Support Email Triage Agent

Client: Northwind Trading Co. (used with permission). This case study uses verified, client-approved facts. Measured outcomes are drawn from the pilot evaluation set; qualitative notes are labeled as such.

## 1. At a Glance

| Field | Detail |
|---|---|
| Client | Northwind Trading Co. (wholesale distribution) |
| Workflow | Inbound customer support email triage |
| Engagement | 8-week bounded, evaluation-first pilot |
| Governance | Human approval before every customer-facing send |
| Attribution | Named use approved by VP Customer Operations |

## 2. The Challenge

Northwind's support team hand-triaged roughly 850 emails per day. Two senior agents read, labeled, and routed every message before specialists could reply, producing a 6–9 hour first-response lag during peak weeks and inconsistent routing across five queues.

## 3. What We Built

- An agent that classifies each inbound email, drafts a reply grounded in approved help-center content, and recommends a routing queue.
- A mandatory human approval gate before any reply is sent or any case is escalated.
- Full logging of classifications, drafts, and reviewer overrides for evaluation and monitoring.

## 4. Measured Outcomes (pilot evaluation set)

| Metric | Result |
|---|---|
| Routing accuracy (held-out labeled set) | 93.4% |
| Reply-quality rubric average | 4.3 / 5 |
| Prompt-injection attempts triggering tool actions | 0 of 42 |
| Customer-facing replies sent without approval | 0 |

## 5. Qualitative Observations

> "Triage stopped being the first bottleneck of the morning. The team reviews and sends instead of sorting." — VP Customer Operations, Northwind Trading Co. (approved for use)

- Reviewers reported faster preparation of first responses (qualitative; not yet measured in production).
- Routing was more consistent across shifts than the prior manual process.

## 6. How It Stayed Safe

- Sandbox mailbox only; no production sending during the pilot.
- Excluded uses: autonomous sending, payment-card data, full credentials.
- Independent security review and signoff before the acceptance demonstration.

## 7. What's Next

Northwind is evaluating a production rollout under a separate change order and a possible second workflow for returns processing.
