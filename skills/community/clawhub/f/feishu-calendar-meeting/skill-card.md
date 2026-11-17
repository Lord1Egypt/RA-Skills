## Description:

Creates Feishu calendar events and video meetings through the Feishu Calendar API, automatically associating events with Feishu video meetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sangy12](https://clawhub.ai/user/sangy12)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help users create scheduled Feishu calendar meetings with titles, start and end times, optional descriptions or locations, and an associated Feishu video meeting link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes storing Feishu OAuth tokens in a plaintext Markdown file.

Mitigation: Use a keychain or secret store for Feishu tokens, restrict token scopes, and revoke or rotate tokens if the workspace file may have been exposed.

Risk: Feishu calendar event titles, descriptions, and locations can contain sensitive business or personal information.

Mitigation: Review event content before sending API requests and avoid including sensitive details unless they are required for the meeting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sangy12/skills/feishu-calendar-meeting)
- [Publisher profile](https://clawhub.ai/user/sangy12)
- [Feishu Calendar API calendars endpoint](https://open.feishu.cn/open-apis/calendar/v4/calendars)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, JSON, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OAuth setup steps, Feishu API request payloads, timestamp calculation guidance, and response summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
