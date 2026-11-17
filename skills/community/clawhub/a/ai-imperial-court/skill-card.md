## Description:

AI朝廷三省六部 maps the Tang dynasty Three Departments and Six Ministries model to a Chinese-language multi-agent workflow for planning, review, execution, and role-based coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuxnd](https://clawhub.ai/user/kukuxnd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to structure complex tasks into draft, review, and execution phases with specialized roles for planning, documentation, strategy, compliance, and engineering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick-start command writes local Markdown records that may retain sensitive task details.

Mitigation: Do not include secrets, credentials, regulated data, or confidential plans unless local retention is acceptable.

Risk: Generated plans, reviews, and execution reports may be incomplete or inaccurate for high-stakes tasks.

Mitigation: Review generated workflow records and risk checks before relying on them for execution.

## Reference(s):

- [Six Ministries Reference](references/six-ministries.md)
- [Execution Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown workflow templates and CLI-generated Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The quick-start command writes draft, review, and execution records under records/.]

## Skill Version(s):

1.1.0 (source: release evidence, package.json, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
