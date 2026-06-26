## Description: <br>
Windows 电脑端钉钉消息自动发送技能，通过键盘模拟给指定联系人发送消息。快捷命令：dt <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpuego123](https://clawhub.ai/user/zhangpuego123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to send DingTalk messages to one contact or a contact list from a logged-in Windows DingTalk desktop session. It automates contact search, message entry, and send actions through keyboard and mouse control rather than a DingTalk API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real DingTalk messages from the user's logged-in account without an additional confirmation step. <br>
Mitigation: Review recipients and message text before each send, and run it only in a DingTalk session where that automation is intended. <br>
Risk: Batch mode increases the chance of sending a message to the wrong recipient or continuing a queue unintentionally. <br>
Mitigation: Avoid batch mode for sensitive messages and verify each queued recipient before continuing to the next send. <br>
Risk: The optional queue_file path can direct queue state to arbitrary local paths. <br>
Mitigation: Do not provide custom queue_file paths; use the default queue behavior unless the file location has been reviewed. <br>
Risk: Dependencies are listed without pinned versions. <br>
Mitigation: Install reviewed, pinned dependency versions in a controlled environment before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhangpuego123/dingding-talk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, command examples, and MCP text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create and update a local send queue file during batch sends.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
