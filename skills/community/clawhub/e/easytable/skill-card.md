## Description:

Use when the user wants to check restaurant availability or make, change, or cancel a table reservation at a restaurant that books through easyTable (a book.easytable.com/book/?id=<id> widget). Covers listing booking areas, dates and times, looking up existing bookings by phone, and creating/modifying/cancelling reservations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Restaurant guests use this skill to check bookable areas, dates, and times, and to find existing reservations. They can create, modify, or cancel a reservation through their connected easyTable booking widget after reviewing and confirming the proposed change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating, changing, or cancelling a reservation can affect the guest's booking.

Mitigation: Keep booking confirmations enabled and review the preview before approving, especially for changes to allergy notes or cancellations.

Risk: The browser extension handles access to the booking widget, and its binary and the MCP server were not audited in the supplied security review.

Mitigation: Review the extension's permissions, allow only the restaurant domain and needed capabilities, and verify the downloaded extension checksum.

Risk: A create or modify request with an unclear result may already have created or changed a booking.

Mitigation: Look up bookings using the guest's mobile number before retrying an action with an uncertain outcome.

## Reference(s):

- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [easyTable booking widget](https://book.easytable.com/book/?id=<restaurantId>)
- [ClawHub easytable release](https://clawhub.ai/chrischall/skills/easytable)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text responses with availability, reservation details, and confirmation previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Availability and booking actions depend on the selected restaurant and a connected booking widget in the user's browser.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
