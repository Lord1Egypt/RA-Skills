## Description:

Finds an available Caly meeting slot, gathers attendee and booking details, and creates a booking after the user confirms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

People scheduling meetings use this skill to find an available time on one of their Caly event types, collect the attendee's required details, and book the meeting after reviewing and confirming the invitation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating a booking writes to Caly and may email the attendee or other guests.

Mitigation: Review the attendee, guests, event type, time and time zones, and obtain explicit user confirmation before creating a booking; do not blindly retry failed bookings.

Risk: The skill uses a Caly connector that acts on the connected account.

Mitigation: Confirm the connector is trusted before connecting it or approving bookings.

## Reference(s):

- [Caly: Booking Meetings on ClawHub](https://clawhub.ai/devino/skills/caly-booking-meetings)
- [Caly connector installation](https://github.com/DevinoSolutions/mcp-servers/tree/main/caly#install)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes the proposed meeting for confirmation and reports the booking status, location or meeting URL, and booking UID.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
