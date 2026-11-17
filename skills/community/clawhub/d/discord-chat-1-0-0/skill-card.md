## Description:

Provides command patterns for Discord messaging, message history search, reactions, and channel management through a configured Discord message tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcdentoncore](https://clawhub.ai/user/jcdentoncore)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external agent users use this skill to have an agent communicate in Discord channels, inspect recent activity, search message history, and manage channel interactions with an already configured Discord bot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents destructive Discord actions, including deleting messages, deleting channels or categories, pinning, editing, and changing channel settings.

Mitigation: Require explicit confirmation before send, edit, delete, pin, channel, category, or permission-changing actions.

Risk: Broad Discord permissions or unrestricted bot access could expose channels or actions that are not needed for the intended workflow.

Mitigation: Use a Discord bot with permissions limited to the specific channels and actions required.

Risk: Message history searches can expose private or sensitive channel content.

Mitigation: Avoid broad searches in private or sensitive channels and scope searches by channel, author, query, and limit.

## Reference(s):

- [Discord Channel Management](references/CHANNELS.md)
- [Discord Bot Configuration](references/CONFIG.md)
- [Discord Search Patterns](references/SEARCH.md)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord API Documentation](https://discord.com/developers/docs)
- [Discord Permissions Documentation](https://discord.com/developers/docs/topics/permissions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume a configured Discord bot and appropriate channel or guild identifiers.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
