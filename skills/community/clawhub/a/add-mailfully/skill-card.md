## Description:

Adds Mailfully transactional email to an app, including migrations from Resend, SendGrid, Postmark, or Nodemailer/SMTP, with test sending and sending-domain DNS setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gbourne1](https://clawhub.ai/user/gbourne1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Mailfully transactional email to an application or migrate transactional sending from a supported provider. It helps wire application code, test delivery, and prepare sending-domain DNS records; it does not write email copy or migrate marketing and bulk mail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API credentials, and browser-based CLI sign-in stores a credential beyond the session.

Mitigation: Keep test credentials local, never expose keys in chat or shell commands, and account for the CLI credential persisting after sign-in.

Risk: Opens and clicks are tracked by default, including rewritten sign-in links.

Mitigation: Disable tracking if it is unsuitable for the application or its users.

Risk: Sharing suppression lists through an unapproved channel could expose sensitive data.

Mitigation: Confirm the support channel and an approved transfer method before sharing suppression lists.

Risk: Enabling live sending before reviewing the integration could result in unintended production email.

Mitigation: Review changes and test credentials before enabling live sending; use a locked local script runner where possible.

## Reference(s):

- [Mailfully](https://mailfully.com)
- [Mailfully pricing](https://mailfully.com/pricing)
- [API essentials](references/api-essentials.md)
- [REST clients](references/rest-clients.md)
- [DNS provider setup](references/dns-providers.md)
- [Webhooks](references/webhooks.md)
- [Migrate from Nodemailer](references/migrate-nodemailer.md)
- [Migrate from Postmark](references/migrate-postmark.md)
- [Migrate from Resend](references/migrate-resend.md)
- [Migrate from SendGrid](references/migrate-sendgrid.md)

## Skill Output:

**Output Type(s):** [Code, Configuration, Shell commands, Guidance]

**Output Format:** [Project code and configuration files with a concise Markdown implementation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transactional email setup and migration only; sends one test-mode email and prepares DNS records without changing email copy.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
