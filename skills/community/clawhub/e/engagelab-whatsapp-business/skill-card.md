## Description: <br>
Call EngageLab WhatsApp Business REST APIs to send WhatsApp messages, manage WABA message templates, and handle callback webhooks for delivery status and user responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DevEngageLab](https://clawhub.ai/user/DevEngageLab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate authenticated EngageLab WhatsApp Business API calls, code examples, template management requests, and webhook handling guidance for messaging integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help send real WhatsApp business messages. <br>
Mitigation: Use least-privilege EngageLab credentials and require human confirmation of recipients, message content, and template names before sending. <br>
Risk: The skill can help update or delete WABA templates. <br>
Mitigation: Review target template IDs or names before mutation and prefer dry-run or approval workflows for destructive changes. <br>
Risk: Artifact guidance notes that callback endpoints do not require authentication while callback security is pending. <br>
Mitigation: Deploy webhooks with compensating controls such as shared-secret validation, allowlists, schema checks, rate limits, and reconciliation against authenticated API state. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DevEngageLab/engagelab-whatsapp-business) <br>
- [EngageLab Website](https://www.engagelab.com) <br>
- [Callback API Reference](references/callback-api.md) <br>
- [Template API Reference](references/template-api.md) <br>
- [Error Codes Reference](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, JSON payloads, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request bodies, authentication placeholders, webhook recommendations, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
