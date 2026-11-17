## Description:

Feishu Calendar management skill for creating calendars and events, checking free/busy availability, and subscribing to calendar changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyyao2222-eng](https://clawhub.ai/user/sunnyyao2222-eng)

### License/Terms of Use:


## Use Case:

Developers and workflow automation agents use this skill to manage Feishu calendars, schedule meetings, check availability before booking, and monitor calendar changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to update or delete calendar events.

Mitigation: Require explicit user confirmation before modifying or deleting events.

Risk: The skill can guide agents to subscribe to calendar changes and monitor ongoing activity.

Mitigation: Enable subscriptions only after explicit opt-in and disclose what calendar changes will be monitored.

Risk: The skill may be used with real Feishu calendar credentials.

Mitigation: Review the skill before installation and restrict use to agents that are authorized to create, update, delete, and monitor calendar events.

## Reference(s):

- [Feishu Calendar v4 API](https://open.feishu.cn/open-apis/calendar/v4)
- [ClawHub Skill Page](https://clawhub.ai/sunnyyao2222-eng/skills/feishu-calender)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Configuration]

**Output Format:** [Markdown guidance with HTTP endpoints and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce calendar create, update, delete, free/busy, attendee, and subscription request patterns.]

## Skill Version(s):

1.0.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
