## Description:

Tracks flight fares for specified routes and dates, reporting price drops or target-price hits and supporting one-off searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memeanalyst](https://clawhub.ai/user/memeanalyst)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers can use the skill to search fares or monitor a route and dates for price drops and target-price hits. It returns concise fare summaries and alert details to help users decide when to review an itinerary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Actor runs and alerts incur charges on the user's Apify account.

Mitigation: Review the stated per-record and per-alert prices and expected check frequency before setting up a watch.

Risk: Flight prices and availability can change after a fare is reported.

Mitigation: Use the provided Google Flights link to confirm current itinerary details and price before booking.

## Reference(s):

- [Flight Price Watch Actor on Apify](https://apify.com/magnova/flight-price-watch)
- [Flight Fare Watcher on ClawHub](https://clawhub.ai/memeanalyst/skills/flight-fare-watcher)

## Skill Output:

**Output Type(s):** [Text, Structured data]

**Output Format:** [Concise fare summaries and alerts with itinerary and price details when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports baseline fares, price drops, target hits, or no-change summaries; does not book flights.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
