## Description:

Uploads local PDF or other files to Feishu/Lark cloud drive using the Feishu OpenAPI upload_prepare, upload_part, and upload_finish flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zheng-xiru](https://clawhub.ai/user/zheng-xiru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to upload generated reports, backups, or selected local files into a target Feishu/Lark cloud drive folder from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload selected local files to Feishu/Lark using configured app credentials.

Mitigation: Use explicit file paths and destination folder tokens, and avoid broad upload prompts for sensitive files.

Risk: Large file uploads may consume substantial memory or stall if Feishu/Lark or network calls hang.

Mitigation: Limit file size for agent-driven uploads and monitor long-running upload attempts.

Risk: Incorrect or over-privileged Feishu/Lark credentials could expose files to an unintended workspace or folder.

Mitigation: Use least-privilege app credentials and verify the target folder token before running uploads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zheng-xiru/skills/feishu-pdf-uploader)
- [Publisher profile](https://clawhub.ai/user/zheng-xiru)
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu upload prepare endpoint](https://open.feishu.cn/open-apis/drive/v1/files/upload_prepare)
- [Feishu upload part endpoint](https://open.feishu.cn/open-apis/drive/v1/files/upload_part)
- [Feishu upload finish endpoint](https://open.feishu.cn/open-apis/drive/v1/files/upload_finish)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON-like upload results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, requests, Feishu/Lark app credentials, and a destination folder token.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
