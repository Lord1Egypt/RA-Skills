## Description:

赛博办公 IM 分身——以用户本人身份值守飞书 / 企业微信 / 钉钉的私聊或群聊，脚本阻塞轮询，新消息才唤醒 agent 起草并以本人身份回复，等待期不跑模型；自动学习本人风格、沉淀服务对象画像，内置体检与故障自愈。当用户说「赛博分身」「办公分身」「IM 分身」「替我盯着某人/某群的消息」「有人发消息时自动回复」「帮我值守私聊/群聊」「给某人当客服」「让 AI 代回消息」时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[buger-gif](https://clawhub.ai/user/buger-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to monitor selected Feishu, WeCom, or DingTalk conversations and prepare replies in the user's voice. It provides setup and troubleshooting guidance for message monitoring, with human review as the default before a reply is sent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permission guidance may not match the permissions actually requested by the connected provider.

Mitigation: Inspect the provider's consent screen directly. Keep draft approval enabled and select conversations explicitly; when existing authorization cannot be determined, have the publisher fix the permission checks.

Risk: Recommendations may enable unrestricted file access.

Mitigation: Leave unrestricted file access disabled and grant only narrowly scoped file permissions.

Risk: Preview mode can write settings, and the deletion command can leave daily summaries behind.

Mitigation: Review settings changes before using preview mode and verify the remaining daily summaries after deleting data.

## Reference(s):

- [Feishu guide](artifact/references/feishu.md)
- [WeCom guide](artifact/references/wecom.md)
- [DingTalk guide](artifact/references/dingtalk.md)
- [Troubleshooting guide](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Concise guidance and message drafts in Markdown or plain text, with shell command examples when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content depends on the selected messaging platform, conversation, and requested task.]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
