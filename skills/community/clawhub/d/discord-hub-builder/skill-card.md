## Description: <br>
Build a complete Discord AI command center server from scratch using the Discord REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CaleCorbett](https://clawhub.ai/user/CaleCorbett) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and server operators use this skill to create a Discord-based AI command center with predefined categories, channels, roles, and pinned workflow cards. It is intended for users who have a Discord bot token and target guild ID and want the setup performed through the Discord REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a powerful Discord bot token that can modify the target server. <br>
Mitigation: Use a dedicated bot, avoid exposing real tokens in shared shells or logs, and run the documented dry run before live execution. <br>
Risk: Created owner-only, readonly, and personal channels may not have the intended permissions automatically applied. <br>
Mitigation: Manually verify channel permissions before using the created channels for sensitive content. <br>
Risk: Re-running after a partial failure can create duplicate channels because channel creation does not deduplicate existing names. <br>
Mitigation: Use dry run to check planned changes and delete any unwanted duplicate channels before retrying a live run. <br>


## Reference(s): <br>
- [Discord Developer Portal](https://discord.com/developers/applications) <br>
- [Discord REST API v10](https://discord.com/api/v10) <br>
- [ClawHub Skill Page](https://clawhub.ai/CaleCorbett/discord-hub-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and terminal output listing created Discord channel IDs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Discord bot token, target guild ID, and bot permissions to manage channels, manage roles, send messages, and pin messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
