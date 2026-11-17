## Description:

Search chats, list/read messages, and send messages via Beeper Desktop using the beeper-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foeken](https://clawhub.ai/user/foeken)

### License/Terms of Use:


## Use Case:

Developers and end users can use this skill to search Beeper chats, read messages, and compose Beeper CLI commands for live messaging workflows from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad Beeper CLI access to private chats, live message changes, chat organization actions, and file transfers.

Mitigation: Use only with explicit user direction, confirm send, edit, archive, create, upload, download, and attachment actions before execution, and quote only the message content needed for the task.

Risk: The release depends on an unpinned third-party Beeper CLI and a Beeper API access token.

Mitigation: Pin and verify the CLI version where possible, store BEEPER_ACCESS_TOKEN securely, and keep the token scoped and revocable.

## Reference(s):

- [Beeper CLI](https://github.com/foeken/beeper-cli)
- [Beeper CLI Releases](https://github.com/foeken/beeper-cli/releases)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Beeper CLI command examples and safety checks for chat, message, and attachment actions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
