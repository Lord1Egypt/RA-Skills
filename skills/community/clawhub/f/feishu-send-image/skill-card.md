## Description:

This skill helps an agent send user-specified images or files to Feishu users or group chats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlif](https://clawhub.ai/user/jlif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send local images or files to Feishu users or chats from an agent when Feishu app credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses local Feishu app credentials to upload and send files externally.

Mitigation: Install only where those credentials are intended for agent use and confirm each recipient ID, recipient type, and file path before sending.

Risk: A mistaken file path or recipient can disclose sensitive local files.

Mitigation: Send only deliberately selected files and avoid sensitive content unless disclosure to the Feishu recipient is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlif/skills/feishu-send-image)
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu image upload API endpoint](https://open.feishu.cn/open-apis/im/v1/images)
- [Feishu file upload API endpoint](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message send API endpoint](https://open.feishu.cn/open-apis/im/v1/messages)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with inline bash commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends user-specified local images or files to Feishu recipients using configured Feishu app credentials.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
