## Description: <br>
从 macOS 邮件应用检索邮件，并根据邮件中的事件信息创建提醒事项，支持按今天、昨天到今天、未读和最近邮件等范围处理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yfwill](https://clawhub.ai/user/yfwill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using macOS Mail can ask an agent to review a selected range of local messages, identify future meetings or events, and create Reminders entries two hours before each event. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads selected local macOS Mail metadata and summaries. <br>
Mitigation: Start with a narrow range such as today or unread messages, and confirm the selected range before running the mail retrieval script. <br>
Risk: The skill can create local Reminders items from detected event times. <br>
Mitigation: Ask the agent to preview proposed reminders before creation when tighter control is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yfwill/email-schedule) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown status text with shell command examples and reminder summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads selected local macOS Mail metadata and summaries, then may create local Reminders items through remindctl.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
