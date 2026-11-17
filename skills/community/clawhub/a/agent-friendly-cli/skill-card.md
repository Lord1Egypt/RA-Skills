## Description:

Design and audit CLIs for agent usability, covering non-interactive design, progressive help discovery, pipeline support, idempotency, error handling, and structured output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g9pedro](https://clawhub.ai/user/g9pedro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design new command-line tools or audit existing CLIs for agent compatibility, including non-interactive flags, pipeline support, idempotent behavior, actionable errors, structured output, and safer destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying agent-facing CLI guidance to production or destructive commands can reduce human confirmation checkpoints.

Mitigation: Keep dry-run support, clear command scoping, audit logs, and safe defaults even when --yes or --force options are available.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with CLI examples and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance-only; no executable code, hidden behavior, or persistence.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
