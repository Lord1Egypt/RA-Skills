## Description:

Helps Caly users review bookings and, with explicit confirmation, reschedule or cancel meetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Caly users can review upcoming or past meetings, locate a booking by attendee or time, and confirm changes to a specific booking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Caly connector can access booking details.

Mitigation: Connect only if you trust the Caly connector and are comfortable granting it access to your bookings.

Risk: Rescheduling or cancelling a booking may notify attendees; cancellation cannot be undone.

Mitigation: Review the booking and intended change, then explicitly confirm before proceeding.

## Reference(s):

- [Caly: Managing Bookings on ClawHub](https://clawhub.ai/devino/skills/caly-managing-bookings)
- [Caly connector installation](https://github.com/DevinoSolutions/mcp-servers/tree/main/caly#install)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Booking times include time zones; changes may notify attendees.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
