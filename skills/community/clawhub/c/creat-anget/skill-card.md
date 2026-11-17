## Description:

Creates standalone OpenClaw agents with isolated workspaces, configuration, identity, memory, and optional Feishu bot routing for multi-bot deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[song5749](https://clawhub.ai/user/song5749)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to create persistent, isolated agents for specific projects, teams, customers, or Feishu bot deployments. It is suited for long-running dedicated agents rather than temporary sub-agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent agent creation can modify openclaw.json, create workspaces, and copy main-agent auth and model files.

Mitigation: Use dry-run first, review configuration changes before restart, restrict openclaw.json permissions, and provision least-privilege per-agent credentials.

Risk: Feishu app secrets can be supplied on the command line and stored in OpenClaw configuration.

Mitigation: Avoid passing real secrets through shell history, rotate credentials when exposed, and limit access to configuration files containing bot secrets.

Risk: Open Feishu group routing can expose an agent to unintended conversations.

Mitigation: Bind only intended account IDs, keep group access closed unless explicitly needed, and test routing in a controlled environment before broader use.

## Reference(s):

- [Standalone Agent Guide](references/standalone-agent-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/song5749/skills/creat-anget)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands; helper scripts can emit JSON or update OpenClaw configuration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create directories, copy agent files, and update openclaw.json when the standalone-agent script is executed.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
