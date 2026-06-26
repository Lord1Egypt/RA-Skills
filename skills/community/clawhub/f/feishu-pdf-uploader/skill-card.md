## Description: <br>
Feishu PDF Uploader uploads local PDF or other files to Feishu (Lark) cloud drive using the Feishu OpenAPI prepare, upload, and finish flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zheng-xiru](https://clawhub.ai/user/zheng-xiru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload generated reports, backups, or other named local files to a chosen Feishu or Lark cloud-drive folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload any local file path the user provides to a Feishu or Lark cloud-drive folder. <br>
Mitigation: Confirm the exact file path, target folder token, and Feishu account before each upload. <br>
Risk: The skill uses Feishu app credentials to obtain a tenant access token for cloud-drive uploads. <br>
Mitigation: Use a least-privileged Feishu app and keep app credentials in the configured credential source rather than in prompts or shared files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zheng-xiru/feishu-pdf-uploader) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu upload prepare endpoint](https://open.feishu.cn/open-apis/drive/v1/files/upload_prepare) <br>
- [Feishu upload part endpoint](https://open.feishu.cn/open-apis/drive/v1/files/upload_part) <br>
- [Feishu upload finish endpoint](https://open.feishu.cn/open-apis/drive/v1/files/upload_finish) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash and Python snippets; the uploader returns JSON-like status, file token, and URL fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, python3-requests, Feishu app credentials, and a target folder token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
