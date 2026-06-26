## Description: <br>
Sends Feishu Interactive Card messages for richer notification cards and formatted message delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kolikoliko](https://clawhub.ai/user/kolikoliko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to compose and send Feishu Interactive Card notifications to chats or users, including scheduled reports and formatted status messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help send Feishu messages to the wrong chat or user if the recipient ID or recipient type is incorrect. <br>
Mitigation: Confirm receive_id, receive_id_type, message content, and any scheduled trigger before sending. <br>
Risk: Interactive cards may include buttons, links, or formatted content that recipients could act on. <br>
Mitigation: Review card text and button URLs before delivery, and grant the Feishu bot only the permissions and audience required for the intended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kolikoliko/feishu-card-sender-beautify) <br>
- [Card template examples](references/card-templates.md) <br>
- [feishu_im_user_message API reference](references/api-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with Python examples and JSON-like Feishu card payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Feishu recipient ID/type, interactive message type, and card content structure guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
