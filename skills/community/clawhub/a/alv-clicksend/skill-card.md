## Description: <br>
SkillBoss API Hub integration for SMS/MMS messaging and voice calls that sends messages, manages contacts and lists, and tracks delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send SMS, MMS, and voice messages through SkillBoss API Hub, query message status and pricing, and manage ClickSend-style contacts, lists, and templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send paid SMS, MMS, and voice messages to real recipients. <br>
Mitigation: Require explicit user confirmation for recipient, message body, provider, and cost-sensitive send details before using billing-enabled accounts. <br>
Risk: The skill documents contact, list, and template create, update, delete, copy, transfer, and cancel operations. <br>
Mitigation: Treat every cancel, delete, or contact/list/template mutation as destructive until confirmed against the intended account and record identifiers. <br>
Risk: Provider routing is unclear across SkillBoss, Prelude, and ClickSend-style endpoints. <br>
Mitigation: Verify the actual service path and account that will process each request before sending to real recipients or relying on delivery, pricing, or receipt data. <br>
Risk: Use requires a sensitive SKILLBOSS_API_KEY with messaging and contact-management authority. <br>
Mitigation: Store the key only in the intended environment variable, limit its account permissions where possible, and avoid exposing it in prompts, logs, or examples. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/alv-clicksend) <br>
- [SkillBoss API Hub](https://heybossai.com) <br>
- [ClickSend Developer Portal](https://developers.clicksend.com/) <br>
- [ClickSend REST API v3 Documentation](https://developers.clicksend.com/docs) <br>
- [ClickSend Help Center](https://help.clicksend.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python, JavaScript, bash, JSON, and HTTP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SKILLBOSS_API_KEY and network access; examples use the SkillBoss /v1/run endpoint and ClickSend-style API paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
