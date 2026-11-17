## Description:

Create, view, update, and delete calendar events using the Claw Calendar API with natural language commands for scheduling and managing personal calendars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[5twang](https://clawhub.ai/user/5twang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and assistants use this skill to manage personal calendar data through a configured Claw Calendar API, including creating, listing, updating, and deleting events from natural language scheduling requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an assistant API-key access to create, update, and delete calendar data.

Mitigation: Use it only with a trusted calendar service and a scoped or revocable API key when available.

Risk: Destructive calendar actions could remove or change the wrong event if details are ambiguous.

Mitigation: Require the assistant to show exact calendar and event details and obtain confirmation before any delete or update operation.

Risk: Calendar events may contain private schedule, location, or contact information.

Mitigation: Review event details before sending them to the API and avoid routing data to untrusted CALENDAR_API_BASE_URL values.

## Reference(s):

- [Claw Calendar API Reference](references/api_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/5twang/skills/claw-calendar-new)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CALENDAR_API_BASE_URL and CALENDAR_API_KEY environment variables for authenticated calendar operations.]

## Skill Version(s):

1.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
