## Description:

Manage Discord servers with direct Bot API calls for focused channel, category, role, and member-role administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datarxdacted](https://clawhub.ai/user/datarxdacted)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Discord community administrators use this skill to inspect and make targeted channel, category, role, and member-role changes through a dedicated bot with explicit IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make real Discord channel and role changes.

Mitigation: Use a dedicated bot with the minimum needed permissions and review every delete, role reorder, and member-role change before running it.

Risk: A bot token can be exposed through command arguments, logs, or shell history.

Mitigation: Prefer DISCORD_BOT_TOKEN over the --token argument and keep tokens out of files, logs, and command history.

Risk: Incorrect IDs or Discord role hierarchy limits can cause failed or unintended administrative actions.

Mitigation: Start with channel-list or role-list, confirm exact IDs before writes, and check bot permissions and role hierarchy on 403 responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/datarxdacted/skills/discord-server-admin)
- [Discord API v10 endpoint](https://discord.com/api/v10)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and Discord API JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Discord bot token and explicit guild, channel, role, or user IDs for write actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
