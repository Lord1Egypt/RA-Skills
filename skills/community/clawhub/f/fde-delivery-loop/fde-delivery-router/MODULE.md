---
name: fde-delivery-router
description: "The stateful control router for FDE Delivery Loop. Identify the current stage of a customer engagement, load only the most appropriate FDE specialist skill, preserve gates, artifacts, versions, owners, decisions, and rollback history, and identify one next material action. Use for end-to-end delivery, uncertain starting points, continuing projects, handoffs, audits, and failure reviews."
---

# FDE Delivery Router

Determine the current stage, select one specialist skill, validate its handoff, and make the next decision explicit.

## Classify the input

| Input | Typical material | Preferred action |
|---|---|---|
| Raw signal | Request, meeting notes, ticket, complaint, sales lead | Enter needs discovery |
| Confirmed problem | Users, workflow, evidence, impact | Check POC-charter readiness |
| POC agreement | Criteria, scope, owners, data, timeline | Enter PRD handoff |
| Specification or solution | PRD, architecture, skill, test set | Find the earliest missing gate |
| Run evidence | Logs, evaluations, feedback, cost, latency | Enter POC run or adoption/value |
| Reusable learning | Repeated integrations, retrospectives, shared failures | Enter productization |

Read [input examples](references/input-examples.md) for common starting points and the [engagement state machine](references/engagement-state-machine.md) for rollback, parallel work, and re-entry.

## Delivery stages

| Stage | Skill | Entry signal | Exit handoff |
|---|---|---|---|
| 1. Needs discovery | `fde-problem-discovery` | Problem is ambiguous or weakly evidenced | Problem-discovery package |
| 2. POC charter | `fde-engagement-charter` | Problem is worth testing but scope and criteria are not aligned | POC charter |
| 3. PRD handoff | `fde-prd-writer` | Charter exists; engineering and QA need an executable specification | PRD handoff package |
| 4. Deployment architecture | `fde-deployment-architect` | Data, permissions, integrations, and environments need design | Architecture and risk package |
| 5. Agent Skill design | `fde-agent-skill-designer` | Approved behavior and architecture must become an evaluable skill | Agent Skill package and minimum POC |
| 6. POC run | `fde-poc-runner` | Runnable solution must be tested against frozen criteria | POC run and decision report |
| 7. Adoption and value | `fde-adoption-and-value` | Observable usage must be translated into adoption and value evidence | Adoption and value review |
| 8. Productization | `fde-playbook-productizer` | Repeated, reviewed learning can become a reusable asset | Delivery playbook or product candidate |

Use three macro phases only for navigation: Stages 1–2 Discover and Align; Stages 3–6 Design and Validate; Stages 7–8 Adopt and Productize. Do not replace the eight specialist responsibilities with the macro phases.

## Routing rules

1. Inspect real artifacts before relying on the user’s description.
2. Route to the earliest stage with a material evidence gap.
3. Start only one specialist skill at a time; do not perform its work inside the router.
4. Report current stage, selected skill, required inputs, expected artifact, and next-stage condition.
5. Keep high-risk, poorly scoped, or uncommitted work in discovery or chartering.
6. If a skill is unavailable, state that clearly and give its exact name and minimum inputs; never fabricate an invocation.
7. When downstream evidence fails, preserve the failure and route to the earliest stage needing correction.

## Four gates

Evaluate every handoff against:

1. **Evidence:** material conclusions trace to interviews, observations, metrics, tests, or accountable confirmation.
2. **Responsibility:** customer and delivery owners are assigned to inputs, decisions, and acceptance.
3. **Executability:** the receiving team has sufficient scope, constraints, and inputs.
4. **Risk:** security, privacy, authorization, compliance, and production impact are controlled or escalated.

When a gate fails, report `gap -> impact -> owner -> closure action`.

## Operating modes

- **Quick route:** return the stage and at most three critical gaps.
- **Single-stage delivery:** verify the upstream handoff and invoke only the requested skill.
- **End-to-end delivery:** maintain project state and advance only within the user’s authorization.
- **Delivery audit:** inspect existing artifacts from the earliest relevant stage.
- **Failure review:** work backward from run evidence to the responsible problem, charter, PRD, architecture, or skill defect.

## Stateful delivery

For end-to-end work, continuation, handoffs, audits, or failure review, maintain `fde-project.json` and append changes to `fde-events.jsonl`. Store only indexes and decisions, never raw sensitive customer material. Read the [project-state contract](references/project-state-contract.md).

```text
node scripts/project-state.js init --file <project-directory/fde-project.json> --project-id <ID> --name <project-name> --mode end_to_end
node scripts/project-state.js validate --file <project-directory/fde-project.json>
node scripts/project-state.js status --file <project-directory/fde-project.json>
node scripts/project-state.js history --file <project-directory/fde-project.json>
```

Every mutation requires `--actor` and `--reason`. A passing stage records its artifact, version, owner, and four gates. End each cycle with exactly one `next_action`. If state and artifact disagree, append a correction and repair the state.

## Interaction and confidence

Begin immediately when evidence is sufficient. Otherwise ask at most three questions that could change routing or a material decision, explaining their effect. If the user requests a skipped stage, list skipped gates, risks, and temporary controls; never skip a high-risk gate silently.

Report confidence as high, medium, or low. Low confidence prioritizes evidence collection rather than forcing a late-stage route.

## Definition of done

The router is done when the user knows the current decision, missing evidence, one next action, accountable owner, and expected handoff—not when it merely lists eight skills.

Use the [routing contract](references/routing-contract.md), [quality rubric](references/router-quality-rubric.md), [field handbook](references/router-field-handbook.md), and [state template](assets/fde-project.template.json) when relevant.
