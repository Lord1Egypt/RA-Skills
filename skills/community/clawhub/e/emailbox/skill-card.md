## Description:

Emailbox helps agents send, receive, search, forward, and schedule email through IMAP/SMTP across common providers, with HTML templates, attachments, and document-data email workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use Emailbox to automate mailbox workflows, including sending messages, reading and searching inboxes, forwarding mail, scheduling delivery, and packaging document or data outputs into emails through configured IMAP/SMTP accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access an email account and send message content, recipients, attachments, and downloaded mailbox data through the configured provider.

Mitigation: Use a dedicated or least-privileged mailbox where possible, use provider app passwords or authorization codes, and confirm recipients and attachments before sending sensitive material.

Risk: Attachment downloads can write outside the chosen folder if unsafe filenames are present.

Mitigation: Download attachments only from trusted senders into an isolated directory, inspect filenames and paths before opening files, and avoid untrusted attachments until filename sanitization is confirmed.

Risk: Scheduled emails are stored as plaintext in ~/.emailbox/queue until they are processed or cancelled.

Mitigation: Treat the queue as sensitive, restrict local filesystem access, avoid scheduling highly sensitive content, and clean up sent, failed, or cancelled queue entries.

Risk: Email authorization codes in environment variables may be exposed through shell history, process listings, CI logs, or crash reports.

Mitigation: Prefer a system credential manager or session-only environment variables, avoid public or shared terminals, and unset EMAIL_AUTH and provider-specific auth variables after use.

## Reference(s):

- [Emailbox ClawHub skill page](https://clawhub.ai/tobewin/skills/emailbox)
- [Email Provider Configuration](references/providers.md)
- [Document Integration Workflows](references/integrations.md)
- [HTML Email Templates](references/templates.md)
- [Microsoft account security](https://account.microsoft.com/security)
- [Google account security](https://myaccount.google.com/security)
- [Google app passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, Python script invocations, optional generated text or HTML email bodies, downloaded attachment files, and scheduled-email queue entries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python standard-library scripts to perform IMAP/SMTP actions against configured email providers; scheduled email content is stored locally until processed.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter says 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
