## Description:

Reads email through POP3 and sends email through SMTP using mailbox configuration supplied by the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hpw03210](https://clawhub.ai/user/hpw03210)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to let an agent inspect mailbox counts, list or read messages, and send text or HTML email through configured POP3 and SMTP servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox credentials and email contents could be exposed if users share configuration files or disable encrypted mail connections.

Mitigation: Use app-specific mailbox credentials, protect config.yaml, and keep use_ssl enabled.

Risk: The undocumented delete-email API could remove mailbox messages if exposed to agents or callers without confirmation.

Mitigation: Avoid exposing undocumented Python methods, or remove deletion until it is clearly documented with an explicit confirmation step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hpw03210/skills/email-manager-pop3)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return mailbox counts, message metadata, message bodies, send status, and setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
