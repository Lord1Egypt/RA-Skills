## Description:

Build event shortlists, dated calendars, and venue comparisons from public Ticketmaster and TicketWeb listings through Crawlora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Event planners and travelers use this skill to compare public event listings, venue details, schedules, ticket fees, and availability caveats before making plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Event queries and the Crawlora API key are sent to Crawlora; sensitive search terms could disclose personal details.

Mitigation: Keep the key in the environment and avoid sensitive personal details in searches.

Risk: Public event availability and prices can change; a listing does not reserve tickets or confirm private venue-booking availability.

Mitigation: Recheck shortlisted listings before use and only create calendar entries or purchase tickets when explicitly requested.

## Reference(s):

- [Event and venue endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [Event Venue Research on ClawHub](https://clawhub.ai/crawlora-org/skills/event-venue-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown table or dated calendar with venue comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links, local event times, status, ticket-price scope, and availability caveats where known.]

## Skill Version(s):

1.0.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
