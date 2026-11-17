## Description:

Google 日历基础版 helps an agent use gcalcli to list, create, search, delete, and back up calendar events for personal calendar management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Google Calendar or CalDAV-backed schedules through an agent, including listing events, creating events, deleting matching events, and preparing basic calendar backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or delete calendar events after receiving calendar credentials.

Mitigation: Use it only for explicit calendar tasks and require confirmation before any event creation or deletion.

Risk: The artifact claims local-only privacy even though calendar operations may contact Google Calendar or CalDAV services.

Mitigation: Verify the target account and service before use, and treat calendar data as data shared with the configured external calendar provider.

Risk: Broad trigger language could activate the skill for project management or reporting requests outside calendar operations.

Mitigation: Limit use to calendar scheduling, lookup, deletion, and backup tasks.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and calendar operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require calendar credentials and user confirmation before creating or deleting calendar events.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
