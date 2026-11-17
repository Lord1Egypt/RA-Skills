## Description:

Exchange Skills helps agents manage Microsoft Exchange/Outlook email, calendar events, contacts, tasks, and notes from a terminal, including reading, replying, archiving, and batch mark-read operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derekhsu](https://clawhub.ai/user/derekhsu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and agent operators use this skill to inspect and act on Microsoft Exchange/Outlook mailbox data from a terminal. It supports everyday mailbox workflows such as listing unread mail, reading messages, replying, archiving, viewing calendars, searching contacts, and listing tasks or notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has full access to the configured Exchange mailbox.

Mitigation: Install only for mailboxes where this access is acceptable, and store EXCHANGE_PASSWORD and related credentials carefully.

Risk: Reply, mark-read, and archive commands can make broad mailbox changes, especially with batch flags.

Mitigation: Review the exact command and target flags before allowing replies or batch mark-read/archive actions.

Risk: The archive command may move messages into deletion folders when the archive folder fallback is used.

Mitigation: Avoid or tightly review archive use until the Archive folder behavior is fixed or clearly configured.

Risk: TLS certificate verification can be disabled with EXCHANGE_DISABLE_SSL_VERIFY=1.

Mitigation: Keep TLS verification enabled unless a reviewed corporate certificate exception is required.

## Reference(s):

- [Exchange Skills on ClawHub](https://clawhub.ai/derekhsu/skills/exchange-skills)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI output is plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Exchange connection environment variables, including EXCHANGE_SERVER, EXCHANGE_EMAIL, EXCHANGE_USERNAME, and EXCHANGE_PASSWORD.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
