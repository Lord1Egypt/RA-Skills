## Description: <br>
Send plain-text emails with optional file attachments through a Gmail SMTP account by specifying a recipient, subject, body, and optional attachment path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elodyzen](https://clawhub.ai/user/elodyzen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and agents use this skill to send plain-text email messages when a task requires delivering reports, logs, or files by email. It is intended for email delivery workflows that need a recipient, subject, required body text, and optional attachment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a hardcoded Gmail app password for the bundled sender account. <br>
Mitigation: Install only after replacing the credential with securely stored user-controlled credentials and rotating the exposed app password. <br>
Risk: The attachment path can cause the skill to email any local file the agent is allowed to read. <br>
Mitigation: Confirm the recipient, body, and attachment before each send, and restrict attachments to approved workspace paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elodyzen/email-sender) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, files] <br>
**Output Format:** [Plain text status message after attempting to send an email] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send an outbound email and may attach a local file path the agent can read.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
