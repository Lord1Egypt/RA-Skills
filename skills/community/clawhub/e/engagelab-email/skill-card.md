## Description: <br>
This skill is used to send emails via the EngageLab REST API. It supports regular sending, template sending, variable replacement, attachment handling, and sending settings such as sandbox mode and tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DevEngageLab](https://clawhub.ai/user/DevEngageLab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send and configure EngageLab email messages, including transactional messages, template sends, personalized content, attachments, sandbox testing, and tracking settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real email through EngageLab when configured with valid credentials. <br>
Mitigation: Use sandbox mode first and require manual confirmation of recipients, subject, body, attachments, tracking settings, and live-send status before sending. <br>
Risk: The provided sender script may mishandle API credentials. <br>
Mitigation: Fix or avoid the helper script before using real credentials, and use a restricted, rotatable API key. <br>
Risk: Email tracking settings may collect engagement signals or change recipient-facing behavior. <br>
Mitigation: Review open, click, and unsubscribe tracking settings for the intended audience and policy requirements before each live send. <br>


## Reference(s): <br>
- [EngageLab Email REST API Detailed Specification](references/api_spec.md) <br>
- [EngageLab Singapore email send endpoint](https://email.api.engagelab.cc/v1/mail/send) <br>
- [EngageLab Turkey email send endpoint](https://emailapi-tr.engagelab.com/v1/mail/send) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline JSON and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or adapt email request payloads, sender script usage, sandbox settings, recipient lists, attachment metadata, and tracking configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
