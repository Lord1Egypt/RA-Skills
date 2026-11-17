## Description:

Full Mail lets an agent send email over SMTP and receive, list, search, read, mark, delete, and download attachments from email over IMAP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legionspace-hackathon](https://clawhub.ai/user/legionspace-hackathon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Full Mail to configure an email account and let an agent send messages, inspect inbox mail, search messages, manage read state, delete messages, and retrieve attachments through SMTP and IMAP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox deletion can cause data loss because delete operations expunge messages immediately.

Mitigation: Confirm the selected message before deletion and avoid automated delete workflows unless recovery requirements are understood.

Risk: Attachment download behavior can overwrite local files or save unsafe attachments from untrusted messages.

Mitigation: Avoid downloading attachments from untrusted mail until filenames are sanitized and confined to the intended download directory.

Risk: Configured mail credentials grant access to send, read, search, mark read, and delete mail for the account.

Mitigation: Use a provider app password, restrict configuration file permissions, and revoke the credential if exposure is suspected.

## Reference(s):

- [Full Mail ClawHub page](https://clawhub.ai/legionspace-hackathon/skills/full-mail)
- [Full Mail configuration guide](artifact/配置指南.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain-text command output, configuration snippets, and downloaded attachment files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SMTP and IMAP account settings in environment variables; actions can send messages and modify mailbox state.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
