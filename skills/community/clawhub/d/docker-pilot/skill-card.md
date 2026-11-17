## Description:

Safe, intelligent Docker container management for fleet status, lifecycle operations, cleanup, compose stacks, troubleshooting, and security hardening with risk-level classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahajahmed010](https://clawhub.ai/user/wahajahmed010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Docker fleets, plan container lifecycle changes, manage cleanup, compose stacks, logs, health checks, and troubleshoot Docker runtime issues while classifying proposed commands by operational risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe Docker daemon exposure could occur if the tcp://0.0.0.0:2375 daemon advice is followed.

Mitigation: Do not use that daemon configuration; keep Docker access on protected local sockets or explicitly secured endpoints.

Risk: First-run setup items may install packages, change daemon.json, alter restart policies, prune Docker resources, or add monitoring jobs.

Mitigation: Treat each first-run item as a separate proposal and require explicit approval before making any host-level or persistent change.

Risk: Cleanup and volume-prune guidance can remove containers, images, networks, or data.

Mitigation: Show the exact affected resources and expected impact before cleanup, and require confirmation for risky or destructive Docker commands.

## Reference(s):

- [Docker Pilot ClawHub Skill Page](https://clawhub.ai/wahajahmed010/skills/docker-pilot)
- [wahajahmed010 ClawHub Publisher Profile](https://clawhub.ai/user/wahajahmed010)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and YAML or JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker CLI access; outputs should present Docker host changes as proposals requiring explicit user approval for risky or destructive operations.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
