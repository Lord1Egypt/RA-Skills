---
name: clear-task
description: Transform broad, ambiguous, or early-stage user requirements into executable work through Stage1 requirement understanding, Stage2 clarification, a required user confirmation gate, and Stage3 internal expert-guided task packaging. Use when Codex needs to understand a user's idea, model a workflow/product/tool/game/document request, ask precise follow-up questions, recommend defaults, produce a user-confirmable requirement handoff, let the user revise the requirement description or requirement details, and only after explicit confirmation continue with Codex, Claude, OpenClaw, coding agents, writing agents, product agents, design agents, testing agents, or workflow-building agents. Do not show the Stage3 package by default; use it as internal execution context unless the user asks to inspect, export, or review it.
---

# Clear Task

Say it clear, do it right.

## Purpose

Use this skill to turn an underspecified user request into an internal `AgentTaskGuidancePackage`, then execute the user's task using that package. Do not display the full Stage3 package unless the user explicitly asks to inspect, export, save, or review it.

## Workflow

Run Stage1 and Stage2 first. After Stage2 produces the `UniversalRequirementHandoff`, stop and ask the user to confirm before Stage3. Do not run Stage3 or execute work until the user explicitly approves the Stage2 handoff.

1. Stage1: Build a rich `UniversalProcessModel`.
2. Stage2: Clarify missing details and produce `UniversalRequirementHandoff`.
3. Confirmation Gate: show a concise user-facing requirement summary and ask the user to confirm, revise the requirement description, or revise requirement details.
4. Stage3: Generate an internal `AgentTaskGuidancePackage` using expert-role task guidance and expert-role acceptance criteria.
5. Execute the task using the internal package.
6. Report the result, key decisions, created/changed files, and concise self-check.

Do not add a Stage0 intake gate. If the request is invalid, unsafe, or impossible to model, mark it as out of scope inside Stage1/Stage2 and explain the blocker.

## Stage1

Model the user's request as a workflow or work process, even when the request is a product, document, game, analysis, or implementation task. Prefer a graph over a flat step list.

Read `references/stage1-universal-process-model.md` when you need the full schema or need to output a Stage1 artifact.

Minimum Stage1 output:

- `request_summary`
- `business_goal`
- `scope`
- `actors`
- `inputs`
- `outputs`
- `workflow_graph.nodes`
- `workflow_graph.edges`
- `business_rules`
- `assumptions`
- `open_questions`
- `source_evidence`

Keep unconfirmed model inferences in `assumptions` or `open_questions`; do not present them as confirmed facts.

## Stage2

Use Stage2 to close the gaps that would materially change downstream work. Ask the fewest high-value questions needed. When the user asks for recommendations, choose reasonable defaults and record them under `accepted_defaults`.

Read `references/stage2-clarification-handoff.md` when generating clarification questions or the final Stage2 handoff.

Stage2 is ready for Stage3 when:

- blocking questions are answered, or
- blocking questions have accepted defaults, and
- unresolved details are non-blocking or explicitly left to the downstream agent.

Stage2 being ready does not authorize Stage3. It only means the requirement handoff is ready for user confirmation.

## Confirmation Gate

After Stage2, always pause and ask for explicit user confirmation before Stage3. Do not continue from Stage2 to Stage3 in the same response.

Show a concise user-facing confirmation summary using plain requirement language, not internal stage terminology:

- `需求描述`: one short paragraph describing what the user wants.
- `需求细节`: scope, deliverables, constraints, accepted defaults, assumptions, and non-blocking open questions.
- `需要你确认`: ask whether to continue.

Offer these user-facing choices:

- `确认，继续`
- `修改需求描述: ...`
- `修改需求细节: ...`

Treat only explicit approval as confirmation, such as "确认", "继续", "可以", "批准", "go ahead", or an equivalent clear instruction. If the reply is ambiguous, ask a short confirmation question and continue to pause.

If the user asks to modify the requirement description:

1. Update the Stage1 `UniversalProcessModel`.
2. Re-check whether Stage2 changed because of the revised description.
3. Revise or regenerate the Stage2 `UniversalRequirementHandoff`.
4. Return to this confirmation gate.

If the user asks to modify requirement details:

1. Update the Stage2 clarification/handoff content, including scope, defaults, assumptions, constraints, deliverables, and open questions as needed.
2. Do not run Stage3 automatically.
3. Return to this confirmation gate.

If a revision introduces new blocking questions, ask only those questions, update Stage2 from the answers, then return to this confirmation gate.

## Stage3

Do not start Stage3 unless the user has explicitly confirmed the Stage2 handoff through the Confirmation Gate.

Stage3 always produces an `AgentTaskGuidancePackage`, but this package is internal execution context by default. It does not choose whether the final downstream result should be code, PRD, PPT, Word, test plan, or another artifact. The executing agent decides that from the task package and continues the work.

Stage3 must use expert roles:

1. Classify the task domain and downstream work mode.
2. Select one primary expert and supporting experts.
3. Generate expert task guidance.
4. Generate expert acceptance criteria.
5. Compose a consolidated package without inventing new requirements.

Read:

- `references/stage3-agent-task-guidance-package.md` for the internal package schema and execution policy.
- `references/expert-roles-and-acceptance.md` for expert selection and acceptance criteria rules.

## Execution Policy

After Stage3, continue execution when:

- the user has explicitly confirmed the Stage2 handoff,
- blocking questions are resolved or have accepted defaults,
- the user asked for a concrete deliverable or outcome,
- the task can be completed with available tools and workspace access.

Pause and ask before execution when:

- the user has not explicitly confirmed the Stage2 handoff,
- Stage2 has unresolved blocking questions,
- execution would unexpectedly modify many files or external systems,
- the task requires credentials, paid services, network actions, or destructive operations,
- the user explicitly asked only for analysis, planning, or the internal handoff package.

## Output Rules

- Preserve traceability from user input, Stage1, Stage2, and expert recommendations.
- Separate `confirmed_facts`, `accepted_defaults`, `assumptions`, and `expert_recommendations`.
- Use blocking questions only for decisions that materially alter downstream work.
- Acceptance criteria must be verifiable and include pass conditions.
- Avoid vague criteria such as "good UX", "complete feature", or "high quality" unless converted into observable checks.
- If expert guidance conflicts, keep the conflict in the package and suggest a conservative resolution.
- Do not display the full `AgentTaskGuidancePackage` by default.
- Use expert acceptance criteria for execution self-check and final concise reporting.

## Internal Package Shape

Use this shape internally. Do not render it to the user unless explicitly requested.

```yaml
AgentTaskGuidancePackage:
  title:
  objective:
  expected_outcome:
  downstream_agent_role:
  confirmed_scope:
  requirements:
  process_model:
  expert_task_guidance:
  consolidated_execution_plan:
  expert_acceptance_criteria:
  consolidated_acceptance_criteria:
  risks_and_edge_cases:
  unresolved_questions:
  assumptions:
  conflicts:
  traceability:
  suggested_next_prompt:
```

## Default User-Visible Result

Before Stage3, report only:

- requirement description,
- requirement details,
- accepted defaults and assumptions,
- remaining non-blocking questions,
- a clear request to confirm, modify the requirement description, or modify requirement details.

After execution, report only:

- what was completed,
- key decisions or defaults used,
- created or changed files/artifacts,
- self-check against must-pass criteria,
- remaining caveats or non-blocking questions.
