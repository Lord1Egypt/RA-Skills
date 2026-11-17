## Description:

Sends text and Markdown messages to Enterprise WeChat group robots through webhook-based commands and JavaScript helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to send operational notifications, reminders, and alerts into Enterprise WeChat group chats through webhook-based commands or JavaScript calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook keys can be exposed through command-line arguments, logs, shared terminal output, or CI output.

Mitigation: Keep webhook keys in private configuration or environment storage, avoid printing full webhook URLs, and rotate any key that was exposed.

Risk: Setup instructions include a high-privilege remote installer pattern for Node.js.

Mitigation: Use a pinned and trusted Node.js installation method instead of running a remote installer through a privileged shell.

Risk: Sent message content leaves the local environment for Enterprise WeChat.

Mitigation: Review message content for secrets, personal data, and confidential operational details before sending.

Risk: Default or broad mentions can notify more recipients than intended.

Mitigation: Confirm target chat IDs and mention lists before sending production alerts or scheduled messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/skills/enterprise-wechat-bot)
- [Enterprise WeChat Developer Center](https://developer.work.weixin.qq.com)
- [Enterprise WeChat group robot API](https://developer.work.weixin.qq.com/document/path/91770)
- [Enterprise WeChat message push API](https://developer.work.weixin.qq.com/document/path/90236)
- [Artifact API research notes](API-RESEARCH.md)
- [Artifact setup guide](SETUP-GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command-line examples and JavaScript helper calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Messages are sent to Enterprise WeChat through a configured webhook key; text messages may mention recipients configured by the caller.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
