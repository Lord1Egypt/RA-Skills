## Description:

Search Booking.com for real-time hotel availability, prices, and room details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtnrabi](https://clawhub.ai/user/mtnrabi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search destinations, check hotel availability, compare prices and room details, and return Booking.com links based on dates, guests, filters, and budget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided travel search details are sent to the Booking Live API on RapidAPI.

Mitigation: Use the skill only when sharing destination, dates, guest count, filters, and hotel names with RapidAPI is acceptable.

Risk: Broad natural-language triggers may activate hotel-search behavior in more conversations than intended.

Mitigation: Review and narrow triggers if the agent runtime supports trigger editing.

Risk: The skill requires a RapidAPI key for authenticated requests.

Mitigation: Store the key in the configured secret or environment variable and scope the subscription to this service where possible.

## Reference(s):

- [Booking Live API on RapidAPI](https://rapidapi.com/mtnrabi/api/booking-live-api)
- [ClawHub Skill Page](https://clawhub.ai/mtnrabi/skills/booking-hotel-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with hotel result tables, direct booking links, curl commands, and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RAPIDAPI_KEY and outbound HTTPS access to booking-live-api.p.rapidapi.com.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
