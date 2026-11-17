## Description:

Manage Docker containers, images, volumes, networks, and Docker Compose projects, including logs, builds, cleanup, compose-file creation, and debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and server operators use this skill to inspect and control Docker resources, troubleshoot container failures, and generate Docker Compose configurations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker cleanup and removal commands can stop services or delete containers, images, volumes, or other data.

Mitigation: Review and explicitly approve destructive Docker operations such as container removal, image pruning, system pruning, and volume pruning before execution.

Risk: The skill is intended to help run Docker commands on the user's machine.

Mitigation: Install and use it only in environments where agent-assisted Docker command generation and execution review are acceptable.

## Reference(s):

- [Docker Helper ClawHub page](https://clawhub.ai/ericlooi504/skills/eric-docker-helper)
- [ClawHub homepage](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Docker command proposals, docker-compose.yml content, and cleanup guidance that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
