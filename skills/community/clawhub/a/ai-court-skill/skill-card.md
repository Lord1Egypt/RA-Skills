## Description:

Ai Court Skill configures an OpenClaw multi-agent collaboration system modeled on Ming Dynasty cabinet roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlkptom-prog](https://clawhub.ai/user/jlkptom-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install a role-based multi-agent coordination setup, choose Feishu or Discord messaging, configure model credentials, and verify the installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-based installation can overwrite existing OpenClaw configuration.

Mitigation: Back up ~/.openclaw and merge the needed files manually before copying configuration directories.

Risk: Some role instructions may route tasks, diffs, or review reports to Discord.

Mitigation: Review and disable Discord routing unless that sharing path is intended for the deployment.

Risk: The setup requires Feishu, Discord, and model-provider credentials.

Mitigation: Store credentials with restrictive permissions or a secret manager, and use Feishu or Discord allowlists for the smallest audience needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jlkptom-prog/skills/ai-court-skill)
- [Feishu Setup Guide](references/feishu-setup.md)
- [Feishu Open Platform](https://open.feishu.cn/app)
- [Feishu API Documentation](https://open.feishu.cn/document)
- [OpenClaw Feishu Channel Documentation](https://docs.openclaw.ai/channels/feishu)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation, configuration, role-routing, and troubleshooting guidance for OpenClaw agents.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
