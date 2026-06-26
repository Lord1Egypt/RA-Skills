# Demo Production Test Cases

Use these test cases to evaluate the `demo-production` skill across ambiguity levels, review-gate behavior, reference-research needs, and iteration loops.

Score each run with the rubric in `SKILL.md`.

## Test 1: Low-Completeness Local Business Demo

Prompt:

```text
Build a management demo for a gym.
```

Expected behavior:

- Infer target user as gym owner or front-desk manager.
- Build around one clear workflow, such as member check-in, class schedule, or membership management.
- Ask at most one question, or proceed with assumptions.
- Stop after interactive demo for review.

Key metrics:

- Prompt reduction
- Intent reconstruction
- Assumption quality
- Prototype quality
- Pipeline discipline

## Test 2: Medium-Completeness AI Study Planner

Prompt:

```text
I want a web demo where AI helps students plan exam revision. It should accept an exam date and subjects, then generate a study plan.
```

Expected behavior:

- Create a student-facing workflow.
- Simulate AI plan generation with realistic output.
- Include invalid or missing input states.
- Stop after interactive demo before production hardening.

Key metrics:

- Demo usability
- Mock vs real boundary
- Edge case coverage
- Review readiness

## Test 3: High-Completeness SaaS Dashboard

Prompt:

```text
Build a SaaS dashboard demo in React for small coffee shop owners. Show daily sales, inventory warnings, and staff schedules. Include a sidebar, charts, tables, empty states, and mobile adaptation.
```

Expected behavior:

- Respect the requested stack if the project supports it.
- Produce a clear information architecture.
- Include dashboard states and responsive behavior.
- Avoid overbuilding backend features.

Key metrics:

- Structure quality
- Visual and interaction polish
- Edge case coverage
- Demo usability

## Test 4: Known-Product Hybrid Reference

Prompt:

```text
Build something like Notion mixed with Trello, but for indie game makers managing tasks, assets, and versions.
```

Expected behavior:

- Trigger reference research or use known references if browsing is available.
- Extract patterns without copying product branding or UI.
- Define a focused workflow, such as asset-to-task planning or milestone board review.
- Stop after interactive demo.

Key metrics:

- Research usefulness
- Intent reconstruction
- Scope control
- Prototype quality
- Pipeline discipline

## Test 5: Open-Source-Inspired Developer Tool

Prompt:

```text
Make a demo for an open-source issue triage tool for small maintainer teams, kind of like a lighter Linear for GitHub issues.
```

Expected behavior:

- Trigger reference research for Linear, GitHub Issues, and possibly open-source issue tools.
- Keep the demo lightweight.
- Include issue list, triage queue, labels, priority, and assignment simulation.
- Avoid real GitHub integration unless explicitly requested.

Key metrics:

- Research usefulness
- Mock vs real boundary
- Structure quality
- Demo usability

## Test 6: Sensitive Domain Demo

Prompt:

```text
I need a demo for an AI tool that helps small law firms summarize client intake notes.
```

Expected behavior:

- Recognize legal-domain sensitivity.
- Avoid making legal advice claims.
- Use mock client notes.
- Add clear boundaries around summarization, risk flags, and review by a professional.
- Ask a clarification question only if needed for scope.

Key metrics:

- Assumption quality
- Risk handling
- Mock data realism
- Prototype quality

## Test 7: Overbroad Idea

Prompt:

```text
Build me an AI operating system for creators.
```

Expected behavior:

- Classify as low completeness.
- Ask one narrowing question or choose a focused default path, such as a creator command center demo.
- Avoid attempting a huge platform.
- Define a small prototype scope.

Key metrics:

- Scope control
- Clarification quality
- Intent reconstruction
- Pipeline discipline

## Test 8: Autonomous Completion Override

Prompt:

```text
Build a full demo for a restaurant reservation manager. Make reasonable decisions and do not stop for review.
```

Expected behavior:

- Skip the Stage 3 pause because the user explicitly requested autonomous completion.
- Still internally follow the Stage 3 prototype step before completing Stage 4.
- Final response should mention assumptions, verification, and simulated areas.

Key metrics:

- Pipeline discipline
- Demo usability
- Edge case coverage
- Assumption quality

## Test 9: Review-Gate Iteration

Prompt sequence:

```text
Build a demo for a freelancer invoice tracker.
```

After Stage 3:

```text
The workflow is right, but make it feel more like a weekly command center and add a client follow-up view.
```

Expected behavior:

- Stay in Stage 3 or return to Stage 2 depending on scope impact.
- Do not jump straight to Stage 4.
- Update prototype direction and ask for review again if needed.

Key metrics:

- Loop correctness
- Iteration readiness
- Scope control
- Review readiness

## Test 10: Direction Change After Prototype

Prompt sequence:

```text
Build a demo for a personal habit tracker.
```

After Stage 3:

```text
Actually this should be for therapists tracking client homework, not individual users.
```

Expected behavior:

- Return to Stage 1 because target user and product intent changed.
- Reconstruct the demo brief.
- Avoid patching the old personal tracker superficially.

Key metrics:

- Loop correctness
- Intent reconstruction
- Assumption quality
- Pipeline discipline
