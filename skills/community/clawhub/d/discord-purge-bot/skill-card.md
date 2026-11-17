## Description:

Operate a Discord message cleanup workflow with an official bot token and Discord HTTP API for scoped guild-channel message deletion, dry-run previews, guarded purge jobs, and channel recreation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ginhoor](https://clawhub.ai/user/ginhoor)

### License/Terms of Use:


## Use Case:

External Discord server operators and developers use this skill to preview and execute scoped cleanup of guild-channel messages by user, text, regular expression, or time window, and to recreate channels when history should be wiped. It is intended for official bot-token workflows, not self-bot or personal DM cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive Discord deletion features can remove broader message history than the operator intended if preview scope and execution scope are not reviewed carefully.

Mitigation: Review before installing, run dry previews first, use least-privileged Discord bot tokens, prefer DISCORD_BOT_TOKEN over command-line token arguments, and confirm the exact scope before deletion.

Risk: Nuke mode with --delete-old can irreversibly remove the original channel.

Mitigation: Avoid nuke mode with --delete-old unless preserving the original channel history is unnecessary and irreversible loss is acceptable.

## Reference(s):

- [Discord Cleanup Limits](references/discord-limits.md)
- [Discord API v10](https://discord.com/api/v10)
- [ClawHub Skill Page](https://clawhub.ai/ginhoor/skills/discord-purge-bot)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON preview, state, and result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deletion runs can persist audit-friendly JSON summaries, including scanned, matched, deleted, failed, recent, and old-message counts.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
