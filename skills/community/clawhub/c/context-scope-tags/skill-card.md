## Description:

Context Scope Tags provides a lightweight chat tagging convention for setting topic boundaries, scope, and memory intent at the start of a message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phenomenoner](https://clawhub.ai/user/phenomenoner)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to make cross-topic chat boundaries explicit and to signal whether a message should be isolated, scoped, globally contextual, remembered, or not stored.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The [REM] tag can request durable memory when the host agent supports memory.

Mitigation: Use [REM] only for preferences or decisions that should be remembered, and use [NOMEM] when no durable memory should be stored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phenomenoner/skills/context-scope-tags)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown cheat sheet and routing rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Portable text tags; memory persistence depends on the host agent's memory subsystem.]

## Skill Version(s):

0.2.0 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
