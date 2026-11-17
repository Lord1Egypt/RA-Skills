## Description:

Automatically logs in to a 189.cn mailbox, downloads the newest inbox message as an .eml file, and saves it to the desktop for ad hoc or scheduled archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xizhima](https://clawhub.ai/user/xizhima)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill when they explicitly want an agent to access a 189.cn mailbox, export the latest message as an EML archive, and report the saved file path. It also supports daily scheduled mailbox archiving when the user understands how credentials, downloaded files, and the schedule will be managed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles mailbox credentials and should only be activated when the user clearly intends to log in to 189 Mail.

Mitigation: Ask for confirmation before using credentials, avoid collecting credentials in ambiguous chats, and do not store credentials in scripts or configuration.

Risk: Exported EML files may contain sensitive email content and attachments.

Mitigation: Save EML files only to a user-approved protected location and report the final path so the user can manage or delete the file.

Risk: Daily scheduled fetching can persist beyond the current session and repeatedly access the mailbox.

Mitigation: Set up scheduling only after explicit user approval and explain where the schedule lives and how to disable it.

## Reference(s):

- [189 Mail](https://mail.189.cn/)
- [ClawHub skill page](https://clawhub.ai/xizhima/skills/189mail-daily-fetch)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [EML file plus concise text status report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the email subject, sender, received time, and local save path when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
