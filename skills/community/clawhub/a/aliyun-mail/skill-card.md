## Description:

A skill to send emails via Aliyun enterprise email service with support for markdown, HTML text, attachments, and syntax highlighting for code blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jixsonwang](https://clawhub.ai/user/jixsonwang)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to send plain text, Markdown, or HTML email through Aliyun Enterprise Mail, optionally attaching local files and reading body content from a file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMTP credentials may be exposed or misused if the configuration file is not protected.

Mitigation: Use a dedicated app password and keep the SMTP configuration file private with restrictive permissions.

Risk: SMTP login may be unencrypted if TLS or STARTTLS is not enabled in configuration.

Mitigation: Require TLS or STARTTLS before using the skill to authenticate or send email.

Risk: Sensitive information may be sent to the wrong recipient or included through the wrong body file or attachment path.

Mitigation: Carefully verify every recipient, message body source, and attachment path before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jixsonwang/skills/aliyun-mail)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Configuration]

**Output Format:** [Email content, attachment selections, and command-line configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local body files and attach local files; SMTP credentials are supplied through a JSON configuration file.]

## Skill Version(s):

1.0.0 (source: release evidence, _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
