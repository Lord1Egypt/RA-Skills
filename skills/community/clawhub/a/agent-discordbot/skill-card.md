## Description:

Interact with Discord servers using bot tokens - send messages, read channels, manage reactions

This skill is ready for commercial/non-commercial use.

## Publisher:

[devxoul](https://clawhub.ai/user/devxoul)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to operate Discord bot-token workflows, including authentication, channel and server inspection, message posting, reactions, file uploads, thread handling, and server snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read from and post to Discord servers using a bot token.

Mitigation: Use a dedicated low-permission bot, restrict server and channel access, and confirm before sending, deleting, uploading files, or exporting snapshots from real servers.

Risk: The bot token grants Discord authority and is stored locally by the CLI.

Mitigation: Protect the credential file, avoid sharing tokens, and rotate the token if exposure is suspected.

Risk: The release uses an unpinned third-party CLI package installation path.

Mitigation: Pin and audit the agent-messenger package before sensitive use, and avoid ad-hoc latest or bunx execution in higher-risk environments.

Risk: The skill describes cross-session memory that may retain Discord IDs, names, aliases, and preferences.

Mitigation: Limit or disable memory behavior unless retention is intended, and do not store bot tokens, credentials, full message content, or file upload contents.

## Reference(s):

- [Agent Discordbot ClawHub Page](https://clawhub.ai/devxoul/skills/agent-discordbot)
- [Authentication Guide](artifact/references/authentication.md)
- [Common Patterns](artifact/references/common-patterns.md)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [jq Download](https://jqlang.github.io/jq/download/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to invoke the agent-discordbot CLI, which returns JSON by default and can emit human-readable pretty output.]

## Skill Version(s):

1.10.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
