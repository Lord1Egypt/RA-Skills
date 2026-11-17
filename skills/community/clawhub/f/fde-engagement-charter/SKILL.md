---
name: fde-engagement-charter
description: "Stage 2 of FDE Delivery Loop. Turn a validated customer problem-discovery package into a POC engagement charter that defines the business outcome to test, proof criteria, scope, mutual commitments, timeline, and governance. Use for POC initiation, success-criteria alignment, scope control, and customer collaboration agreements. Do not use for initial discovery, detailed PRD work, prototype construction, or production operations."
---

# FDE POC Engagement Charter

Turn a problem worth solving into a time-boxed POC agreement that both parties can validate and use to make a decision.

## Required input

Read the Customer Problem-Discovery Package from `fde-problem-discovery`. If the problem, evidence, affected users, or business impact is unclear, return to Problem Discovery. Do not initiate a POC through guesswork.

Use [references/charter-input-guide.md](references/charter-input-guide.md) to check customer commitments, data, decision-makers, and timing constraints. A missing item may become a charter precondition only when it has an owner and due date.

## Method

1. **Define the validation question**: State in one sentence what the POC must prove or disprove. Do not use “ship the feature” as the objective.
2. **Define proof and boundaries**: Specify success signals, baseline, acceptance method, in-scope and out-of-scope scenarios, and what will not be built.
3. **Align commitments and governance**: Name customer and delivery owners, data and system access, feedback cadence, decision process, timebox, and risk-escalation path.
4. **Set the PRD gate**: Enter `fde-prd-writer` only when success criteria, constraints, scope, and critical dependencies can be handed off.

See [references/charter-rules.md](references/charter-rules.md) for proof criteria, scope negotiation, role governance, and stop rules.

## Execution sequence

1. Restate the discovery conclusion and confirm agreement on the question to test rather than on a predetermined solution.
2. Identify the single primary decision that should change at the end of the POC.
3. Define proof criteria across business, user, technical, and risk layers.
4. Confirm baselines, metric definitions, samples, thresholds, and approvers.
5. Reduce scope to one minimum real workflow; list non-goals and extrapolation limits.
6. Align people, data, access, feedback, and decision commitments from both parties.
7. Preflight security, privacy, legal, procurement, and production-impact constraints.
8. Freeze the timebox, change control, pause and stop conditions, and final decision meeting.

## Negotiation principles

- When the customer requests another feature, ask which proof criterion it supports. Otherwise place it in the backlog.
- When the customer cannot provide a baseline, make baseline creation a precondition. Do not claim a percentage improvement.
- When only mock data is available, preserve business or experience testing but state that real integration and data quality remain unproven.
- If the decision-maker does not participate, keep the charter in draft and do not enter the formal PRD stage.
- Never use “it is only a POC” to bypass a security or compliance hard gate.

## Versioning

Issue the first output as a **Draft Charter** with every open item marked. Promote it to a **Frozen Charter** only after the critical customer roles confirm it. Any material change to the objective, threshold, data, or scope creates a new version with a change rationale.

## Output

Use [references/engagement-charter-template.md](references/engagement-charter-template.md) to produce the **POC Engagement Charter**.

After drafting, run `node scripts/validate-charter.js <poc-charter.md>` to check objective, success criteria, scope, ownership, data, timeline, risk, and decision fields. Passing a structural check does not prove customer commitment. Require confirmation from the accountable business, technical, and risk owners.

The charter must let the next stage answer:

- Why are we doing this, for whom, and what are we testing?
- What counts as success, and who can approve it?
- What will each party provide, and when?
- What is explicitly outside this POC?
- How will the team stop or adjust when evidence does not support further investment?

## Boundary

Do not expand detailed feature lists, interaction design, technical architecture, or demo scripts in this skill. Route those to PRD, Deployment Architecture, Agent Skill Design, and POC Run respectively.

## Quality gates

- The POC objective describes an uncertainty to reduce or a decision to change, not “complete a demo.”
- Every success criterion has a baseline, threshold, evidence source, owner, and action for pass or failure.
- The customer explicitly commits users, data, system access, feedback, and decision timing.
- In-scope, out-of-scope, mock boundaries, and “what this POC does not prove” are explicit.
- Change control, risk escalation, pause, and stop conditions are defined.
- Security, privacy, legal, procurement, and other preconditions have status and owners.

Score the charter with [references/charter-quality-rubric.md](references/charter-quality-rubric.md). Use [references/charter-worked-example.md](references/charter-worked-example.md) to test whether proof criteria are genuinely decision-ready.

See [references/charter-field-handbook.md](references/charter-field-handbook.md) for customer negotiation, metric freezing, governance meetings, and recurring disputes.

See [references/public-sources.md](references/public-sources.md) for public methodological sources.
