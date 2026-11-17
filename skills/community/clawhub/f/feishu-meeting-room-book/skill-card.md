## Description:

Initializes and refreshes Feishu meeting-room preferences, creates calendar events, and books preferred rooms for new or existing meetings while keeping a local single-city room preference file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyinghanger](https://clawhub.ai/user/flyinghanger)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workplace assistants use this skill to learn a user's commonly used Feishu meeting rooms, keep an ordered single-city preference list, create calendar events, and attach the first available preferred room.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Feishu calendar permissions to read recent events, create events, update attendees, and check room availability.

Mitigation: Install only when those scopes are acceptable for the workspace and complete the Feishu OAuth flow before use.

Risk: The saved default city and room priority order can affect which room is booked automatically.

Mitigation: Review state/feishu-meeting-room-book.json after initialization or refresh when room order or default city matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyinghanger/skills/feishu-meeting-room-book)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON state file descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Feishu calendar tools and writes local state under state/feishu-meeting-room-book.json plus temporary refresh files under tmp/.]

## Skill Version(s):

0.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
