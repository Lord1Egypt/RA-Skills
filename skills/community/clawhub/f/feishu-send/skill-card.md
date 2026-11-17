## Description:

飞书发送图片/文件/语音。用 curl 调用飞书 API 发送，比 message 工具更可靠。用于需要发送图片、文件、语音到飞书时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare shell-based Feishu API calls for sending images, files, and audio messages to Feishu chats or users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad credential-backed uploads could send unintended files or media to Feishu.

Mitigation: Use tightly scoped Feishu credentials, known recipient IDs, and explicit user approval for each file or media item sent.

Risk: The account fallback can silently use the main Feishu account when the requested account is unavailable.

Mitigation: Remove the fallback or require an explicit authorized choice before using the main account.

Risk: The credential lookup snippets interpolate AGENT_NAME into Python source.

Mitigation: Rewrite the lookup to pass AGENT_NAME as data and only accept trusted account names.

## Reference(s):

- [Feishu Send on ClawHub](https://clawhub.ai/axelhu/skills/feishu-send)
- [Feishu Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu Image Upload API](https://open.feishu.cn/open-apis/im/v1/images)
- [Feishu File Upload API](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu Message Send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces credential lookup, upload, and message-send command patterns for Feishu media delivery.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
