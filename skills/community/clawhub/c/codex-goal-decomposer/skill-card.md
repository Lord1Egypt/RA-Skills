## Description:

Break a large, fuzzy, or long-running objective into smaller goal-mode tasks with clear scope, stop conditions, and validation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjo92](https://clawhub.ai/user/hanjo92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Codex use this skill to turn broad project goals into a short sequence of scoped /goal commands with done conditions and validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated /goal commands may carry forward an ambiguous or overly broad user objective.

Mitigation: Review each command before execution and refine the objective, scope, validation method, and stopping condition where needed.

Risk: A decomposed plan may become too large or open ended for goal mode.

Mitigation: Keep the output to the next useful chain of 3-7 goals and split any risky or ambiguous goal again before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanjo92/skills/codex-goal-decomposer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Agent commands]

**Output Format:** [Markdown with inline /goal commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a final objective, recommended sub-goals, suggested execution order, notes, and validation steps.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
