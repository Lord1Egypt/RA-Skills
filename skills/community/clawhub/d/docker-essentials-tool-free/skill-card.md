## Description:

Docker基础工具免费版 helps developers manage Docker containers, images, Docker Compose projects, networks, and volumes through Docker CLI guidance and commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for local containerized development, single-host Docker Compose orchestration, and container troubleshooting. It is intended for explicit Docker management tasks where the agent can propose or run Docker CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker removal, prune, down -v, and volume deletion commands can delete containers, images, networks, or saved data.

Mitigation: Require the agent to list the exact targets and obtain explicit approval before running destructive Docker commands.

Risk: Docker commands can affect important local development or single-host deployment environments.

Mitigation: Review proposed commands before execution and use the skill only for explicit Docker tasks in environments where changes are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/docker-essentials-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell, YAML, and Dockerfile code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable Docker CLI commands that affect containers, images, networks, and volumes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
