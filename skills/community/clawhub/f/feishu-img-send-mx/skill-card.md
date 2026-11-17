## Description:

通过飞书开放平台 API 直接发送图片，让截图、二维码等图片以内嵌消息形式送达用户，而不是作为文件附件发送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[moistenxx](https://clawhub.ai/user/moistenxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare Feishu API calls that upload a local image, obtain an image key, and send it as an inline image message to a user or chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published example includes a real-looking Feishu app secret.

Mitigation: Treat the secret as exposed, rotate it if it belongs to a real app, and replace it with securely stored credentials before use.

Risk: The workflow uploads local images and sends them to selected Feishu recipients.

Mitigation: Confirm recipient identifiers and upload only images that are intended to be delivered through Feishu.

Risk: The shell example builds JSON through string interpolation.

Mitigation: Prefer a JSON serializer or the serialized Node.js-style request construction for safer request bodies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moistenxx/skills/feishu-img-send-mx)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu image upload API](https://open.feishu.cn/open-apis/im/v1/images)
- [Feishu image message API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu API endpoint usage, credential placeholders, recipient identifier options, and image-message constraints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
