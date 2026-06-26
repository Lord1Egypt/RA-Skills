## Description: <br>
Email management and automation. Send, read, search, and organize emails across multiple providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awspace](https://clawhub.ai/user/awspace) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure SMTP email sending, send test messages, and send emails with optional CC, BCC, HTML body, and attachments across common providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real emails and local file attachments outside the system. <br>
Mitigation: Require a final human review that names the recipients, subject, body summary, and every attachment path before sending. <br>
Risk: Email account credentials may be exposed if configuration files are committed or reused broadly. <br>
Mitigation: Use a dedicated sending account or app password, keep email_config.json out of version control, and rotate credentials regularly. <br>


## Reference(s): <br>
- [ClawHub Email skill listing](https://clawhub.ai/awspace/email-skill) <br>
- [Google account security](https://myaccount.google.com/security) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute SMTP email sending when configured with account credentials and explicit recipient, subject, body, and attachment inputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
