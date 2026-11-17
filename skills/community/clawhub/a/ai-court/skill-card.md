## Description:

Configures an OpenClaw multi-agent collaboration system modeled on historical Chinese governance and modern enterprise structures, with Feishu and Discord deployment options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanikua](https://clawhub.ai/user/wanikua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team operators use this skill to deploy a coordinated AI agent team with selectable governance patterns, bot counts, and Feishu or Discord channel bindings. It supports lightweight personal setups through larger team configurations that route work among specialized agents.

### Deployment Geography for Use:

Global, with Feishu-oriented setup for China mainland workspaces and Discord-oriented setup for international workspaces.

## Known Risks and Mitigations:

Risk: Powerful agents may be exposed to open Feishu or Discord channels with weak scoping.

Mitigation: Use trusted spaces only, restrict group and direct-message access, and avoid broad @everyone or @here triggers.

Risk: Agent credentials and gateway configuration can include sensitive secrets.

Mitigation: Protect ~/.openclaw/openclaw.json as a secrets file and run the gateway under a low-privilege account.

Risk: Broad logging or archival can retain sensitive workspace content.

Mitigation: Disable archival for sensitive work or scope retention to the minimum required channels and tasks.

Risk: Unbounded agent tools can increase the impact of accidental or unsafe actions.

Mitigation: Enable sandboxing where available and apply per-agent tool limits before use in shared workspaces.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wanikua/skills/ai-court)
- [Feishu Setup Guide](artifact/docs/feishu-setup-simple.md)
- [Flexible Feishu Bot Configuration Guide](artifact/docs/feishu-flexible-setup.md)
- [Docker Image Configuration Guide](artifact/references/docker-config.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance and reusable OpenClaw configuration choices for 1-11 bot deployments.]

## Skill Version(s):

2.3.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
