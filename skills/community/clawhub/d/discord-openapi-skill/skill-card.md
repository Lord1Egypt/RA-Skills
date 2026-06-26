## Description: <br>
Operate Discord REST and Gateway workflows through UXC using Discord's OpenAPI schema, with bot-token guidance and documented OAuth2 limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure Discord authentication, discover schema-backed Discord operations, execute REST calls through UXC, and subscribe to Discord Gateway events with permission guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord bot tokens can grant broad powers, including message, server management, moderation, and administrative actions. <br>
Mitigation: Use a dedicated low-permission bot, restrict it to specific servers and intents, verify OAuth scopes, and require explicit approval before posting, deleting, moderation, or administrative actions. <br>
Risk: Discord Gateway subscriptions can persist live Discord events locally and may capture private data. <br>
Mitigation: Avoid event logging unless needed, limit Gateway intents, enable privileged message-content access only when required, and tightly manage any NDJSON sink files. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Discord API Documentation](https://discord.com/developers/docs) <br>
- [Discord OAuth2 Documentation](https://discord.com/developers/topics/oauth2) <br>
- [Discord API OpenAPI Spec](https://github.com/discord/discord-api-spec) <br>
- [ClawHub Skill Page](https://clawhub.ai/jolestar/discord-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agents may execute commands that return UXC JSON envelopes or write Discord Gateway events to NDJSON sink files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
