## Description: <br>
Send, read, and summarize email through SMTP and IMAP using environment-based credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hansonjames](https://clawhub.ai/user/hansonjames) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send email, read recent inbox messages, and summarize recent email activity through configured SMTP and IMAP accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private mailbox contents. <br>
Mitigation: Use it only with mailboxes the agent is authorized to inspect, and request inbox reads or analysis only when that access is intended. <br>
Risk: The skill can send outbound email from the configured account. <br>
Mitigation: Review the recipient, subject, body, CC list, and HTML body before allowing a send operation. <br>
Risk: Mailbox credentials are loaded from environment variables or nearby .env files. <br>
Mitigation: Use an app-specific or limited email password and keep unrelated secrets out of nearby .env files. <br>
Risk: The skill can attach arbitrary local files whose paths are supplied to it. <br>
Mitigation: Review every attachment path before sending and provide only files intended for the recipient. <br>


## Reference(s): <br>
- [Email Configuration](references/configuration.md) <br>
- [ClawHub skill page](https://clawhub.ai/hansonjames/email-send-hanson) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON results or concise Markdown summaries with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Email reads are limited by the requested message count; send operations return recipient, subject, and attachment status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
