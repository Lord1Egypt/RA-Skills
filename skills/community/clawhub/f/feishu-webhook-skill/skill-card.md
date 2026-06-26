## Description: <br>
Sends Feishu/Lark webhook messages, including plain text, rich text post messages, interactive cards, and image uploads with a tenant access token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaniu001](https://clawhub.ai/user/shaniu001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare and send Feishu/Lark group notifications from an agent, including text notices, formatted posts, card layouts, and images that require upload before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook URLs and FEISHU_TENANT_ACCESS_TOKEN can grant access to send messages or upload images. <br>
Mitigation: Treat them as secrets, prefer environment variables over command-line token arguments, and use the least-privileged token available. <br>
Risk: The skill can send selected text and images to an external Feishu/Lark destination. <br>
Mitigation: Confirm the webhook destination and review message contents before sending sensitive internal information. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shaniu001/feishu-webhook-skill) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Feishu image upload API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create) <br>
- [Feishu file upload API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create) <br>
- [Feishu user identity guide](https://open.feishu.cn/document/home/user-identity-introduction/open-id) <br>
- [VChart documentation](https://www.visactor.io/vchart/guide/tutorial_docs/Chart_Concepts/Understanding_VChart) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Feishu/Lark webhook payload structures and image upload commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
