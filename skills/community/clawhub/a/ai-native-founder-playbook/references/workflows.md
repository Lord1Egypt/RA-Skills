# Workflows

Use these workflows to turn startup strategy into concrete AI-agent execution loops.

## Idea Validation Loop

Purpose: Prevent building before the founder has enough evidence.

Steps:

1. Draft the problem hypothesis in one sentence: target segment, painful workflow, frequency, severity, current workaround, and proposed outcome.
2. Ask an AI reasoning assistant to rewrite it until it is testable.
3. Ask for the strongest case against the hypothesis.
4. Map direct competitors, indirect substitutes, adjacent products, potential acquirers, and incumbents that could enter the space.
5. Identify why each competitor or substitute could win.
6. Draft discovery questions by hand.
7. Ask the assistant to flag leading, future-facing, broad, or socially desirable questions.
8. Run interviews with real target users.
9. After every five interviews, synthesize supporting evidence and challenging evidence separately.
10. If evidence supports the problem, define the smallest prototype that tests one core interaction.

Prompt pattern:

```text
Act as a skeptical startup advisor. Here is my problem hypothesis:
<hypothesis>

Separate facts from assumptions. Rewrite it as a testable hypothesis, then list the strongest disconfirming evidence I should look for before building.
```

## MVP Build Loop

Purpose: Build fast without letting agentic coding create incoherent product, architecture, or security debt.

Steps:

1. Write `MVP_SCOPE.md` with included features, excluded features, and feature amendment criteria.
2. Write an architecture/context document for coding agents.
3. Define expected scale for the next six months, not a fantasy future scale.
4. Pick dependencies deliberately and document tradeoffs.
5. Use short coding-agent sessions with one task per session.
6. Start each session with scope, architecture context, constraints, and verification expectations.
7. End each session with a decision log entry: what changed, why, assumptions introduced, and follow-up checks.
8. Run a security review before real users touch the product.
9. Define activation, retention, revenue, referral, and false-positive signals before launch.
10. Review user feedback weekly and sort it into product signal, onboarding signal, positioning signal, and outlier requests.

Coding-agent session template:

```text
Task:
<one implementation goal>

Context:
- Read MVP_SCOPE.md.
- Read the architecture context file.
- Preserve existing architectural decisions unless the task explicitly revises them.

Constraints:
- Do not add out-of-scope features.
- Add or update tests for changed behavior.
- Document any new architectural assumption.

Verification:
- Run the relevant tests or explain exactly why they cannot run.
```

## PMF Diagnostic Loop

Purpose: Avoid mistaking early excitement for product-market fit.

Use when:

- Signups spike but activation is weak.
- Revenue exists but retention is poor.
- Users praise the product but do not return.
- Three or more iterations fail to move PMF benchmarks.

Steps:

1. Gather activation, Day 7, Day 30, retention, revenue, referral, and qualitative feedback.
2. Ask for the skeptical interpretation of the numbers.
3. Segment users by behavior, not only persona.
4. Identify whether the gap is product, positioning, onboarding, pricing, or audience.
5. Decide: adjust, narrow, pivot, pause, or return to Idea.

Prompt pattern:

```text
Here are our PMF metrics and feedback:
<data>

Make the strongest skeptical case against our traction. Then identify whether we have a segment responding differently, whether the gap is product or positioning, and what would have to be true for this product to reach genuine PMF.
```

## Launch Operating System Loop

Purpose: Replace founder attention with repeatable systems while hardening product and operations.

Steps:

1. Run a technical debt audit with a coding agent.
2. Group findings into release blockers, next-sprint work, acceptable debt, and monitoring items.
3. Inventory founder-owned recurring tasks, decisions, approvals, and workflows.
4. Categorize each item as automate, delegate, document, or founder-only.
5. Design triggers, inputs, decision rules, outputs, owners, and escalation paths for automatable workflows.
6. Create a lightweight product management system: sprint cadence, minimum spec template, bug triage tree, and weekly metrics brief.
7. Make security and compliance recurring workstreams, not one-off audits.
8. Re-check whether acquisition is channel-driven and unit economics are known.

Prompt pattern:

```text
Audit this launch-stage operation. Classify every founder-owned workflow as automate, delegate, document, or founder-only. For each automation candidate, propose trigger, input, decision rule, output, owner, and escalation path.
```

## Scale Moat Loop

Purpose: Convert domain expertise, customer data, integrations, and workflows into defensible advantage.

Steps:

1. Create a founder bottleneck map and test what stalls if the founder is unavailable for a week.
2. Capture institutional knowledge into documented playbooks, decision rules, and reusable agent context.
3. Build enterprise readiness artifacts: documentation, SLAs, support playbooks, incident response, observability, procurement answers, and compliance evidence.
4. Build a GTM engine: segmentation, messaging, sales playbooks, analyst narrative, outbound cadence, CRM hygiene, and pipeline reporting.
5. Identify vertical edge cases generic competitors would miss.
6. Turn those edge cases into tests, validations, prompts, integrations, support workflows, or evaluation suites.
7. Audit user interaction data for behavioral patterns that can improve the product.
8. Map customer integrations and estimate switching cost.
9. Decide what integrations, APIs, webhooks, SDKs, or automations deepen workflow lock-in.

Prompt pattern:

```text
Here is our current product, customers, integrations, and usage data:
<context>

Identify three defensible advantages we can compound over the next two quarters: domain edge cases, proprietary behavioral data, and workflow lock-in. For each, propose a product action, an agent workflow, a metric, and a proof point for enterprise buyers.
```
