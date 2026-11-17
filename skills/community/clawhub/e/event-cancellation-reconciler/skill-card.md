## Description:

Standard Operating Procedure (SOP) to autonomously detect cancelled events and sync the calendar state using atomic nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

People who manage calendars use this skill to reconcile Google Calendar events after receiving cancellation or reschedule emails. The skill guides an agent through extracting event details, locating the matching calendar event, deleting or marking it cancelled, and reporting the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete or modify Google Calendar events based on email content.

Mitigation: Require the agent to show the exact email, matched calendar event, organizer or attendee evidence, and proposed action, then obtain explicit user confirmation before deleting or marking an event cancelled.

Risk: Incorrect extraction or event matching could change the wrong calendar event.

Mitigation: Stop when extraction fails or no clear matching event is found, and ask the user for clarification before taking calendar action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zvirb/skills/event-cancellation-reconciler)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown-style procedural guidance with command examples and confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and Google Calendar access configured outside the skill.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
