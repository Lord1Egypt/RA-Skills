## Description: <br>
飞书日历与日程管理工具集，帮助代理处理日历管理、日程管理、参会人管理和忙闲查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and assistants use this skill to create, list, search, update, and reply to Feishu calendar events, manage attendees, and check user availability. It is intended for agents that need structured guidance for Feishu calendar actions and parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar-changing actions may create or update live events with the wrong time, timezone, attendees, or RSVP status. <br>
Mitigation: Before allowing writes, confirm the exact time, timezone, attendees, RSVP action, and intended calendar target with the user. <br>
Risk: Broad attendee edit authority can let invitees modify events or manage participants when shared editing was not intended. <br>
Mitigation: Use lower attendee permissions unless invitees are explicitly meant to edit the event or manage participants. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a3152557994-ship-it/feishu-calendar-suite) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, API usage instructions] <br>
**Output Format:** [Markdown with tables and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Feishu calendar actions, required parameters, ID format guidance, timezone constraints, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
