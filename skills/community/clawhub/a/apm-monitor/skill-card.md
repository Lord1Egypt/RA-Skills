## Description:

APM, (Application Performance Management) tool for large-scale distributed systems. apm-monitor, java, agent, apm, distributed-tracing, monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill for basic APM monitor command guidance, status checks, and local data-tooling outputs. The shipped artifacts should be reviewed before relying on them for real distributed tracing or Pinpoint monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised Pinpoint/APM monitoring behavior does not match the shipped placeholder and generic data commands.

Mitigation: Review the skill and test commands in a non-sensitive environment before using it for monitoring decisions.

Risk: Command arguments may be persisted in local history logs.

Mitigation: Avoid passing secrets, tokens, credentials, or sensitive paths as command arguments and clear the configured data directory when needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bytesagain1/skills/apm-monitor)
- [BytesAgain homepage](https://bytesagain.com)
- [Pinpoint upstream project](https://github.com/pinpoint-apm/pinpoint)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local command history under the configured APM_MONITOR_DIR data directory.]

## Skill Version(s):

2.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
