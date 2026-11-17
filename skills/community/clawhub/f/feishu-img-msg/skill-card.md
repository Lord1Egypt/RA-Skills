## Description:

飞书图片消息 helps agents upload, send, download, and view Feishu image messages using local Feishu account credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imbing](https://clawhub.ai/user/imbing)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to operate Feishu image workflows from an assistant, including uploading local images, sending images to chats or users, downloading images by image_key, and returning image data for viewing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill disables normal HTTPS server-certificate checks while using Feishu credentials and transferring image data.

Mitigation: Review before installation, avoid use on untrusted networks, and restore default TLS certificate verification before broad deployment.

Risk: The skill can send local image files to Feishu chats or users and write downloaded images to local disk paths.

Mitigation: Require explicit confirmation of recipients, source files, and output paths before executing send or download operations.

Risk: The skill reads Feishu app credentials from the local OpenClaw configuration.

Mitigation: Use only Feishu credentials intended for this workflow and rotate or scope credentials according to the Feishu permissions required by the release.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/imbing/skills/feishu-img-msg)
- [Feishu upload image API](https://open.feishu.cn/document/server-docs/im-v1/image/create)
- [Feishu get image API](https://open.feishu.cn/document/server-docs/im-v1/image/get)
- [Feishu send message API](https://open.feishu.cn/document/server-docs/im-v1/message/create)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands, JSON command responses, data URI text, and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Feishu image_key values, local file paths, chat IDs, and an OpenClaw Feishu account configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
