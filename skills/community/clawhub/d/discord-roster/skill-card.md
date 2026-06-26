## Description: <br>
Query Discord guild members, list bots, get channel and role info via REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wehub4me](https://clawhub.ai/user/wehub4me) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and Discord server administrators use this skill to inspect guild members, bots, roles, channel details, and permissions with a configured Discord bot token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a configured Discord bot token to query guild, member, role, channel, and permission metadata. <br>
Mitigation: Use a least-privilege bot token and run the skill only against servers where the operator is authorized to inspect roster and permission metadata. <br>
Risk: Requests may route through a configured proxy. <br>
Mitigation: Review proxy configuration before use, especially for sensitive Discord servers or organization-managed networks. <br>


## Reference(s): <br>
- [Discord API v10](https://discord.com/api/v10) <br>
- [ClawHub Skill Page](https://clawhub.ai/wehub4me/discord-roster) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Tab-separated text and concise command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires channels.discord.token; proxy settings may route requests through a configured proxy.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
