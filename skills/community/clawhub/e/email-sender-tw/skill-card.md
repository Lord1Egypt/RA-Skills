## Description: <br>
Email sending and template management tool for OpenClaw agents that supports SMTP sending, email templates, and attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sgb999520-hsu](https://clawhub.ai/user/sgb999520-hsu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use this skill to configure SMTP accounts, compose plain text or HTML messages, send templated email, and include attachments from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real external email and attachments using stored SMTP credentials. <br>
Mitigation: Install only when that behavior is intended, use a dedicated low-risk SMTP account or app password, and verify every recipient, message body, and attachment before sending. <br>
Risk: The bundled Gmail profile and stored credential workflow can expose or reuse an unintended account. <br>
Mitigation: Remove the bundled Gmail profile before use and configure a fresh SMTP profile for the intended account. <br>
Risk: Unsafe template or file handling can cause the wrong template or attachment to be used. <br>
Mitigation: Use only trusted template names and known attachment paths until path validation is fixed. <br>
Risk: The welcome template can include password-like content in outgoing email. <br>
Mitigation: Avoid the welcome password template for sensitive credentials and send account setup secrets through a separate approved channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sgb999520-hsu/email-sender-tw) <br>
- [Gmail App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples and shell commands; runtime scripts can produce plain text or HTML email messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can send external email, use SMTP configuration, render templates, and include attachments when executed.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
