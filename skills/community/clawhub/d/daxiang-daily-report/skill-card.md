## Description: <br>
生成大象每日沟通分析报告，汇总个人对话、群聊消息、沟通频率、活跃联系人、群聊摘要、整体洞察和待办事项。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kindhf](https://clawhub.ai/user/kindhf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or authorized users with access to Daxiang chat exports use this skill to generate daily communication summaries from personal and group chat records. It supports one-off report generation for a selected date and scheduled daily reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive workplace chat messages may be collected, cached, and reproduced in generated JSON and Markdown reports. <br>
Mitigation: Run only with authorization for the Daxiang chats involved, use a private output directory, and handle generated files as sensitive records. <br>
Risk: Scheduled execution can continue collecting chat data beyond a one-off report. <br>
Mitigation: Enable cron or OpenClaw scheduled jobs only when ongoing collection is intended, and review retention needs before keeping generated files. <br>
Risk: Complete conversation content may be exposed in reports. <br>
Mitigation: Prefer redacted or aggregate-only reports when full message detail is not necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kindhf/daxiang-daily-report) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [OpenClaw documentation](https://openclaw.com/docs) <br>
- [Daxiang web app](https://x.sankuai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and JSON chat data files, with optional shell commands for manual or scheduled execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes date-keyed reports such as daxiang_YYYYMMDD_vN.md and can cache raw chat data as daxiang_messages_YYYYMMDD_full.json.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
