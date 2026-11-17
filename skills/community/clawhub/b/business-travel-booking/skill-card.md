## Description:

Helps agents search Booking.com hotels, compare rooms and prices, and manage reservation workflows for international business travel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, travel coordinators, and agent developers use this skill to search international hotel options, compare rooms and prices, and prepare Booking.com reservation management actions. It is most appropriate when connected to verified live Booking.com API credentials and confirmation flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel results may be mistaken for live Booking.com inventory, pricing, availability, reviews, taxes, or cancellation terms.

Mitigation: Require verified live API calls and visible source timestamps before users rely on hotel, room, price, review, tax, or cancellation information.

Risk: The artifact advertises booking management behavior that security evidence says is not implemented.

Mitigation: Disable or clearly gate reservation creation, lookup, and cancellation until verified booking APIs, data-sharing notices, and explicit user confirmation flows are implemented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/business-travel-booking)
- [Booking.com Distribution API endpoint](https://distribution-xml.booking.com/json/bookings.getHotels)
- [Booking.com Distribution JSON base URL](https://distribution-xml.booking.com/json)

## Skill Output:

**Output Type(s):** [text, markdown, code, API calls, configuration]

**Output Format:** [Markdown tables and JSON-style function call results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Booking.com API credentials for live operation; security evidence says the artifact currently contains mock travel result paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
