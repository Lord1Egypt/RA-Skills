## Description:

Full access to Exchange 2010 EWS for managing emails, folders, attachments, calendar events, contacts, tasks, and out-of-office settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pes0](https://clawhub.ai/user/pes0)

### License/Terms of Use:


## Use Case:

Developers and agents with Exchange delegate credentials use this skill to manage Exchange 2010 EWS mailboxes, calendars, contacts, tasks, attachments, and out-of-office settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad mailbox write access can affect email, calendar, task, attachment, and out-of-office data.

Mitigation: Install only for a tightly scoped, least-privileged Exchange account and add confirmations for send, delete, update, and out-of-office actions.

Risk: Credential defaults and credential-file handling may expose or misuse Exchange account access.

Mitigation: Require explicit Exchange server, username, email, domain, and password variables; remove hardcoded defaults; and protect the credentials file.

Risk: Attachment download and temporary-file behavior can expose sensitive files or write outside intended locations.

Mitigation: Sanitize and restrict attachment download paths, and avoid processing sensitive attachments until temp-file cleanup and download containment are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pes0/skills/exchange-2010-ews)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, API calls, Configuration, Guidance]

**Output Format:** [Python function calls and structured Python dictionaries, with Markdown examples and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read, send, update, and delete Exchange mailbox, calendar, contact, task, out-of-office, and attachment data when installed with valid credentials.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
