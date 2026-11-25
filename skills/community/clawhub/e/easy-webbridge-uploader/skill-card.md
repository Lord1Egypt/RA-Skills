## Description:

通过用户已安装的 Easy WebBridge，将用户明确指定的本地文件上传到其指定网页中的文件输入框；完成上传核验后停止，不提交或发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

适用于需要通过已连接的 Easy WebBridge 浏览器，将明确指定的本地文件上传到指定网页文件输入框并核验页面状态的用户；流程在上传核验后停止，不提交表单。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this skill suspicious because browser controls may exceed file-upload needs and part of the CLI was only partially inspected.

Mitigation: Consider avoiding installation until the CLI is fully inspected and browser controls are limited to upload; if used, authorize only the named file and destination and stop after verifying the upload.

## Reference(s):

- [Upload command manual](references/upload-cookbook.md)
- [Project homepage](https://github.com/aiispower/easy-webbridge)
- [ClawHub release](https://clawhub.ai/xxjrq/skills/easy-webbridge-uploader)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task-specific instructions for an explicitly selected file and destination; stop after upload verification.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
