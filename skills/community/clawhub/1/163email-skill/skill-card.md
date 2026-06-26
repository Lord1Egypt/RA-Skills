## Description: <br>
Sends plain text email through the 163 SMTP service with custom recipients, subject, and content from the command line or Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liubindashen](https://clawhub.ai/user/liubindashen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send notification or workflow emails from a configured 163 account via command line or Python code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real email from the configured 163 account and may expose account access if SMTP credentials are mishandled. <br>
Mitigation: Use a dedicated or least-privilege sender account, keep CLAW_EMAIL_AUTH out of code, logs, and shell history, and rotate it if exposed. <br>
Risk: Email recipients or message content may include sensitive information. <br>
Mitigation: Review recipients and message content before sending sensitive or regulated information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liubindashen/163email-skill) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration] <br>
**Output Format:** [Plain text email content with CLI status text or Python Boolean return value] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAW_EMAIL and CLAW_EMAIL_AUTH; CLAW_SMTP_SERVER and CLAW_SMTP_PORT may override the default 163 SMTP endpoint.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
