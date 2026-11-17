## Description:

Creates Feishu calendar events and video meetings through the Calendar API with optional Feishu video conference linkage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelaner](https://clawhub.ai/user/kelaner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare Feishu calendar event creation requests, including required event fields, optional descriptions and locations, and video meeting linkage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu access or refresh tokens may be stored in a plaintext workspace markdown file.

Mitigation: Store tokens in a credential store or tightly permissioned secret mechanism instead of normal workspace files.

Risk: Calendar and video meeting scopes can grant broad account access if over-provisioned.

Mitigation: Grant only the minimum Feishu scopes required for calendar event creation and video meeting creation.

Risk: A token may already have been exposed through plaintext storage.

Mitigation: Rotate any Feishu token that may have been exposed before using the skill in a shared or persistent workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelaner/skills/feishu-calendar-meeting-tmp)
- [ClawHub publisher profile](https://clawhub.ai/user/kelaner)
- [Feishu calendar event creation endpoint](https://open.feishu.cn/open-apis/calendar/v4/calendars/${CALENDAR_ID}/events)
- [Feishu calendar list endpoint](https://open.feishu.cn/open-apis/calendar/v4/calendars)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON request examples, and a short success-response summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Feishu user OAuth token and a calendar ID; output may include a Feishu meeting link after successful event creation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
