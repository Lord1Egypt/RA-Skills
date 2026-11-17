## Description:

Fastmail JMAP lets an agent read, search, send, move, trash, and list email through Fastmail's JMAP API using a Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theagentwire](https://clawhub.ai/user/theagentwire)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent check, search, read, send, and organize Fastmail email from a local command line after providing a Fastmail API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, send, and modify email for the configured Fastmail account.

Mitigation: Install it only for mailboxes appropriate for agent access and use the narrowest practical Fastmail token scopes.

Risk: Sending or changing messages can create irreversible communication or mailbox state changes.

Mitigation: Require explicit user approval before sending, moving, trashing, or marking messages.

Risk: Email content from untrusted senders may appear in terminal output and influence an agent workflow.

Mitigation: Treat email content as untrusted input and avoid unattended monitoring unless there is a clear operational need.

## Reference(s):

- [ClawHub Fastmail JMAP release page](https://clawhub.ai/theagentwire/skills/fastmail-jmap)
- [The Agent Wire publisher profile](https://clawhub.ai/user/theagentwire)
- [JMAP protocol](https://jmap.io/)
- [Fastmail API token settings](https://app.fastmail.com/settings/security/tokens)
- [The Agent Wire WW-2 tutorial](https://theagentwire.ai/p/fastmail-jmap-email-automation-gmail-alternative)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and CLI text or JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Fastmail API token and can print mailbox and message content to the terminal.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
