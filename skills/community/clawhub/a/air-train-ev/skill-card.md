## Description:

Provides flight prices with Amadeus, public transport and train itineraries with Navitia, and nearby EV charge point lookups through Open Charge Map.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaureli](https://clawhub.ai/user/aaureli)

### License/Terms of Use:


## Use Case:

Travelers and mobility-planning agents use this skill to compare flight offers, look up public transport journeys, and find nearby EV charging stations from command-line clients backed by external travel APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured host overrides can send API credentials and travel or location queries to endpoints other than the documented service hosts.

Mitigation: Use official HTTPS API hosts unless the endpoint is controlled and trusted, and review host environment variables before running the scripts.

Risk: Flight, transit, and EV charging searches can transmit sensitive itinerary or location details to external services.

Mitigation: Avoid submitting sensitive trips or precise coordinates unless external API processing is acceptable for the use case.

Risk: Raw response dumping can store sensitive travel or location data locally.

Mitigation: Use dump options only when needed, protect generated files, and remove them after review.

## Reference(s):

- [Navitia documentation](https://doc.navitia.io/)
- [Open Charge Map API documentation](https://openchargemap.org/site/develop/api)
- [Open Charge Map POI API endpoint](https://api.openchargemap.io/v3/poi/)
- [ClawHub skill page](https://clawhub.ai/aaureli/skills/air-train-ev)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command-line examples and plain-text API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided API credentials for Amadeus, Navitia, and Open Charge Map.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
