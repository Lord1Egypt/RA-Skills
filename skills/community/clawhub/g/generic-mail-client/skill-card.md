## Description:

Send, receive, and manage emails through configured IMAP/POP3 and SMTP mail accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuwenke123](https://clawhub.ai/user/xuwenke123)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to operate one or more configured mailboxes: sending messages, listing and reading recent mail, and updating IMAP read status or folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, send, and modify email using stored mailbox credentials.

Mitigation: Install it only for a tightly controlled mailbox, preferably a dedicated automation account with an app-specific password.

Risk: Stored credentials and broad mailbox access can expose sensitive email content or enable unintended sending.

Mitigation: Move secrets out of config.yaml and add explicit recipient, payload, rate, and confirmation controls before use with real accounts.

Risk: Dependencies and the lockfile may need review before deployment.

Mitigation: Review and patch dependencies, then regenerate the lockfile from an HTTPS registry.

## Reference(s):

- [Generic Mail Client on ClawHub](https://clawhub.ai/xuwenke123/skills/generic-mail-client)

## Skill Output:

**Output Type(s):** [text, configuration, email operation results]

**Output Format:** [JSON-like handler responses with message metadata, message content, attachment metadata, and send or update status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform mailbox side effects such as sending email, marking messages read or unread, and moving IMAP messages.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
