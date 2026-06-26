# Customer Support Email Triage Agent — Pilot Proposal

Prepared for Northwind Trading Co. by CompleteTech LLC. This proposal scopes a bounded, evaluation-first pilot. It becomes a contract or invoice input only after written approval.

## 1. Executive Summary

Northwind's support team hand-triages ~850 emails per day, producing a 6–9 hour first-response lag. We propose an 8-week pilot that builds an agent to classify inbound email, draft grounded replies, and recommend routing — with a human approving every customer-facing send. Success is measured against a labeled test set before any production use.

## 2. Objectives

- Reduce first-response preparation time from hours to minutes.
- Increase routing consistency across the five support queues.
- Prove control and safety with human approval gates and logged evaluation.

## 3. Scope of Work

- Discovery confirmation: queue taxonomy, approved help-center subset, data boundaries.
- Build: classification, retrieval-grounded reply drafting, and routing recommendation.
- Human-in-the-loop approval workflow before any send or escalation.
- Evaluation: labeled test set, reply-quality rubric, and prompt-injection checks.
- Documentation, operator runbook, and handoff.

## 4. Out of Scope (this pilot)

- Autonomous sending without human review.
- Production deployment beyond the sandbox mailbox (separate change order).
- Payment-card or full-credential data handling.

## 5. Approach & Timeline

| Phase | Weeks | Outcome |
|---|---|---|
| Discovery confirmation | 1 | Locked taxonomy, data boundaries, test-set plan |
| Prototype | 2–4 | Working classify/draft/route on sandbox mailbox |
| Evaluation | 5–6 | Accuracy + safety results on held-out cases |
| Documentation & handoff | 7 | Runbook, operator quickstart, monitoring plan |
| Buffer | 8 | Fixes from acceptance review |

## 6. Commercials

| Term | Value |
|---|---|
| Engagement type | Fixed-fee pilot |
| Fee | USD 28,000 |
| Deposit | USD 8,400 at signing |
| Payment terms | Net 15 from invoice date |
| Included revisions | Two review rounds per major deliverable |

## 7. Acceptance Criteria

- Routing accuracy at or above 90% on the held-out labeled test set.
- Reply-quality rubric average at or above 4 of 5 across sampled drafts.
- Zero customer-facing replies sent without human approval.

## 8. Assumptions & Exclusions

> Pricing assumes a sandbox mailbox, access to ~90 current help-center articles, and legal approval to use de-identified historical email for the test set.

- New queues, channels, or languages are handled by written change order.
- Northwind owns model/provider account configuration and production authorization.

## 9. Recommended Next Step

Approve this pilot direction so we can issue the Agentic Development Services Agreement and a deposit invoice, then schedule kickoff.
