## Description: <br>
GetResponse API integration with managed OAuth for managing email marketing campaigns, contacts, newsletters, autoresponders, segments, workflows, ecommerce/shops, SMS, landing pages, webinars, transactional emails, forms, and account data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate GetResponse accounts through Maton-managed OAuth, including reading account data and managing marketing, ecommerce, automation, messaging, and contact resources. It is intended for workflows where the user can review and approve actions before any create, update, delete, send, or publish operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send newsletters, SMS, and transactional emails to real contacts. <br>
Mitigation: Confirm the audience, message content, and send timing with the user before executing any messaging operation. <br>
Risk: Write, publish, update, or delete operations can modify GetResponse account resources. <br>
Mitigation: Keep confirmation prompts enabled and require explicit user approval with the target resource and intended effect before executing changes. <br>
Risk: The skill requires a sensitive MATON_API_KEY credential and managed OAuth access. <br>
Mitigation: Install only when Maton-mediated GetResponse access is intended, store credentials securely, and use the correct connection identifier when multiple GetResponse accounts are connected. <br>


## Reference(s): <br>
- [GetResponse Skill on ClawHub](https://clawhub.ai/byungkyu/getresponse) <br>
- [Maton Homepage](https://maton.ai) <br>
- [GetResponse API Documentation](https://apidocs.getresponse.com/v3) <br>
- [GetResponse OpenAPI Spec](https://apireference.getresponse.com/open-api.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a MATON_API_KEY credential, and explicit user approval for write, send, publish, update, or delete operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
