## Description:

Manages Feishu/Lark calendars by listing calendars, searching schedules, checking availability, creating events with attendees, and syncing calendar state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Feishu/Lark calendar workflows, including calendar discovery, schedule search, availability checks, event creation, attendee setup, and local schedule synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read calendars and contacts, create events, add attendees, and store synced calendar data locally.

Mitigation: Limit credentials and Feishu/Lark scopes to the required calendar tasks, review requested actions before execution, and protect any local cache or environment files.

Risk: Security evidence flags inconsistent routing, privacy claims, and collaboration scope for a calendar tool with write access.

Mitigation: Use the skill only for Feishu/Lark calendar tasks and require publisher clarification before relying on local-only privacy claims or broader collaboration behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/feishu-calendar-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured text with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include calendar operation status, returned schedule data, setup guidance, and error-handling guidance.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
