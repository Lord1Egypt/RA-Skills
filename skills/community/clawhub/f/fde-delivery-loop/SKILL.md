---
name: fde-delivery-loop
description: "An end-to-end delivery skill for Forward Deployed Engineers, solution architects, and enterprise AI POC teams. It combines one delivery router with eight independently runnable specialist modules to turn ambiguous customer needs into evidence, a POC charter, an acceptance-ready PRD, deployment architecture, an Agent Skill, POC evidence, adoption and value conclusions, and reusable delivery assets."
---

# FDE Delivery Loop

> Turn ambiguous customer needs into an evidence-based delivery loop that engineering can implement, QA can verify, customers can evaluate, and delivery teams can reuse.

FDE Delivery Loop makes delivery handoffs executable. Engineering receives implementation boundaries, QA receives verifiable acceptance criteria, customers receive a reviewable POC, and delivery teams receive evidence for rework and reuse.

It uses one delivery router and eight specialist modules. A module may run independently; do not restart an engagement at Stage 1 when reliable upstream work already exists. When the material or current stage is unclear, use the router to identify the earliest evidence gap and the single highest-priority next action.

## What it addresses

- An “AI assistant” request without a validated business problem, user, or priority.
- A PRD that cannot be implemented or tested.
- A polished POC without frozen success criteria or hard-failure conditions.
- A technically successful POC without adoption or business-value evidence.
- A delivery failure without evidence showing where rework belongs.
- One-off customer work that has not been codified into reusable assets.

## Delivery chain

```text
Customer evidence
  -> Problem hypothesis and baseline
  -> Business outcome and success criteria
  -> Functional and non-functional requirements
  -> Acceptance criteria and scenarios
  -> Architecture and Agent Skill
  -> Test and POC-run evidence
  -> Adoption and value realization
  -> Reusable delivery assets
```

For every material conclusion, identify its evidence, intended outcome, implementation boundary, acceptance method, pass/fail evidence, and earliest justified rollback point.

## Capability map

| Stage | Specialist module | Question | Key outputs |
|---|---|---|---|
| 1. Needs discovery | [`fde-problem-discovery/MODULE.md`](fde-problem-discovery/MODULE.md) | What problem matters and is evidence sufficient? | Evidence ledger, problem statement, hypotheses, baseline |
| 2. POC charter | [`fde-engagement-charter/MODULE.md`](fde-engagement-charter/MODULE.md) | What will be tested and when should it stop? | Outcomes, scope, success criteria, owners, risks |
| 3. Engineering handoff | [`fde-prd-writer/MODULE.md`](fde-prd-writer/MODULE.md) | How can engineering implement it and QA verify it? | FRs, NFRs, acceptance criteria, traceability |
| 4. Deployment architecture | [`fde-deployment-architect/MODULE.md`](fde-deployment-architect/MODULE.md) | How does it work under real constraints? | Architecture, data and interface contracts, controls, rollback |
| 5. Skill and POC design | [`fde-agent-skill-designer/MODULE.md`](fde-agent-skill-designer/MODULE.md) | How does it become executable and evaluable? | Skill package, guardrails, mocks, evaluations, minimum POC |
| 6. POC execution | [`fde-poc-runner/MODULE.md`](fde-poc-runner/MODULE.md) | Did it meet frozen criteria? | Run plan, evidence pack, hard-failure log, decision |
| 7. Adoption and value | [`fde-adoption-and-value/MODULE.md`](fde-adoption-and-value/MODULE.md) | Are users adopting it and is value real? | Adoption funnel, resistance analysis, value measurement |
| 8. Playbook productization | [`fde-playbook-productizer/MODULE.md`](fde-playbook-productizer/MODULE.md) | What is reusable versus customer-specific? | Reusable core, configuration, playbook, roadmap |

## Operating modes

**Smart routing.** For uncertain starting points, ongoing projects, audits, or failures, read [`fde-delivery-router/MODULE.md`](fde-delivery-router/MODULE.md) in full before loading a specialist module.

**Single-stage work.** If the user requests one stage and supplies sufficient inputs, run only that module.

**Multi-stage work.** Load one module at a time. Record the artifact, evidence gaps, version, owner, and next decision before checking the next stage’s entry conditions.

**Evidence-based rollback.** When a POC, adoption, or productization gate fails, return to the earliest stage that needs evidence or rework. The loop is reversible, not a waterfall.

**Independent audit.** Audit existing materials rather than regenerating them. Look for broken evidence chains, untestable requirements, missing non-functional constraints, unauthorized commitments, and unsupported value claims.

## Module loading rules

1. This directory is one installable suite containing all child modules.
2. In the source repository, each child entry point is `SKILL.md`. In the one-click release, children become `MODULE.md` so the archive has exactly one`SKILL.md`. Treat a module file as the corresponding specialist instructions.
3. Resolve each child module’s required `references/`,`templates/`,`assets/`, and`scripts/` relative to that child directory.
4. Load only references required for the user’s task.
5. For stateful delivery, use the router’s `scripts/project-state.js`to maintain` fde-project.json`and` fde-events.jsonl`. State integrity is not proof that a business conclusion is correct.

## Delivery discipline

- State the selected operating mode before starting.
- Inspect source material and existing artifacts; do not route solely on request keywords.
- Distinguish facts, inferences, assumptions, and open questions.
- Ask at most three questions that could change a decision; continue work that does not depend on them.
- Do not commit customer resources, scope, success criteria, production approval, or business value on the customer’s behalf.
- At every stage, report evidence, open items, artifacts, blocking risks, owner, and next decision.
- Preserve hard failures. Do not hide one behind an average score.
- Use scripts for deterministic structure checks and scaffolding only; they do not replace field judgment, architecture review, acceptance, or authorization.
- Treat POC success, production readiness, adoption, and business value as distinct claims requiring distinct evidence.
- Before productization, separate reusable core, configuration, and customer-specific exceptions.

## Definition of done

For a single-stage task, use that module’s definition of done. An end-to-end engagement is closed only when all eight stages form a continuous evidence chain, material risks have owners, adoption claims are not overgeneralized, and reusable knowledge is explicitly separated from customer-specific work.

If these conditions are not met, report the current state, missing evidence, blocking risks, and one next action. Do not create the appearance of completion.

## Author and contact

Author: xukun  
Focus: Forward Deployed Engineering, enterprise AI POCs, Agent Skills, and AI solution delivery  
Contact: xukun0821@gmail.com

This ClawHub distribution is licensed under MIT-0.
