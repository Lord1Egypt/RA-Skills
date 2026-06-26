## Description: <br>
Helps agents configure and use Enterprise WeChat webhooks to send group text and Markdown notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure an Enterprise WeChat webhook and send operational notifications, reminders, alerts, and text or Markdown updates to group chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook keys and related credentials can be exposed through command history, shared terminals, logs, or CI output. <br>
Mitigation: Store keys in protected configuration or environment variables, mask them in automation logs, avoid shared terminals for tests, and rotate keys after exposure or broad testing. <br>
Risk: Messages can disclose secrets, personal data, stack traces, or sensitive incident details to an Enterprise WeChat group. <br>
Mitigation: Review destination chats and message content before sending; keep secrets, personal data, and sensitive operational details out of notifications. <br>
Risk: Text messages can notify the entire chat by default when no mention list is provided. <br>
Mitigation: Set an explicit mention list or adjust defaults before using the skill in active enterprise groups. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaising-openclaw1/enterprise-wechat-bot) <br>
- [Enterprise WeChat Developer Center](https://developer.work.weixin.qq.com) <br>
- [Enterprise WeChat Robot API](https://developer.work.weixin.qq.com/document/path/91770) <br>
- [Enterprise WeChat Message Push](https://developer.work.weixin.qq.com/document/path/90236) <br>
- [Artifact setup guide](artifact/SETUP-GUIDE.md) <br>
- [Artifact API research notes](artifact/API-RESEARCH.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI, JavaScript, shell, and JSON examples; runtime output is Enterprise WeChat API responses and terminal status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Enterprise WeChat webhook key; text messages may mention everyone by default when no mention list is supplied.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
