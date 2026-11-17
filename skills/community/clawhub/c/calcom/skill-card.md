## Description:

Interact with the Cal.com API v2 to manage scheduling, bookings, event types, availability, and calendars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peerrich](https://clawhub.ai/user/peerrich)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to build Cal.com scheduling integrations that check availability, create and manage bookings, configure event types, manage schedules, connect calendars, and configure webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cal.com API keys and OAuth secrets can expose real scheduling data if placed in prompts, client-side code, logs, or shared examples.

Mitigation: Store credentials in environment variables or a secrets manager, use narrowly scoped keys, and avoid logging or displaying raw credential values.

Risk: Booking, schedule, calendar, and webhook operations can create, cancel, reschedule, delete, disconnect, or forward real user data.

Mitigation: Require explicit user confirmation before state-changing actions and verify the target booking, schedule, calendar, or webhook endpoint before sending requests.

Risk: Requests sent outside the expected Cal.com API endpoint could disclose scheduling data or credentials to an unintended service.

Mitigation: Restrict agent requests to https://api.cal.com/v2 unless a reviewer has approved a different endpoint.

Risk: Webhook payloads may contain booking and attendee details.

Mitigation: Send webhooks only to trusted endpoints and avoid logging raw webhook payloads.

## Reference(s):

- [Authentication API Reference](references/authentication.md)
- [Bookings API Reference](references/bookings.md)
- [Calendars API Reference](references/calendars.md)
- [Event Types API Reference](references/event-types.md)
- [Schedules API Reference](references/schedules.md)
- [Slots and Availability API Reference](references/slots-availability.md)
- [Webhooks API Reference](references/webhooks.md)
- [Cal.com API v2 Reference](https://cal.com/docs/api-reference/v2)
- [Cal.com API v2 OpenAPI Specification](https://api.cal.com/v2/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP, JSON, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
