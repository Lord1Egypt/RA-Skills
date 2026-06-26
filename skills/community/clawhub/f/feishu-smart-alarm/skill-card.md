## Description: <br>
读取飞书/Lark 消息文本，识别是否包含需要提醒的待办和截止时间，并在由系统根据消息语义和时间跨度自动判断，更偏宽松一点的预留时间发出一次提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hei-MaoM](https://clawhub.ai/user/Hei-MaoM) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect a Feishu/Lark bot to chat streams, detect reminder-worthy Chinese messages, store one-time reminders, and post confirmation and due reminder messages back to the original conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process every Feishu/Lark chat message routed to it. <br>
Mitigation: Restrict the chats connected to the bot and require an explicit reminder phrase or bot mention where possible. <br>
Risk: Reminder records can include message text, sender identifiers, chat identifiers, deadlines, and reminder text in a local SQLite database. <br>
Mitigation: Protect the SQLite database path, limit filesystem access, and define retention or deletion handling for stored reminders. <br>
Risk: The skill can later post confirmation and due reminder messages back into Feishu/Lark conversations. <br>
Mitigation: Use a dedicated low-permission Feishu/Lark app and review app permissions before installing in shared or sensitive spaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hei-MaoM/feishu-smart-alarm) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Feishu integration guide](references/integration_cn.md) <br>
- [Chinese time parsing rules](references/time_rules_cn.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command output, Feishu/Lark text messages, and Markdown usage guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local SQLite reminder records and sends one-time confirmation and reminder messages through Feishu/Lark when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
