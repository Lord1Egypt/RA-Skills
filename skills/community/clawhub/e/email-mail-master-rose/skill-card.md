## Description:

Sends and receives email through supported mailbox providers, including plain messages, attachments, mailbox checks, and deletion operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roseknife520](https://clawhub.ai/user/roseknife520)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use this skill to configure a mailbox and run command-line email operations such as sending messages, sending attachments, reading recent mail, checking for new mail, and deleting selected messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact ships non-placeholder mailbox credentials.

Mitigation: Remove packaged credentials, rotate exposed auth codes or passwords, and use only a placeholder configuration example before installation.

Risk: The skill can send email and delete mailbox messages without strong confirmation or scoping.

Mitigation: Require explicit confirmation for sending mail and all deletion operations, and run it only against intended mailboxes with least-privilege credentials.

Risk: Some deletion paths can be permanent, including POP3 deletion for 163 Mail and explicit permanent deletion.

Mitigation: Verify message IDs and mailbox provider behavior before deleting, and avoid permanent deletion unless recovery is not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roseknife520/skills/email-mail-master-rose)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Plain text or JSON command output with inline shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send email, read mailbox contents, check recent mail, and delete messages through configured mailbox credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
