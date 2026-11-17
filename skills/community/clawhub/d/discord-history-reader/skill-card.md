## Description:

Read Discord channel and thread message history directly through the Discord Bot API outside OpenClaw session-based message visibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easonc13](https://clawhub.ai/user/easonc13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to fetch historical context from Discord channels or threads when an agent has no active OpenClaw session visibility. It is intended for authorized read-only context retrieval with a Discord bot token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives the agent direct, reusable access to a raw Discord bot token.

Mitigation: Use a brokered read-only tool instead of exposing the token directly, and avoid installing the skill unless this level of credential access is intentional.

Risk: The skill can read Discord channels or threads outside normal OpenClaw session visibility.

Mitigation: Restrict access with channel allowlists, per-request approval, and audit logging before allowing history reads.

Risk: A Discord bot token may grant broader channel access than the immediate task requires.

Mitigation: Limit the bot's Discord permissions to only required channels and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/easonc13/skills/discord-history-reader)
- [Discord channel messages API example](https://discord.com/api/v10/channels/{channel_or_thread_id}/messages?limit=50)
- [Discord message pagination API example](https://discord.com/api/v10/channels/{channel_id}/messages?limit=50&before={message_id})
- [Discord active threads API example](https://discord.com/api/v10/channels/{parent_channel_id}/threads/active)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Discord bot token and channel or thread IDs supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
