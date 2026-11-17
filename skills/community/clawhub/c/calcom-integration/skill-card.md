## Description:

Integrates with Cal.com to list event types, create and cancel bookings, check available slots, manage availability schedules, and retrieve user information through the Cal.com REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaolfun](https://clawhub.ai/user/gaolfun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent inspect Cal.com account data, summarize booking availability, and prepare or execute booking and availability changes through authenticated API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or cancel bookings and modify availability schedules using a Cal.com API key.

Mitigation: Use a least-privilege API key and require the agent to show booking or schedule details and obtain explicit approval before write actions.

Risk: Availability schedule updates can replace existing schedule data.

Mitigation: Fetch and review the current schedule before submitting updates, then send the complete intended schedule object.

Risk: Calendar operations can be wrong when timezones or daylight saving changes are misunderstood.

Mitigation: Use ISO 8601 timestamps with explicit UTC offsets and confirm the user's local timezone before booking or updating availability.

## Reference(s):

- [Cal.com](https://cal.com)
- [ClawHub skill page](https://clawhub.ai/gaolfun/skills/calcom-integration)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and structured JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Cal.com API responses, booking summaries, setup guidance, and proposed booking or schedule changes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
