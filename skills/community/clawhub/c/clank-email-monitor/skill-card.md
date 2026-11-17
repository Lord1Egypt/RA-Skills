## Description:

Monitor email inboxes for important messages and get alerts. Works with AgentMail, Gmail, and any IMAP inbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t3mr0i](https://clawhub.ai/user/t3mr0i)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure monitoring across AgentMail, Gmail, or IMAP inboxes, receive keyword and priority alerts, generate digests, and optionally manage urgent-message auto-replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox credentials or API keys may be exposed through the local email monitor configuration.

Mitigation: Use app-specific or narrowly scoped credentials, keep ~/.email-monitor/config.json out of source control and backups, and restrict the file to the current user.

Risk: Background monitoring and auto-replies may process or respond to emails in ways the user did not intend.

Mitigation: Review the implementation and configuration before enabling watch mode or auto-replies, especially for urgent-message rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/t3mr0i/skills/clank-email-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce email monitoring commands, alert criteria, digest settings, notification settings, and auto-reply configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
