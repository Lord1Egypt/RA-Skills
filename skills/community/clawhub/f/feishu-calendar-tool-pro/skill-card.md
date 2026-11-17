## Description:

This skill helps enterprise teams and professional users manage Feishu calendar workflows, including shared calendars, event collaboration, cross-time-zone synchronization, intelligent scheduling, webhooks, and batch operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Enterprise teams and automation-focused users use this skill to create and share Feishu calendars, coordinate attendees, synchronize events across time zones, and run higher-volume calendar operations through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad file and command authority could let the agent perform actions beyond calendar management.

Mitigation: Review the skill before deployment, grant only the tools needed for the workflow, and require confirmation before executing commands.

Risk: Shared-calendar, event-sharing, and batch operations can affect multiple users or calendars.

Mitigation: Use tightly scoped Feishu calendar credentials, test batch actions on a small set first, and confirm create, update, share, and batch requests before execution.

Risk: Callback or webhook destinations could send calendar data to unapproved endpoints.

Mitigation: Allow only organization-approved HTTPS webhook destinations and avoid arbitrary callback URLs in production tenants.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/feishu-calendar-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON configuration examples, and structured result examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include calendar action status, result data, execution logs, and configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
