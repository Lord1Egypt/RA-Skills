## Description: <br>
Sends local images through the Feishu Open Platform API as inline image messages rather than file attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moistenxx](https://clawhub.ai/user/Moistenxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to upload screenshots, QR codes, or other supported image files to Feishu and send them to a user or chat as inline image messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports hardcoded Feishu app credentials in the artifact. <br>
Mitigation: Rotate the exposed credentials and configure scoped Feishu app credentials through environment variables or a secret manager before use. <br>
Risk: The skill uploads local images to Feishu and sends them to a recipient identifier. <br>
Mitigation: Verify the recipient ID and only send images that are approved for upload to Feishu. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Moistenxx/feishu-img-send-mx) <br>
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu image upload API endpoint](https://open.feishu.cn/open-apis/im/v1/images) <br>
- [Feishu message send API endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with bash commands and JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials, a recipient identifier, and a local image path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
