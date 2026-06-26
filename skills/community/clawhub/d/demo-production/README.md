# Demo Production

Demo Production is a coding agent skill for turning rough, incomplete, or fuzzy product ideas into interactive demos with minimal prompting.

It is designed for moments when a user has a project idea in their head but has not fully specified the product scope, workflow, data model, UI structure, or technical implementation. The skill helps a coding agent infer the missing pieces, design a practical demo plan, build an interactive prototype, stop for user feedback, and then continue toward a more complete demo only after approval.

## What It Does

- Reconstructs vague ideas into an actionable demo brief.
- Assesses prompt completeness and fills safe gaps with explicit assumptions.
- Optionally researches similar products, open-source projects, or mature product patterns when they would improve the demo.
- Designs a practical development plan and project structure.
- Builds an interactive prototype with mock data and simulated behavior.
- Stops at the interactive demo stage for user review by default.
- Continues to a production-style demo and edge case validation after user approval.
- Supports autonomous completion when the user explicitly says not to stop.

## Pipeline

The skill uses a 4-stage pipeline:

1. **Intent Intake & Reconstruction**
   - Assess prompt completeness.
   - Infer the target user, core workflow, demo goal, assumptions, and risks.
   - Decide whether clarification or reference research is needed.

2. **Planning & Structure Design**
   - Create a short development plan.
   - Design the project structure.
   - Define prototype scope.
   - Separate mocked, simulated, and real behavior.

3. **Interactive Demo Production**
   - Build a clickable prototype with realistic mock data.
   - Include key states such as empty, loading, success, error-like, selected, and no-selection.
   - Stop for user review by default.

4. **Production Demo & Edge Case Validation**
   - Continue only after user approval, unless the user requested autonomous completion.
   - Improve core functionality, polish, responsive behavior, and edge cases.
   - Clearly report what remains mocked or simulated.

## Review Gate

The defining behavior of this skill is the Stage 3 review gate.

By default, the coding agent should stop after the interactive prototype and ask:

```text
Interactive demo is ready for review.

Please check:
1. Is the core workflow right?
2. Is the visual direction close?
3. Are any screens, actions, or states missing?
4. Should I continue to the production demo stage?
```

This prevents the coding agent from overbuilding in the wrong direction when the original prompt is vague.

## Reference Research

The skill can trigger focused web or GitHub research when an idea resembles known products, open-source projects, or mature software categories.

References are used for:

- Workflow patterns
- Information architecture
- Interaction models
- Feature boundaries
- Domain terminology
- Expected UI states

References should not be used to clone branding, proprietary UI, marketing copy, or protected assets.

## Good Use Cases

- "Build a management demo for a gym."
- "Make something like Notion mixed with Trello for indie game makers."
- "Create an AI study planner demo."
- "Build a dashboard demo for small coffee shop owners."
- "Make a prototype for an AI tool that summarizes client intake notes."

## Not Ideal For

- Fully specified engineering tickets where the implementation is already clear.
- Production-grade backend systems that require real infrastructure, auth, billing, or compliance.
- Tasks where the user wants only a plan and no prototype.
- Domains where safe assumptions would be risky and the user has not clarified requirements.

## Evaluation

The skill includes a scoring rubric in `SKILL.md` and separate test cases in `TEST_CASES.md`.
Offline scoring guidance lives in `EVAL.md`; runtime stage checklists live in `SKILL.md`.

The main success metrics are:

- Prompt reduction
- Intent reconstruction
- Assumption quality
- Research usefulness
- Pipeline discipline
- Prototype quality
- Review readiness
- Demo usability
- Edge case coverage
- Iteration readiness

In an initial A/B pilot against baseline coding agent behavior, `$demo-production` improved average score from `68.3/100` to `89.7/100`, with the largest gains in review gate compliance, mock/real boundary clarity, and edge case reporting.

## Example Invocation

```text
Use $demo-production to turn this rough idea into an interactive demo with a review gate:

Build a management demo for a gym.
```

For autonomous completion:

```text
Use $demo-production to build a full demo for a restaurant reservation manager. Make reasonable decisions and do not stop for review.
```
