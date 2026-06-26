## Description: <br>
Uploads a local image to Feishu/Lark and sends it to a configured group webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imBing](https://clawhub.ai/user/imBing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Feishu/Lark app credentials and a group bot webhook, then upload selected local images and post them into a chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local images are uploaded to Feishu/Lark and may be posted to the configured group chat. <br>
Mitigation: Verify the destination webhook and avoid confidential screenshots, documents, photos, or customer data unless the organization has approved that sharing flow. <br>
Risk: The skill requires app credentials and a webhook URL in a local config.py file. <br>
Mitigation: Keep config.py out of public repositories and rotate credentials if the file is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imBing/feishu-image-webhook) <br>
- [Publisher profile](https://clawhub.ai/user/imBing) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu image upload endpoint](https://open.feishu.cn/open-apis/im/v1/images) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local image path, Feishu/Lark app credentials, and a configured group webhook.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
