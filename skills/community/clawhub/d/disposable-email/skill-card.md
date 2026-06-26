## Description: <br>
Create disposable Mail.tm inboxes and programmatically read incoming emails and OTP codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fantaclaw-ai](https://clawhub.ai/user/fantaclaw-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to create temporary Mail.tm inboxes, receive messages, and extract OTP codes for authorized email verification testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox credentials, bearer tokens, email contents, and OTP values can appear in command output or saved result files. <br>
Mitigation: Use only private terminals and trusted logs, avoid committing saved results, and delete any saved OTP result files after the test is complete. <br>
Risk: Disposable inbox automation can be misused against accounts or services the user does not control. <br>
Mitigation: Use the skill only for authorized testing flows and accounts you control. <br>
Risk: Mail.tm temporary domains may be blocked or unreliable for production services. <br>
Mitigation: Use stable paid inbox providers for CI or production-critical verification tests. <br>


## Reference(s): <br>
- [Disposable Email on ClawHub](https://clawhub.ai/fantaclaw-ai/disposable-email) <br>
- [Mail.tm API endpoint](https://api.mail.tm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit mailbox address, password, bearer token, message metadata, message text or HTML, and extracted OTP values.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
