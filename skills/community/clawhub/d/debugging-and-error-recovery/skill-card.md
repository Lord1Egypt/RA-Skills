## Description:

Provides generated debugging and error-recovery guidance for agents, including troubleshooting steps, command-oriented workflows, API setup guidance, batch processing, and structured fallback handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide systematic debugging when tests fail, builds break, behavior is unexpected, or recovery steps are needed. It is also presented as broad automation guidance for command execution, API setup, file handling, and batch-processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags the release as suspicious because it asks for command authority while describing broader automation, API, credential, and batch-processing behavior than its stated debugging purpose supports.

Mitigation: Review commands, file reads, API interactions, credential requests, and batch operations before execution; install only where those agent permissions are acceptable.

Risk: The release contains generated automation claims and broad recovery behavior that may not be tightly scoped to debugging.

Mitigation: Use the skill as guidance, not as an autonomous recovery system, and require human review for proposed changes or actions that affect files, services, credentials, or production systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/debugging-and-error-recovery)
- [SkillHub homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and structured text with JSON examples and command-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include troubleshooting tables, setup steps, command checks, API credential guidance, and error-recovery recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
