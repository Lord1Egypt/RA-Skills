## Description:

Sends email through SMTP using Nodemailer, with support for common providers such as 163, QQ, and Gmail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anbangzhiguo](https://clawhub.ai/user/anbangzhiguo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent send plain text or HTML email through a configured SMTP account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMTP credentials can be exposed if real secrets are placed directly in command text or logs.

Mitigation: Use a dedicated SMTP app password with minimal permissions and inject it through a secret manager or inherited environment.

Risk: The skill can send outbound email broadly once SMTP credentials are configured.

Mitigation: Require explicit user confirmation before sending and review recipient, subject, body, cc, and html mode.

Risk: Evidence reports a vulnerable Nodemailer dependency.

Mitigation: Update Nodemailer to a patched supported version before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anbangzhiguo/skills/email-send-cn)
- [Nodemailer package artifact](https://registry.npmjs.org/nodemailer/-/nodemailer-6.10.1.tgz)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text]

**Output Format:** [Command-line execution with textual success or failure output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SMTP_HOST, SMTP_USER, and SMTP_PASS; SMTP_PORT, SMTP_SECURE, SMTP_FROM, cc, subject, body, and html mode are optional.]

## Skill Version(s):

1.0.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
