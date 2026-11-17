## Description:

Optimize Docker Compose configurations for development and production by auditing services, networking, volumes, health checks, and resource management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to review Docker Compose files for security, performance, reliability, and production readiness. It helps identify issues and improvements in service configuration, networking, volumes, health checks, dependencies, secrets handling, and resource limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read Docker Compose files in the current working directory during analysis.

Mitigation: Invoke it only in the intended project workspace and use Compose-specific prompts for configuration reviews.

## Reference(s):

- [Docker Compose Optimizer on ClawHub](https://clawhub.ai/charlie-morrison/skills/docker-compose-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are grouped as issues, improvements, and good practices.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
