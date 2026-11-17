## Description:

Check easyTable restaurant availability and manage bookings from a shell using fpx and a signed-in browser tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and restaurant guests use it to check easyTable availability, find bookings by phone, cancel reservations, and prepare booking changes through their own browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking changes or cancellations can affect a real reservation.

Mitigation: Act only on authorized requests and verify the restaurant, guest details, and requested change before submitting.

Risk: Reservation workflows involve personal details such as guest names and phone numbers.

Mitigation: Share only the information needed for the booking and remove temporary booking or token files after use.

Risk: Browser pairing persists and the CLI and extension are external dependencies.

Mitigation: Review the CLI and extension before installing, limit browser access to easyTable, and revoke pairing when it is no longer needed.

## Reference(s):

- [easyTable fpx request examples](references/easytable-requests.md)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and booking information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Booking creation and modification require a manually retrieved, short-lived browser token.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
