## Description:

Researches places, categories, guides, routes, transit, and travel times through Apple Maps via the Crawlora API, returning clean JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and location-intelligence users use this skill to search Apple Maps places, categories, guides, directions, transit departures, reverse geocoding, and ETA estimates through Crawlora without browser automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apple Maps searches, coordinates, destinations, place IDs, and the Crawlora API key are sent to Crawlora's API.

Mitigation: Use a dedicated Crawlora key where possible, install only if that data sharing is acceptable, and avoid unusually sensitive locations unless necessary.

Risk: Transit route planning is not supported even though transit departures are documented.

Mitigation: Use this skill for transit stop departures and use another route-planning source when a full transit route is required.

## Reference(s):

- [Apple Maps endpoint reference](reference/endpoints.md)
- [Crawlora API base](https://api.crawlora.net/api/v1)
- [Crawlora profile](https://clawhub.ai/user/crawlora-org)
- [ClawHub skill page](https://clawhub.ai/crawlora-org/skills/apple-maps-research)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON returned by shell commands and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CRAWLORA_API_KEY and sends requested Apple Maps queries to the Crawlora API.]

## Skill Version(s):

1.0.10 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
