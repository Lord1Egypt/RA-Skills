## Description: <br>
Manage Discord servers with a narrow, medium-risk scope using direct Bot API calls for channel, category, role, and member-role administration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datarxdacted](https://clawhub.ai/user/datarxdacted) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and community administrators use this skill to let an agent inspect and make targeted Discord server channel and role changes with explicit guild, channel, role, and user IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Discord server channels and roles when used with a bot token. <br>
Mitigation: Use a dedicated bot with only the minimum Discord permissions needed and avoid Administrator when practical. <br>
Risk: Deletes, role reorders, or role assignments can affect the wrong server object if IDs are incorrect. <br>
Mitigation: Confirm exact guild, channel, role, and user IDs before writes, test in a non-production server first, and require explicit confirmation for destructive or privilege-changing actions. <br>


## Reference(s): <br>
- [Discord API v10](https://discord.com/api/v10) <br>
- [ClawHub skill page](https://clawhub.ai/datarxdacted/discord-server-admin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and Discord API JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DISCORD_BOT_TOKEN or --token, exact Discord IDs, and Discord integer permission bitfields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
