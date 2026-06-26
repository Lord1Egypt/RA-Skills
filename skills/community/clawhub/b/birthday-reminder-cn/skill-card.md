## Description: <br>
管理并计算生日提醒（阳历与农历），支持每条记录单独配置和全局默认值，支持当天提醒、提前 N 天、多次提醒和提醒时间配置，默认使用北京时间。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[905583906](https://clawhub.ai/user/905583906) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal users and agent assistants use this skill to maintain birthday reminder configuration, calculate due reminders, and prepare notification runs for scheduled execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birthday records and notification settings may contain private dates, names, webhook URLs, bot tokens, or chat identifiers. <br>
Mitigation: Keep birthday and notification files private, avoid committing credentials, and use trusted notification destinations. <br>
Risk: Configured notification channels can send reminder data externally or write it to local files. <br>
Mitigation: Run the notification bridge with --dry-run first and review the notify.json channels before enabling scheduled execution. <br>
Risk: Scheduled automation can repeatedly trigger notifications if the schedule or reminder window is misconfigured. <br>
Mitigation: Review the Automation schedule you enable and test the reminder window with known timestamps before relying on recurring runs. <br>


## Reference(s): <br>
- [Birthday Config Schema](references/config-schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/905583906/birthday-reminder-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands; reminder checks may produce text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read local birthday and notification configuration files and can send notifications through configured channels.] <br>

## Skill Version(s): <br>
1.0.6 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
