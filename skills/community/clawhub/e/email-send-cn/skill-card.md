## Description: <br>
Sends email through SMTP with Nodemailer using environment-provided SMTP credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anbangzhiguo](https://clawhub.ai/user/anbangzhiguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send plain-text or HTML email through a configured SMTP account when an email-sending workflow is requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real email using configured SMTP credentials. <br>
Mitigation: Require a visible final approval step for each email, including recipients, subject, and body, before executing the send command. <br>
Risk: SMTP credentials may grant broad mailbox access. <br>
Mitigation: Use dedicated or least-privilege SMTP credentials and store them in environment variables or a secrets manager instead of command history or source files. <br>
Risk: The release ships an affected Nodemailer dependency according to the security evidence. <br>
Mitigation: Prefer an updated release that pins a patched Nodemailer version before production use. <br>
Risk: Recipients and message content are passed directly to the send script. <br>
Mitigation: Validate recipients and review generated message content before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anbangzhiguo/email-send-cn) <br>
- [Publisher profile](https://clawhub.ai/user/anbangzhiguo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and environment-variable configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SMTP_HOST, SMTP_USER, SMTP_PASS, and node; SMTP_PORT, SMTP_SECURE, SMTP_FROM, cc, and html are optional.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
