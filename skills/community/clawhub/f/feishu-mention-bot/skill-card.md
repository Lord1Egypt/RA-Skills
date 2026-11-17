## Description:

飞书群聊中 @机器人并发送消息。当用户需要在飞书群里艾特机器人、通知其他机器人、或让机器人之间互相通信时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcjinglang](https://clawhub.ai/user/pcjinglang)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to format Feishu group messages that mention another bot, retrieve bot open_id values from message history, and send mention messages through a message tool or Feishu API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill works with Feishu app secrets, bearer tokens, chat history, and message sending examples.

Mitigation: Use approved chats, least-privilege Feishu app permissions, secure secret storage, redacted logs, and avoid placing real secrets or bearer tokens directly in shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pcjinglang/skills/feishu-mention-bot)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu messages API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline command and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu mention markup, open_id retrieval guidance, permission notes, and message-sending examples.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
