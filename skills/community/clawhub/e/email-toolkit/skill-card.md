## Description:

Automates SMTP email sending across providers with support for attachments, HTML templates, TLS encryption, and delivery status tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and automation workflow builders use this skill to configure SMTP credentials, compose plain-text or HTML email, send attachments, and track delivery results for reports, alerts, and batch notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMTP credentials and app passwords may be exposed if stored in local configuration files.

Mitigation: Use environment variables or a secrets manager, keep app passwords scoped and revocable, and avoid committing or logging credentials.

Risk: Automated outbound or bulk email can send unintended messages or exceed provider limits.

Mitigation: Require explicit confirmation before sending, especially for bulk sends, and apply recipient validation plus provider-aware rate limits.

Risk: User-provided text, template names, or attachment paths could be misused if passed into shell commands or file access without validation.

Mitigation: Validate and allowlist attachment paths and avoid constructing shell commands directly from user input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/email-toolkit)
- [Google Account security settings](https://myaccount.google.com/security)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, bash commands, Python snippets, and SMTP delivery status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local files such as email_config.json, HTML templates, CSV recipient lists, and attachments.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 0.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
