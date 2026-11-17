## Description:

Cross-platform OpenClaw agent migration and deployment support for backing up, restoring, transferring, and syncing agent state across environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haha8d](https://clawhub.ai/user/haha8d)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to move, back up, restore, and deploy OpenClaw agent identity, memory, configuration, skills, and workspace state across local machines, servers, WSL, and Docker environments. It is not intended for general file backup or non-agent data migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload or transfer sensitive OpenClaw configuration, memory, identity, and workspace state.

Mitigation: Use only repositories and archives you control, sanitize or encrypt OpenClaw configuration and memory before transfer, and rotate exposed credentials after migration.

Risk: Restore workflows can run generated or retrieved restore.sh scripts.

Mitigation: Inspect restore.sh before running pull or restore workflows, and only restore from trusted archives.

Risk: The GitHub sync workflow includes a force-push fallback that can overwrite remote history.

Mitigation: Remove or disable the force-push fallback before use in shared or production repositories.

Risk: Docker deployment can expose the OpenClaw gateway publicly if ports and volumes are configured loosely.

Mitigation: Avoid public gateway exposure unless strong authentication, pinned images, and restricted volumes are in place.

## Reference(s):

- [Docker Deploy Guide](references/docker-deploy.md)
- [ClawHub Skill Page](https://clawhub.ai/haha8d/skills/agent-migrate)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash, Dockerfile, and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce export archives, restore scripts, and GitHub sync workflows for OpenClaw agent state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
