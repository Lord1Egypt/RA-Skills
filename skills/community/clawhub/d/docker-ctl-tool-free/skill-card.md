## Description:

Podman/Docker container inspection skill for checking container status, logs, resource usage, health, ports, volumes, and configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect local Podman or Docker containers, review logs, check resource usage, and diagnose common container state or configuration issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Container inspection output may expose sensitive logs, mounts, ports, or environment variables.

Mitigation: Use only on containers whose data can be shared with the agent, and instruct the agent to redact secrets before returning output.

Risk: The artifact claims sensitive data will not appear in outputs, but security evidence says environment variables and logs can be exposed.

Mitigation: Treat all outputs as potentially sensitive and review them before sharing or storing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/docker-ctl-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include container status, logs, ports, mounts, environment variables, health checks, and resource usage summaries.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
