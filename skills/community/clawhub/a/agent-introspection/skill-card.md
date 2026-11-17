## Description:

Agent Introspection guides agents through structured self-review at task start, decision points, blockers, and before delivery to reduce drift, unchecked assumptions, and overconfidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[demo112](https://clawhub.ai/user/demo112)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make an agent pause, inspect assumptions, choose corrective action, and verify changed behavior during normal task execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases could cause ordinary requests about reflection or review to trigger an introspection workflow.

Mitigation: Narrow activation phrases or require explicit invocation when routine uses of words like reflect should not change the agent's workflow.

Risk: Self-review output can be mistaken for completed validation if it does not lead to a concrete behavior change.

Mitigation: Require the skill's action and verification fields to describe what was already changed and what result was observed.

## Reference(s):

- [Philosophical Foundations](references/philosophical-foundations.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
