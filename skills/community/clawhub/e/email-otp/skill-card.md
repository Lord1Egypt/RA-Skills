## Description: <br>
Create temporary email addresses and monitor for registration OTP codes or validation links <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etopro](https://clawhub.ai/user/etopro) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to create disposable email inboxes for low-risk signup or verification flows, then extract OTP codes or validation links from incoming messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary mailbox credentials, OTPs, and validation links are stored locally under ~/.tempmail_otp/. <br>
Mitigation: Treat the state directory as sensitive and delete ~/.tempmail_otp/ after the verification flow. <br>
Risk: The workflow depends on the third-party mail.tm disposable email service. <br>
Mitigation: Use it only for low-risk verification flows and avoid high-value personal, financial, recovery, or work accounts. <br>


## Reference(s): <br>
- [Email OTP on ClawHub](https://clawhub.ai/etopro/email-otp) <br>
- [mail.tm API](https://api.mail.tm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text or JSON CLI output, plus local state files for the active mailbox, latest OTP, and first validation link.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python standard library commands and stores state under ~/.tempmail_otp/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
