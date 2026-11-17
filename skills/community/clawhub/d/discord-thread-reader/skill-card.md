## Description:

Discord Context helps agents read Discord channel and thread history through the Discord Bot API when relevant messages are outside the current OpenClaw session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easonc13-agent](https://clawhub.ai/user/easonc13-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Discord channel or thread history that is not visible in the current OpenClaw session, including historical context, mentioned threads, and conversations where the agent was not previously active.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill deliberately gives agents access to a raw Discord bot token, which can grant broad Discord authority across channels the bot can access.

Mitigation: Use a dedicated least-privileged bot restricted to the smallest set of channels, avoid write and admin permissions, rotate exposed tokens, and prefer a constrained read-only broker or native OpenClaw tool when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/easonc13-agent/skills/discord-thread-reader)
- [Discord channel messages endpoint](https://discord.com/api/v10/channels/{channel_or_thread_id}/messages?limit=50)
- [Discord message pagination endpoint](https://discord.com/api/v10/channels/{channel_id}/messages?limit=50&before={message_id})
- [Discord active threads endpoint](https://discord.com/api/v10/channels/{parent_channel_id}/threads/active)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and Discord API URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Discord bot token and channel or thread IDs; responses are constrained by Discord permissions, pagination, and rate limits.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
