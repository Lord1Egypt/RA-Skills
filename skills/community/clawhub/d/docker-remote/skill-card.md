## Description:

Remotely manage Docker Compose instances via SSH. Execute docker compose commands, view logs, update images, and exec into containers on remote servers. Use when deploying, monitoring, or debugging containerized applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elric2011](https://clawhub.ai/user/elric2011)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to administer trusted remote Docker Compose deployments over SSH, including service lifecycle operations, logs, image updates, and container exec commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can stop, restart, update, or execute commands inside services on remote Docker hosts.

Mitigation: Require human confirmation before stop, down, update, or exec operations on production services.

Risk: Broad SSH or Docker socket permissions can allow high-impact changes outside the intended application.

Mitigation: Use a dedicated least-privilege deployment user, avoid root where possible, and audit Docker socket access.

Risk: Host aliases and custom update commands in deploy-apps.json can route actions to unintended systems or run unexpected commands.

Mitigation: Review deploy-apps.json host mappings, SSH credentials, paths, and update commands before installing or invoking the skill.

## Reference(s):

- [Docker Remote Reference](references/README.md)
- [Command Examples](examples/docker-remote.json)
- [Deployment Configuration Example](examples/deploy-apps.json)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured success or failure status, relevant logs, and error context from remote Docker Compose operations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
