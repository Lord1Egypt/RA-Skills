## Description: <br>
Proactively send messages to Feishu (Lark) users or group chats from an OpenClaw agent, with recipient lookup by contact label, open_id, or chat_id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingzuer](https://clawhub.ai/user/lingzuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to let an agent notify Feishu users or group chats with task results, reports, status updates, or coordination messages after the Feishu plugin and recipient permissions are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Feishu or Lark direct messages and group messages using configured app credentials. <br>
Mitigation: Use it only where agent-initiated messaging is intended, keep Feishu app permissions narrow, and require confirmation or recipient limits for sensitive messages. <br>
Risk: OpenClaw configuration contains Feishu app credentials used by the script. <br>
Mitigation: Protect openclaw.json and avoid exposing task outputs, logs, secrets, or private data in messages unless the recipient and content are approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lingzuer/feishu-dm-sender) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, JSON, Text messages] <br>
**Output Format:** [Markdown usage guidance with bash examples; the script returns JSON and sends text messages through Feishu.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python 3 standard library and the user's configured OpenClaw Feishu credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
