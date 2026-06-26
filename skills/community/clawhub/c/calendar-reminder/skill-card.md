## Description: <br>
每晚22:00自动扫描明天的Outlook日历，上午日程提前2小时提醒，下午日程12:00统一提醒，通过飞书发送通知。依赖 owa-outlook skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilove323](https://clawhub.ai/user/ilove323) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and personal productivity users can use this skill to scan the next day's Outlook calendar and schedule Feishu reminders for morning and afternoon events. It is intended for OpenClaw environments where the user has configured the dependent owa-outlook skill and their own Feishu recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send private calendar details to a hard-coded Feishu user if installed or run without editing the target. <br>
Mitigation: Replace the Feishu target with the user's own verified recipient before any manual run or cron setup. <br>
Risk: Automatic nightly scanning and reminder creation may continue after the user no longer wants calendar automation. <br>
Mitigation: Review the registered OpenClaw cron entry and remove the nightly scan when automatic calendar reminders are no longer needed. <br>
Risk: The skill depends on the owa-outlook helper path and may fail or report incorrect results if that dependency is missing or unexpected. <br>
Mitigation: Confirm the owa-outlook helper installation and path before relying on scheduled reminders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ilove323/calendar-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with command examples and runtime Feishu messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, openclaw, the owa-outlook skill, and a user-edited Feishu target.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
