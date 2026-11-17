## Description:

用钉钉给自己/同事发通知与私信：工作通知（应用消息）、机器人单聊私信、以本人身份私信，支持 text/markdown/文件，失败自动留痕。当需要「钉钉通知 / 钉钉私信 / 工作通知 / 机器人消息 / 把结果推到钉钉 / dingtalk notify / 配置钉钉企业内部应用 AppKey」时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hero81yf](https://clawhub.ai/user/hero81yf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send DingTalk work notifications, bot or self-identity direct messages, and text, Markdown, or file content to configured recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review warns that DingTalk credentials could be exposed through error output or logs, which may be visible to other users.

Mitigation: Restrict access to process output and the configured log directory, and protect the credential configuration file.

Risk: The security review flags external messaging and full environment copying for review; its analysis is incomplete because the referenced INSTALL.md was missing.

Mitigation: Review recipients and message content before sending, check how dws handles inherited environment variables, and review the complete installation instructions before enabling self-identity messaging.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hero81yf/skills/dtflow-notify)

## Skill Output:

**Output Type(s):** [Text, Markdown, File notifications, Delivery status]

**Output Format:** [DingTalk messages and file notifications sent through the command-line interface]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DingTalk app credentials; --dm-self requires dws. Individual file messages are limited to 20 MB.]

## Skill Version(s):

0.1.1 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
