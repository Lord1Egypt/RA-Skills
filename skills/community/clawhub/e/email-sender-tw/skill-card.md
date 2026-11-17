## Description:

Email sending and template management tool for OpenClaw agents. Supports SMTP sending, email templates, and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sgb999520-hsu](https://clawhub.ai/user/sgb999520-hsu)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers use this skill to configure SMTP profiles, send plain text or HTML email, manage reusable templates, and attach files from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled sample SMTP profile contains a live-looking Gmail account.

Mitigation: Remove the bundled sample profile and configure a user-owned SMTP profile before use.

Risk: Template operations can escape the intended template folder and modify or delete local .html or .txt files.

Mitigation: Use only trusted template names and review or restrict path handling before allowing untrusted input to control template names.

Risk: HTML template variables and template content can carry sensitive or unsafe email content.

Mitigation: Do not put passwords or secrets in templates or variables, and sanitize or review HTML content before sending.

Risk: Attachment paths can send any readable file path provided to the skill.

Mitigation: Treat attachment paths as sensitive and attach only files that were explicitly intended for the recipient.

Risk: SMTP credentials are required to send mail.

Mitigation: Use app-specific passwords where supported and rotate email credentials regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sgb999520-hsu/skills/email-sender-tw)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Gmail App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python and shell commands; bundled scripts produce CLI status text and send SMTP email.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports plain text and HTML email, CC/BCC, batch sending, local templates, and attachments; requires macOS Keychain for stored SMTP passwords.]

## Skill Version(s):

1.2.0 (source: server release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
