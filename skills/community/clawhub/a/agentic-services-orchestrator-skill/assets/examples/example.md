# Engagement Orchestration Overview

Worked example of the CompleteTech LLC agentic services lifecycle for one engagement: the Northwind Trading Co. Customer Support Email Triage Agent pilot. The orchestrator owns state, routing, sequencing, handoffs, and approval gates; specialist skills own their artifacts.

## 1. Lifecycle Routing

| Stage | Skill | Artifact produced | Gate before next |
|---|---|---|---|
| Discovery | discovery | Requirements brief (DISC-2026-0117) | Facts verified |
| Proposal | proposal | Pilot proposal (PRO-2026-0188) | Commercial approval |
| Contract | contract | Agreement (ADSA-2026-0142) | Signature + deposit |
| Delivery | delivery | Launch readiness checklist | Security signoff |
| Overlay | security review | Signoff memo (SEC-2026-0090) | Conditional GO |
| Support | customer success | Health scorecard & QBR | Renewal decision |
| Proof | case study | Named case study (approved) | Public-use approval |
| Billing | invoice | Milestone invoice (INV-2026-0461) | Billing approval |
| Comms | email | Outbound sequence | Verified recipient |
| Packaging | envelope | #10 addressed envelope | Approved to send |

## 2. Example project_state Handoff

> The orchestrator passes a compact state object between skills and uses TBD for unknowns rather than inventing facts.

| Field | Value |
|---|---|
| client | Northwind Trading Co. |
| workflow | Support email triage agent |
| lifecycle_stage | delivery |
| approvals.commercial | approved |
| approvals.security | conditional (R-03 open) |
| approvals.external_send | unknown |
| next_skill | security-review → delivery |
| next_action | Close R-03, then run acceptance demo |

## 3. Routing Logic

- Select the earliest missing lifecycle artifact unless the user requests a specific support output.
- Invoke security review before launch, new tools, external actions, billing, or public proof.
- Use email only for message copy; use envelope only for packaging and delivery-readiness.
- Return a handoff package: artifact paths, decisions, open questions, blockers, approvals, next owner.

## 4. Boundary Reminders

- Discovery facts are not a proposal; a proposal is not a contract; a contract does not authorize launch.
- Case studies, testimonials, and named references require verified client approval.
- Certificates require verified recipient/course facts and are not delivery acceptance or public proof.

## 5. Messy Real-World Scenario

During delivery, Northwind asks whether the pilot can recommend refunds. The signed scope excludes refund decisions, so the orchestrator keeps the current delivery track inside the approved support-triage scope and opens two parallel draft-only tracks.

| Track | Status | Owner | Blocker |
|---|---|---|---|
| Delivery | Active | CompleteTech delivery lead | Launch waits on retention policy |
| Security review | Blocked | TBD | Security contact and refund-policy risk unknown |
| Change order | Draft only | CompleteTech engagement lead | Commercial approval for refund recommendations missing |

The prior security approval remains conditional for the original pilot only. Refund-related delivery, billing, contract updates, and external send stay blocked until commercial, legal, billing, security, and recipient approvals are current.

## 6. Recovery Action

- Keep the pilot sandboxed and inside approved support-triage scope.
- Ask the sponsor whether refund recommendations should become a formal change order.
- Route refund data, policy access, and tool permissions to security review before any implementation.
- Mark any expanded-scope approval as `requested` or `conditional`, never approved, until evidence names the approver and permitted action.
