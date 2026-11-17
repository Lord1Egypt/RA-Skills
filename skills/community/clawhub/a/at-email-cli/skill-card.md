## Description:

Use the AgentTeam Email CLI command `at-email` to operate an agent mailbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentteamhq](https://clawhub.ai/user/agentteamhq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent manage a configured AgentTeam email mailbox, including checking status, listing and reading messages, searching mail, marking or archiving messages, and sending or replying to email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent access to a configured mailbox and supports actions that mutate or send email.

Mitigation: Install only if you trust the AgentTeam package and require explicit confirmation before sending, replying, archiving, marking messages read, installing globally, or updating the CLI.

Risk: The skill recommends unpinned package execution through the latest npm package.

Mitigation: Prefer a pinned, reviewed package version or checksum-verified binary before granting mailbox access.

## Reference(s):

- [at-email CLI homepage](https://github.com/agentteamhq/agentteam-email/tree/main/apps/at-email-cli)
- [ClawHub skill page](https://clawhub.ai/agentteamhq/skills/at-email-cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON-output recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose mailbox read, send, reply, archive, mark-read, install, and update commands; uses configured environment variables and should avoid printing secrets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
