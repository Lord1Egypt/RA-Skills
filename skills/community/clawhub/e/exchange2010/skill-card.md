## Description:

Connects an agent to Exchange 2010 through EWS to work with email, calendars, contacts, tasks, attachments, shared calendars, recurring events, and out-of-office settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pes0](https://clawhub.ai/user/pes0)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an agent read, search, and manage Exchange 2010 mailbox, calendar, contact, task, attachment, shared-calendar, recurring-event, and out-of-office workflows. It is intended for environments where delegated Exchange access can be explicitly controlled and reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated Exchange mailbox access can expose or change email, calendar, contact, task, attachment, shared-calendar, and out-of-office data.

Mitigation: Constrain delegated permissions and require explicit human review before sending email, deleting or changing calendar events or tasks, downloading attachments, or setting out-of-office replies.

Risk: Attachment downloads can write untrusted mailbox content to disk.

Mitigation: Restrict downloads to a safe directory, sanitize filenames, scan downloaded files, and clean up temporary or downloaded files after use.

Risk: Credential configuration and default Exchange connection values may cause unintended account or server access.

Mitigation: Do not deploy until credential variables and Exchange endpoint configuration are fixed, explicit, and verified for the target environment.

## Reference(s):

- [Exchange2010 skill page](https://clawhub.ai/pes0/skills/exchange2010)
- [pes0 publisher profile](https://clawhub.ai/user/pes0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Exchange item metadata, message and calendar content, contact and task records, attachment metadata, downloaded files, extracted text, and status booleans.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
