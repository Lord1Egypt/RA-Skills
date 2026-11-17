## Description:

Operate Discord HTTP API through UXC with Discord OpenAPI schema. Bot token recommended for full API access including messages and server management. OAuth2 user authentication available for limited profile operations only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to discover and execute Discord REST API operations through UXC, with bot-token setup guidance, OpenAPI schema mapping, and Gateway subscribe examples for inbound events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OAuth2 flow uses a fixed client ID and broad scopes that may expose user account data.

Mitigation: Prefer a bot token controlled by the user, verify the OAuth application owner before use, and reduce OAuth scopes to only the data required.

Risk: Discord bot tokens can enable message access, server management, moderation, and write operations according to the bot permissions granted.

Mitigation: Grant the bot only the minimum Discord permissions needed and require explicit user confirmation before write, delete, update, or moderation operations.

Risk: Gateway subscriptions and REST calls can capture or produce sensitive Discord messages and events.

Mitigation: Store subscription sinks in a controlled location, limit privileged intents such as MESSAGE_CONTENT, and avoid collecting data unrelated to the task.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Discord API docs](https://discord.com/developers/docs)
- [Discord OAuth2 documentation](https://discord.com/developers/topics/oauth2)
- [Discord API OpenAPI spec](https://github.com/discord/discord-api-spec)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/discord-openapi-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for UXC-based Discord API calls; execution still depends on user-provided Discord credentials and permissions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
