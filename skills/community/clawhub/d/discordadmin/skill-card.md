## Description: <br>
Complete A-Z Discord server administration for channel, role, member, AutoMod, webhook, template, audit log, scheduled event, thread, and full server control via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheBigBrainChad](https://clawhub.ai/user/TheBigBrainChad) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Discord server administrators and agent operators use this skill to inspect and manage Discord servers through shell commands backed by the Discord API. It covers routine administration, moderation, message management, webhooks, templates, audit logs, scheduled events, and bulk operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad live Discord server control. <br>
Mitigation: Install only when intentional, use a dedicated bot with the minimum permissions needed, and test on a non-production server first. <br>
Risk: Bot tokens can be exposed through command arguments, logs, or shared terminals. <br>
Mitigation: Prefer DISCORD_BOT_TOKEN from a protected environment, avoid passing tokens with --token, and keep terminal output and logs private. <br>
Risk: Delete, ban, prune, webhook, guild-edit, template, stage, and bulk actions can have destructive or high-impact effects. <br>
Mitigation: Require human review before high-impact commands and confirm target guild, channel, role, member, message, and webhook IDs before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/TheBigBrainChad/discordadmin) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/TheBigBrainChad) <br>
- [Discord API v10](https://discord.com/api/v10) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, a Discord bot token, and Discord server permissions appropriate to the requested operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
