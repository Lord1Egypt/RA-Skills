## Description:

Boka tvättid helps agents search Boka tvättid/Visir buildings, list laundry or guest-apartment availability, and book, cancel, or view reservations through the bundled CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patello](https://clawhub.ai/user/patello)

### License/Terms of Use:

MIT-0

## Use Case:

Residents and assistants use this skill to manage laundry-room or guest-apartment reservations for buildings that use bokatvattid.se v1 mode. It supports checking availability, making confirmed bookings, cancelling confirmed reservations, and listing current bookings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform real bookings and cancellations using a building, apartment number, and PIN.

Mitigation: Confirm the exact room, date, and time before booking or cancelling, and avoid using non-interactive confirmation unless the user has explicitly approved that action.

Risk: PINs, account tokens, or booking data may be exposed if sensitive values are placed in chat, shell history, process arguments, or debug logs.

Mitigation: Prefer environment variables or the local config file for credentials, keep BOKA_DEBUG unset, and do not include PINs in chat text or final reports.

## Reference(s):

- [Boka tvättid legacy API reference](artifact/references/bokatvattid-api.md)
- [ClawHub skill page](https://clawhub.ai/patello/skills/boka-tvattid)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with CLI commands and concise booking status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include booking IDs, room names, dates, time slots, availability results, and cancellation status. Sensitive PINs should not be included in chat text or final reports.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
