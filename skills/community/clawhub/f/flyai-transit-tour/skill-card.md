## Description:

中转不浪费 helps Chinese-speaking travelers identify 6-15 hour layover flight options and generate timed half-day transit-city itineraries with flight, POI, visa, safety-buffer, hotel, and booking-link guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking travelers and travel-planning agents use this skill to compare direct and connecting flights, find layovers long enough for a city visit, and produce a practical transit itinerary. The skill also highlights visa, luggage, timing, airport-buffer, hotel, attraction, and booking-link considerations for the trip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill may ask an agent to install or upgrade mutable global software, including with elevated privileges.

Mitigation: Require explicit user approval before installing or upgrading CLI tooling, avoid sudo/global installs where possible, and prefer an isolated Node environment.

Risk: The security review says the skill may instruct agents to bypass TLS certificate validation.

Mitigation: Do not disable TLS validation for normal use; resolve certificate or network issues before running travel searches.

Risk: The security review says the skill may add booking links to generated travel plans.

Mitigation: Ask users to verify booking URLs, prices, dates, cancellation terms, and vendor identity before clicking or purchasing.

Risk: The security review says the skill may persist personal travel profile data.

Mitigation: Treat profile storage as opt-in, confirm before saving preferences, and avoid storing sensitive travel or family details.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hello-ahang/skills/flyai-transit-tour)
- [Workflow](reference/workflow.md)
- [Flight Search](reference/search-flight.md)
- [POI / Attraction Search](reference/search-poi.md)
- [Hotel Search](reference/search-hotel.md)
- [Keyword Search](reference/keyword-search.md)
- [User Profile Storage](reference/user-profile-storage.md)
- [Airport Guide](reference/airport-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown travel-plan response with tables, timelines, booking links, and inline shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include booking URLs returned by FlyAI tools and optional profile-storage updates after user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
