## Description:

Create and manage calendar events via Claw Calendar API for scheduling meetings, adding reminders, and managing personal calendars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[5twang](https://clawhub.ai/user/5twang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an assistant list calendars and create, view, update, or delete calendar events through the Claw Calendar API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an assistant API-key authority to create, update, and delete calendar data.

Mitigation: Use a limited-scope key if available and confirm exact calendar or event details before allowing update or delete actions.

## Reference(s):

- [Claw Calendar API Reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON API request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CALENDAR_API_BASE_URL and CALENDAR_API_KEY; calendar and event mutations can change user data.]

## Skill Version(s):

1.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
