## Description: <br>
Guides agents to create precise cron-based reminders and recurring tasks, with timezone confirmation, cleanup, and chat-platform delivery guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn reminder, scheduling, and periodic-task requests into reliable cron-style agent jobs. It is especially useful when a user needs a reminder delivered at a specific time or through a supported chat platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create persistent scheduled tasks that continue after the immediate conversation. <br>
Mitigation: Confirm each schedule, recurrence, delivery target, and cleanup behavior before creating or retaining a task. <br>
Risk: Reminder content may be sent to external chat platforms. <br>
Mitigation: Review the destination channel, recipient, and message content, and avoid placing secrets or sensitive data in reminders. <br>
Risk: The skill may store timezone preferences in MEMORY.md. <br>
Mitigation: Ask the user before persisting timezone information and skip the write when they do not want that preference stored. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/cron-precision-scheduler) <br>
- [ISO 8601 Date and Time Format](https://www.iso.org/iso-8601-date-and-time-format.html) <br>
- [Cron Expression Syntax](https://crontab.guru/) <br>
- [WeCom Webhook Documentation](https://developer.work.weixin.qq.com/document/path/91770) <br>
- [DingTalk Custom Robot Access](https://open.dingtalk.com/document/robots/custom-robot-access) <br>
- [Feishu Card JSON Structure](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/feishu-cards/card-json-structure) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON task examples and inline shell or tool commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent scheduled tasks, timezone memory updates, and external chat delivery settings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
