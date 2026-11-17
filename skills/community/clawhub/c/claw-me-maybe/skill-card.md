## Description:

Beeper integration for Clawdbot that helps agents search chats, send messages, summarize unread conversations, manage reactions and reminders, mark chats read, and download attachments across Beeper-supported messaging platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickhamze](https://clawhub.ai/user/nickhamze)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate Beeper Desktop through an agent, including searching message history, sending messages, managing unread chats, reactions, reminders, and attachments across connected messaging services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive personal or work chats through Beeper.

Mitigation: Use only the minimum connected accounts needed for the task and review access before installing.

Risk: Persistent Beeper token storage could expose messaging access if the local configuration is compromised.

Mitigation: Avoid plaintext token storage when possible, and revoke or rotate the token when the skill is no longer needed.

Risk: Agent actions can send, react to, archive, mark read, download attachments, or create chats and reminders.

Mitigation: Require explicit confirmation before the agent performs message-changing or attachment-download actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nickhamze/skills/claw-me-maybe)
- [Beeper](https://www.beeper.com)
- [Beeper Download](https://www.beeper.com/download)
- [Beeper Developer Docs](https://developers.beeper.com)
- [Beeper Desktop API Reference](https://developers.beeper.com/desktop-api-reference/)
- [Beeper MCP](https://www.beeper.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and inline curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Beeper Desktop API enabled locally and curl; may use BEEPER_ACCESS_TOKEN.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter is 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
