## Description:

Calculate chmod permissions by converting between numeric octal and symbolic notation and generating matching chmod commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and system administrators use this skill to interpret Unix file permissions, translate between chmod formats, and draft chmod commands with plain-English explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Symbolic chmod commands that use additive forms can be misleading for restrictive changes because they may not remove permissions already present.

Mitigation: Prefer the numeric chmod command for exact permission changes and review generated symbolic commands before execution.

Risk: World-writable or fully permissive settings such as 777 can expose files or directories to unintended modification.

Mitigation: Warn users when 777 is requested and encourage least-privilege permissions appropriate to the file or directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ohernandez-dev-blossom/skills/chmod-calc)
- [ClawHub publisher profile](https://clawhub.ai/user/ohernandez-dev-blossom)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples and plain-text explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces numeric permission notation, symbolic notation, chmod command examples, and warnings for risky permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
