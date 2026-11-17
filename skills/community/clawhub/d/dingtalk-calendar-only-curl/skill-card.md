## Description:

Guides an agent through DingTalk Calendar operations using curl, including primary-calendar event CRUD, free/busy checks, DingTalk video meetings, meeting-room scheduling, sign-in and sign-out links, and recurrence rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breath57](https://clawhub.ai/user/breath57)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and calendar operators use this skill to prepare and execute DingTalk calendar API calls for scheduling meetings, managing events, checking availability, booking rooms, and handling sign-in or sign-out workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DingTalk app credentials can modify organizational calendar data.

Mitigation: Restrict DingTalk app scopes to only the needed calendar permissions and install only when that access is acceptable.

Risk: Local credential storage can expose app secrets and access tokens.

Mitigation: Store the configuration file in a private 0700 directory with a 0600 file.

Risk: Shared temporary task scripts can expose or tamper with calendar operations.

Mitigation: Avoid shared /tmp task scripts and review generated shell commands before execution.

Risk: Calendar-changing actions can affect organizational schedules and attendance workflows.

Mitigation: Require explicit confirmation for delete, update, meeting-room removal, sign-in, and sign-out actions.

## Reference(s):

- [DingTalk Calendar API Reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/breath57/skills/dingtalk-calendar-only-curl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and curl snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in DingTalk API calls that create, update, delete, or query organizational calendar data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
