## Description:

Windows 电脑端钉钉消息自动发送技能，通过键盘模拟给指定联系人发送消息。快捷命令：dt

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangpuego123](https://clawhub.ai/user/zhangpuego123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send single or batch DingTalk desktop messages to named contacts or groups through keyboard automation on a controlled Windows session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real DingTalk messages through desktop automation.

Mitigation: Use it only in a controlled desktop session where the active window, recipient, and message can be monitored before sending.

Risk: The batch queue_file option can use a caller-controlled path.

Mitigation: Avoid the queue_file option unless it is restricted to a safe application-owned directory.

Risk: Keyboard automation may send to the wrong chat if the DingTalk window focus or search result is unexpected.

Mitigation: Prefer a version that confirms the recipient and message before pressing Enter.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Messages are sent through the local DingTalk desktop client and may append an OpenClaw auto-send suffix.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
