## Description: <br>
Send messages, reply to messages, and search message history in Discord channels using the message tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bowenQT](https://clawhub.ai/user/bowenQT) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to read, search, send, reply to, react to, edit, and manage Discord messages and channels through a configured Discord bot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bot with broad Discord permissions can post publicly, edit or delete messages, pin content, or change channels in ways users did not intend. <br>
Mitigation: Install only for a Discord bot you control, grant minimum required server and channel permissions, and require explicit confirmation before public posting or destructive channel and message actions. <br>
Risk: Discord bot tokens, guild IDs, webhook secrets, or channel configuration can expose access if committed or shared. <br>
Mitigation: Store tokens and secrets in environment variables or a secret manager, rotate exposed tokens, and monitor Discord bot usage. <br>
Risk: Channel and category deletion is permanent. <br>
Mitigation: Check the target channel or category before deletion and include audit-log reasons for administrative actions. <br>


## Reference(s): <br>
- [Discord Chat Skill](https://clawhub.ai/bowenQT/discord-chat) <br>
- [Discord Bot Configuration](references/CONFIG.md) <br>
- [Discord Channel Management](references/CHANNELS.md) <br>
- [Discord Search Patterns](references/SEARCH.md) <br>
- [Discord Developer Portal](https://discord.com/developers/applications) <br>
- [Discord Permissions Documentation](https://discord.com/developers/docs/topics/permissions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline message-tool commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Discord bot and Discord gateway channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
