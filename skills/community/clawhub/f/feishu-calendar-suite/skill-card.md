## Description:

飞书日历与日程管理工具集，支持日历管理、日程管理、参会人管理和忙闲查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operators who use Feishu calendars can use this skill to create, list, search, modify, reply to, and inspect calendar events, manage attendees, and check free/busy availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invited attendees, groups, rooms, or external email invitees may receive rights to edit events and manage participants by default.

Mitigation: Review attendee permissions before using the skill and choose narrower permissions unless collaborators explicitly need to modify events or manage participants.

Risk: The skill assumes a fixed Asia/Shanghai timezone, which can produce incorrect meeting times for other calendar workflows.

Mitigation: Confirm that Asia/Shanghai matches the intended workflow and supply explicit RFC 3339 timestamps with timezone offsets.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON argument examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides Feishu calendar action names, required parameters, ID formats, fixed Asia/Shanghai timezone assumptions, attendee permission behavior, limits, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
