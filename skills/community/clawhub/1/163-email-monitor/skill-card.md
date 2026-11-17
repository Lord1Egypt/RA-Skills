## Description:

Connect to 163/126/yeah.net (Coremail) email via IMAP, read inbox, search emails, and send emails via SMTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanyuhh](https://clawhub.ai/user/hanyuhh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and email users use this skill to let an agent check, search, and send mail for 163.com, 126.com, and yeah.net accounts that require the Coremail IMAP ID command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use stored mailbox authorization credentials to read mailbox contents and send messages.

Mitigation: Install and configure it only for accounts where agent access is intended, and store only the required mailbox authorization code in the configured environment file.

Risk: The send command can email arbitrary local attachments without a built-in confirmation step.

Mitigation: Before using send or --attach, manually verify the recipient, message body, and each attachment path, and avoid attaching secrets or private files unless that disclosure is intended.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Email read and search commands may include message metadata, body previews, or JSON-formatted results; send commands produce status text.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
