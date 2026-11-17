## Description:

139mail lets an OpenClaw agent send, list, receive, and read email over IMAP/SMTP for 139, QQ, 163, Gmail, and other common mailbox providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chang-tong](https://clawhub.ai/user/chang-tong)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an OpenClaw agent send email, list inbox messages, inspect unread mail, and read selected message details through configured IMAP and SMTP accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles mailbox credentials and email content, and the authoritative security summary reports unsafe TLS behavior and weak credential-file protections.

Mitigation: Review before installing, use only email authorization codes, restrict config/email.json to owner-only permissions, and avoid use over untrusted networks unless IMAP TLS certificate validation is fixed.

Risk: Broad natural-language activation can lead an agent to send attachments or read mailbox content in sensitive contexts.

Mitigation: Require user confirmation for sending email or attachments and limit mailbox reads to the smallest necessary message set.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chang-tong/skills/139mail-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/chang-tong)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Natural-language agent responses with JSON command results and configuration or shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May expose mailbox metadata, message content, send results, and attachment-related paths depending on the requested email operation.]

## Skill Version(s):

1.0.0 (source: release metadata, openclaw.skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
