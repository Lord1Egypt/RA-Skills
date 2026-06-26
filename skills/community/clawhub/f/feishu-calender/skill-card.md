## Description: <br>
Feishu calendar management skill for creating calendars and events, checking free/busy status, and subscribing to calendar changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyyao2222-eng](https://clawhub.ai/user/sunnyyao2222-eng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external collaborators, developers, and automation agents use this skill to manage Feishu calendars, schedule meetings, check time conflicts, and monitor calendar changes through Calendar v4 API guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide calendar event creation, update, deletion, attendee invitation, and ongoing calendar monitoring. <br>
Mitigation: Install only for authorized Feishu tenants, use least-privilege credentials, and require explicit confirmation before updating or deleting events or inviting attendees. <br>
Risk: Calendar subscriptions can enable ongoing monitoring of calendar changes. <br>
Mitigation: Enable subscriptions only for approved calendars with authenticated webhooks, retention limits, audit logging, and a clear unsubscribe path. <br>


## Reference(s): <br>
- [Feishu Calendar v4 API](https://open.feishu.cn/open-apis/calendar/v4) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, code, configuration] <br>
**Output Format:** [Markdown with HTTP endpoints and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authorized Feishu tenant access token and calendar permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
