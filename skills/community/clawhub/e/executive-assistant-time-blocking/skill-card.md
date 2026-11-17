## Description:

Standard Operating Procedure (SOP) that acts as an executive assistant to block out calendar time using TS atomic plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and scheduling assistants use this skill to collect incomplete Google Tasks, estimate time needs, find calendar gaps, and create non-overlapping time blocks on the primary calendar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and delete primary-calendar events without clear confirmation or rollback safeguards.

Mitigation: Require a preview and explicit confirmation before changes, and limit deletion to events the skill created.

Risk: The skill needs Google Tasks and primary-calendar access through the required `gog` command.

Mitigation: Install only when that account access is appropriate, and review requested permissions before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zvirb/skills/executive-assistant-time-blocking)
- [Publisher Profile](https://clawhub.ai/user/zvirb)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with task schedule details and overlap status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a concise schedule summary after calendar event creation and overlap auditing.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
