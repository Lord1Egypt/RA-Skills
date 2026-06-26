## Description: <br>
Sends Feishu card messages, including text and image cards, through the message tool using configured Feishu app credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blackswan-mohu](https://clawhub.ai/user/blackswan-mohu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare and send Feishu interactive card notifications to known users or group chats. It also provides a helper script to upload local images and retrieve the img_key required by Feishu image card elements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Feishu messages using the user's app identity. <br>
Mitigation: Use a least-privileged Feishu app with only the needed message permission and review recipients and card content before sending. <br>
Risk: Feishu App Secret exposure could allow unauthorized use of the Feishu app. <br>
Mitigation: Prefer environment variables or a secret manager, avoid committing secrets in plaintext, and rotate the secret if exposed. <br>
Risk: The image upload helper reads and uploads a local image path. <br>
Mitigation: Review image paths before upload and avoid sending sensitive or unintended files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blackswan-mohu/feishucard-sender) <br>
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu image upload API endpoint](https://open.feishu.cn/open-apis/im/v1/images) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Feishu card JSON examples and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu App ID, App Secret, im:message permission, and valid Feishu recipient targets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
