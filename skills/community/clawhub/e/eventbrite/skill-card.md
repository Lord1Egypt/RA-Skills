## Description:

Helps agents manage Eventbrite events, venues, tickets, orders, and attendees through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Event organizers and their agents use this skill to look up Eventbrite account information, manage events and attendees, and, with approval, make changes or set up automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Event or attendee changes can affect real business data.

Mitigation: Start with read/list commands and confirm each write with the user.

Risk: Hosted functions and triggers can continue acting after setup.

Mitigation: Get explicit approval before creating automation and scope it to the intended account and action.

Risk: Attendee information or a raw API key could be exposed through logs or shared output.

Mitigation: Show only needed response fields; prefer OAuth through the CLI and use the raw API-key fallback only when the CLI is unavailable.

## Reference(s):

- [Eventbrite API documentation](https://www.eventbrite.com/platform/api)
- [Maton homepage](https://maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton API reference](https://docs.maton.ai/api-reference/overview)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return Eventbrite account and attendee data; optional hosted functions and triggers support automation.]

## Skill Version(s):

1.2.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
