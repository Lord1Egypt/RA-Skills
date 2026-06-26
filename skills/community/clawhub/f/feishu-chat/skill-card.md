## Description: <br>
Feishu (Lark) group chat messaging guide for OpenClaw. Includes Raw/Card message modes, @ mention formatting, and group member management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Heimo-He](https://clawhub.ai/user/Heimo-He) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to send Feishu group messages with the right raw or card formatting, @ mention syntax, and member ID handling. It is useful when coordinating group chat replies, formatted Markdown messages, and bot or human mentions in Feishu groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages may be sent to the wrong Feishu group or include unintended @ mentions, including @everyone. <br>
Mitigation: Confirm the target group, message content, and mention IDs before sending, and use @everyone only when the group policy allows it. <br>
Risk: Changing renderMode or restarting the OpenClaw gateway can affect how Feishu messages are delivered. <br>
Mitigation: Apply renderMode and gateway restart changes intentionally, then verify the active setting before relying on formatted messages. <br>
Risk: Stored Feishu member IDs can expose group membership details if kept too broadly. <br>
Mitigation: Store member IDs only when needed in a private, scoped memory file. <br>


## Reference(s): <br>
- [ClawHub Feishu Chat Skill Page](https://clawhub.ai/Heimo-He/feishu-chat) <br>
- [Feishu Developer Console](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces messaging instructions only; users should confirm groups, message content, mentions, and configuration changes before sending.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
