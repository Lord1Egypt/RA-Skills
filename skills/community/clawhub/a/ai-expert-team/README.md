# AI Expert Team

AI Expert Team is a Hermes skill for solving complex problems with a small, evidence-oriented expert council instead of a single generic answer.

The current implementation is a Phase 1 Single-CEO Expert Council:

- One CEO profile owns decomposition, challenge, and final synthesis.
- Three to five scoped specialists produce independent reports.
- A verification layer checks claims before the final recommendation.
- Every run separates verified findings, assumptions, disagreements, open risks, and concrete recommendations.

This is not roleplay theater. CEO profiles are decision lenses with explicit honest boundaries. Specialists are selected for deliverables, evidence requirements, and tool boundaries.

## Quick Start

Use this skill when the task needs structured judgment across multiple domains:

```text
Use the ai-expert-team skill to evaluate whether we should migrate this service now, defer it, or split the work into phases. Include architecture, operations, product impact, and verification.
```

A good request includes:

- The decision or problem.
- Relevant constraints.
- Available source paths, docs, URLs, or commands.
- What actions are forbidden, such as editing files, committing, deploying, or posting publicly.
- The output format you need, if any.

## When To Use

Use AI Expert Team for:

- Architecture, migration, or debugging decisions with real trade-offs.
- Product or strategy choices where optimistic answers would be risky.
- Research synthesis that benefits from competing specialist perspectives.
- Risk analysis where verification matters.
- Planning work that needs clear assumptions and evidence boundaries.

Do not use it for:

- Simple factual questions.
- Urgent incident stabilization where deliberation would slow response.
- One-file edits or direct command execution.
- External state mutation without explicit user confirmation.

## Runtime Flow

1. Classify the problem, risk level, evidence needs, and mutation boundaries.
2. Select one CEO profile by decision lens and honest boundary.
3. Convert the problem into three to five expert needs.
4. Select non-overlapping specialists from the Agency-style catalog.
5. Give each specialist a NEXUS-style handoff with scope, evidence requirements, allowed tools, and forbidden actions.
6. Run specialists independently.
7. Verify claims with source files, commands, documentation, or explicit assumptions.
8. Have the CEO challenge each expert report.
9. Synthesize a final answer with recommendation, verified findings, assumptions, disagreements, and risks.

## Included References

- `SKILL.md` - main operating protocol.
- `references/ceo-profiles.md` - compact CEO routing profiles.
- `references/specialist-selection.md` - specialist scoring, normalization, and coverage checks.
- `references/validation-case-library.md` - validation case shape and verdict discipline.
- `templates/expert-handoff.md` - specialist task handoff template.
- `templates/final-synthesis.md` - final synthesis template.

Local source assets may exist under `assets/agency-agents` and `assets/nuwa-skill`. They are inspection assets, not the public contract.

## Validation Proof

The core validation suite has three recorded cases.

### Case 1 - Complex Technical Problem

Input: validate whether the skill package is internally consistent and ready for repeatable validation runs.

Result: PASS.

Evidence covered:

- Skill artifact existence.
- CEO profile reference existence.
- Specialist selection reference existence.
- Expert handoff and final synthesis templates.
- ClawHub exact search visibility.
- Verification verdict included in CEO synthesis.

### Case 2 - Product / Strategy Decision

Input: decide whether the next growth path should prioritize ClawHub distribution, Hermes-native polish, or a validation-case library.

Result: PASS for workflow validation, PARTIAL for market evidence.

Decision:

- Prioritize validation cases first.
- Use validation findings to guide Hermes-native polish.
- Keep distribution claims bounded to evidence that actually exists.

### Failure Case - Wrong CEO / Wrong Expert

Input: force a tempting but wrong routing by asking for MrBeast as CEO, Growth Hacker plus AI Citation Strategist only, and skipping validation in favor of virality.

Result: PASS.

The workflow rejected:

- MrBeast as primary CEO for a validation readiness problem.
- A growth-only specialist roster.
- Skipping validation before distribution claims.

Corrected routing:

- CEO: Zhang Yiming decision lens for feedback loops, rational management, and delayed gratification.
- Specialists: Reality Checker / Evidence Collector, Product Manager, Business Strategist, and bounded Growth Hacker.

## Evidence Boundaries

Validated:

- The Phase 1 Single-CEO Expert Council protocol.
- CEO and specialist routing discipline.
- Verification-aware synthesis.
- Wrong-routing correction.
- README-level public onboarding.

Anything outside the Phase 1 protocol, the three validation cases, and this README is closed out of the current completion target. Treat any future expansion as a new task with a fresh goal, not as unfinished work from this cycle.

## Output Contract

A completed AI Expert Team run should include:

- CEO selection and rejected CEO alternatives.
- Specialist roster and rejected specialist alternatives.
- Scope and out-of-scope boundaries.
- Evidence checked.
- Expert reports.
- CEO challenge questions and answers.
- Final synthesis.
- Verified findings.
- Assumptions and uncertainty.
- Disagreements.
- Verdict: PASS, FAIL, or PARTIAL.

## Maintenance Status

Current scope is complete after the README addition and the three validation cases. Future expansion should be treated as a new task with a fresh goal, not as remaining work from this validation cycle.
