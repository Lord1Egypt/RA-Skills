## Description:

163 email-sending tool that uses an authorization password for SMTP authentication and supports text email, HTML email, attachments, cc, and bcc.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imnull](https://clawhub.ai/user/imnull)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send email through a 163 mailbox from an agent workflow, including simple text messages, HTML messages, attachments, and copied recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TLS certificate validation is disabled for SMTP connections.

Mitigation: Do not use the skill for sensitive email until TLS certificate validation is restored and reviewed.

Risk: Recipients, subjects, cc/bcc, and send timestamps may be saved in local workspace history.

Mitigation: Treat the workspace history file as sensitive, clear it when no longer needed, and avoid sending sensitive metadata through this skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and Python CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EMAIL_163_USER and EMAIL_163_AUTH_CODE or equivalent command-line arguments; can write local send-history metadata.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
