## Description:

生成飞书AI助手团队工作日报：按北京时间收集团队成员当天工作内容，整理为日报，保存文件并发送到飞书。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tilly266](https://clawhub.ai/user/tilly266)

### License/Terms of Use:


## Use Case:

Employees and AI assistant operators use this skill to produce a same-day team work report from OpenClaw agent session messages, save it as a Markdown daily report, and send it to a configured Feishu destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects raw same-day DM-derived work messages from multiple agent session logs.

Mitigation: Use only where affected agents and users have explicitly approved this collection, and narrow the work-log source to messages intended for reporting.

Risk: The generated report may include private or sensitive message content and is stored as a plaintext Markdown file.

Mitigation: Review and redact report content before sending or retaining it, and apply local access controls to generated report files.

Risk: The report is sent to a Feishu destination without evidence of fixed recipient controls.

Mitigation: Configure an allowlisted Feishu destination and require approval before external or broad distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tilly266/skills/feishu-ai-dailyreport)
- [ClawHub publisher profile](https://clawhub.ai/user/tilly266)

## Skill Output:

**Output Type(s):** [Markdown, Files, API Calls]

**Output Format:** [Markdown daily report saved as a .md file and sent as a Feishu message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Beijing time and same-day OpenClaw agent session messages; the report format is fixed by the artifact template.]

## Skill Version(s):

1.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
