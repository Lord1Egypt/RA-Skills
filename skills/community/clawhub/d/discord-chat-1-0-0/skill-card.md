## Description: <br>
Send messages, reply to messages, and search message history in Discord channels using the message tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcdentoncore](https://clawhub.ai/user/jcdentoncore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent interact with Discord channels through the configured message tool, including sending replies, checking recent activity, searching history, reacting to messages, and managing channel-related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to read, post, edit, delete, and administer Discord channels through the message tool. <br>
Mitigation: Limit the Discord bot to the minimum permissions needed and require explicit user approval before edits, deletes, channel changes, webhook setup, or gateway configuration changes. <br>
Risk: Discord bot tokens, guild identifiers, and webhook secrets may be exposed if placed in committed files or shared transcripts. <br>
Mitigation: Store credentials in environment variables or a secrets manager, rotate exposed tokens immediately, and avoid pasting secrets into agent-visible context. <br>
Risk: Channel and category deletion actions are permanent. <br>
Mitigation: Avoid granting deletion permissions unless required, confirm the target channel or category before deletion, and use audit-log reasons for administrative actions. <br>


## Reference(s): <br>
- [Discord Search Patterns](references/SEARCH.md) <br>
- [Discord Channel Management](references/CHANNELS.md) <br>
- [Discord Bot Configuration](references/CONFIG.md) <br>
- [Discord Developer Portal](https://discord.com/developers/applications) <br>
- [Discord API Documentation](https://discord.com/developers/docs) <br>
- [Discord Permissions Documentation](https://discord.com/developers/docs/topics/permissions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the configured Discord message tool and may require bot credentials and Discord server or channel identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
