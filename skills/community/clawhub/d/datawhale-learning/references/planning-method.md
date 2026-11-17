# Project-based Planning Method

## Inputs

Use five variables: target deliverable, current ability, weekly hours, deadline, and preferred stack. State reasonable assumptions instead of blocking on a questionnaire; ask only when a missing answer materially changes the route.

## Build the plan

1. Rewrite the goal as an observable deliverable.
2. Derive the shortest dependency chain from that deliverable.
3. Search the catalog for lessons covering each dependency.
4. Remove topics that do not affect the next acceptance test.
5. Introduce at most one major unknown per phase.
6. End every phase with an artifact and a test a learner can run without the tutor.
7. If a test fails, route to the narrow prerequisite instead of continuing forward.

## Capability levels

- **L0 — User:** can describe needs and run guided commands.
- **L1 — Prototyper:** can produce, version, and deploy a small prototype.
- **L2 — Full-stack builder:** can connect UI, API, data, authentication, and deployment.
- **L3 — AI application builder:** can integrate models, retrieval, and tools and evaluate outputs.
- **L4 — Agent engineer:** can choose paradigms, manage memory/context/protocols, and evaluate agent systems.
- **L5 — AI-native delivery lead:** can design artifact handoffs, verification evidence, governance gates, autonomy tiers, and incident feedback loops.

## AI-native SDLC routes

Use [ai-native-sdlc.md](ai-native-sdlc.md) only when the goal includes repeatable software delivery, team governance, or production operations.

- **Solo developer:** `intent.md → spec/plan → code/tests → review checklist`. Finish when another person can understand the request, reproduce verification, and trace the result to the plan.
- **AI engineer:** add project instructions, policy Skills, protected verification, continuous evals, and agent-assisted PR review. Finish when configuration changes are regression-tested like code.
- **Technical lead:** add a declared source of truth, risk-based human gates, environment-specific autonomy, audit evidence, rollback, and incident-to-eval feedback. Finish when every judgment owner and deterministic boundary is explicit.

Do not introduce autonomous maintenance before the repository has stable tests, scoped permissions, a review gate, and a rehearsed rollback path.

## Time allocation

- 3 hours/week: one small milestone; approximately 70% building, 20% review, 10% reading.
- 4–5 hours/week: one focused build plus one short verification block; keep the same 70/20/10 ratio and defer optional theory.
- 6–8 hours/week: one demonstrable increment each week; reserve every fourth week for integration and deployment.
- 12+ hours/week: one primary project plus one prerequisite gap only. Do not start two primary projects.

## Acceptance gates

Use at least one gate every one or two weeks: reproduce from a clean folder; explain the trade-off without notes; diagnose an introduced failure; let another person follow the README; or run a fixed evaluation set more than once. Reading completion is not evidence of capability.
