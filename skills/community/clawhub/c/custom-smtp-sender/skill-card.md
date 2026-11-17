## Description:

A skill that sends email messages with optional HTML bodies and attachments through an existing SMTP configuration file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scccmsd](https://clawhub.ai/user/scccmsd)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to send SMTP email messages and attachments from an agent workflow using a preconfigured SMTP account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses stored SMTP credentials and can send messages through the configured SMTP account.

Mitigation: Install only from a trusted publisher, use a dedicated app password, keep the SMTP configuration file permission-restricted, and keep TLS enabled.

Risk: Attachment support can transmit local files outside the intended scope.

Mitigation: Review recipient addresses and attachment paths before sending, and avoid attaching sensitive files unless explicitly intended.

Risk: The advertised Markdown conversion, retry behavior, and logging are not implemented in the inspected code.

Mitigation: Test expected behavior before operational use and do not rely on retry, Markdown conversion, or audit logging unless those features are added and reviewed.

## Reference(s):

- [Custom Smtp Sender on ClawHub](https://clawhub.ai/scccmsd/skills/custom-smtp-sender)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send email and local file attachments through the configured SMTP account.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
