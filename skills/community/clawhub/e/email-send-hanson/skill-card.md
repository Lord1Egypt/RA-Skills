## Description:

Send, read, and summarize email through SMTP and IMAP using environment-based credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hansonjames](https://clawhub.ai/user/hansonjames)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send email through SMTP, read recent inbox messages through IMAP, and summarize recent email activity when mailbox credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically load mailbox credentials from nearby parent .env files.

Mitigation: Run it from a controlled directory and use only a dedicated mailbox or app password.

Risk: Send and read actions can expose email contents, recipients, attachments, and mailbox metadata.

Mitigation: Confirm the account, recipients, subject, body, attachments, and message limits before invoking send, read, or analyze actions.

## Reference(s):

- [Email Configuration](references/configuration.md)
- [ClawHub Skill Page](https://clawhub.ai/hansonjames/skills/email-send-hanson)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON results or concise text/Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Send actions return recipient, subject, sender, CC, and attachment status; read and analyze actions return recent mailbox data bounded by the requested message limit.]

## Skill Version(s):

1.0.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
