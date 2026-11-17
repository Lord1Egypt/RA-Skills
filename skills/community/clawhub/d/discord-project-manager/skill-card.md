## Description:

Discord project collaboration infrastructure for OpenClaw agents. Manage Forum Channels, threads, participant permissions, and mention mode. Supports 3-tier architecture (Forum Channel -> Thread -> Default Channel) for multi-agent project coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lemodigital](https://clawhub.ai/user/lemodigital)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to coordinate OpenClaw multi-agent project work in Discord by creating project forums and threads, managing participant permissions, and tracking project status from a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive OpenClaw and Discord credentials and can alter central agent configuration.

Mitigation: Install only from a trusted publisher, back up ~/.openclaw/openclaw.json before use, and avoid diagnostic commands or logs that print raw configuration.

Risk: Discord bot authority can affect forum, thread, and participant access in the configured guild.

Mitigation: Restrict the bot to the minimum Discord permissions and guilds needed, and review target channels and participants before applying permission changes.

Risk: Security guidance identifies config-file permission preservation and token redaction issues for review.

Mitigation: Review and fix those issues before production use, then rescan the release before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lemodigital/skills/discord-project-manager)
- [Discord API v10](https://discord.com/api/v10)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [CLI text and JSON status output with OpenClaw configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates Discord project channels, threads, permission entries, and skill-local registry files.]

## Skill Version(s):

2.1.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
