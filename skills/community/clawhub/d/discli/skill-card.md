## Description:

Discli helps agents and humans manage Discord servers from the terminal, including channels, roles, permissions, messages, embeds, uploads, emojis, invites, audit logs, and server settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibbybuilds](https://clawhub.ai/user/ibbybuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, server operators, and agents use this skill to control Discord server administration workflows from a CLI while keeping command output compact and structured. It is suited for channel, role, permission, member, message, invite, emoji, audit-log, and server-setting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact Discord administration actions using a bot token with broad authority.

Mitigation: Use a least-privileged bot token, require explicit human approval for destructive or public actions, and review commands before execution.

Risk: Token handling and local persistent configuration may expose sensitive Discord credentials if copied into chats, command histories, or shared files.

Mitigation: Avoid pasting bot tokens into command lines or chats, and review local discli configuration files such as ~/.discli/.env before use.

Risk: Persistent bot personality instructions may influence public bot behavior in ways the operator did not intend.

Mitigation: Review ~/.discli/SOUL.md and keep persona instructions aligned with the server operator's approval and moderation expectations.

## Reference(s):

- [Discli GitHub Repository](https://github.com/ibbybuilds/discli)
- [Discli Bot Setup Guide](https://github.com/ibbybuilds/discli/blob/master/docs/BOT_SETUP.md)
- [ClawHub Skill Page](https://clawhub.ai/ibbybuilds/skills/discli)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ibbybuilds)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text, Markdown]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers compact YAML output for agent-facing command results and recommends explicit confirmation for destructive actions.]

## Skill Version(s):

0.6.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
