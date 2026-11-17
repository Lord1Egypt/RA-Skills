## Description:

Helps an agent learn a user's decision patterns and reuse them conservatively for consequential choices over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to help an agent handle major branching decisions, such as architecture, vendor, workflow, publishing, spending, and long-term project choices, by checking local decision memory and asking before unsafe reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps persistent local decision notes under ~/decide/, which may contain sensitive project context if the user stores it there.

Mitigation: Review first-run setup, keep permissions restrictive, and do not store secrets, credentials, or copied private third-party data in decision memory.

## Reference(s):

- [Decide on ClawHub](https://clawhub.ai/ivangdavila/skills/decide)
- [Decide Homepage](https://clawic.com/skills/decide)
- [Setup Guide](setup.md)
- [Memory Template](memory-template.md)
- [Decision Components](components.md)
- [Confidence Calibration](confidence.md)
- [Exceptions and Always-Ask Cases](exceptions.md)
- [Migration Guide](migration.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local decision notes under ~/decide/ and may propose non-destructive workspace steering snippets for approval.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
