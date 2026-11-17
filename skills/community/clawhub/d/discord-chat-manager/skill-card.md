## Description:

Helps agents interact with Discord channels through the message tool to send, reply to, search, read, react to, edit, delete, and inspect channel messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, community managers, and automation teams use this skill to operate Discord support, announcement, search, and message maintenance workflows through an agent-connected Discord bot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose posting, editing, deleting, or exporting Discord messages without enough scoping or confirmation.

Mitigation: Use the minimum Discord bot permissions needed for the target channels and require human confirmation before send, edit, delete, or export actions.

Risk: Search and archive workflows can expose or retain private Discord channel content.

Mitigation: Archive only approved channels or messages, and confirm the retention location and duration before saving message history.

Risk: High-frequency message operations can trigger Discord rate limits or resemble bulk messaging.

Mitigation: Throttle automated actions, avoid unsolicited bulk messaging, and monitor for Discord 429 responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/discord-chat-manager)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Discord bot with scoped channel and moderation permissions; sending, editing, deleting, and exporting messages should be confirmed by a human.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
